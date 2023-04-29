#!/bin/bash

# Loop through all JSON files in the current directory
for file in ./test_data/cooper_hevit/one_line/*.json; do
    # Replace "tms:id" with "tms_id" in the current file
    sed -i 's/tms:id/tms_id/g' "$file"
    # Replace "woe:country_id" with "woe_country_id" in the current file
    sed -i 's/woe:country_id/woe_country_id/g' "$file"
    # Replace "woe:country" with "woe_country" in the current file
    sed -i 's/woe:country/woe_country/g' "$file"
done

