import requests
import os
from bs4 import BeautifulSoup

# GovInfo API configuration
API_KEY = "Nznn3n4fA09KW7bDN3wcEUmiwMnMvwddffOWVKW0"
BASE_URL = "https://api.govinfo.gov/packages"
OUTPUT_DIR = "./datasets"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Titles to retrieve
TITLES = [
    "USCODE-2023-title15",  # Commerce and Trade
    "USCODE-2023-title26",  # Internal Revenue Code
    "USCODE-2023-title29",  # Labor
    "USCODE-2023-title11"   # Bankruptcy
]

# Function to retrieve package details
def get_package_details(title):
    url = f"{BASE_URL}/{title}/summary?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        downloads = package_data.get("download", {})
        return {
            "html": downloads.get("txtLink")
        }
    else:
        print(f"Failed to retrieve package details for {title}: {response.status_code}")
        return None

# Function to download and save HTML content
def download_and_save_html(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"HTML content downloaded and saved: {filepath}")
        return filepath
    else:
        print(f"Failed to download HTML content from {url}: {response.status_code}")
        return None

# Function to extract and clean text from HTML file
def extract_text_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text()
    cleaned_text = os.path.join(OUTPUT_DIR, os.path.basename(html_path).replace(".html", "_text.txt"))
    with open(cleaned_text, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Extracted and saved text from HTML: {cleaned_text}")
    return cleaned_text

# Function to analyze the text file
def analyze_text_file(txt_file):
    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Basic operations
    print("First 5 lines of the file:")
    print("\n".join(lines[:5]))

    # Calculate size and dimensions
    total_lines = len(lines)
    print(f"Total lines in the file: {total_lines}")

    # empty lines
    empty_lines = sum(1 for line in lines if not line.strip())
    print(f"Number of empty lines: {empty_lines}")

# Main execution
def main():
    for title in TITLES:
        details = get_package_details(title)
        if not details or not details["html"]:
            print(f"No HTML link available for {title}")
            continue

        # Download HTML content
        html_path = download_and_save_html(f"{details['html']}?api_key=Nznn3n4fA09KW7bDN3wcEUmiwMnMvwddffOWVKW0", f"{title}.html")
        if html_path:

            txt_path = extract_text_from_html(html_path)

            analyze_text_file(txt_path)

if __name__ == "__main__":
    main()