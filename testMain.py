#!/usr/bin/env python
# encoding: utf-8

"""
@author: kyle
@time: 10/12/17 3:40 PM
"""

import pandas as pd
import numpy as np

train_online = pd.read_csv('/home/kyle/Documents/tianchi/o2o/ccf_online_stage1_train.csv')
train_offline = pd.read_csv('/home/kyle/Documents/tianchi/o2o/ccf_offline_stage1_train.csv')
test = pd.read_csv('/home/kyle/Documents/tianchi/o2o/ccf_offline_stage1_test_revised.csv')

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
        return float((num_max - num_min) / num_max)
    else:
        return column['Discount_rate']

all_offline['Discount_rate'] = all_offline.apply(percent, axis=1)


def discount_limit(column):
    if column['Coupon_id'] == 'null' or column['Discount_rate'] == 'null':
        return 'null'
    elif re.match(regex, column['Discount_rate']):
        num_max, num_min = column['Discount_rate'].split(':')
        return num_max
    else:
        return 0

all_offline['Discount_limit'] = all_offline.apply(discount_limit, axis=1)

import datetime

def used_in_15day(column):
    if column['is_used'] == 1 and column['Date_received'] != 'null' and column['Date'] != 'null':
        days = (datetime.datetime.strftime(column['Date'], "%Y%m%d") - datetime.datetime.strftime(column['Date_received'], "%Y%m%d"))
        if days < 15:
            return 1
        else:
            return 0
    else:
        return 0

all_offline['is_used_in_15day'] = all_offline.apply(used_in_15day, axis=1)

print(all_offline['Discount_percent'].value_counts())

