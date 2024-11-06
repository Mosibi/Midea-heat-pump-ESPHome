import sys
import datetime

# Define filenames as variables
CHANGELOG_FILE = 'CHANGELOG.md'
YAML_FILE = 'heatpump.yaml'

# Get the version from command-line arguments
new_version = sys.argv[1]

# Get the current date in 'yyyy-mm-dd' format
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Step 1: Read the YAML file as raw text (to preserve formatting)
with open(YAML_FILE, 'r') as yaml_file:
    yaml_content = yaml_file.readlines()

# Step 2: Find the esphome section and update the version field under project
inside_esphome = False
inside_project = False

for i, line in enumerate(yaml_content):
    line = line.strip()
    
    # Check for the start of the esphome section
    if line.startswith("esphome:"):
        inside_esphome = True
    
    # Check for the start of the project section under esphome
    if inside_esphome and line.startswith("project:"):
        inside_project = True

    # If inside the project section, look for the version field
    if inside_project and line.startswith("version:"):
        yaml_content[i] = f"    version: {new_version}\n"  # Update version field
        break  # Exit the loop after the version is found and updated

    # If we've reached the end of the project section, stop processing
    if inside_project and line == "":
        inside_project = False

# Step 3: Write the updated YAML content back to the file
with open(YAML_FILE, 'w') as yaml_file:
    yaml_file.writelines(yaml_content)

print(f'Updated version to {new_version} in {YAML_FILE}')

# Step 4: Read and update the changelog
with open(CHANGELOG_FILE, 'r') as f:
    changelog = f.read()

# Step 5: Update the changelog for the new version
# Simply replace [Unreleased] with the new version info and current date
updated_changelog = changelog.replace(
    '[Unreleased]',
    f'[Unreleased]\n### Changed:\n- \n## [{new_version}] - {current_date}'
)

# Step 6: Write the updated changelog to the file
with open(CHANGELOG_FILE, 'w') as f:
    f.write(updated_changelog)

print(f'Replaced [Unreleased] with [Unreleased]\n### Changed:\n- \n## [{new_version}] - {current_date} in {CHANGELOG_FILE}')
