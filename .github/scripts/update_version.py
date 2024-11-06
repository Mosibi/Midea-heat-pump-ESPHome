import re
import yaml
import sys

# Define filenames as variables
CHANGELOG_FILE = 'CHANGELOG.md'
YAML_FILE = 'heatpump.yaml'

# Get the version from command-line arguments
new_version = sys.argv[1]

# Define a custom loader to handle unknown tags and leave them untouched
class IgnoreUnknownTagsLoader(yaml.SafeLoader):
    def construct_tagged(self, tag, node):
        # This method is called to process any tagged node. If the tag is one we don't want to process,
        # we simply return the node value (this way PyYAML doesn't try to process it).
        if tag in ['!secret', '!lambda']:  # Ignore !secret and !lambda tags
            return node.value
        return super().construct_tagged(tag, node)  # Use the default behavior for other tags

# Use the custom loader to load the YAML
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml.load(yaml_file, Loader=IgnoreUnknownTagsLoader)

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

updated_changelog = re.sub(r'\[Unreleased\](.*?)\n##', f'[Unreleased]\n### Changed:\n- \n##[{new_version}]\\1\n##', changelog, flags=re.DOTALL)

with open(CHANGELOG_FILE, 'w') as f:
    f.write(updated_changelog)

print(f'Replaced [Unreleased] with [{new_version}] in {CHANGELOG_FILE}')
