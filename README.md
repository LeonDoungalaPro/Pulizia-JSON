# Data Cleaner

This repository contains a Python script named `DataCleaner.py`, developed by **Leon Doungala** from **Peoplelab**, which is designed to clean and process JSON data.

## Overview

The `DataCleaner.py` script offers a set of functions to parse, clean, map, and process JSON data. It is specifically useful for preparing data acquired from diverse sources, including web scraping or API responses, for subsequent analysis or storage.

## Functions

### `DataCleaner(input_string)`

This is the main function of the script. It takes a JSON string as input, cleans and processes it, and returns the cleaned JSON data.

**Parameters:**
- `input_string` (str): The input JSON data as a string.

**Returns:**
- `str`: The cleaned and processed JSON data as a string, or 0 if the data is empty.

### Parsing Functions

#### `parse_string_to_json(input_string)`

This function parses the input string into JSON format.

### Cleaning Functions

#### `strip_html_tags(text)`

This function removes HTML tags and special characters from the input text.

### Mapping Functions

#### `map_user_data(referto_data, output_data)`

This function maps user data based on reference data and output data.

### Processing Functions

#### `process_file(data, output)`

This function processes the JSON data and filters out unnecessary information.

## Testing

The script includes a testing section where you can insert your input JSON data and see the cleaned output.

## Dependencies

    - `json`: For JSON parsing and manipulation.
    - `html`: For handling HTML entities.
    - `re`: For regular expression-based text processing.

## Usage

To use the `DataCleaner` function, follow these steps:

1. Insert the input JSON string into the `input_string` variable in the script.
2. Call the `DataCleaner` function with the input string as an argument.
3. The function will return the cleaned and processed JSON data as a string.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Author:** Leon Doungala  
**Employee:** Peoplelab

© 2024 Peoplelab. All rights reserved.

*Date: April 19, 2024*
