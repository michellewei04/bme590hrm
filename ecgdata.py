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

    def __init__(self, file_number=None, data=pd.read_csv('test_data/test_data1.csv', na_values=0),
                 mean_hr_bpm=None, voltage_extremes=None,
                 duration=None, num_beats=None, beats=None):
        self.file_number = file_number
        self.data = data
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats

    # def calc_mean_hr_bpm(self):

    def butter_bandpass(self):
        voltages = self.data[:, 1]
        time = self.data[:, 0]
        max_time = np.nanmax(time)
        samples = len(voltages)
        fs = samples / max_time
        nyq = 0.5 * fs
        cutoffs = {'low': 0.1 / nyq, 'high': 6 / nyq}
        order = 3
        bp_coeffs = butter(order, [cutoffs['low'], cutoffs['high']], btype='band')
        filtered_data = lfilter(bp_coeffs[0], bp_coeffs[1], voltages)
        return filtered_data, max_time, samples

    def autocorrelation(self, file_number):
        voltages = self.data[:, 1]
        time = self.data[:, 0]
        (filtered_data, max_time, samples) = self.butter_bandpass()
        autocorr = np.correlate(filtered_data, filtered_data, mode='same')
        # autocorr = np.correlate(voltages, voltages, mode='same')
        autocorr = autocorr/np.mean(autocorr)

        hr_est = {'min_hr': 30, 'max_hr': 200}
        sample_range = {'min_spb': samples/(hr_est['max_hr']*max_time/60),
                        'max_spb': samples/(hr_est['min_hr']*max_time/60)}
        # autocorr_window = autocorr[int(samples / 2):]
        autocorr_window = autocorr[int(samples/2+sample_range['min_spb']):int(samples/2+sample_range['max_spb'])]
        peaks_index = find_peaks_cwt(autocorr_window, np.arange(30, 700), min_length=100)

        if len(acorr_peaks_index) < 1:
            acorr_peaks_index = [0]
            print('No peaks detected in autocorrelation')
        if len(peaks_index) < 1:
            peaks_index = [0]
            print('No peaks detected in data')

        figures[file_number] = plt.figure(file_number)
        plt.subplot(311)
        plt.plot(voltages)
        plt.scatter(peaks_index, voltages[peaks_index], color='red')
        plt.title('{0}, {1}'.format(len(peaks_index), len(acorr_peaks_index)))

        plt.subplot(312)
        plt.plot(time, filtered_data)

        plt.subplot(313)
        plt.plot(autocorr_window)
        plt.scatter(acorr_peaks_index, autocorr_window[acorr_peaks_index], color='red')
        figures[file_number].show()
        print('End autocorrelation of file {}'.format(file_number))

    # def detect_acorr_peaks(self):
    #     peaks_index = find_peaks_cwt(autocorr_window, np.arange(1, 40)
    #     plt.scatter(np.array(peaks_index), color = 'red')

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
