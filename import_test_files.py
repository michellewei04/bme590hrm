import pandas as pd
import numpy as np
from glob import glob


def main():
    collect_all_test_data()


def collect_all_test_data():
    files_dict = {}
    all_csv_files = glob('test_data/*.csv')
    # if 'test_data/test_data30.csv' in all_csv_files:
    #     all_csv_files.remove('test_data/test_data30.csv')
    for n, file in enumerate(all_csv_files):
        if len(file) == 24:
            file_number = int(file[19])
            filename = 'file%d' % file_number
            files_dict[filename] = pd.read_csv(file, delimiter=',', index_col=None)
        elif len(all_csv_files[n]) == 25:
            file_number = int(file[19:21])
            filename = 'file%d' % file_number
            files_dict[filename] = pd.read_csv(file, delimiter=',', index_col=None)
        else:
            print('Unexpected filename, csv filename length = {}'.format(len(all_csv_files[n])))
    return files_dict


if __name__ == "__main__":
    main()
