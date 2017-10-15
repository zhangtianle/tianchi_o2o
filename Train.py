#!/usr/bin/env python
# encoding: utf-8

"""
@author: kyle
@time: 10/13/17 7:37 PM
"""
import pandas as pd

root_dir_remote = '~/dataset/o2o/'
root_dir_local = '~/Documents/tianchi/o2o/'

root_dir = root_dir_remote

train_offline = pd.read_csv(root_dir + 'ccf_offline_stage1_train.csv')

all_offline = pd.read_csv('output/all_offline.csv')
all_offline_new = all_offline[['User_id', 'Merchant_id', 'Coupon_id', 'is_used', 'is_used_in_15day', 'Distance', 'discount_percent_layer', 'discount_limit_layer', 'has_coupon']]

print(all_offline_new.head(10))
all_offline_new = pd.get_dummies(all_offline_new)
train_, test_ = all_offline_new[:train_offline.shape[0]], all_offline_new[train_offline.shape[0]:]

train_ = train_[train_['has_coupon'] == 1]

train_ = train_.drop(['has_coupon'], axis=1)
test_ = test_.drop(['has_coupon'], axis=1)

X_train = train_.drop(['is_used_in_15day'], axis=1)
Y_train = pd.DataFrame({"is_used_in_15day": train_['is_used_in_15day']})
X_test = test_.drop(['is_used_in_15day'], axis=1)

from sklearn.linear_model import LinearRegression
clf = LinearRegression()
clf.fit(X_train, Y_train)
predict = clf.predict(X_test)

result = pd.read_csv(root_dir + 'ccf_offline_stage1_test_revised.csv')
result['Probability'] = predict
result = result.drop(['Merchant_id', 'Discount_rate', 'Distance'], axis=1)

result['Probability'] = result['Probability'].apply(lambda x:0 if x<0 else x)
result.to_csv('./output/sample_submission.csv')

