import re
import yaml

# Read the latest version from changelog.md
with open('CHANGELOG.md', 'r') as f:
    changelog = f.read()
    version_match = re.search(r'\[([0-9]+\.[0-9]+\.[0-9]+)\]', changelog)
    if version_match:
        new_version = version_match.group(1)

        # Load the YAML file
        with open('heatpump.yaml', 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        # Update the version
        yaml_content['esphome']['esphome']['project']['version'] = new_version

        # Write back to the YAML file
        with open('heatpump.yaml', 'w') as yaml_file:
            yaml.safe_dump(yaml_content, yaml_file)

        print(f'Updated version to {new_version} in heatpump.yaml')
    else:
        print('No version found in changelog.md')
