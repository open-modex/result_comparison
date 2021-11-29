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

### Chart and Data

Charts and data will not be re-/loaded automatically, when selecting scenarios or changing filters and graph options.
This is by design, as loading of charts and data might take long. 
Instead, loading can be started using the "Refresh" button of either the sclars or timeseries plot.
This has to be done after every change (scenario, filters, units, chart type or chart options), in order to see related
changes in the chart and data.
By default, underlying data of the chart is not shown. 
This can be activated by clicking on the "Chart + Data" icon, in the left upper corner of the chart.
After refreshing the chart, an additional data table with related data will be shown below the chart.

### Errors and Warnings

In some cases, there might occur errors while processing the data or plotting the chart. 
If this is the case, chart and data table will not be updated. 
Instead, the error tab (in the upper left corner of the chart) will turn red and error log will show related error message.
Additionally, warnings (error tab will turn orange) might be logged in the log as well, 
considering missing units, unreadable time index (timeseries plot) etc.

### Filtering, Ordering and Aggregation

*Filtering*  
In the filter section, each column of the underlying data can be filtered by contained values. 
If nothing is selected, related column is not filtered at all. 
Otherwise, only data rows containing given filter values are selected for further processing and plotting.

*Ordering*  
Data is ordered by given values in *Order-by* dropdown using [order-by](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html) function from `pandas.Dataframe`.
This is especially useful if data comes in unordered, as in this case order in plots can be unexpected. 

*Aggregation*  
Aggregation is implemented by summing up the `value` column of the data using pandas [grouping](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function.
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

*Save/Load Filters*  
Adjusted filters, units, chart type and chart options can be stored and restored from database.
To store a filter set, a name has to be given under "Save filters as" and saved via "Save" button.
Restoring a filter set loads data from database and fills up all saved filter and graph options.
**Note:** Color and label sets are re-/stored separately.

### Units

The dashboard is unit-aware. This means, that column "unit" is registered to define the unit of related row.
If a known unit is used in column "unit", the underlying value is scaled regarding the related chosen unit in the unit form.
The following units will be recognized (and scaled accordingly) by the dashboard:
* Energy: TWh, GWh, MWh, kWh (default: GWh)
* Power: TW, GW, MW, kW
* Power per hour: TW/h, GW/h, MW/h, kW/h
* Mass: Gt, Mt
* Mass per year: Gt/a, Mt/a

**Note:** If a unit is unknown, a warning will be raised (see Error and Warnings section) and the related value will 
be used as-is.

### Presentation

In the presentation section, chart labels and colors can be adapted and afterwards saved and loaded from database. 
Changing labels or colors is done by providing (JSON-like) key-value pairs, 
whereby the key represents the related data entry and the value represents the desired output.
In case of color map, keys are related to current color selection in chart settings and values represent colors which will be used in the chart. 
In case of labels, values are used to override related keys which represent any data entry (i.e. technology, technology_type, parameter, etc.).

An example entry for a color map could be:
```
{"hydro turbine": "#00549f", "wind turbine": "#8ebae5", "chp": "#6c7b8b", "generator": "#b6c5be", "photovoltaics": "#ffed00", "nuclear": "#a8859e"}
```
An example entry for labels could be (*storage* example):
```
{"all": "accumulated", "hydrogen gas": "hydrogen", "pumped": "pumped hydro"}
```

### Chart Type

For both charts (scalars and timeseries), different chart types are available. 
Right now, the scalars chart can be shown as bar, radar or dot chart, while the timeseries chart can be plotted as line or box chart or as heat map.
Changing the chart type will also affect related chart settings, as settings depend on given chart 
(not all settings are available for every chart, some charts have extra settings, etc.).
Again, after changing chart type, chart has to be refreshed to see changes.

### Chart Settings

Chart settings are separated into "General" settings regarding the setup of the chart and "Display" settings related to
minor visualization aspects of the chart. 
Some options are related to data columns, some contain fixed options to select from and others provide an input field for user entries.

**Note:** Plotlys [facet plots](https://plotly.com/python/facet-plots/) are used in order to create subplots - they behave slightly different from original subplots.

In the following, available chart settings for chart type *bar chart* will be explained:

**General settings:**
* X-Axis (from data): column to be used as x-axis.
* Y-Axis (from data): column to be used as y-axis.
* Text (from data): column to be shown as text on chart. Selection can be cleared to hide texts on chart.
* Color (from data): column to use for color mapping.
* Hover (from data): column to show when chart is hovered.
* Axis Type (list): linear or logarithmic axes.
* Orientation (list): horizontal or vertical bars.
* Mode (list): select barmode; relative (default bars), group (multiple bars per x-tick) or overlay.
* Subplots (from data): Creates multiple charts, related to selected column.
* Subplots per Row (input): Subplots are wrapped according to given input (integer).

** Display settings:**
* Chart Height (input): Height of chart can be set. Automatically set, if no value set. This is especially useful for multiple subplot rows, where automated height does not work very well.
* X-Axis Title (input): Title for x-axis; if not set, selected x-axis column (see above) will be used.
* Y-Axis Title (input): Title for y-axis; if not set, selected y-axis column (see above) will be used.
* Subplot Title (input-list): (Comma-separated) List of titles per subplot; number of list entries must equal number of subplots. If not set, selected subplot column (see above) will be used. 
* Show Legend (checkbox): whether to show or hide chart legend.
* Legend title (input): Title for legend; if not set, selected color column (see above) will be used.
* Bar Gap (input): Space between bars (float between 0-1).
* Margin Left/Right/Top/Bottom (input): Margin in px (integer)
* Subplot Spacing (input): Fraction to be used as spacing between subplots (float); see [Controlling facet spacing](https://plotly.com/python/facet-plots/#controlling-facet-spacing) for more information

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
