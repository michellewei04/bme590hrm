import pandas as pd
import numpy as np
from glob import glob
import logging
from logging_config import config

logging.basicConfig(**config)
logger = logging.getLogger(__name__)


def main():
    collect_data()


def collect_data(filename):
    """ Gets data from csv file and into desired format

          :param filename: name of csv file
          :raises TypeError: All input in list must be numbers
          :raises TypeError: Input array must have two columns
    """
    data = pd.read_csv(filename)

    if any(num == np.NaN for num in data.iloc[:, 1].values):
        logger.warning("Data contains NaN values")
    if any(num == np.nan for num in data.iloc[:, 1].values):
        logger.warning("Data contains nan values")
    if not all([type(num) is float or int for num in data]):
        logger.error("TypeError in input list: All inputs must be numbers")
        raise TypeError('All inputs in list must be numbers.')

    data.iloc[:, 1].fillna(0, inplace=True)
    data.iloc[:, 0].fillna(np.nan, inplace=True)
    data = data.values

    if any(num > 300 for num in data[:, 1]):
        logger.warning("Voltage values exceed the normal range of ECG data at 300 mV")
    return data


if __name__ == "__main__":
    main()
