# OpenModex Visualization

## About

This dashboard was developed by the [open_MODEX](https://reiner-lemoine-institut.de/open_modex/) project. 
One goal of the project was, to compare scenario results from different energsystem modelling frameworks. 
Therefore, a standardized input and output format ([oedatamodel](https://github.com/open-modex/oedatamodel)) has been defined, 
which can be read by the dashboard. Afterwards, underlying data can be filtered and compared/analyzed using various charts and plotting options.

## Internal Data Processing

A short introduction of how data is imported, processed and finally plotted, shall be given here.

**Note**: At the moment, data import is fixed to Open_MODEX specific tables on the OEP. 
Other data sources, such as filesystem, different tables on OEP or datapackages could be easily implemented, 
as all further processing steps are independent of the given source.

At first, available scenarios are scanned from OEP using the [Advanced API](https://oep-data-interface.readthedocs.io/en/latest/api/advanced.html) of the OEP.
After selection of a scenario, the following steps are running within the application:

1. Loading  
Data is loaded into application. Currently, this is done by loading data from OEP via oedatamodel_api.
2. Processing  
Data is loaded into a `pandas.Dataframe` (one DF for each, scalars and timeseries). Afterwards, filtering, [ordering](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html), and [grouping](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) from pandas is applied, regarding the user input.
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
