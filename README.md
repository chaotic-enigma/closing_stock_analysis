# closing_stock_analysis

This is for analysing the closing stock values wherein it requires a *Qunadle* datasets, easily acquired from the quandle website after creating an account. 

The package requirements are: 
```
dash
dash_core_components
dash_html_components
plotly

easily obtained by just typing pip install <package_name> on terminal or command prompt

```
Make sure of having the API key which is the core component for obtaing the dataset. After installing *quandl* package, by typing

```
df = quandl.get(dataset_that_is_to_be_analyzed, authtoken=your_api_key) #easily dataset can be obtained.

```
The data will be on yearly basis that requires better organising of it. __Better Organisation of the data, better plot__.

## Working

```
from test_plot import analyze_close_stock

analyze_close_stock('provide_the_dataset')

```
and on terminal 

```
python file_name.py

```
The graphs will be opened on the browser and by specifing the year and the month, the granted graph of that particular year and month will be plotted.

### Example Grpahs

![example_image](https://user-images.githubusercontent.com/26375997/38781682-9ff21ebe-4106-11e8-991d-1c3333203b15.png)

![another_eample](https://user-images.githubusercontent.com/26375997/38781707-1ceeced0-4107-11e8-95dd-6142ea029ce3.png)


The updation of the data automatically happens when it gets updated in the website (*Qundle*) and since the API call is being called, the graphs will be updated easily. No worries.
