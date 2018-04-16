import quandl
import auth
import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import simplejson as json
import csv

app = dash.Dash(__name__)

api_key = auth.key

def data_as_per_the_year_and_month(dataset):	
	try:
		df = quandl.get(dataset, authtoken=api_key)
		df = df.reset_index()

		outcsv = pd.DataFrame.to_csv(df, sep=",")
		with open('whole_data.csv','w') as dump_data:
			dump_data.write(outcsv)

		dates = [date.year for date in df['Date']]
		dates = sorted(list(set(dates)))

		m_dates = [m.month for m in df['Date']]
		m_dates = sorted(list(set(m_dates)))

		years = [each_year for each_year in dates]
		months = [each_month for each_month in m_dates]

		fields = [field.decode('utf-8') for field in df]
		whole_data = pd.read_csv('whole_data.csv', skipinitialspace=True)

		each_head = whole_data[fields]
		row_list = [list(x) for x in each_head.values]

		def add_element(dict, key):
			if key not in dict:
				dict[key] = months

		store_value = {}
		for each_year in years:
			add_element(store_value, each_year)

		y_m_close = zip(df['Date'],df['Close']) # len 1546
		def collect_closing_stock(year, month):
			try:
				close = []
				for i in y_m_close:
					y = i[0].year
					m = i[0].month
					if y == year and m == month:
						close.append(i[1])
				return close
			except Exception as e:
				return ''

		app.layout = html.Div([
			html.H3(str(dataset),style={'textAlign' : 'center'}),
			html.Div([
				html.H4('Select Year: '),
				dcc.Dropdown(
					id='years',
					options=[{'label' : s,'value' : s} for s in store_value.keys()],
					value=2018
				),
				html.Hr(),
				html.H4('Select Month: '),
				dcc.Dropdown(id='months'),
				html.Hr(),
			],
			className='container',style = {'width' : '30%','margin-left' : 10,'margin-right' : 10}),
			html.Div([
				dcc.Graph(id='close_stock'),
				html.Div(id='display-selected-values')
			]),
		])

		app.config['suppress_callback_exceptions']=True
		@app.callback(
			Output('months','options'),
			[Input('years','value')]
		)
		def set_months_options(year_selected):
			return [{'label' : s,'value' : s} for s in store_value[year_selected]]

		app.config['suppress_callback_exceptions']=True
		@app.callback(
			Output('months','value'),
			[Input('months','options')]
		)
		def set_months_values(option_present):
			return option_present[0]['value']

		def grab_important_data(year, month):
			try:
				for row in row_list:
					stds = pd.Timestamp(row[0])
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

				dfd = pd.read_csv('imp_data.csv')
				dfd.to_html('table.html')

			except Exception as e:
				print(e)

		def generate_table(year, month):
			imp_df = pd.read_csv('imp_data.csv')
			return html.Table(className='reaponsive-table',
					children=[
						html.Thead(
							html.Tr(
								children=[html.Th(col.title()) for col in imp_df.columns.values]
							)
						),
						html.Tbody([
							html.Tr(
								children=[html.Td(data) for data in d]
							)
						for d in imp_df.values.tolist()])
					])

		app.config['suppress_callback_exceptions']=True
		@app.callback(
			Output('display-selected-values', 'children'),
			[Input('years', 'value'),
			 Input('months', 'value')]
		)
		def monthly_close(provide_year, provide_month):
			whole_data = []
			for i in store_value:
				for m in store_value.values():
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
									accurate.append(accu)

			closed = json.dumps(accurate)
			grab_important_data(provide_year, provide_month)
			return generate_table(provide_year, provide_month)

		@app.callback(
			Output('close_stock','figure'),
			[Input('years','value'), Input('months','value')]
		)
		def draw_close_stock(year, month):
			graphs = []
			close_value = collect_closing_stock(year, month)
			graphs.append(go.Scatter(
					x=[i+1 for i in range(len(close_value))],
					y=close_value,
					name=str(year) + ' ' + str(month),
					mode='lines+markers',
				)
			)
			layout = dict(title = str(year) + '-' + str(month) + ' Stock',
				yaxis = dict(zeroline = False),
				xaxis = dict(zeroline = False)
			)
			
			return {'data' : graphs,'layout' : layout}

		app.run_server(debug=True)

	except Exception as e:
		print(str(e))
