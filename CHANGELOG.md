# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed 
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