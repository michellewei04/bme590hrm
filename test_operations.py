<<<<<<< HEAD
import pandas as pd
import numpy as np
from glob import glob



def main():
    collect_all_test_data()


def collect_all_test_data():
    # samples 16-21 are simulated (beautiful)
    # sample 23-34 are really fast
    # 25-26 have heart problems
    # 28 has NaN values
    # 29 has nan values
    # 30 has strings
    # 31 has bad data "sparse gaps"
    # 32 has values over 300 mV
    files_dict = {}
    all_files = glob('test_data/*.csv')
    for n, file in enumerate(all_files):
        filename = 'file%d' % n
        files_dict[filename] = pd.read_csv(file, delimiter=',', index_col=None)
    pass
=======
from inputlist import InputList
import logging
from logging_config import config
import pytest
from exceedsamplesexception import ExceedSamplesException
from import_test_files import collect_all_test_data

# init logging config
logging.basicConfig(**config)
logger = logging.getLogger(__name__)

files_dict = collect_all_test_data()

# samples 16-21 are simulated (beautiful)
# sample 23-34 are really fast
# 25-26 have heart problems
# 28 has NaN values
# 29 has nan values
# 30 has bad data "sparse gaps"
# 32 has values over 300 mV


def main():
    test_setter()


def test_setter():
    logger.debug('Begin testing setter function')
    error_input_list = files_dict['test_data/test_data30.csv']

    error_output_list = TypeError
    # loop over exception triggers and module functions
    for i, l in enumerate(error_input_list):
        with pytest.raises(error_output_list[i]):
            InputList(nums=l)
    logger.debug('Complete testing check inputs function')


if __name__ == "__main__":
    main()
