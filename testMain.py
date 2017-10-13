#!/usr/bin/env python
# encoding: utf-8

"""
@author: kyle
@time: 10/12/17 3:40 PM
"""

import pandas as pd
import numpy as np

root_dir_remote = '~/dataset/'
root_dir_local = '~/Documents/tianchi/'

root_dir = root_dir_remote

train_online = pd.read_csv(root_dir + 'o2o/ccf_online_stage1_train.csv')
train_offline = pd.read_csv(root_dir + 'o2o/ccf_offline_stage1_train.csv')
test = pd.read_csv(root_dir + 'o2o/ccf_offline_stage1_test_revised.csv')

all_offline = pd.concat([train_offline, test], keys=['train', 'test'])

all_offline.apply(lambda x : sum(x.isnull()))

all_offline['Date'] = all_offline['Date'].fillna('null')

# pd.merge(all_offline, train_offline, on=['User_id', 'Merchant_id'])

def is_used(column):
    if column['Coupon_id'] != 'null' and column['Date'] != 'null':
        return 1
    elif column['Coupon_id'] != 'null' and column['Date'] == 'null':
        return -1
    else:
        return 0

all_offline['is_used'] = all_offline.apply(is_used, axis=1)

all_offline['has_coupon'] = all_offline.apply(lambda x: 1 if x['Coupon_id'] != 'null' else 0, axis=1)

import re
regex = re.compile(r'^\d+:\d+$')

def percent(column):
    if column['Coupon_id'] == 'null' or column['Discount_rate'] == 'null':
        return 'null'
    elif re.match(regex, column['Discount_rate']):
        num_max, num_min = column['Discount_rate'].split(':')
        num_max = float(num_max)
        num_min = float(num_min)
        return float((num_max - num_min) / num_max)
    else:
        return column['Discount_rate']

all_offline['discount_percent'] = all_offline.apply(percent, axis=1)


def discount_limit(column):
    if column['Coupon_id'] == 'null' or column['Discount_rate'] == 'null':
        return 'null'
    elif re.match(regex, column['Discount_rate']):
        num_max, num_min = column['Discount_rate'].split(':')
        return num_max
    else:
        return 0

all_offline['discount_limit'] = all_offline.apply(discount_limit, axis=1)

import datetime

def used_in_15day(column):
    if column['is_used'] == 1 and column['Date_received'] != 'null' and column['Date'] != 'null':
        days = (datetime.datetime.strptime(column['Date'], "%Y%m%d") - datetime.datetime.strptime(column['Date_received'], "%Y%m%d")).total_seconds() / 86400
        if days < 15:
            return 1
        else:
            return 0
    else:
        return 0

all_offline['is_used_in_15day'] = all_offline.apply(used_in_15day, axis=1)

print(all_offline['discount_percent'].value_counts())

# null                  701602
# 0.9                   403589
# 0.8333333333333334    330255
# 0.75                  103748
# 0.95                   69099
# 0.8                    56084
# 0.7                    38425
# 0.85                   29585
# 0.5                    28785
# 0.9666666666666667     22195
# 0.95                   21559
# 0.8666666666666667     17685
# 0.6666666666666666     13497
# 0.9                     8912
# 0.6                     8300
# 0.9333333333333333      5452
# 0.8                     4176
# 0.98                    3693
# 0.85                     650
# 0.99                     551
# 0.5                      196
# 0.75                     121
# 0.2                      110
# 0.975                     75
# 0.6                       59
# 0.3333333333333333        56
# 0.7                       55
# 0.4                        9
# 0.94                       1
# Name: Discount_percent, dtype: int64


"""
no discount_percent_layer
"""

def discount_limit_layer(column):
    if column == 'null':
        return 'null'
    column = int(column)
    if column <= 10:
        return 10
    elif column <= 20:
        return 20
    elif column <= 30:
        return 30
    elif column <= 50:
        return 50
    elif column <= 100:
        return 100
    elif column <= 200:
        return 200
    else:
        return 300

all_offline['discount_limit_layer'] = all_offline['discount_limit'].apply(discount_limit_layer, axis=1)

train_finally, test_finally = all_offline[:train_offline.shape[0]], all_offline[train_offline.shape[0]:]
all_offline.to_csv('output/all_offline.csv')
train_finally.to_csv('output/train_finally.csv')
test_finally.to_csv('output/test_finally.csv')

# all_offline_new = pd.get_dummies(all_offline_new)






