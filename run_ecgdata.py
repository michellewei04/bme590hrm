import pandas as pd
from ecgdata import EcgData
from glob import glob
import numpy as np

files_dict = {}
file_number = 0
all_csv_files = glob('test_data/*.csv')
if 'test_data/test_data30.csv' in all_csv_files:
    all_csv_files.remove('test_data/test_data30.csv')
# print(all_csv_files)
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
    print('Begin running file {}'.format(file_number))
    ecg_data = EcgData()
    ecg_data.data = files_dict[filename]
    print('file {0}, min: {1}, max:{2}'.format(file_number, np.nanmin(ecg_data.data[:, 1]),
                                               np.nanmax(ecg_data.data[:, 1])))
