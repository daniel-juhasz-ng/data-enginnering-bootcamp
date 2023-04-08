from datetime import datetime
import re


def remove_ce(string):
    # check if there is BCE in the string
    if re.search(r'bce', string):
        return string
    else:
        return re.sub(r'ce$', '', string)


# Modeled case
def modeled(date_str):
    match = re.search(r"\b\d{4}\b", date_str)
    if match:
        year = int(match.group())
    else:
        year = None
    return year

def get_middle_year_century(date_str):
    # remove whitespace and convert to lower case
    date_str = date_str.strip().lower()

    # check if the date string includes "bce" or "ce" and set appropriate multiplier
    multiplier = -1 if re.search(r"\b(bce)\b", date_str) else 1

    # check for ranges specified with a hyphen
    match = re.search(r"(\d+)\s*(th|st|nd|rd)?\s*-\s*(\d+)\s*(th|st|nd|rd)?\s*(century)?", date_str)
    if match:
        start_year = int(match.group(1)) * multiplier * 100
        end_year = int(match.group(3)) * multiplier * 100
        middle_year = (start_year + end_year) // 2
        return middle_year

    # check for ranges specified with "to"
    match = re.search(r"(\d+)\s*(th|st|nd|rd)?\s*(century)?\s*to\s*(\d+)\s*(th|st|nd|rd)?\s*(century)?", date_str)
    if match:
        start_year = int(match.group(1)) * 100 * multiplier
        end_year = int(match.group(4)) * 100 * multiplier
        middle_year = (start_year + end_year) // 2
        return middle_year

    # check for "century" dates
    match = re.search(r"(early|mid|late)\s+(\d+)\s*(th|st|nd|rd)?\s*(century)?\s+(century)?", date_str)
    if match:
        century = int(match.group(2))
        century_start = (century - 1) * 100 * multiplier
        if "early" in match.group():
            middle_year = century_start + 25 * multiplier
            return middle_year
        elif "mid" in match.group():
            middle_year = century_start + 50 * multiplier
            return middle_year
        elif "late" in match.group():
            middle_year = century_start + 75 * multiplier
            return middle_year
        else:
            middle_year = century * 100 - 50
            return middle_year

    # check for "century" dates without "early", "mid", or "late"
    match = re.search(r"(\d+)\s*(th|st|nd|rd)?\s*(century)?", date_str)
    if match:
        century = int(match.group(1))
        middle_year = century * 100 - 50 * multiplier
        return middle_year

    # if the date string doesn't match any known formats, raise an error
    else:
        raise ValueError("Invalid date string format")



def parse_date(date_str):
    date_str = date_str.lower()
    date_str = date_str.replace("ca. ", "").replace("c. ", "")
    date_str = date_str.replace(" or before", "")
    date_range = remove_ce(date_str)

    if 'modeled' in date_range:
        return modeled(date_str)

    if 'century' in date_range:
        return get_middle_year_century(date_range)

    m = re.match(r'^(\d{1,4})$', date_range)
    if m:
        year = int(m.group(1))
        return year

    m = re.match(r'(\d{1,4})s bce', date_range)
    if m:
        decade = int(m.group(1))
        if decade % 100 == 0:
            start_year = -decade
            end_year = -decade - 100
        else:
            start_year = -decade
            end_year = -decade - 10
        return (start_year + end_year) // 2

    m = re.match(r'(\d{1,4})s', date_range)
    if m:
        decade = int(m.group(1))
        if decade % 100 == 0:
            start_year = decade
            end_year = decade + 100
        else:
            start_year = decade
            end_year = decade + 10
        return (start_year + end_year) // 2

    m = re.match(r'(\d{1,4})\s?bce$', date_range)
    if m:
        year = -int(m.group(1))
        return year

    m = re.match(r'(\d{1,4})\s?-?\s?(\d{1,4})\s?bce', date_range)
    if m:
        start_year = -int(m.group(1))
        end_year = -int(m.group(2))
        return (start_year + end_year) // 2

    m = re.search(r'(\d{4})\s?-?\s?(\d{4})', date_range)
    if m:
        start_year = int(m.group(1))
        end_year = int(m.group(2))
        return (start_year + end_year) // 2

    m = re.search(r'(\d{1,4})\s?-?\s?(\d{1,4})', date_range)
    if m:
        start_year = int(m.group(1))
        end_year = int(m.group(2))
        return (start_year + end_year) // 2

    m = re.match(r'(early|mid|late)\s(\d{1,4})s bce', date_range)
    if m:
        decade = int(m.group(2))
        addition = 0
        if decade % 100 == 0:
            addition = 100
        else:
            addition = 10
        if m.group(1) == 'early':
            start_year = -decade
            end_year = -decade - (addition // 4)
        elif m.group(1) == 'mid':
            start_year = -decade + (addition // 2)
            end_year = start_year
        elif m.group(1) == 'late':
            start_year = -decade + (addition // 2)
            end_year = -decade - addition
        return (start_year + end_year) // 2

    m = re.match(r'(early|mid|late)\s(\d{1,4})s', date_range)
    if m:
        decade = int(m.group(2))
        addition = 0
        if decade % 100 == 0:
            addition = 100
        else:
            addition = 10
        if m.group(1) == 'early':
            start_year = decade
            end_year = decade + (addition // 4)
        elif m.group(1) == 'mid':
            start_year = decade + (addition // 2)
            end_year = start_year
        elif m.group(1) == 'late':
            start_year = decade + (addition // 2)
            end_year = decade + addition
        return (start_year + end_year) // 2

    return None


import os
import csv

# Define the directory containing CSV files
dir_path = '/Users/danieljuhasz/Documents/data-eng-bootcamp/project/file1.csv'
i = 1
# Loop through all files in the directory
for filename in os.listdir(dir_path):
    if filename.endswith('.csv'):
        # Open the CSV file in read mode
        with open(os.path.join(dir_path, filename), 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            next(csv_reader)
            # Loop through each row in the CSV file
            for row in csv_reader:
                # Process the row here
                # For example, print each row to the console
                print(f'{row[0]} - {parse_date(row[0])}')
