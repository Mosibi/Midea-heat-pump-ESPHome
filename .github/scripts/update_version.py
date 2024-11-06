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
current_date = "- " + datetime.datetime.now().strftime('%Y-%m-%d')

# Define a custom loader to treat `!secret` and `!lambda` tags as literal values
class IgnoreTagsLoader(yaml.SafeLoader):
    def construct_yaml_str(self, node):
        # Override the default string constructor to treat all tags as plain text
        return node.value

# Register this custom constructor for `!secret` and `!lambda`
IgnoreTagsLoader.add_constructor('!secret', IgnoreTagsLoader.construct_yaml_str)
IgnoreTagsLoader.add_constructor('!lambda', IgnoreTagsLoader.construct_yaml_str)

# Load the YAML file with the custom loader
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml.load(yaml_file, Loader=IgnoreTagsLoader)

# Update the version field under esphome
if 'esphome' in yaml_content and 'project' in yaml_content['esphome']:
    yaml_content['esphome']['project']['version'] = new_version

# Use the default YAML Dumper to maintain order and write back the modified YAML
with open(YAML_FILE, 'w') as yaml_file:
    yaml.safe_dump(yaml_content, yaml_file, default_flow_style=False, sort_keys=False)

print(f'Updated version to {new_version} in {YAML_FILE}')

# Replace unreleased section in CHANGELOG.md
with open(CHANGELOG_FILE, 'r') as f:
    changelog = f.read()

# Replace the [Unreleased] section with the new version and add the current date
updated_changelog = re.sub(
    r'\[Unreleased\](.*?)\n##',
    f'[Unreleased]\n### Changed:\n- \n##[{new_version} ({current_date})]\\1\n##',
    changelog,
    flags=re.DOTALL
)

with open(CHANGELOG_FILE, 'w') as f:
    f.write(updated_changelog)

print(f'Replaced [Unreleased] with [{new_version} ({current_date})] in {CHANGELOG_FILE}')
