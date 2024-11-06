import re
import yaml
import sys

# Define filenames as variables
CHANGELOG_FILE = 'CHANGELOG.md'
YAML_FILE = 'heatpump.yaml'

# Get the version from command-line arguments
new_version = sys.argv[1]

# Define the constructor for the !secret tag
def ignore_secret(loader, node):
    # Simply return the node value (you could also return a placeholder if needed)
    return None  # Or return "SECRET_VALUE" to use a placeholder

# Add the custom constructor for the !secret tag
yaml.add_constructor('!secret', ignore_secret)
yaml.add_constructor('!lambda', ignore_secret)


# Update the YAML file
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)  # Use FullLoader instead of safe_load   yaml.safe_load(yaml_file)

yaml_content['esphome']['project']['version'] = new_version

# Use the default YAML Dumper to maintain order
with open(YAML_FILE, 'w') as yaml_file:
    yaml.safe_dump(yaml_content, yaml_file, default_flow_style=False, sort_keys=False)

print(f'Updated version to {new_version} in {YAML_FILE}')

# Replace unreleased section in CHANGELOG.md
with open(CHANGELOG_FILE, 'r') as f:
    changelog = f.read()

updated_changelog = re.sub(r'\[Unreleased\](.*?)\n##', f'[Unreleased]\n### Changed:\n- \n[{new_version}]\\1\n##', changelog, flags=re.DOTALL)

with open(CHANGELOG_FILE, 'w') as f:
    f.write(updated_changelog)

print(f'Replaced [Unreleased] with [{new_version}] in {CHANGELOG_FILE}')
