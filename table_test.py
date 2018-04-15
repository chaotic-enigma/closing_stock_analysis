import quandl
import auth
import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dte
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import simplejson as json
import pandas as pd
import base64
import csv
import io

app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

api_key = auth.key

df = quandl.get('NSE/KOTAKNIFTY', authtoken=api_key)
df = df.reset_index()

outcsv = pd.DataFrame.to_csv(df, sep = ",")
with open('whole_data.csv','w') as dump_data:
	dump_data.write(outcsv)

dates = [date.year for date in df['Date']]
dates = sorted(list(set(dates)))

m_dates = [m.month for m in df['Date']]
m_dates = sorted(list(set(m_dates)))

years = [each_year for each_year in dates]
months = [each_month for each_month in m_dates]

fields = [field.decode('utf8') for field in df]
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
		return close
	except Exception as e:
		return ''

app.layout = html.Div([
	#html.H3(str(quandl_api_call),style={'textAlign' : 'center'}),
	html.Div([
		html.H4('Select Year: '),
		dcc.Dropdown(
			id='years',
			options=[{'label' : s,'value' : s} for s in adani_ports.keys()],
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
	html.Div([
		html.H4('Table Contents'),
		html.Div(dte.DataTable(rows=[{}], id='table')),
		dcc.Upload(id='upload-data')
	])
])

@app.callback(
	Output('months','options'),
	[Input('years','value')]
)
def set_months_options(year_selected):
	return [{'label' : s,'value' : s} for s in adani_ports[year_selected]]

@app.callback(
	Output('months','value'),
	[Input('months','options')]
)
def set_months_values(option_present):
	return option_present[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('years', 'value'),
     dash.dependencies.Input('months', 'value')]
)
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
							accurate.append(accu)
	#print(accurate)
	closed = json.dumps(accurate)
	return list(closed)

def parse_contents(contents, filename):
	content_type, content_string = contents.split(',')

	decoded = base64.b64decode(content_string)
	try:
		if filename == 'imp_data.csv':
			tdf = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
	except Exception as e:
		print(e)
		return None

	return tdf

@app.callback(
	Output('table', 'rows'),
	[Input('upload-data', 'contents'), Input('upload-data', 'filename')]
)
def update_output(contents, filename):
	if contents is not None:
		tdf = parse_contents(contents, filename)
		if tdf is not None:
			return tdf.to_dict('records')
		else:
			return[{}]
	else:
		return [{}]

@app.callback(
	Output('close_stock','figure'),
	[Input('years','value'), Input('months','value')]
)
def draw_close_stock(year, month):
	graphs = []
	close_value = collect_closing_stock(year, month)
	grab_important(year, month)
	graphs.append(go.Scatter(
		x=[i+1 for i in range(len(close_value))],
		y=close_value,
		name=str(year) + ' ' + str(month),
		mode='lines+markers'
		)
	)
	return {'data' : graphs}


app.run_server(debug=True)