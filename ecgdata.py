import pandas as pd
import numpy as np
import logging
from logging_config import config
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks_cwt

logging.basicConfig(**config)
logger = logging.getLogger(__name__)

figures = [None] * 50



class EcgData():

    def __init__(self, data=pd.read_csv('test_data/test_data1.csv', na_values=0), mean_hr_bpm=None,
                 voltage_extremes=None, duration=None, num_beats=None, beats=None):
        self.data = data
        self.max_time = np.nanmax(self.data[:, 0])
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats

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
        autocorr = autocorr/np.mean(autocorr)

        hr_est = {'min_hr': 30, 'max_hr': 200}
        sample_range = {'min_spb': samples/(hr_est['max_hr']*self.max_time/60),
                        'max_spb': samples/(hr_est['min_hr']*self.max_time/60)}
        # autocorr_window = autocorr[int(samples / 2):]
        # autocorr_window = autocorr[int(samples/2+sample_range['min_spb']):int(samples/2+sample_range['max_spb'])]
        autocorr_window = autocorr
        peaks_index = find_peaks_cwt(voltages, np.arange(9, 200), min_length=samples/self.max_time*0.08, noise_perc=5)
        acorr_peaks_index = find_peaks_cwt(autocorr_window, np.arange(30, 700), min_length=samples/self.max_time*0.07,
                                           noise_perc=25)

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

        return samples, acorr_peaks_index, peaks_index

    def calc_mean_hr(self):
        """Returns mean heart rate

        :param self: pandas DataFrame containing ecg data with two columns: time and voltage
        :returns: mean heart rate in beats per minute
        """
        (samples, acorr_peaks_index, peaks_index) = self.autocorrelate()
        mean_hr_acorr = len(acorr_peaks_index)/self.max_time*60  # in bpm
        mean_hr = len(peaks_index)/self.max_time*60  # in bpm
        return mean_hr_acorr


    @property
    def data(self):
        logger.debug("Getting data as 2-column array")
        return self.__data

    @data.setter
    def data(self, raw_data):
        """ Sets raw_data into desired format

               :param self: pandas DataFrame containing ecg data with two columns: time and voltage
               :raises TypeError: All input in list must be numbers
               :raises TypeError: Input array must have two columns
               :raises ExceedSampleException: Sample in input array must not exceed 100,000
               """

        if type(raw_data) is pd.DataFrame:
            if any(num == np.NaN for num in raw_data.iloc[:, 1].values):
                logger.warning("Data contains NaN values")
            if any(num == np.nan for num in raw_data.iloc[:, 1].values):
                logger.warning("Data contains nan values")
            if any(isinstance(num, str) for num in raw_data.iloc[:, 1].values):
                logger.error("TypeError in input list: input contains strings")
                raise TypeError("All inputs in list must be numbers, input contains strings")

            raw_data.iloc[:, 1].fillna(0, inplace=True)
            raw_data.iloc[:, 0].fillna(np.nan, inplace=True)
            raw_data = raw_data.values

        if not all([type(num) is float or int for num in raw_data]):
            logger.error("TypeError in input list: All inputs must be numbers")
            raise TypeError('All inputs in list must be numbers.')

        shape = np.shape(raw_data)
        if not (len(shape) == 2 and shape[1] == 2):
            logger.error("TypeError in data: data array must have two columns")
            raise TypeError('Data array must have two columns, array shape = ' '{}'.format(np.shape(raw_data)))

        if shape[0] > 100000:
            logger.error("Too many samples, number of samples must be less than 100,000")
            raise ExceedSamplesException('Number of samples cannot exceed 100,000')
        elif shape[0] > 90000:
            logger.warning('Number of samples is %s, close to exceeding limit of 100,000' % shape[0])
            print('Number of samples is %s, close to exceeding limit of 100,000' % shape[0])

        if any(num > 300 for num in raw_data[:, 1]):
            logger.warning("Voltage values exceed the normal range of ECG data at 300 mV")

        logger.debug("Setting data")
        self.__data = raw_data
