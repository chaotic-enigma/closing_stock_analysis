import quandl
import auth
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.graph_objs as go
import simplejson as json

app = dash.Dash(__name__)

current_year = datetime.now().year
current_month = datetime.now().month

api_key = auth.key

def analyze_close_stock(quandl_api_call):

	df = quandl.get(quandl_api_call, authtoken=api_key)
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
			return close
		except Exception as e:
			return ''

	app.layout = html.Div([
		html.H3(str(quandl_api_call),style={'textAlign' : 'center'}),
		html.Div([
			html.H4('Select Year: '),
			dcc.Dropdown(
				id='years',
				options=[{'label' : s,'value' : s} for s in adani_ports.keys()],
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

	app.config['suppress_callback_exceptions']=True
	@app.callback(
		Output('months','options'),
		[Input('years','value')]
	)
	def set_months_options(year_selected):
		return [{'label' : s,'value' : s} for s in adani_ports[year_selected]]

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

	@app.callback(
		Output('close_stock','figure'),
		[Input('years','value'), Input('months','value')]
	)
	def draw_close_stock(year, month):
		graphs = []
		close_value = collect_closing_stock(year, month)
		graphs.append(go.Scatter(
			x=[i+1 for i in range(len(close_value)+1)],
			y=close_value,
			name=str(year) + ' ' + str(month),
			mode='lines+markers'
			)
		)
		return {'data' : graphs}

	app.run_server(debug=True)
