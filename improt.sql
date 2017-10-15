CREATE TABLE offline_train (
  User_id       INT,
  Merchant_id   INT,
  Coupon_id     INT,
  Discount_rate VARCHAR(10),
  Distance      VARCHAR(20),
  Date_received VARCHAR(10),
  Date          VARCHAR(10)
);

CREATE TABLE offline_test (
  User_id       INT,
  Merchant_id   INT,
  Coupon_id     INT,
  Discount_rate VARCHAR(10),
  Distance      VARCHAR(20),
  Date_received VARCHAR(10)
);

CREATE TABLE online_train (
  User_id       INT,
  Merchant_id   INT,
  Action        INT,
  Coupon_id     INT,
  Discount_rate VARCHAR(10),
  Date_received VARCHAR(10),
  Date varchar(10)
);


LOAD DATA LOCAL INFILE '~/dataset/o2o/ccf_offline_stage1_train.csv'
INTO TABLE offline_train FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '~/dataset/o2o/ccf_offline_stage1_test_revised.csv'
INTO TABLE offline_test FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '~/dataset/o2o/ccf_online_stage1_train.csv'
INTO TABLE online_train FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';