import pandas as pd
import numpy as np
from glob import glob


def main():
    collect_all_test_data()


def collect_all_test_data():
    files_dict = {}
    all_csv_files = glob('test_data/*.csv')
    for n, file in enumerate(all_csv_files):
        filename = 'file%s' % all_csv_files[n]
        files_dict[filename] = pd.read_csv(file, delimiter=',', index_col=None)


if __name__ == "__main__":
    main()
