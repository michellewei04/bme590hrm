import pandas as pd
from ecgdata import EcgData
from glob import glob


# test_data1 = pd.read_csv('test_data/test_data25.csv', na_values=0)
# ecg_data1 = EcgData()
# ecg_data1.data = test_data1
# # print(test_data1.iloc[:, 1].values)
# ecg_data1.autocorrelation()

files_dict = {}
file_number = 0
all_csv_files = glob('test_data/*.csv')
if 'test_data/test_data30.csv' in all_csv_files:
    all_csv_files.remove('test_data/test_data30.csv')
print(all_csv_files)
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
    ecg_data.autocorrelation(file_number)
    print('End running file {}'.format(file_number))
