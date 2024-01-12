
# CompanyScope Analyzer
![Script Demonstration](img/ScriptDemonstration.gif)

## Overview
This script is designed to automate the process of checking the availability of company names and associated domains. It simplifies the task of verifying these details across various platforms.

## Features
- __Company Name Availability Check:__ Determines whether a company name is available or already taken on state Portal.
- __Domain Name Availability Check:__ Checks the availability of any domains for the company names on NameCheap.
- __Configurable Checks:__ Allows enabling or disabling the company name and domain name checks via configuration settings.
- Generates a report with the availability status of each company and domain name.

## Supported formats:
- Input: txt
- Output: txt, xml, xls, json
## Report Output Example:
#### TXT
```
Company: Tech Dev LLC
BNS Status: Available
techdev.com: Taken
techdev.net: $7,995.00
techdev.tech: Available at $9.97/yr
```
#### Json
```
    {
        "Company Name": "Tech Dev LLC",
        "BNS Status": "Available",
        "Domains": {
            "techdev.com": "Taken",
            "techdev.net": "Available at $7,995.00",
            "techdev.tech": "Available at $9.97/yr"
        }
    }
```
## Installation
- To run this script, you need to have Python installed on your system along with the necessary packages. You can install the required packages using pip:
```
pip install selenium webdriver-manager PyYAML xlwt
```
- Or to install these packages, you can use the following command:
```
pip install -r requirements.txt
```
- This will install the specific versions of the selenium package and the webdriver-manager package, which are essential for running the script. The selenium package is used for automating web browser interaction, while webdriver-manager simplifies the management of binary drivers for different browsers.

## Usage
1. __Prepare the Input File:__ Create a text file named company.txt in folder __data__ containing the list of company names you want to check. Each company name should be on a new line.
2. __Set the Configuration:__ In the __[config.yml](configs%2Fconfig.yml)__, modify the following lines to enable or disable specific checks:
```
company_name_check_enabled: True
domain_check_enabled: True
domain_zones:
  - ".com"
  - ".net"
  - ".tech"
```
3. __Run the Script:__ Execute the script in your Python environment:
```
python CompanyScopeAnalyzer.py
```
4. __Review the Results:__ Once the script finishes running, check the generated output file in folder __data/reports__ (e.g., __result_08_04_2023.txt__) for the availability status of each company and domain name.

## How It Works
- The script reads company names from the __data/input/company.txt__ file.
- For each company name, it formats the name appropriately for domain checking and state Portal search.
- If enabled, it checks the company name's availability on state Portal and logs the result as "Available," "Not Available," or "Status Unknown."
- If domain checking is enabled, the script checks for domain availabilities on NameCheap and logs the results.
- All results are written to an output file with a timestamp in the file name.


## To Do or Not To Do
- Optimization and Enhancement of Logging.
- Add proxy support.
- Implement cflags functionality.
- Process lists from CSV, XLS, DOC, JSON.
- Add tests.
- Code and project structure optimization.
- Add support for business name searches in other states with a toggle feature.
- Create bots for Telegram, Slack, etc.
- Docker support.
- Implement asynchronous processing for faster results.
- Integrate Trade Mark checks.
- Generate company names dynamically.
- Develop a WebUI.
- Develop an API.

However, these enhancements might be considered in the future or perhaps in another lifetime.

## Notes
- If you are not located in the United States, you may need to use a VPN or Proxy for the script to function correctly.
## Development
- Created in a couple of hours to automate a tedious manual task.
- Tested on Windows and MacOS with Python version 3.12 and 3.9.

## Disclaimer
This script is provided as-is. Feel free to download, modify, and use it as you see fit.

---
