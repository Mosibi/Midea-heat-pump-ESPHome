# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2024-01-13

### Fixed

- Changed some temperature sensor value types from a unsigned integerer to a signed integer. Which this fix,
  potential negative values are displayed as they should instead of displayed as very high positive values.

## [1.0.0]

### Added

- Sensor that shows if the heatpump is running.
- Fault to Error code mapping overview.
- Mapping from fault to error code and from current fault to error description.
- Heatpump status.
- Homeassistant dashboard and automations.
- Uptime.
- Key friendly_name, enabled the web server and add api.encryption.key.
- Switch for register 0 bit 2.

### Fixed

- DHW Tank Temperature T5s can be set between 20 and 60 degrees, instead of 40-60 what the docs state.
- Condenser temperature is a signed value.
- Fix bitmask for register 0 / bit 1.
