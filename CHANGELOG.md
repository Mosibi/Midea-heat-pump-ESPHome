# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.1.2] - 2025-06-08

- Fixed compile issue in R290 model

## [7.1.1] - 2025-06-07

### Changed

- Removed space from the identifier of register 210 bit 5
- Fixed some copy issues in the R290 model

## [7.1.0] - 2025-06-01

### Added

- A generic configuration for R290 heat pump models is added
  - BE AWARE: This configuration is untestable by myself. Please test and report the results back via an issue.

### Changed

- Register 5 bit 12 is renamed from "Weather Compensation Zone 1" to "Weather Compensation Zone 1 Invalid"
- Register 5 bit 13 is renamed from "Weather Compensation Zone 2" to "Weather Compensation Zone 2 Invalid"
- Python script `model-generator.py` is now able to also `replace` a section

## [7.0.0] - 2025-05-31

### Changed

- From this version, the ESPHome yaml files are stored in the models directory, where the file `R32-generic.yaml` is (almost) the same as the previous `heatpump.yaml`
  - R32-generic.yaml contains three updated sensor registers
    - 120 (Tbt1) and 121 (Tbt2), which where previously called "Hydraulic Module Current 1" and ""Hydraulic Module Current 2"
    - 210 bit 5 is renamed to "Parameter Setting 1 PUMPI silent mode" from "Parameter Setting 1 Supports T1 Sensor"
  - R32-airwell.yaml is for certain Airwell models (I own one of those myself)
- A file DEVELOPMENT.md is added which describes the "model" structure
- The directory `source` contains the input files to generate the model specific file, using the new `model-generator.py` Python script
  - At every release, the Python script will be used to create the yaml files for all the models, so that users are not required to run it themself

## [6.0.2] - 2025-05-30

### Changed

- Adjust pressure sensor to comply with ESPHome HA integration. [bzyx](https://github.com/bzyx)
- Removed space in front of `name` at register 117 (sensor)

## [6.0.1] - 2025-04-20

### Changed

- Update version in heatpump.yaml which was forgotten to change in release 6.0.0

## [6.0.0] - 2025-04-20

### Changed

- Register 3 has been changed from type `sensor` to `number` to make them configurable.
- Updated several entities with `device_class` and `state_class` options, for better compatibility in Home Assistant sensors.

### Added

- Introduced a `binary_sensor` to detect when the compressor is running based on operating frequency > 0.
  - Counted compressor start events by monitoring transitions from OFF → ON.
- Added a `template sensor` to expose the number of starts per hour (`starts/h`).
  - Automatically resets the counter every hour.

## [5.1.0] - 2025-01-12

### Added

- Active State Map: A sensor that represents the state as a number. This can be used for example in Grafana to plot a state time timeline
  - 0: Inactive, 1: Heating, 2: Cooling, 3: DHW, 4: Defrosting, 99: Unknown (no mapping found)

### Removed

- Register 4 `sensor` entity removed and now only present as `number`

## [5.0.0] - 2024-11-24

### Changed

- Add COP - heat pump efficiency factor
  - Be aware that the energy metering is not acurate at all, therefor do not trust the COP from this sensor
- Update registers
  - 2: min/max value with verifing depending emmision type settings
  - 3: min/max value range
  - 4: min/max value range
  - 103: convert valve open position to percent representation
  - 101: moved to text sensor with status
  - 200: moved to text sensor with home appliance decode value code to text names
  - 211: completely configurable except reserved values
  - 210: completely configurable except reserved values
- Built-in web frontend change from CSS v2 to v3

## [4.1.2] - 2024-10-16

### Changed

- Update Register: 5 to be fully configurable

## [4.1.1] - 2024-10-15

### Changed

- Update Register: 0 to be fully configurable

## [4.1.0] - 2024-10-12

### Changed

- Added icons to all entities, code provided by [rysiulg](https://github.com/rysiulg)

## [4.0.0] - 2024-10-04

### Changed

- esp-idf is used as ESP32 framework instead of arduino (breaking change)
  - This framework is recommended for ESP32 chips by ESPHome. Be aware that this is a breaking change. To apply this configuration update on an existing board, an one-time serial flash will be needed
- Removed "ssid" and "password" from the wifi section. These will be stored by the captive portal component
- Renamed "Power Air Conditioner Zone 1" to "Room Temperature Control", "Power Floor Heating Zone 1" to "Water Flow Temperature Control Zone 1" and "Power Air Conditioner Zone 2" to "Water Flow Temperature Control Zone 2"
- Removed "${entity_prefix} from all etries. Got a tip from user "Septillion" on https://tweakers.net that this is not needed (anymore?) in ESPHome (breaking change (potential))
  - If needed, ESPHome will add the "friendly name" to an entity, which is "Heatpump Controller" in the current configuration.

### Fixed

- "Active State" now also takes into account when the temperature is controlled by the water flow temperature and not only the room thermostat

## [3.2.1] - 2024-10-01

### Changed

- 'Electricity Consumption' and 'Power Output' configured as device class 'energy'

## [3.2.0] - 2024-08-05

### Changed

- Add value "T1S DHW", which is the T1S value when in DHW mode (TS1 DHW = T5 + dT1S5)

## [3.1.0] - 2024-06-30

### Changed

- Register 0: Bit 0, 1 and 3 changed from `binary sensor` to `switch` to make them configurable
  - Bit 0: Power Air Conditioner Zone 1
  - Bit 1: Power Floor Heating Zone 1
  - Bit 3: Power Air Conditioner Zone 2

## [3.0.1] - 2024-06-23

### Fixed

- ESPHome version 2024.6.0 requires a `platform` key under `ota`

## [3.0.0] - 2024-02-11

### Changed

- Register 1: Operational mode is now configurable (heat, cool, auto)
- Register 269: Power Input Limitation Type is configurable with a list of options
- The following registers are changed from type `sensor` to `number` to make them configurable:
  - register: 270, t_T4 FRESH_H and t_T4 FRESH_C
  - register: 271, Built-in Circulating Pump Delay
- Register 272: Emission type for heating zone 1 and 2 and cooling zone 1 and 2 is now configurable with a list of options

## [2.0.0] - 2024-01-20

### Changed

- Set some min/max values on numbers to fix an issue with very high and low number limits.
- Documented default values for registers
- Entity `heat_pump_running` is changed to check is the fan speed is above 0, the compressor frequency is above 0, or the water pump in the external unit is on. Previously only the fan speed was taken into account.
- The following registers are changed from type `sensor` to `number` to make them configurable:
  - register: 205, Temperature Upper Limit Of TS Setting
    - Reverted in a later commit due to an issue
  - register: 206, Temperature Lower Limit Of TS Setting
    - Reverted in a later commit due to an issue
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

### Remarks

- Many thanks to [Yocee84](https://github.com/Yocee84) with the help on issues #8 and #17

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
