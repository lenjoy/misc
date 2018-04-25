# create a shared dir
mkdir -p $LOCAL_S3_DIR
if [ $USER = "admin" ]
then
  chmod 777 -R $LOCAL_S3_DIR
fi
aws s3 sync s3://blabla/somepath $LOCAL_S3_DIR

# clean up old versions in S3
for FN in dir_name1 dir_name2 dir_name3
do
    for (( i=90; i <= 120; i++ ))
    do
        DT=`date +%Y-%m-%d --date="$i days ago"`
        CMD="aws s3 rm s3://blabla/data_pipeline/DailyReportToS3/$FN/$DT"
        echo $CMD
        eval $CMD
    done
done
