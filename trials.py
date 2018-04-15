import quandl
import auth
import datetime
import simplejson as json
import matplotlib.pyplot as plt


#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#from dash.dependencies import Input, Output

api_key = auth.key

df = quandl.get('NSE/ADANIPORTS', authtoken=api_key)
df = df.reset_index()

dates = [date.year for date in df['Date']]
dates = sorted(list(set(dates)))

m_dates = [m.month for m in df['Date']]
m_dates = sorted(list(set(m_dates)))

years = [each_year for each_year in dates]
months = [each_month for each_month in m_dates]

def add_element(dict, key):
    if key not in dict:
        dict[key] = months

adani_ports = {}

for each_year in years:
	add_element(adani_ports, each_year)

y_m_close = zip(df['Date'],df['Close']) # len 1546
def collect_closing_stock(year, month):
	try:
		close = []
		for i in y_m_close:
			y = i[0].year
			m = i[0].month
			if y == year and m == month:
				close.append(i[1])
		return i[0]
	except Exception as e:
		return ''

print collect_closing_stock(2018,2)
'''
def monthly_close(provide_year, provide_month):
	whole_data = []
	for i in adani_ports:
		for m in adani_ports.values():
			for mi in m:
				stock = {}
				stock.update({i : {mi : collect_closing_stock(i,mi)}})
				whole_data.append(stock)

	clean = []
	for i in whole_data:
		if i not in clean:
			clean.append(i)

	accurate = []
	for i in clean:
		for year, months in i.items():
			if year == provide_year:
				for month_key, month_value in months.items():
					if month_key == provide_month:
						for accu in month_value:
							accurate.append(float(accu))
	accurate = json.dumps(accurate)
	return accurate
for i in monthly_close(2018,3):
	print type(i)'''