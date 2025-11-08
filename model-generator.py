#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "ruamel.yaml",
# ]
# ///
import os
import glob
import copy
import re
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.yaml.compat import StringIO
from ruamel.yaml.comments import CommentedMap


def remove_comments(input):
    output = ""

    for line in input.splitlines(True):
        if not re.match("^ +#", line):
            output += line

    return output


def load_yaml(file_path):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(file_path, "r") as f:
        yaml_data = yaml.load(f)

    if yaml_data is None:
        return {}
    else:
        return yaml_data


def save_yaml(data, filename):
    yaml = YAML()
    # yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 4096
    yaml.default_flow_style = False

    # Patch None values to be dumped as empty scalars (key:)
    def none_representer(dumper, _):
        return dumper.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.representer.add_representer(type(None), none_representer)

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, transform=remove_comments)


def apply_overrides(base_data, overrides={}):
    base = copy.deepcopy(base_data)
    remove_identifiers = []

    # REMOVE per component type
    if "remove" in overrides:
        for component_type, remove_items in overrides["remove"].items():
            for remove_item in remove_items:
                remove_identifiers.append(remove_item["id"])
            if not isinstance(remove_identifiers, list):
                print(
                    f"Error: 'remove' section for '{component_type}' must be a list of identifiers."
                )
                continue
            if component_type in base and isinstance(base[component_type], list):
                base[component_type] = [
                    item
                    for item in base[component_type]
                    if item.get("id") not in remove_identifiers
                ]

    # MODIFY per component type
    if "modify" in overrides:
        for component_type, items in overrides["modify"].items():
            if not isinstance(items, list):
                print(f"Error: 'modify' section for '{component_type}' must be a list.")
                continue
            if component_type not in base or not isinstance(base[component_type], list):
                print(f"Warning: component type '{component_type}' not found in base.")
                continue
            for modify_item in items:
                entity_id = modify_item.get("id")
                modified = False
                for item in base[component_type]:
                    if item.get("id") == entity_id:
                        item.update(modify_item)
                        modified = True
                        break
                if not modified:
                    print(
                        f"Warning: id {entity_id} not found to modify in '{component_type}'."
                    )

    # REPLACE per component type
    if "replace" in overrides:
        for component_type, replace_identifiers in overrides["replace"].items():
            if not isinstance(replace_identifiers, list):
                print(
                    f"Error: 'replace' section for '{component_type}' must be a list."
                )
                continue
            if component_type not in base or not isinstance(base[component_type], list):
                print(f"Warning: component type '{component_type}' not found in base.")
                continue
            for replace_item in replace_identifiers:
                entity_id = replace_item.get("id")
                replaced = False
                for item in base[component_type]:
                    if item.get("id") == entity_id:
                        item_index = base[component_type].index(item)
                        replace_item["id"] = replace_item["newid"]
                        replace_item.pop("newid", None)
                        base[component_type].remove(item)
                        base[component_type].insert(item_index, replace_item)
                        replaced = True
                        break
                if not replaced:
                    print(
                        f"Warning: id {entity_id} not found to replace in '{component_type}'."
                    )

    # ADD per component type
    if "add" in overrides:
        for component_type, items in overrides["add"].items():
            if not isinstance(items, list):
                print(f"Error: 'add' section for '{component_type}' must be a list.")
                continue
            base.setdefault(component_type, [])
            existing_addresses = {item.get("id") for item in base[component_type]}
            for new_item in items:
                addr = new_item.get("id")
                if addr in existing_addresses:
                    print(
                        f"Warning: id {id} already exists in '{component_type}', skipping."
                    )
                else:
                    base[component_type].append(new_item)

    return base


def main():
    base_file = "source/heatpump-base.yaml"
    override_dir = "source/models"
    output_dir = "models"

    os.makedirs(output_dir, exist_ok=True)

    base_data = load_yaml(base_file)

    override_files = glob.glob(os.path.join(override_dir, "*.yaml"))

    for override_file in override_files:
        model_name = os.path.splitext(os.path.basename(override_file))[0]
        overrides = load_yaml(override_file)
        merged_data = apply_overrides(base_data, overrides)
        output_file = os.path.join(output_dir, f"{model_name}.yaml")
        save_yaml(merged_data, output_file)
        print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
