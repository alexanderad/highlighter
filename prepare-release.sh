#!/bin/bash

# Exit on error
set -e

# Store the project root directory
PROJECT_ROOT=$(pwd)
echo "Project root directory: $PROJECT_ROOT"

# Get today's date in YYYY.MM.DD format
TODAY=$(date +%Y.%m.%d)
echo "Today's date: $TODAY"

# Update version in manifest.json
MANIFEST_PATH="chrome-extension/manifest.json"
echo "Updating version to $TODAY"
sed -i '' "s/\"version\": \".*\"/\"version\": \"$TODAY\"/" "$MANIFEST_PATH"

# Read version from manifest
VERSION=$(grep '"version":' "$MANIFEST_PATH" | cut -d'"' -f4)
echo "Current version: $VERSION"

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy extension files
echo "Copying extension files..."
cp -r chrome-extension/* "$TEMP_DIR/"

# Create zip file with version
ZIP_NAME="highlighter-extension-v${VERSION}.zip"
ZIP_PATH="$PROJECT_ROOT/$ZIP_NAME"
echo "Creating zip file: $ZIP_PATH"
cd "$TEMP_DIR"
zip -r "$ZIP_PATH" . -x "*.DS_Store" "__MACOSX/*"

# Clean up
cd "$PROJECT_ROOT"
rm -rf "$TEMP_DIR"

echo "Extension package created: $ZIP_PATH"