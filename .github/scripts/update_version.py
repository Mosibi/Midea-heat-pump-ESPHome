import re
import yaml
import sys
import datetime

# Define filenames as variables
CHANGELOG_FILE = 'CHANGELOG.md'
YAML_FILE = 'heatpump.yaml'

# Get the version from command-line arguments
new_version = sys.argv[1]

# Get the current date in 'yyyy-mm-dd' format
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Define custom loaders for the `!secret` and `!lambda` tags
def secret_constructor(loader, node):
    return node.value  # Return the raw value of `!secret` without modification

def lambda_constructor(loader, node):
    return node.value  # Return the raw value of `!lambda` without modification

# Add custom constructors for `!secret` and `!lambda` tags
yaml.SafeLoader.add_constructor('!secret', secret_constructor)
yaml.SafeLoader.add_constructor('!lambda', lambda_constructor)

# Define a custom dumper to preserve block-style literals for multi-line strings (like C++ code)
class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow=flow, indentless=indentless)

# Load the YAML file with the custom loaders
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml.safe_load(yaml_file)

# Update the version field under esphome if available
if 'esphome' in yaml_content and 'project' in yaml_content['esphome']:
    yaml_content['esphome']['project']['version'] = new_version

# Write the updated YAML back to the file, preserving multi-line blocks (like `!lambda`)
with open(YAML_FILE, 'w') as yaml_file:
    yaml.dump(yaml_content, yaml_file, Dumper=CustomDumper, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f'Updated version to {new_version} in {YAML_FILE}')

# Replace unreleased section in CHANGELOG.md
with open(CHANGELOG_FILE, 'r') as f:
    changelog = f.read()

# Insert "[Unreleased]" and update the changelog with the new version part
updated_changelog = re.sub(
    r'\[Unreleased\](.*?)\n',
    f'[Unreleased]\n### Changed:\n- \n## [{new_version}] - {current_date}\\1\n',
    changelog,
    flags=re.DOTALL
)

# Write updated changelog to the file
with open(CHANGELOG_FILE, 'w') as f:
    f.write(updated_changelog)

print(f'Replaced [Unreleased] with [Unreleased]\n### Changed:\n- \n## [{new_version}] - {current_date} in {CHANGELOG_FILE}')
