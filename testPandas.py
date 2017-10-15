#!/usr/bin/env python
# encoding: utf-8

"""
@author: kyle
@time: 10/13/17 7:31 PM
"""

import pandas as pd

root_dir_remote = '~/dataset/o2o/'
root_dir_local = '~/Documents/tianchi/o2o/'

root_dir = root_dir_local

train_online = pd.read_csv(root_dir + 'ccf_offline_stage1_test_revised.csv')
# print(train_online.head(1))
print(train_online[['User_id', 'Merchant_id']])
