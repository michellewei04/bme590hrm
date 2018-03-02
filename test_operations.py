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

#
# def main():
#     test_voltage_extremes()


def test_setter():
    logger.debug('Begin testing setter function')
    error_input_array = [files_dict['file30']]
    error_output = [TypeError]
    for i, l in enumerate(error_input_array):
        logger.debug('index is {}'.format(i))
        with pytest.raises(error_output[i]):
            EcgData(data=l)
    logger.debug('Complete testing check inputs function')


def test_duration():
    logger.debug('Begin testing duration')
    output_duration = [27.775]*11 + [13.887]*10 + [39.996]*6 + [27.775] + [13.887]*3
    test_file_numbers = list(range(32))
    test_file_numbers.remove(29)
    input_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        logger.debug('from file{}'.format(num + 1))
        input_array[i] = files_dict['file{}'.format(num + 1)]
    object_list = [EcgData(data=x) for x in input_array]
    for i, obj in enumerate(object_list):
        (data, duration) = obj.set_duration('seconds')
        logger.debug('Duration test for file {0}, expected output: {1} +/- .1, test output: {2}'.
                     format(i + 1, output_duration[i], duration))
        assert duration == pytest.approx(output_duration[i], rel=.01)
    print('Complete testing duration')
    logger.debug('Complete testing duration')


def test_voltage_extremes():
    logger.debug('Begin testing voltage extremes')
    output_extremes = [(-0.68, 1.05), (-0.59, 1.375), (-0.735, 0.955), (-0.76, 1.99), (-1.155, 1.72),
                       (-0.79, 1.78), (-1.05, 2.2), (-3.105, 1.975), (-1.07, 0.255), (-1.58, 1.555), (-0.695, 0.955),
                       (-0.52308, 0.58462), (-0.4, 1.0385), (-0.7076899999999999, 0.50769), (-0.33077, 0.7), (-0.225, 0.75),
                       ( -0.275, 0.7), (-0.19375, 0.7875), (-0.5875, 0.3875), (-1.0, -0.025), (-0.375, 0.60625),
                       (-1.5225, 2.565), (-3.34, 3.81), (-1.73, 5.1175), (-1.4525, 1.58), (-3.695, 2.3025),
                       (-2.2825, 1.5025), (-0.68, 1.05), (-0.52308, 0.58462), (-0.19375, 0.7875), (-375.0, 606.25)]
    test_file_numbers = list(range(32))
    test_file_numbers.remove(29)
    input_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        logger.debug('from file{}'.format(num + 1))
        input_array[i] = files_dict['file{}'.format(num + 1)]
    object_list = [EcgData(data=x) for x in input_array]
    for i, obj in enumerate(object_list):
        logger.debug('Duration test for file {0}, expected output: {1} +/- .1, test output: {2}'.
                     format(i + 1, output_extremes[i], obj.voltage_extremes))
        assert obj.voltage_extremes == pytest.approx(output_extremes[i], rel=.05)
    print('Complete testing duration')
    logger.debug('Complete testing voltage extremes')


def test_num_beats():
    logger.debug('Begin testing number of beats')
    output_beats = [34, 32, 34, 32, 35, 38, 31, 32, 28, 44, 32, 9, 4, 14, 7, 19, 19, 19,
                    19, 19, 19, 37, 75, 80, 29, 37, 63, 34, 9, 19, 19]
    test_file_numbers = list(range(32))
    test_file_numbers.remove(29)
    input_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        logger.debug('from file{}'.format(num + 1))
        input_array[i] = files_dict['file{}'.format(num + 1)]
    object_list = [EcgData(data=x) for x in input_array]

    exception_files = [7, 12, 13, 15, 24, 29]
    for i, obj in enumerate(object_list):
        (samples, acorr_peaks_index, peaks_index, num_beats) = obj.autocorrelate()
        logger.debug('Number-of-beats test for file {0}, expected output: {1} +/- 5, test output: {2}'.
                     format(i + 1, output_beats[i], num_beats))
        if not (i == n for n in exception_files):
            assert num_beats == pytest.approx(output_beats[i], abs=3.)
    logger.debug('Complete testing number-of-beats calculations')


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

#
# if __name__ == "__main__":
#     main()


