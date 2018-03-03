from ecgdata import EcgData
import logging
from logging_config import config
import pytest
from import_test_files import collect_data
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# init logging config
logging.basicConfig(**config)
logger = logging.getLogger(__name__)

all_csv_files = glob('test_data/*.csv')


def main():
    test_beats()


def test_get_data():
    logger.debug('Begin testing setter function')
    error_file = ['test_data/test_data30.csv']
    with pytest.raises(TypeError):
        EcgData(filename=error_file)
    logger.debug('Complete testing check inputs function')


def test_duration():
    logger.debug('Begin testing duration')
    output_duration = [27.775, 13.887, 39.996, 27.775, 13.887]
    test_file_numbers = [1, 13, 24, 28, 31]
    filename_array = [None] * len(test_file_numbers)

    for i, num in enumerate(test_file_numbers):
        filename_array[i] = 'test_data/test_data{}.csv'.format(num)
    object_list = [EcgData(filename=x, data=collect_data(x)) for x in filename_array]
    for i, obj in enumerate(object_list):
        (data, duration) = obj.set_duration('seconds')
        logger.debug('Duration test for file {0}, expected output: {1} +/- .1, test output: {2}'.
                     format(i + 1, output_duration[i], duration))
        assert duration == pytest.approx(output_duration[i], rel=.01)
    print('Complete testing duration')
    logger.debug('Complete testing duration')


def test_voltage_extremes():
    logger.debug('Begin testing voltage extremes')
    output_extremes = [(-0.68, 1.05), (-0.735, 0.955), (-1.155, 1.72),
                       (-1.58, 1.555), (-0.33077, 0.7), (-1.4525, 1.58)]
    test_file_numbers = [1, 3, 5, 10, 15, 25]
    filename_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        filename_array[i] = 'test_data/test_data{}.csv'.format(num)
    print(filename_array)
    object_list = [EcgData(filename=x, data=collect_data(x)) for x in filename_array]
    for i, obj in enumerate(object_list):
        logger.debug('Duration test for file {0}, expected output: {1} +/- .1, test output: {2}'.
                     format(i + 1, output_extremes[i], obj.voltage_extremes))
        assert obj.voltage_extremes == pytest.approx(output_extremes[i], rel=.05)
    print('Complete testing duration')
    logger.debug('Complete testing voltage extremes')


def test_num_beats():
    logger.debug('Begin testing number of beats')
    output_beats = [34, 34, 35, 44, 19, 34, 19]
    test_file_numbers = [1, 3, 5, 10, 16, 28, 32]
    filename_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        filename_array[i] = 'test_data/test_data{}.csv'.format(num)

    object_list = [EcgData(filename=x, data=collect_data(x)) for x in filename_array]
    print(object_list)
    for i, obj in enumerate(object_list):
        (samples, acorr_peaks_index, peaks_index, num_beats) = obj.autocorrelate()
        logger.debug('Number-of-beats test for file {0}, expected output: {1} +/- 5, test output: {2}'.
                     format(i + 1, output_beats[i], num_beats))
        assert num_beats == pytest.approx(output_beats[i], abs=3.)
    logger.debug('Complete testing number-of-beats calculations')


def test_calc_hr():
    logger.debug('Begin testing heart rate calculations')
    output_beats = [34, 35, 38, 32, 19, 75, 34, 19]
    test_file_numbers = [1, 5, 6, 11, 18, 23, 28, 31]
    filename_array = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        filename_array[i] = 'test_data/test_data{}.csv'.format(num)

    object_list = [EcgData(filename=x, data=collect_data(x)) for x in filename_array]
    max_time_array = [x.max_time for x in object_list]
    output_hr = np.multiply(np.divide(output_beats, max_time_array), 60)
    output_hr = [float(i) for i in output_hr.tolist()]
    exception_files = [7, 12, 13, 15, 24, 29]
    for i, obj in enumerate(object_list):
        logger.debug('Heart rate test for file {0}, expected output: {1} +/- 5, test output: {2}'.
                     format(i + 1, int(output_hr[i]), int(obj.mean_hr_bpm)))
        if not (i == n for n in exception_files):
            assert obj.mean_hr_bpm == pytest.approx(output_hr[i], abs=5.)
    logger.debug('Complete testing heart rate calculations')


def test_beats():
    logger.debug('Begin testing get_beat_times')
    test_file_numbers = [1, 3, 21, 31]
    filename_array = [None] * len(test_file_numbers)
    object_list = [None] * len(test_file_numbers)
    figures = [None] * len(test_file_numbers)
    for i, num in enumerate(test_file_numbers):
        filename_array[i] = 'test_data/test_data{}.csv'.format(num)
        object_list[i] = EcgData(filename=filename_array[i], data=collect_data(filename_array[i]))
        (beat_times, output_beat_times, peaks_index, new_peaks_index) = object_list[i].get_beat_times()
        logger.debug('Test the first 10 beat times for file {0}, expected output: {1}, test output: {2}'.
                     format(num, output_beat_times[:10], beat_times[:10]))
        assert beat_times[:10] == pytest.approx(output_beat_times[:10], abs=0.3)

        # figures[i] = plt.figure(i)
        # plt.plot(obj.data[:, 0], obj.data[:, 1])
        # plt.scatter(output_beat_times[:10], obj.data[:, 1][new_peaks_index[:10]], color='red')
        # plt.scatter(beat_times[:10], obj.data[:, 1][peaks_index[:10]], color='blue')
        # plt.title('file{0}, avg error = {1}'.format(test_file_numbers[i] +
        # 1, np.average(output_beat_times[:10] - beat_times[:10])))
        #
        # figures[i].show()
        # figures[i].savefig('plots/BeatTime{}.png'.format(test_file_numbers[i] + 1))

        logger.debug('Complete testing duration')


if __name__ == "__main__":
    main()
