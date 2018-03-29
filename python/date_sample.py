from datetime import datetime, timedelta

# check a time window
lookback_days = 28

now = datetime.now()
date_N_days_ago = now - timedelta(days=lookback_days)
start_dt_str = date_N_days_ago.strftime('%Y-%m-%d')

given_day = datetime.strptime('2018-03-15', '%Y-%m-%d')
print((now - given_day).days)
