# Web Scraping of Book Data Using Python

## Internship Task 1: Web Scraping

### Project Overview

This project demonstrates web scraping using Python. Data was collected from the publicly available Books to Scrape website.

The project uses Python libraries such as Requests, BeautifulSoup, and Pandas to extract, process, and store book information in a CSV dataset.

## Objectives

- Extract data from a public website.
- Understand and work with HTML structure.
- Navigate through multiple web pages.
- Collect relevant information from web pages.
- Create a structured dataset for further analysis.

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- HTML
- CSV

## Data Collected

The following information was collected for each book:

- Book Title
- Price
- Rating
- Availability
- Product URL

## Methodology

### 1. Send HTTP Request

The Requests library is used to access the web pages.

### 2. Parse HTML

BeautifulSoup is used to parse the HTML content and locate the required elements.

### 3. Extract Data

Book titles, prices, ratings, availability, and URLs are extracted from the HTML structure.

### 4. Navigate Multiple Pages

The scraper automatically visits catalogue pages and collects data from each page.

### 5. Store Data

The extracted information is converted into a Pandas DataFrame and saved as a CSV file.

## Output

The final dataset is stored at:

`data/books_dataset.csv`

## Project Structure

```text
Web-Scraping
│
├── data
│   └── books_dataset.csv
│
├── scraper.py
├── README.md
└── requirements.txt