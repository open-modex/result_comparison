# OpenModex Visualization

## About

This dashboard was developed by the [open_MODEX](https://reiner-lemoine-institut.de/open_modex/) project. 
One goal of the project was, to compare scenario results from different energsystem modelling frameworks. 
Therefore, a standardized input and output format ([oedatamodel](https://github.com/open-modex/oedatamodel)) has been defined, 
which can be read by the dashboard. Afterwards, underlying data can be filtered, compared and analyzed using various charts and plotting options. 
In the end, generated charts can be downloaded as SVG to be used in presentations or publications.

## Usage

### Scenario selection

Multiple scenarios can be examined at once. Simply select them via dropdown *SCENARIO*. 
After selection of scenarios, related filter values are internally loaded and propagated to filter dropdowns.

### Filtering, Ordering and Aggregation

*Filtering*  
In the filter section, each column of the underlying data can be filtered by contained values. 
If nothing is selected, related column is not filtered at all. 
Otherwise, only data rows containing given filter values are selected for further processing and plotting.

*Ordering*  
Data is ordered by given values in *Order-by* dropdown using [order-by](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html) function from `pandas.Dataframe`.
This is especially useful if data comes in unordered, as in this case order in plots can be unexpected. 

*Aggregation*  
Aggregation is implemented by summing up the `value` column of the data. 
While aggregating data, underlying columns, which are not selected by *Group-By* dropdown are removed.
On the other hand, selecting columns by the *Group-By* dropdown preserves those columns and will not aggregate columns, containing different values in those columns.
For a better understanding, see the following aggregation examples:

* Example data:  
  
|Region|Technology|Parameter|Value|
|------|----------|---------|-----|
|HE|Photovoltaic|Investment|2000|
|HE|Wind Turbine|Investment|3000|
|BY|Photovoltaic|Investment|2200|
|BY|Wind Turbine|Investment|4000|

* Group-By *region* would lead to:

|Region|Value|
|------|-----|
|HE|5000|
|BY|6200|

* Group-By *Parameter* would lead to:

|Parameter|Value|
|------|-----|
|Investment|11200|

* Group-By *Region* and *Technology* would lead to:

|Region|Technology|Value|
|------|----------|-----|
|HE|Photovoltaic|2000|
|HE|Wind Turbine|3000|
|BY|Photovoltaic|2200|
|BY|Wind Turbine|4000|

## Internal Data Processing

A short introduction of how data is imported, processed and finally plotted, shall be given here.

**Note**: At the moment, data import is fixed to Open_MODEX specific tables on the [OEP](https://openenergy-platform.org/), 
specifically from tables `oed_scenario`, `oed_data`, `oed_scalars` and `oed_timeseries` from schema `model_draft`. 
Other data sources, such as filesystem, different tables on OEP or datapackages could be easily implemented, 
as all further processing steps are independent of the given source (see step *Loading*).

Following steps are running within the application:

1. Loading  
At first, available scenarios are scanned and listed (Currently, scenarios are read from OEP using the [Advanced API](https://oep-data-interface.readthedocs.io/en/latest/api/advanced.html) of the OEP).  
After selecting one or multiple scenarios, related data is loaded into application (Currently, data is loaded from OEP via [oedatamodel_api](https://github.com/open-modex/oedatamodel_api) as JSON).  
From this point on, the dashboard is source agnostic, meaning the following steps (processing and plotting) are independent of previous data fetching and related data sources.  
Thus, implementing a new data source, would only affect step 1.
2. Processing  
Data is loaded into a `pandas.Dataframe` (one DF for each, scalars and timeseries).  
Afterwards, filtering, [ordering](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html), and [grouping](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) from pandas is applied, regarding the user input.
3. Plotting  
Charts are made using plotly. Plot-dependent options (labels, margins, colors, axis type, etc.) depending on chart type are applied to chart.

## Setup

### Running locally

(see running locally with docker below)

To run a development instance locally, follow steps:
- create a virtualenv, 
- install the requirements from `requirements.txt`
- setup database locally (i.e. SQLite or postgres and point DB_URL env to it - see below)
- create DB tables via `make create_db`
- launch `app.py` using the python executable from the virtualenv
- open app in browser

Following env variables should/can be set:
- `DEBUG` (True/False): Execute dash app in debug mode
- `SECRET_KEY`: Should be set to a long random password
- `DB_URL`: URL to local database
- `SKIP_TS`: Timeseries are not (down-)loaded (this is not recommended for production!)

### Running locally with docker:

```
sudo docker-compose -f local.yml up -d --build
sudo docker-compose -f local.yml run --rm modex_visualization make create_db
```

### Admin Mode:

Create all tables in DB (must be done once - see above):
`make cerate_db`

Filters, color maps and labels from DB can be deleted using the _Makefile_:
- delete filter: `make delete_filter FILTER=<filter_name>`
- delete color map: `make delete_color_map COLOR_MAP=<color_map>`
- delete label: `make delete_label LABEL=<label>`


### Developer Mode:

If you want to use the dashboard without requesting data from OEP all the time, 
you can download scenario data for specific scenario and run the dashboard using downloaded data, by following steps:
- run `data/dev.py` using env variable `USE_DUMMY_DATA=True` and `SCENARIO_ID=<scenario_id>` (for scenario you want to download)
- (data will be downloaded into folder _data/scenarios/_)
- run dashboard using env variable `USE_DUMMY_DATA=True` - this will throw errors, when trying to load non-downloaded scenarios
- (scenarios are loaded from disk within this mode)
