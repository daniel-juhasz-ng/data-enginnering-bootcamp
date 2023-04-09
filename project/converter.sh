#!/bin/bash

# Function to convert JSON files to single line JSON documents
convert_json_to_single_line() {
  local file="$1"
  local output_file="${file}.singleline"

  # Check if the file is a JSON file
  if [[ "${file}" == *.json ]]; then
    # Read the JSON file and remove newlines, leading/trailing whitespaces, and replace with a single line
    cat "${file}" | tr -d '\n' | tr -d '\r' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | tr -s '[:space:]' ' ' > "${output_file}"
    # Wrap the single line JSON document with '{' and '}' at the beginning and end
    echo "{" >> "${output_file}"
    echo -n $(cat "${output_file}") >> "${output_file}"
    echo "}" >> "${output_file}"
    # Remove original JSON file
    rm "${file}"
    # Move the single line JSON document to the original file name
    mv "${output_file}" "${file}"
    echo "Converted: ${file}"
  fi
}

# Find all JSON files recursively in the directory
find . -name "*.json" -type f | while read -r file; do
  convert_json_to_single_line "${file}"
done

echo "Conversion complete!"
