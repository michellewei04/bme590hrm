import pandas as pd
from ecgdata import EcgData


test_data1 = pd.read_csv('test_data/test_data29.csv', na_values=0)
ecg_data1 = EcgData()
ecg_data1.data = test_data1
# print(test_data1.iloc[:, 1].values)
ecg_data1.autocorrelation()

