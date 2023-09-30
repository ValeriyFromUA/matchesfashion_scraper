# Description

This application gathers information about products from the resource https://www.matchesfashion.com/ and saves it to a
CSV or JSON file. The application collects the following fields:

- title
- url
- price full
- price drop
- image url
- category
- gender

## Usage

To use the application, follow these steps:

1. Clone the code using `git clone ...` or download it as a zip archive.
2. Set up a virtual environment and install dependencies using the command `poetry install`.
3. Run `run.py` and wait for the results. Depending on the number of links, this process may take some time. The
   current progress will be displayed in the logs.