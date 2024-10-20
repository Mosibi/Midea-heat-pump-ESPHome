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

function Error() {
  local MESSAGE="${1}"
  Message "ERROR" "${MESSAGE}"
  exit 101
}

VERSION_FROM_CHANGELOG=$(grep '^## \[[0-9]' CHANGELOG.md | sed -E 's/^##\ \[([0-9].*)\]\ -.*/\1/g' | head -1)

if [[ ! -z "${VERSION_FROM_CHANGELOG}" ]] && [[ "${VERSION_FROM_CHANGELOG}" =~ ^[0-9].*$ ]]; then
  Info "Version extracted from changelog is ${VERSION_FROM_CHANGELOG}"

  # Check if version already exists
  git describe "${VERSION_FROM_CHANGELOG}" --tags  1>/dev/null 2>/dev/null

  if [[ $? -eq 0 ]]; then
    Error "Version (tag) ${VERSION_FROM_CHANGELOG} already exists"
  else
    sed -i -E "s/(^\ {4}version:)(.*$)/\1 ${VERSION_FROM_CHANGELOG}/g" heatpump.yaml || Error "Could not update version in heatpump.yaml"
    Info "Version in heatpump.yaml is successful updated to ${VERSION_FROM_CHANGELOG}"
  fi
fi
