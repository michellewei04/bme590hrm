from ecgdata import EcgData
import logging
from logging_config import config
import pytest
from import_test_files import collect_all_test_data
import numpy as np

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
    test_calc_hr()


def test_setter():
    logger.debug('Begin testing setter function')
    error_input_array = [files_dict['file30']]
    error_output = [TypeError]
    for i, l in enumerate(error_input_array):
        logger.debug('index is {}'.format(i))
        with pytest.raises(error_output[i]):
            EcgData(data=l)
    logger.debug('Complete testing check inputs function')


def test_calc_hr():
    logger.debug('Begin testing heart rate calculations')
    output_beats = [34, 32, 34, 32, 35, 38, 31, 32, 28, 44, 32, 9, 4, 14, 7, 19, 19, 19,
                 19, 19, 19, 37, 75, 80, 29, 37, 63, 34, 9, 19, 19]
    test_file_numbers = list(range(32))
    test_file_numbers.remove(29)
    input_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        logger.debug('from file{}'.format(num+1))
        input_array[i] = files_dict['file{}'.format(num+1)]
    object_list = [EcgData(data=x) for x in input_array]
    max_time_array = [x.max_time for x in object_list]
    output_hr = np.multiply(np.divide(output_beats, max_time_array), 60)
    output_hr = [float(i) for i in output_hr.tolist()]
    exception_files = [7, 12, 13, 15, 24, 29]
    for i, obj in enumerate(object_list):
        mean_hr_bpm = obj.calc_mean_hr()
        logger.debug('Heart rate test for file {0}, expected output: {1} +/- 5, test output: {2}'.
                     format(i+1, int(output_hr[i]), int(mean_hr_bpm)))
        if not (i == n for n in exception_files):
            assert mean_hr_bpm == pytest.approx(output_hr[i], abs=5.)
    logger.debug('Complete testing heart rate calculations')


def test_num_beats():



if __name__ == "__main__":
    main()
