# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.0] - 2021-07-09
## Changed
- option "Energy per Year" to "Power" ("GW" instead of "GWh/a")

## [0.8.0] - 2021-07-05
### Added 
- option to customize bargap for bar chart
- option to rename data labels

### Changed
- font sizes
- no padding between bars

## [0.7.0] - 2021-06-30
### Added
- discrete color map can be edited
- color map can be saved/loaded  
- optional ability to set axis labels
- option to set legend title
- download data table as csv
- border around plots

### Changed
- plotly template to "plotly_white"
- graph text option is clearable

## [0.6.0] - 2021-06-24
### Added
- warning information addressing "nan not in list" error
- limitation for warnings and infos

### Fixed
- year filter initialization
- plot options can be set "clearable"

## [0.5.1] - 2021-06-23
### Fixed
- year column is not aggregated

## [0.5.0] - 2021-06-03
### Added
- error message if TS have different lengths during aggregation

### Changed
- aggregation is not triggered on change (but on chart refresh)

### Fixed 
- TS not loading 
- missing unit column in group-by during aggregation
- filter export
- dummy data loading (dev)
- filter loading (depending on scenarios)

## [0.4.0] - 2021-05-19
### Added
- heat map for timeseries
- simple loggings for scenario loading
- warning if data is empty for current filter settings
- barmode options to bar plot
- version number to layout

### Changed
- plots can be downloaded as SVG

### Fixed
- removed artefacts
- empty data in timeseries error

## [0.3.0] - 2021-05-19
### Added
- unit to x-/y-axis (if unit is unique)
- box plots for timeseries
- subplots for bar charts
- facets for box plots

## [0.2.0] - 2021-05-07
### Added 
- static plot options 
- orientation option to bar chart

### Changed
- default mapping to "dashboard" mapping

### Fixed
- timeseries groupby 
- removed regions mapping

## [0.1.0] - 2021-05-05
### Added
- timeseries plot (from https://plotly.com/python/time-series/#time-series-with-range-selector-buttons)
- button to reload scenarios
- pinned requirements
- loading spinner
- messaging to handle warnings and errors
- corrupt timeseries dates are fixed and user gets warned
- radar plot for scalars
- data table is shown
- filters can be saved/loaded
- postgres db to docker (local and production)
- refresh button to plot options
- added dot plot to scalar graph
- unit support 

### Changed
- multiple plots with different options can be loaded

### Fixed
- added redis to requirements
- error message if daterange index is wrong

### Cleaned
- moved timeseries duplicate and columns handling to preprocessing