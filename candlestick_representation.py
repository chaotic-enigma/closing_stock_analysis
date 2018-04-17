import quandl
import auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import simplejson as json

app = dash.Dash(__name__)

current_year = datetime.now().year
current_month = datetime.now().month

api_key = auth.key
df = quandl.get('NSE/ZENSARTECH', authtoken=api_key)
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

store_value = {}
for each_year in years:
	add_element(store_value, each_year)

y_m_close = zip(df['Date'],df['Close']) # len 1546
y_m_open = zip(df['Date'],df['Open'])
y_m_high = zip(df['Date'],df['High'])
y_m_low = zip(df['Date'],df['Low'])
def collect_stock_value(year, month):
	close = []
	for i in y_m_close:
		y = i[0].year
		m = i[0].month
		if y == year and m == month:
			close.append(i[1])

	open_v = []
	for i in y_m_open:
		y = i[0].year
		m = i[0].month
		if y == year and m == month:
			open_v.append(i[1])

	high = []
	for i in y_m_high:
		y = i[0].year
		m = i[0].month
		if y == year and m == month:
			high.append(i[1])

	low = []
	for i in y_m_low:
		y = i[0].year
		m = i[0].month
		if y == year and m == month:
			low.append(i[1])

	return close, open_v, high, low

app.layout = html.Div([
	#html.H3(str(quandl_api_call),style={'textAlign' : 'center'}),
	html.Div([
		html.H4('Select Year: '),
		dcc.Dropdown(
			id='years',
			options=[{'label' : s,'value' : s} for s in store_value.keys()],
			value=current_year
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
		])
	]	#html.Hr()s
)

def generate_table(year, month):
	return html.Table(className='reaponsive-table',
			children=[
				html.Thead(
					html.Tr(
						children=[html.Th(col.title()) for col in df.columns.values]
					)
				),
				html.Tbody([
					html.Tr(
						children=[html.Td(data) for data in d]
					)
				for d in df.values.tolist()])
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
	if current_year:
		return current_month
	else:
		return option_present[0]['value']

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
				stock.update({i : {mi : collect_stock_value(i,mi)}})
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
	return generate_table(provide_year, provide_month)

@app.callback(
	Output('close_stock','figure'),
	[Input('years','value'), Input('months','value')]
)
def draw_close_stock(year, month):
	graphs = []
	close_value, open_value, high_value, low_value = collect_stock_value(year, month)
	graphs.append(go.Candlestick(
			x=[i+1 for i in range(len(close_value)+1)],
			open=open_value,
			high=high_value,
			low=low_value,
			close=close_value,
			name=str(year) + ' ' + str(month),
			#mode='lines+markers',
		)
	)
	layout = dict(title = str(year) + ' - ' + str(month) + ' Stock',
        yaxis = dict(zeroline = False),
        xaxis = dict(zeroline = False)
    )
	return {'data' : graphs,'layout' : layout}

if __name__ == '__main__':
	app.run_server(debug=True)
