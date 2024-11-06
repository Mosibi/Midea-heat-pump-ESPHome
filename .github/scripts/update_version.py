import re
import sys
import datetime

# Define filenames as variables
CHANGELOG_FILE = 'CHANGELOG.md'
YAML_FILE = 'heatpump.yaml'

# Get the version from command-line arguments
new_version = sys.argv[1]

# Get the current date in 'yyyy-mm-dd' format
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Read the YAML file as raw text
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml_file.read()

# Use a regular expression to find and replace the version under `esphome -> project -> version`
yaml_content_updated = re.sub(
    r'(?<=esphome:\s*\n\s*project:\s*\n\s*version:\s*)([^\n]+)',  # Match version under `esphome -> project`
    new_version,  # Replace with new version
    yaml_content
)

# Write the updated YAML content back to the file
with open(YAML_FILE, 'w') as yaml_file:
    yaml_file.write(yaml_content_updated)

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
