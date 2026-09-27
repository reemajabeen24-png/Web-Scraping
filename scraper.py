import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import re


# ==========================================
# WEBSITE SETTINGS
# ==========================================

BASE_URL = "https://books.toscrape.com/"

# Store scraped books
books = []

# Create a requests session
session = requests.Session()

# Browser-like header
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
})


# ==========================================
# SCRAPING
# ==========================================

page_number = 1

while True:

    url = BASE_URL + f"catalogue/page-{page_number}.html"

    print(f"Scraping page {page_number}...")

    try:

        # Request webpage
        response = session.get(
            url,
            timeout=30
        )

        # Check HTTP status
        if response.status_code != 200:

            print(
                f"Page {page_number} returned "
                f"status code {response.status_code}."
            )

            print("Stopping scraper.")
            break

        # Parse HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find all books
        book_items = soup.select(
            "article.product_pod"
        )

        # Stop if no books are found
        if not book_items:

            print(
                "No books found. "
                "Scraping completed."
            )

            break


        # ==========================================
        # EXTRACT BOOK INFORMATION
        # ==========================================

        for book in book_items:

            # --------------------------------------
            # TITLE
            # --------------------------------------

            title = book.h3.a.get(
                "title",
                ""
            ).strip()


            # --------------------------------------
            # PRICE
            # --------------------------------------

            price_text = book.select_one(
                ".price_color"
            ).get_text(
                strip=True
            )

            # Extract only the numeric part.
            # This handles:
            # £51.77
            # Â£51.77
            # Â51.77
            # etc.

            price_match = re.search(
                r"\d+(?:\.\d+)?",
                price_text
            )

            if price_match:

                price = float(
                    price_match.group()
                )

            else:

                price = None


            # --------------------------------------
            # AVAILABILITY
            # --------------------------------------

            availability_element = book.select_one(
                ".availability"
            )

            if availability_element:

                availability = (
                    availability_element
                    .get_text(
                        " ",
                        strip=True
                    )
                )

            else:

                availability = "Unknown"


            # --------------------------------------
            # RATING
            # --------------------------------------

            rating_element = book.select_one(
                ".star-rating"
            )

            if rating_element:

                rating_classes = (
                    rating_element.get(
                        "class",
                        []
                    )
                )

                if len(rating_classes) > 1:

                    rating = rating_classes[1]

                else:

                    rating = "Unknown"

            else:

                rating = "Unknown"


            # --------------------------------------
            # BOOK URL
            # --------------------------------------

            link_element = book.h3.a

            relative_url = link_element.get(
                "href",
                ""
            )

            book_url = urljoin(
                url,
                relative_url
            )


            # --------------------------------------
            # STORE BOOK DATA
            # --------------------------------------

            books.append({

                "Title": title,

                "Price": price,

                "Rating": rating,

                "Availability": availability,

                "URL": book_url

            })


        # --------------------------------------
        # NEXT PAGE
        # --------------------------------------

        page_number += 1

        # Wait before requesting next page
        time.sleep(1)


    # ==========================================
    # CONNECTION ERROR HANDLING
    # ==========================================

    except requests.exceptions.RequestException as error:

        print(
            f"Connection error on page "
            f"{page_number}: {error}"
        )

        print(
            "Waiting 5 seconds before retrying..."
        )

        time.sleep(5)


        # Retry once
        try:

            response = session.get(
                url,
                timeout=30
            )

            if response.status_code != 200:

                print(
                    "Retry failed."
                )

                print(
                    "Stopping scraper."
                )

                break


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            book_items = soup.select(
                "article.product_pod"
            )


            if not book_items:

                print(
                    "No books found after retry."
                )

                break


            # ======================================
            # PROCESS RETRY RESULTS
            # ======================================

            for book in book_items:

                # Title
                title = book.h3.a.get(
                    "title",
                    ""
                ).strip()


                # Price
                price_text = book.select_one(
                    ".price_color"
                ).get_text(
                    strip=True
                )


                price_match = re.search(
                    r"\d+(?:\.\d+)?",
                    price_text
                )


                if price_match:

                    price = float(
                        price_match.group()
                    )

                else:

                    price = None


                # Availability
                availability_element = (
                    book.select_one(
                        ".availability"
                    )
                )


                if availability_element:

                    availability = (
                        availability_element
                        .get_text(
                            " ",
                            strip=True
                        )
                    )

                else:

                    availability = "Unknown"


                # Rating
                rating_element = book.select_one(
                    ".star-rating"
                )


                if rating_element:

                    rating_classes = (
                        rating_element.get(
                            "class",
                            []
                        )
                    )


                    if len(rating_classes) > 1:

                        rating = (
                            rating_classes[1]
                        )

                    else:

                        rating = "Unknown"

                else:

                    rating = "Unknown"


                # URL
                relative_url = (
                    book.h3.a.get(
                        "href",
                        ""
                    )
                )


                book_url = urljoin(
                    url,
                    relative_url
                )


                # Store
                books.append({

                    "Title": title,

                    "Price": price,

                    "Rating": rating,

                    "Availability": availability,

                    "URL": book_url

                })


            page_number += 1

            time.sleep(1)


        except requests.exceptions.RequestException as retry_error:

            print(
                f"Retry failed: {retry_error}"
            )

            print(
                "Scraping stopped."
            )

            break


# ==========================================
# CREATE DATAFRAME
# ==========================================

print("\nCreating dataset...")

df = pd.DataFrame(books)


# ==========================================
# REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates(
    subset=["Title"]
)


# ==========================================
# CLEAN AVAILABILITY
# ==========================================

if "Availability" in df.columns:

    df["Availability"] = (
        df["Availability"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
    )


# ==========================================
# CLEAN PRICE
# ==========================================

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)


# ==========================================
# SAVE DATASET
# ==========================================

output_file = "data/books_dataset.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# FINAL OUTPUT
# ==========================================

print("\n===================================")
print("       SCRAPING COMPLETED")
print("===================================")

print(
    f"Total books collected: {len(df)}"
)

print(
    f"Dataset saved to: {output_file}"
)

print(
    f"Columns: {list(df.columns)}"
)

print("===================================")