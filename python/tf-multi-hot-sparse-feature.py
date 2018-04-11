"""
Support multi-hot sparse feature

From the sample code in https://www.tensorflow.org/tutorials/wide_and_deep
"""

def input_fn(data_file, num_epochs, shuffle, batch_size):
    """Generate an input function for the Estimator."""

    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    table = tf.contrib.lookup.index_table_from_file(
        vocabulary_file='test.txt', num_oov_buckets=1)

    def parse_csv(value):
        print('Parsing', data_file)
        columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
        features = dict(zip(_CSV_COLUMNS, columns))

        # support multi-hot sparse features, such as: "12,34,aa|bb|cc,23"
        split_tags = tf.string_split([columns[6]], "-")
        print(split_tags.get_shape())
        categorical_cols = {
            k + '_sp': tf.SparseTensor(
                indices=split_tags.indices,
                values=table.lookup(split_tags.values),
                dense_shape=split_tags.dense_shape)
            for k in ['occupation']}
        features.update(categorical_cols)
        
        labels = features.pop('income_bracket')
        return features, tf.equal(labels, '>50K')

    # Extract lines from input files using the Dataset API.
    dataset = tf.data.TextLineDataset(data_file)

    if shuffle:
        dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

    dataset = dataset.map(parse_csv, num_parallel_calls=5)

    # We call repeat after shuffling, rather than before, to prevent separate
    # epochs from blending together.
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset
