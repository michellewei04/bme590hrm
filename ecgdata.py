import pandas as pd
import numpy as np
import logging
from logging_config import config
# import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks_cwt
from bisect import bisect_left

logging.basicConfig(**config)
logger = logging.getLogger(__name__)

figures = [None] * 50


class EcgData():

    def __init__(self, filename, data, mean_hr_bpm=None,
                 voltage_extremes=None, duration=None, num_beats=None, beats=None):
        self.filename = filename
        self.data = data
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats
        # self.set_duration(input('Are the time units in minutes or seconds? '))
        self.set_duration('seconds')
        self.set_v_extremes()
        # self.calc_mean_hr(float(input('Calculate mean heart rate over __ minutes: ')))
        self.calc_mean_hr(self.duration)
        self.get_beat_times()

    def set_duration(self, time_unit):
        """Returns duration of ECG recording

            :param self: pandas DataFrame containing ecg data with two columns: time and voltage
            :param time_unit: user input for unit of time
            :returns: duration of ECG recording in seconds and adjusts time in self.data to be seconds
        """
        time = self.data[:, 0]
        if time_unit == 'seconds':
            self.duration = np.nanmax(time)
        elif time_unit == 'minutes':
            self.duration = np.multiply(np.nanmax(time), 60)
            self.data[:, 0] = np.multiply(time, 60)
        else:
            print('Please enter ''seconds'' or ''minutes''')
        return self.data, self.duration

    def set_v_extremes(self):
        """Detects minimum and maximum lead voltages

            :param self: pandas DataFrame containing ecg data with two columns: time and voltage
            :returns: tuple containing minimum and maximum lead voltages
        """
        voltages = self.data[:, 1]
        self.voltage_extremes = (np.nanmin(voltages), np.nanmax(voltages))
        return self.voltage_extremes

    def butter_bandpass(self):
        """Returns bandpass-filtered voltages

            :param self: pandas DataFrame containing ecg data with two columns: time and voltage
            :returns: bandpass-filtered voltages
            :returns: number of samples
        """
        voltages = self.data[:, 1]
        time = self.data[:, 0]
        self.max_time = np.nanmax(time)
        samples = len(voltages)
        fs = samples / self.max_time
        nyq = 0.5 * fs
        cutoffs = {'low': 0.1 / nyq, 'high': 6 / nyq}
        order = 3
        bp_coeffs = butter(order, [cutoffs['low'], cutoffs['high']], btype='band')
        filtered_data = np.square(lfilter(bp_coeffs[0], bp_coeffs[1], voltages))
        return filtered_data, samples

    def autocorrelate(self):
        """Returns number of samples in dataset and indices of peaks in voltages and the autocorrelation of voltages

                :param self: pandas DataFrame containing ecg data with two columns: time and voltage
                :returns: number of samples in dataset
                :returns: indices of peaks in voltages
                :returns: indices of peaks in the autocorrelation of voltages
        """
        voltages = self.data[:, 1]
        time = self.data[:, 0]
        (filtered_data, samples) = self.butter_bandpass()
        autocorr = np.correlate(filtered_data, filtered_data, mode='same')
        autocorr_window = autocorr
        peaks_index = find_peaks_cwt(voltages, np.arange(9, 200), min_length=samples / self.max_time * 0.08, noise_perc=5)
        acorr_peaks_index = find_peaks_cwt(autocorr_window, np.arange(30, 700), min_length=samples / self.max_time * 0.07,
                                           noise_perc=25)
        self.num_beats = len(acorr_peaks_index)

        if len(acorr_peaks_index) < 1:
            acorr_peaks_index = [0]
            print('No peaks detected in autocorrelation')
        if len(peaks_index) < 1:
            peaks_index = [0]
            print('No peaks detected in data')

        # figures[file_number] = plt.figure(file_number)
        # plt.subplot(311)
        # plt.plot(voltages)
        # plt.scatter(peaks_index, voltages[peaks_index], color='red')
        # plt.title('{0}, {1}'.format(len(peaks_index), len(acorr_peaks_index)))
        #
        # plt.subplot(312)
        # plt.plot(time, filtered_data)
        #
        # plt.subplot(313)
        # plt.plot(autocorr_window)
        # plt.scatter(acorr_peaks_index, autocorr_window[acorr_peaks_index], color='red')
        # figures[file_number].show()
        # figures[file_number].savefig('plots/fig{}.png'.format(file_number))
        # print('End autocorrelation of file {}'.format(file_number))

        return samples, acorr_peaks_index, peaks_index, self.num_beats

    def calc_mean_hr(self, time_period):
        """Returns mean heart rate

        :param self: pandas DataFrame containing ecg data with two columns: time and voltage
        :returns: mean heart rate in beats per minute
        """
        (samples, acorr_peaks_index, peaks_index, num_beats) = self.autocorrelate()
        time_period = time_period / 60
        if time_period >= self.max_time:
            mean_hr_acorr = num_beats / self.max_time * 60  # in bpm
        if time_period < self.max_time:
            time_lim = self.data[:(bisect_left(self.data[:, 0], time_period))]
            index_lim = len(time_lim)
            lim_peaks = acorr_peaks_index[:(bisect_left(acorr_peaks_index, index_lim))]
            num_beats = len(lim_peaks)
            mean_hr_acorr = num_beats / time_period * 60
        self.mean_hr_bpm = mean_hr_acorr
        return self.mean_hr_bpm

    def get_beat_times(self):
        """Returns times when a beat occurred

                :param self: pandas DataFrame containing ecg data with two columns: time and voltage
                :returns: numpy array of times (in seconds) when a beat occurred
        """
        time = self.data[:, 0]
        (samples, acorr_peaks_index, peaks_index, num_beats) = self.autocorrelate()
        diff = acorr_peaks_index[0] - peaks_index[0]
        new_peaks_index = [None] * len(acorr_peaks_index)
        if diff <= 300:
            new_peaks_index[:] = [x-diff for x in acorr_peaks_index]
            if np.max(new_peaks_index) <= len(time):
                beat_times = time[new_peaks_index]
            else:
                new_peaks_index = new_peaks_index[:(len(new_peaks_index) - 5)]
                beat_times = time[new_peaks_index]
        else:
            logger.warning('Sparse peaks detected in data, beat times may be inaccurate')
            new_peaks_index = acorr_peaks_index
            beat_times = time[new_peaks_index]
        raw_times = time[peaks_index]
        self.beats = np.array(beat_times)
        return self.beats, raw_times, peaks_index, new_peaks_index
