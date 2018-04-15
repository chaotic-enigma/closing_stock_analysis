import quandl
import auth
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

api_key = auth.key

df = quandl.get('NSE/ADANIPORTS', authtoken=api_key)
df = df.reset_index()

dates = [date.year for date in df['Date']]
dates = sorted(list(set(dates)))

m_dates = [m.month for m in df['Date']]
m_dates = sorted(list(set(m_dates)))

years = [str(each_year) for each_year in dates]
months = [str(each_month) for each_month in m_dates]

def add_element(dict, key):
    if key not in dict:
        dict[key] = months

adani_ports = {}

for each_year in years:
	add_element(adani_ports, each_year)

app.layout = html.Div([
		dcc.Dropdown(
			id='years',
			options=[{'label' : s,'value' : s} for s in adani_ports.keys()],
			value='2018'
		),
		html.Hr(),
		dcc.Dropdown(id='months'),
		html.Hr(),
		#html.Div(id='display-selected-values')
	],
	className = 'container',style = {'width' : '30%','margin-left' : 10,'margin-right' : 10,'max_width' : 50000}
)

app.scripts.config.serve_locally=True

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
	return option_present[0]['value']

if __name__ == '__main__':
	app.run_server(debug=True)


'''
app.config['suppress_callback_exceptions']=True
@app.callback(
	Output('display-selected-values','children'),
	[Input('years','value'),Input('month','value')]
)
def set_display_children(year_selected, month_selected):
	return '{} is a month in {}'.format(month_selected, year_selected)
'''