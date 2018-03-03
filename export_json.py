import pandas as pd
import numpy as np
from glob import glob
from ecgdata import EcgData
import os
import re
import json
from import_test_files import collect_data


def main():
    export_json()


def export_json():
    """
    Reads all csv files and writes json file with all object attributes

    """
    allcsvfiles = glob('test_data/*.csv')

    for i, csvfile in enumerate(allcsvfiles):
        if csvfile != 'test_data/test_data30.csv':
            obj = EcgData(filename=csvfile, data=collect_data(csvfile))
            filename = os.path.splitext(csvfile)[0]
            jsonfile = filename + '.json'
            print(jsonfile)
            data = {
                'mean_hr_bpm': [obj.mean_hr_bpm],
                'voltage_extremes': [obj.voltage_extremes[0], obj.voltage_extremes[1]],
                'duration': [obj.duration],
                'number of beats in the recording': [obj.num_beats],
                'times that beats occurred': [obj.beats.tolist()],
            }
            print(data)

            with open(jsonfile, 'w') as fp:
                json.dump(data, fp)
    pass


if __name__ == "__main__":
    main()
