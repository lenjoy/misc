import csv
import os

import tensorflow as tf

COLUMNS = [
  'age', 'workclass', 'fnlwgt', 'education', 'education_num',
  'marital_status', 'occupation', 'relationship', 'race', 'gender',
  'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'income_bracket']

TAG_DICT = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6,
            'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13}


def float_feature(x):
  return tf.train.Feature(float_list=tf.train.FloatList(value=[float(x)]))

def int64_feature(x):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[int(x)]))

def bytes_feature(x):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[bytes(x, 'utf-8')]))


def generate_tfrecords(input_filename, output_filename):
  print("Start to convert {} to {}".format(input_filename, output_filename))
  writer = tf.python_io.TFRecordWriter(output_filename)

  with open(input_filename, 'r') as csvfile:
    r = csv.reader(csvfile)
    cnt = 0
    for row in r:
      cnt += 1
      # 39,State-gov,77516,Bachelors,13,Never-married,Adm-clerical,Not-in-family,White,Male,2174,0,40,United-States,<=50K

      if cnt % 1000 == 0:
        print('{} rows are processed'.format(cnt))

      if not row:
        continue

      example = tf.train.Example(features=tf.train.Features(
          feature={
            'age': int64_feature(row[0]),
            'education_num': int64_feature(row[4]),
            'capital_gain': int64_feature(row[10]),
            'capital_loss': int64_feature(row[11]),
            'hours_per_week': int64_feature(row[12]),

            'education': bytes_feature(row[3]),
            'marital_status': bytes_feature(row[5]),
            'relationship': bytes_feature(row[7]),
            'workclass': bytes_feature(row[1]),
            'occupation': bytes_feature(row[6]),

            'income_bracket': bytes_feature(row[14]),

            # multi-hot: aa-bb-cc
            'occupation_sp': tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[bytes(x, 'utf-8') for x in row[6].split('-')])),

            'fnlwgt': int64_feature(row[12]),
            'native_country': bytes_feature(row[13]),
            'race': bytes_feature(row[8]),
            'gender': bytes_feature(row[9]),
            }))

      writer.write(example.SerializeToString())

  writer.close()
  print('Successfully convert {} to {}'.format(input_filename, output_filename))


def main():
  for filename in ['/tmp/census_data/adult.data', '/tmp/census_data/adult.test']:
    generate_tfrecords(filename, filename + '.tfrecords')


if __name__ == "__main__":
    main()
