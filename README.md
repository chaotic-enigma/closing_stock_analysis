# closing_stock_analysis

This is for analysing the closing stock values wherein it requires a *Qunadle* datasets, easily acquired from the quandle website after creating an account. 

The package requirements are: 
```
quandl
dash
dash_core_components
dash_html_components
plotly

easily obtained by just typing pip install <package_name> on terminal or command prompt
```
Make sure of having the API key which is the core component for obtaing the dataset. After installing **quandl** package, by typing

```
df = quandl.get(dataset_to_be_analyzed, authtoken=your_api_key) # easily dataset can be obtained.
```
The data will be on yearly basis that requires better organising of it (according to years and months updating it into a dictionary). __Better Organisation of the data, the beautiful plot__.

### Working

```
from test_plot import analyze_close_stock

analyze_close_stock('provide_the_dataset(mostly_quandle_API_call)')
```
and on terminal

```
python file_name.py
```
The graphs will be opened on the browser and by specifing the year and the month, the granted graph of that particular year and month will be plotted.

### Example Grpahs

![example_image](https://user-images.githubusercontent.com/26375997/38781682-9ff21ebe-4106-11e8-991d-1c3333203b15.png)

![another_eample](https://user-images.githubusercontent.com/26375997/38781707-1ceeced0-4107-11e8-95dd-6142ea029ce3.png)

#### Candlestick representation

![candle_cake](https://user-images.githubusercontent.com/26375997/38854034-c8ebcd06-423c-11e8-975e-a78ac06b7a1a.png)


The updation of the data automatically happens when it gets updated on the website (*Qundle*) and since the API call is being called, the graphs will be updated easily. No worries.

__End Users__

As of now, this model is only used by the company stakeholders, investors and other parties involved in the `Stock Trading Activities`. But this can be automated and developed in such a way that other interested `Share Holders` can use to take their granted decision of buying and selling the share and achieve gain.
