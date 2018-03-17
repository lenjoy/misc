from datetime import datetime, timedelta

# check a time window
lookback_days = 28
date_N_days_ago = datetime.now() - timedelta(days=lookback_days)

start_dt = date_N_days_ago.strftime('%Y-%m-%d')
