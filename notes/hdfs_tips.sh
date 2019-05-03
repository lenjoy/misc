# ls
hdfs dfs -ls hdfs://nameservice1/user/hive/warehouse/test.db/test_table 

# copy to local from hdfs
hdfs dfs -copyToLocal hdfs://nameservice1/user/hive/warehouse/test.db/test_table /tmp/test_table/

# copy from local to hdfs
hdfs dfs -copyFromLocal /tmp/test_table/000000_0 hdfs://nameservice1/user/hive/warehouse/test.db/test_table/000000_0
hdfs dfs -copyFromLocal /tmp/test_table/000000_1 hdfs://nameservice1/user/hive/warehouse/test.db/test_table/000000_1

# delete files in hdfs
hdfs dfs -rm -r hdfs://nameservice1/user/hive/warehouse/test.db/test_table/dt=2019-04-01
