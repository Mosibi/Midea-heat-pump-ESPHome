#!/usr/bin/env bash

# This script extracts the new version from the
# file CHANGELOG.md and uses that version to update
# .esphome.project.version in heatpump.yaml


function Message() {
  local LEVEL="${1:=INFO}"
  local MESSAGE="${2}"
  echo "$(basename $0) [${LEVEL}]: ${MESSAGE}"
}

function Info() {
  local MESSAGE="${1}"
  Message "INFO" "${MESSAGE}"
}

function Warning() {
  local MESSAGE="${1}"
  Message "WARNGIN" "${MESSAGE}"
}

function Error() {
  local MESSAGE="${1}"
  Message "ERROR" "${MESSAGE}"
  exit 101
}

VERSION_FROM_CHANGELOG=$(grep '^## \[[0-9]' CHANGELOG.md | sed -E 's/^##\ \[([0-9].*)\]\ -.*/\1/g' | head -1)
VERSION_IN_YAML=$(awk '/^ {4}version:/ {print $NF}' heatpump.yaml)

if [[ ! -z "${VERSION_FROM_CHANGELOG}" ]] && [[ "${VERSION_FROM_CHANGELOG}" =~ ^[0-9].*$ ]]; then
  Info "Version extracted from changelog is ${VERSION_FROM_CHANGELOG}"
  Info "Current version in heatpump.yaml is ${VERSION_IN_YAML}"

  if [[ "${VERSION_FROM_CHANGELOG}" == "${VERSION_IN_YAML}" ]]; then
    Info "Versions are the same, nothing has to be done now"
    exit 0
  fi

  # Check if version already exists
  git describe "${VERSION_FROM_CHANGELOG}" --tags  1>/dev/null 2>/dev/null

  if [[ $? -eq 0 ]]; then
    Error "Version (tag) ${VERSION_FROM_CHANGELOG} already exists"
  else
    sed -i -E "s/(^\ {4}version:)(.*$)/\1 ${VERSION_FROM_CHANGELOG}/g" heatpump.yaml || Error "Could not update version in heatpump.yaml"
    Info "Version in heatpump.yaml is successful updated to ${VERSION_FROM_CHANGELOG}"
    echo "YAML_UPDATED=true" >> $GITHUB_ENV
  fi
else
  Warning "Version extracted from CHANGELOG.md does not seem to be a version tag: ${VERSION_FROM_CHANGELOG}, version will not be updated"
fi
