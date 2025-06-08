import os
import csv
import re
import requests
import argparse
import json
from urllib.parse import urlparse

def safe_filename(text):
    """
    Generates a filesystem-safe filename from a string.
    Replaces invalid characters with an underscore and limits length.
    """
    # Replace slashes and other problematic characters with a space first
    text = re.sub(r'[<>:"/\\|?*]', ' ', text)
    # Replace multiple spaces with a single underscore
    text = re.sub(r'\s+', '_', text).strip()
    # A filename cannot end with a dot in Windows
    if text.endswith('.'):
        text = text[:-1]
    # Limit length to avoid filesystem errors
    return text[:200]

def scrape_powerdms_site(url):
    """
    Scrapes a public PowerDMS site, extracts document info, and generates
    a CSV file and a wget download script.
    """
    print(f"-> Starting scrape for: {url}")

    # --- 1. Determine Site Name and API Endpoint ---
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path_parts = [part for part in parsed_url.path.split('/') if part]

        if not domain.endswith('powerdms.com') or not path_parts:
            print("! ERROR: This does not appear to be a valid public PowerDMS URL.")
            print("! Example: https://public.powerdms.com/MassStatePolice/tree/147101")
            return

        site_name = path_parts[0]
        json_api_url = f"https://{domain}/{site_name}/documents"
        print(f"   Site Name: {site_name}")
        print(f"   API Endpoint: {json_api_url}")

    except Exception as e:
        print(f"! ERROR: Could not parse the provided URL. {e}")
        return

    # --- 2. Fetch JSON Data from the API ---
    try:
        print("\n-> Fetching document list from API...")
        # A valid User-Agent is crucial to avoid being blocked.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(json_api_url, timeout=45)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        print("   ✓ Successfully fetched JSON data.")

    except requests.exceptions.HTTPError as e:
        print(f"! HTTP ERROR: {e.response.status_code} for URL {json_api_url}")
        print("! The site may not have a public document API or may be private.")
        return
    except requests.exceptions.RequestException as e:
        print(f"! REQUEST ERROR: Could not connect to the server. {e}")
        return
    except json.JSONDecodeError:
        print("! ERROR: Failed to decode JSON. The response may not be valid JSON.")
        print("   Saving server response to 'error_response.html' for debugging.")
        with open('error_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        return

    # --- 3. Parse JSON and Prepare for Output ---
    documents = data.get('data')
    if documents is None or not isinstance(documents, list):
        print("! ERROR: The JSON response does not contain a 'data' list.")
        print("   Saving JSON response to 'debug.json' for inspection.")
        with open('debug.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return
        
    if not documents:
        print("! No public documents were found at this endpoint.")
        return

    print(f"   ✓ Found {len(documents)} document entries.")

    # --- 4. Define Output Files and Directories ---
    download_dir = f"downloaded_{site_name}"
    csv_filename = f"{site_name}_documents.csv"
    script_filename = f"download_{site_name}.sh"

    # --- 5. Write Data to CSV File ---
    print(f"\n-> Writing document list to '{csv_filename}'...")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'url'])  # CSV Header
        for doc in documents:
            name = doc.get('name', 'no-name-found')
            public_url = doc.get('publicUrl', 'no-url-found')
            writer.writerow([name, public_url])
    print(f"   ✓ Success.")

    # --- 6. Generate wget Download Script ---
    print(f"-> Generating download script '{script_filename}'...")
    with open(script_filename, 'w', encoding='utf-8') as f:
        f.write("#!/bin/sh\n")
        f.write("# Auto-generated PowerDMS download script\n\n")
        f.write(f"# Create the download directory if it doesn't exist\n")
        f.write(f"mkdir -p \"{download_dir}\"\n\n")

        for doc in documents:
            name = doc.get('name', 'no-name-found')
            public_url = doc.get('publicUrl', 'no-url-found')
            
            if 'no-url-found' in public_url:
                f.write(f"# SKIPPING: No publicUrl found for '{name}'\n\n")
                continue

            # Generate a safe filename and add a .pdf extension
            output_filename = f"{safe_filename(name)}.pdf"
            full_output_path = os.path.join(download_dir, output_filename)

            # Write the wget command for the current file
            f.write(f"echo \"Downloading: {name}\"\n")
            # Using -U for User-Agent, -O for Output file, --no-check-certificate for compatibility
            f.write(f'wget -U "Mozilla/5.0" --no-check-certificate -O "{full_output_path}" "{public_url}"\n\n')

    print(f"   ✓ Success.")
    print("\n" + "="*50)
    print("ALL DONE!")
    print(f"To download the files, run these commands in your terminal:")
    print(f"1. chmod +x {script_filename}")
    print(f"2. ./{script_filename}")
    print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape a public PowerDMS website for all document URLs and create a download script.",
        epilog="Example: python powerdms_scraper.py \"https://public.powerdms.com/MassStatePolice/tree/147101\""
    )
    parser.add_argument(
        "url",
        type=str,
        help="The public URL of the PowerDMS site you want to scrape."
    )
    args = parser.parse_args()
    
    scrape_powerdms_site(args.url)

