# Internals

This document describes how the heat pump behaves internally and how this ESPHome configuration maps to it.

> Most of this information is based on information from users of this project and observations done by myself on our own Airwell R32 unit.

## Contents
- [User versus installer options](#user-versus-installer-options)
- [Switching heating and DHW on and off](#switching-heating-and-dhw-on-and-off)
- [Heat pump state](#heat-pump-state)

## User versus installer options

This project provides the modbus registers from the heat pump 'as they are', which means that both the **user** and the **installer** options are present. The modbus registers are structured as this:

| Range       | Descripion                                                   |
| ----------- | ------------------------------------------------------------ |
| 0 - 99      | User settings                                                |
| 100 - 199   | Sensor values                                                |
| 200 - 299   | Installer settings (for serviceman)                          |
| 1000 - 1099 | Sensor values for slave units (when running in cascade mode) |

In general as a **regular user**, you should **never touch** a value outside the `0-99` range. Use your specific model YAML file to see what settings are within this range.

## Switching heating and DHW on and off

| Bit | Switch                                      | Function                 |
|-----|---------------------------------------------|--------------------------|
| 0   | `Room Temperature Control`                  | Room thermostat          |
| 1   | `Water Flow Temperature Control Zone 1`     | Heating zone 1           |
| 2   | `Power DHW T5S`                             | Domestic Hot Water (DHW) |
| 3   | `Water Flow Temperature Control Zone 2`     | Heating zone 2           |

Switching on/off these behaves like the user switching it on/off on the remote controller.

> Do not use the `Parameter Setting 1 Enable ...` switches for this. These are installer options, see [User versus installer options](#user-versus-installer-options).

When `Room Temperature Control` is enabled, the temperature sensor in the remote controller will be used to define when the heat pump should be turned (powered) on or off.

When `Water Flow Temperature Control` is enabled for zone 1 or zone 2, the target outlet water temperature will be used to define when the heat pump should be turned (powered) on or off. If `room thermostat` is enabled, the `Water Flow Temperature Control Zone 1` and/or `Water Flow Temperature Control Zone 2` switch will be controlled by the heat pump. In other words, the room thermostat will decide when this will be on or off.

## Heat pump state

The heat pump provides a modbus register (101) called `Operating mode` which reflects the mode which is set using the `Mode setting` register (1). Since this does not reflect completely what the heat pump is doing, an extra ESPHome entity is created called `Active State`.

### Active state

The `Active State` sensor combines several registers into one human-readable status. The conditions are evaluated in the order below, so a status higher in the list takes precedence over the ones below it.

| State         | Meaning |
|---------------|---------|
| `Inactive`    | The heat pump is not active, e.g. off. `Operating Mode` is `OFF`. |
| `Idle`        | The heat pump is switched on (`Operating Mode` is not `OFF`), but the compressor is not running (`Load Output Run` is off). This happens, for example, while the unit is preparing for a DHW run or in the pause between two heating sessions. |
| `Defrosting`  | The heat pump is defrosting its outdoor coil (`Status Bit 1 Defrosting`), to remove frost or ice that built up while heating. |
| `Oil return`  | The heat pump is in an oil return cycle (`Status Bit 1 Oil Return`), which brings lubricating oil that has collected in the refrigerant circuit back to the compressor. |
| `DHW`         | The heat pump is heating the domestic hot water tank. |
| `Heating`     | The compressor is running and `Operating Mode` reports heating. |
| `Cooling`     | The compressor is running and `Operating Mode` reports cooling. |

#### Notes

- `DHW` is detected through `Load Output SV1` and not through `Operating Mode`, because `Operating Mode` reports "Heating" during a DHW cycle.
- `Idle` is not an error state. It simply means the unit is on but currently not producing heat or cold.
- `Oil return` is not an error state. It is a regular operation which is executed periodically when the compressor is on.