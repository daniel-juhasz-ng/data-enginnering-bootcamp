#!/bin/bash

# Check if source and destination directory paths are provided as parameters
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <source_directory> <destination_directory>"
  exit 1
fi

# Function to convert JSON files to single line JSON documents
convert_json_to_single_line() {
  local source_file="$1"
  local destination_file="$2"

  # Check if the file is a JSON file
  if [[ "${source_file}" == *.json ]]; then
    # Convert the JSON file to a single line JSON document using the provided command
    cat "${source_file}" | tr '\n' ' ' > "${destination_file}"
    sed -i 's/;/-/g' "${destination_file}"
    echo "Converted: ${source_file} -> ${destination_file}"
  fi
}

# Get the source and destination directory paths from the parameters
source_directory="$1"
destination_directory="$2"

# Create the destination directory if it doesn't exist
if [ ! -d "${destination_directory}" ]; then
  mkdir -p "${destination_directory}"
  echo "Created destination directory: ${destination_directory}"
fi

# Find all JSON files recursively in the source directory
find "${source_directory}" -name "*.json" -type f | while read -r file; do
  # Construct the destination file path by replacing the source directory path with the destination directory path
  destination_file="${file//$source_directory/$destination_directory}"
  convert_json_to_single_line "${file}" "${destination_file}"
done

echo "Conversion complete!"
