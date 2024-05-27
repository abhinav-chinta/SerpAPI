# SerpApi Job Scraper

This script is designed to search for job listings on Google Jobs, retrieve detailed information about each job, and save the results into a CSV file. It uses the SerpApi to perform the job searches and handles retries in case of failed requests. The script can handle multiple job queries simultaneously using multi-threading to speed up the process.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Functions](#functions)
6. [Example Usage](#example-usage)
7. [Notes](#notes)

## Requirements
- Python 3.6+
- SerpApi Python package
- Python-dotenv package

## Installation

1. Clone the repository or download the script.

2. Install the required packages:
    ```sh
    pip install serpapi python-dotenv
    ```

## Configuration

1. Create a `.env` file in the same directory as the script.
2. Add your SerpApi key to the `.env` file:
    ```
    SERP_KEY=your_serpapi_key
    ```

## Usage

1. Modify the `jobs` list with the job titles you want to search for.
2. Modify the `queries` list to include the location you are interested in.
3. Set the desired output file path in the `filepath` variable.
4. Run the script using Python:
    ```sh
    python job_scraper.py
    ```

## Functions

### `search_job_listings(job_id, max_retries=1, retry_delay=1)`

**Description:** Searches for detailed job listings using a given job ID. If the request fails, it retries up to `max_retries` times with a delay of `retry_delay` seconds between attempts.

**Parameters:**
- `job_id` (str): The ID of the job to search for.
- `max_retries` (int): The maximum number of retries in case of failure. Default is 1.
- `retry_delay` (int): The delay in seconds between retries. Default is 1.

**Returns:** A list of dictionaries containing the apply options (links and titles) for the job.

### `clean_text(text)`

**Description:** Cleans the given text by replacing newline characters with spaces and stripping leading/trailing whitespace.

**Parameters:**
- `text` (str): The text to clean.

**Returns:** The cleaned text.

### `convert_indeed_link(link)`

**Description:** Converts an Indeed job link to a standardized format.

**Parameters:**
- `link` (str): The original Indeed job link.

**Returns:** The standardized Indeed job link or the original link if it's not an Indeed link.

### `search_and_save_jobs(queries, filepath, num_listings=1)`

**Description:** Searches for job listings based on the given queries, retrieves detailed information about each job, and saves the results to a CSV file.

**Parameters:**
- `queries` (list of str): The list of job queries to search for.
- `filepath` (str): The path to the CSV file where results will be saved.
- `num_listings` (int): The number of listings to retrieve for each job. Default is 1.

## Example Usage

```python
jobs = ["Administrative Assistant", "Sales Associate", "Customer Service Representative", "Nurse", "Accountant", "Teacher", "Software Developer", "Marketing Manager", "Cashier", "Project Manager", "Executive Assistant", "Analyst", "Human Resources Manager", "Graphic Designer", "Mechanical Engineer", "Data Analyst", "Financial Analyst", "Office Manager", "Electrician", "Product Manager", "Operations Manager", "IT Technician", "Receptionist", "Physical Therapist", "Paralegal", "Pharmacist", "Security Officer"]

queries = [jobs[i] + " kalamazoo michigan" for i in range(len(jobs))]
filepath = 'outputs/single_link_run_1.csv'
search_and_save_jobs(queries, filepath, num_listings=1)
```

## Notes

- Make sure to keep your SerpApi key secure and do not share it publicly.
- Adjust the `max_retries` and `retry_delay` parameters based on your network conditions and API rate limits.
- The script currently appends results to the specified CSV file. If you want to overwrite the file, change the file opening mode from `'a'` to `'w'` in the `search_and_save_jobs` function.
- This script retrieves only the first job listing per query. Adjust the `num` parameter in the search parameters to retrieve more listings.
