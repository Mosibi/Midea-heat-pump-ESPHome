
# Development

First of all, thanks for checking this file, it means that your are interested in making changes to this project, which in the end, will help us all !

## Model support

The model yaml files are created using a Python script that reads the file `source/heatpump-base.yaml` and a model file from the directory `sources/models/`. The changes listed in the model file are applied against `source/heatpump-base.yaml` and written to the `models/` directory with the same name as the original model file. So a file called `source/modes/myfile.yaml` will result in `models/myfile.yaml`

While the model generation is done automatically in pull requests, you can run it locally for debugging and testing:

```bash
uv run model-generator.py
```

This works best with [uv](https://docs.astral.sh/uv/getting-started/installation/) which will automatically handle all dependencies. Alternatively, you can run `python model-generator.py` if you have Python >=3.8 with `ruamel.yaml` installed. Running the generator locally is useful when you want to verify your changes to `source/heatpump-base.yaml` or `source/models/*.yaml` files before committing.

A model file can be used to `modify`, `remove`, `replace` and `add` a register. The syntax of a model file is as follow:

```yaml
<change_type>:
  <entity_type>:
    - id: one
    - id: two
```

In which `<change_type>` is one of modify, remove, replace or add and `<entity_type>` is one of the ESPHome entity types, which are for example `select`, `sensor` and `number`. For `replace` it is required that keys `id` and `newid` are present, where `id` refers to the original `id` in `source/heatpump-base.yaml`. In the resulting model file, the `id` field will be replaced with `newid`.

### Example model file

```yaml
replace:
  sensor:
    - platform: template
      id: compressor_starts_per_hour
      newid: "{devicename}_coffee cups per month"
      name: "Number of coffee cups per month"
      unit_of_measurement: "cups"

modify:
  number:
    - id: "${devicename}_t4_dhw_max"
      max_value: 46

remove:
  number:
    - id: number123
    - id: "${devicename}_set_water_temperature_t1s_zone_1"
    - id: "${devicename}_dt1s5"
  sensor:
    - id: sensor123
  select:
    - id: "${devicename}_operational_mode"

add:
  sensor:
    - plaform: modbus_controller
      id: "${devicename}_extra_temp_sensor"
      address: 250
      name: "Extra Temp Sensor"
      value_type: "U16"
      unit_of_measurement: "°C"
      device_class: "temperature"
      accuracy_decimals: 1
```

### Global parameters for a model

When a global parameter needs to be present for a model, then add that parameter to the global section in `source/heatpump-base.yaml`, so that it is useable in the model file.

## Creating a pull/merge request

Pull requests are very welcome and it would be perfect if your pull request also updates the `CHANGELOG.md` to describe your changes.