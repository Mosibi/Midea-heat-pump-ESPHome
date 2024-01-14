# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Documented default values for registers
- Entity `heat_pump_running` is changed to check is the fan speed is above 0, the compressor frequency is above 0, or the water pump in the external unit is on. Previously only the fan speed was taken into account.
- The following registers are changed from type `sensor` to `number` to make them configurable:
  - register: 205, Temperature Upper Limit Of TS Setting
  - register: 206, Temperature Lower Limit Of TS Setting
  - register: 207, Temperature Upper Limit Of water Heating
  - register: 208, Temperature Lower Limit Of Water Heating
  - register: 209, DHW Pump Return Running Time
  - register: 212, dT5_On
  - register: 213, dT1S5
  - register: 214, T Interval DHW
  - register: 215, T4 DHW max
  - register: 216, T4 DHW min
  - register: 217, t TBH Delay
  - register: 218, dT5 TBH Off
  - register: 219, T4 TBH On
  - register: 220, Temperature For Disinfection Operation
  - register: 221, Maximum Disinfection Duration
  - register: 222, Disinfection High Temperature Duration
  - register: 223, Time Interval Of Compressor Startup In Cooling mode
  - register: 224, dT1SC
  - register: 225, dTSC
  - register: 226, T4cmax
  - register: 227, T4cmin
  - register: 228, Time Interval Of Compressor Startup In Heating mode

## [1.1.0] - 2024-01-13

### Changed

- The following registers are changed from type `sensor` to `number` to make them configurable:
  - register: 233, Ambient Temperature For Enabling Hydraulic Module Auxiliary Electric Heating IBH
  - register: 234, Temperature Return Difference For Enabling The Hydraulic Module Auxiliary IBH
  - register: 235, Delay Time Of Enabling The Hydraulic Module Auxiliary Electric Heating IBH
  - register: 237, Ambient Temperature Trigger For AHS
  - register: 238, Trigger Temperature Difference Between T1S And Current Heat for AHS
  - register: 240, Delay Time for Enabling AHS
  - register: 241, Water Heating Max Duration
  - register: 242, T DHWHP Restrict
  - register: 243, T4autocmin
  - register: 244, T4autohmax
  - register: 245, Heating Or Cooling Temperature When Holiday Mode Is Active
  - register: 246, Domestic Hot Water Temperature When Holiday Mode is Active
  - register: 247, PER START Ratio
  - register: 248, TIME ADJUST
  - register: 249, DTbt2
  - register: 250, IBH1 Power
  - register: 251, IBH2 Power
  - register: 252, TBH Power
  - register: 255, Temperature Rise Day Number
  - register: 256, Drying Day Number
  - register: 257, Temperature Drop Day Number
  - register: 258, Highest Drying Temperature
  - register: 259, Running Time Of Floor Heating For The First Time
  - register: 260, T1S Of Floor Heating For The First Time
  - register: 261, T1SetC1
  - register: 262, T1SetC2
  - register: 263, T4C1
  - register: 264, T4C2

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
