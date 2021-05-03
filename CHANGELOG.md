# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

### Changed
- multiple plots with different options can be loaded

### Fixed
- added redis to requirements
- error message if daterange index is wrong

### Cleaned
- moved timeseries duplicate and columns handling to preprocessing