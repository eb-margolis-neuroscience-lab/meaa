#!/usr/bin/env python
# coding: utf-8

import os, re
import csv

# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import scipy.io
# from scipy import signal, stats

# constants and unchanged function
from med64_data import bins_per_sec, lag_bins, lag_bins_ms, read_units_file

# in new Notebook (or new med64_data)
# from med64_data_v0_diff import find_expt_files as find_expt_files_2021
# or
# import med64_data_v0_diff as v0
# or 
# __ DO THIS __
# create YAML file manually changed names to old filenames
# and then only need:
# import med64_data_v0_diff as v0
# and call  v0.get_expt_data  in a couple places in new notebook.


# __NEXT__: 
# - perhaps the export notebook has it's own differences besides file load
# - make changes to observable to accept the new treatment row names
# everything else for observable should line up. (check this!!!)


def find_expt_files(data_dir):
    """Version v0 (2021) for legacy data format

    called once in old Notebook to supply list of filenames for tx, unit etc
        and called once and outside of function in the new Notebook too
    called only by main() in med_64.py

    To alternate, import this as a seperate name from new version and then 
    change that one line of code to call the old version

    This can also be REPLACED by creating appropriate YAML file:
        this is a copy of standard YAML with filenames manually 
        changed for the older unit_times.mat and treatments.csv files
    """
    files = os.listdir(data_dir)

    re_units = re.compile(r'^units.*')
    re_tx = re.compile(r'^treatmentinfo.*')
    re_expr_id = re.compile(r"([0-9]{3}_[0-9]{2}h[0-9]{2}m[0-9]{2}s)\.['csv|mat']{3}")

    unit_files = dict()
    tx_files = dict()

    for file in files:
        expr_id = re_expr_id.findall(file)
        if expr_id:
            units_file = re_units.findall(file)
            if units_file:
                unit_files[expr_id[0]] = units_file[0]
            tx_file = re_tx.findall(file)
            if tx_file:
                tx_files[expr_id[0]] = tx_file[0]
    expt_list = sorted(list(unit_files.keys()))

    print('FOUND Data FILES:')
    print('Experiment IDs: \n\t' + '\n\t'.join(expt_list))
    print('Units Files: \n\t' + '\n\t'.join(unit_files.values()))
    print('Treatment Files: \n\t' + '\n\t'.join(tx_files.values()))
    
    return expt_list, tx_files, unit_files


def read_tx_file(tx_filename):
    """Version v0 (2021) for legacy data format

    not called directly by the 2021 notebook
    called indirectly by other med64_data.py function: get_expt_data

    No changes necessary to alternate
    """
    tx_times = dict()
    with open(tx_filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            tx_times[row[1]] = float(row[0])
    return tx_times


def get_expt_data(data_dir, expt_id, unit_files, tx_files):
    """Version v0 (2021) for legacy data format
    called in old functions:
        get_mean_firing_rates, 
        data_to_qq
    and also called by these functions in new Notebook

    called only by main() in med_64.py

    To Alternate: ... this may be only tough one...
    change the code to use this v0.get_expt_data after importing as such
    these changes will need to be made in the notebook or the med64_data.main()
    and only on about 3 lines.  These could easily be flagged with a constant
    and if statements to allow alternation with a single line change for testing.

    the change to med64_data.main() only needed if using to analyze plots
    for autocorrelograms.  So for Observable, just make these changes for
    the few cells that use them, and an IF CONSTANT in the two functions that
    use this function.
    """
    unit_filename = data_dir + unit_files[expt_id]
    units_data = read_units_file(unit_filename)

    tx_filename = data_dir + tx_files[expt_id]
    tx_times = read_tx_file(tx_filename)
    
    return units_data, tx_times
