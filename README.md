# BME 590 Heart Rate Monitor

## ECG Signal Processing

[![Build Status](https://travis-ci.org/michellewei04/bme590hrm.svg?branch=master)](https://travis-ci.org/michellewei04/bme590hrm)
[![Documentation Status](https://readthedocs.org/projects/yw145bme590hrm/badge/?version=latest)](http://yw145bme590hrm.readthedocs.io/en/latest/?badge=latest)

__Contributors:__ Michelle Wei (@michellewei04)

__Documentation:__ [readthedocs.org](http://yw145bme590hrm.readthedocs.io/en/latest/)

## Overview

This project uses an object-oriented approach to process ECG data. The class, `EcgData` , is used to analyze the data read from a CSV file, and several attributes of the class are assigned:
- `filename`: a string containing the name of the CSV file from which the data were read
- `data`: a numpy array of a two-column set of floats in which column 1 specifies time of recording and column 2 specifies voltage
- `mean_hr_bpm`: an estimate of the average heart rate over a user-specified number of minutes (the default interval is the entire recording)
- `voltage_extremes`: a tuple containing the minimum and maximum lead voltages in the recording
- `duration`: the time duration of the ECG strip in seconds
- `num_beats`: the total number of detected beats in the recording
- `beats`: a numpy array of times (in seconds) when a beat occurred

Additionally, a set of JSON files with the same name as the input CSV file are generated and saved. They contain the values of all of the `EcgData` attributes.
