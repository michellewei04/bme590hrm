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


if __name__ == "__main__":
    main()
