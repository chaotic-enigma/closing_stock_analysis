import quandl
import pandas as pd
import csv
from datetime import datetime
from collections import defaultdict

key = 'tq-Xb-y63br1eq1j1jD3'
q_df = quandl.get('NSE/KOTAKNIFTY',authtoken=key)
q_df = q_df.reset_index()

outcsv = pd.DataFrame.to_csv(q_df, sep = ",")
with open('whole_data.csv','w') as dump_data:
	dump_data.write(outcsv)

years = [date.year for date in q_df['Date']]
years = sorted(list(set(years)))

months = [m.month for m in q_df['Date']]
months = sorted(list(set(months)))

fields = [field.decode('utf8') for field in q_df]
whole_data = pd.read_csv('whole_data.csv', skipinitialspace=True)

each_row = whole_data[fields]
row_list = [list(x) for x in each_row.values]

def grab_important(year, month):
	for row in row_list:
		stds = datetime.strptime(row[0], '%Y-%m-%d')
		row[0] = stds

	specific_data = []
	for row in row_list:
		if row[0].year == year and row[0].month == month:
			specific_data.append(row)

	with open('imp_data.csv', 'w') as imp:
		writer = csv.writer(imp)
		writer.writerows(specific_data)

	add_head = pd.read_csv('imp_data.csv')
	add_head.columns = fields
	add_head.to_csv('imp_data.csv')

grab_important(2016,7)