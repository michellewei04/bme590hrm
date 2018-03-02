import pandas as pd
import numpy as np
from glob import glob
import logging
from logging_config import config
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks_cwt

logging.basicConfig(**config)
logger = logging.getLogger(__name__)


class EcgData():

    def __init__(self, data=pd.read_csv('test_data/test_data1.csv', na_values=0),
                 mean_hr_bpm=None, voltage_extremes=None,
                 duration=None, num_beats=None, beats=None):
        self.data = data
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats

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
