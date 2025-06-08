# PowerDMS Public Document Scraper

A command-line Python script to efficiently scrape all public document links from a `public.powerdms.com` website and generate a `wget` script to download them.

## Overview

Many organizations use PowerDMS to host their public-facing documents and policies. This tool automates the process of fetching the entire list of these public documents from a specific site's API. It then creates two essential files:

1. A **CSV file** (`.csv`) containing the names and direct URLs of all documents, perfect for record-keeping or analysis.
    
2. A **Shell Script** (`.sh`) containing `wget` commands to download every document, intelligently naming them and saving them into an organized folder.
    

This approach saves a significant amount of time compared to manually clicking and saving each file.

## Features

- **Simple to Use**: Just provide the public URL of the PowerDMS site.
    
- **Automated API Discovery**: Automatically finds the correct JSON API endpoint from a standard "tree" URL.
    
- **Robust Error Handling**: Provides clear feedback if the URL is invalid, the site is private, or the connection fails.
    
- **Organized Output**: Creates a dedicated folder for the downloaded files, named after the site (e.g., `downloaded_ExampleSite`).
    
- **Safe Filenames**: Automatically cleans up document names to create valid, filesystem-safe filenames for the PDFs.
    
- **Cross-Platform Download Script**: Generates a standard shell script that works on Linux, macOS, and Windows (via WSL or Git Bash).
    

## Requirements

Before you begin, ensure you have the following installed on your system:

- **Python 3**: The script is written in Python 3.
    
- **Requests Library**: A Python library for making HTTP requests. If you don't have it, install it with pip:
    
    ```
    pip install requests
    ```
    
- **wget**: A command-line utility for downloading files.
    
    - **macOS**: Can be installed via [Homebrew](https://brew.sh/ "null"): `brew install wget`
        
    - **Linux**: Usually pre-installed on most distributions.
        
    - **Windows**: Can be used via the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install "null") or by installing [Git for Windows](https://git-scm.com/download/win "null"), which includes Git Bash.
        

## How to Use

1. **Save the Script**: Save the code from the Canvas to a file named `powerdms_scraper.py`.
    
2. **Run the Script from Your Terminal**: Execute the script and pass the target URL as the only argument. The URL should be enclosed in quotes.
    
    ```
    python powerdms_scraper.py "YOUR_POWERDMS_URL_HERE"
    ```
    
3. **Make the Download Script Executable**: The scraper will generate a `.sh` file. You need to give it permission to run.
    
    ```
    # Example for a site named "ExampleSite"
    chmod +x download_ExampleSite.sh
    ```
    
4. **Run the Download Script**: Execute the script to begin downloading all the files.
    
    ```
    # Example for a site named "ExampleSite"
    ./download_ExampleSite.sh
    ```
    

## Example

Here is a complete example from start to finish.

```
# Step 1: Run the scraper with a target URL
python powerdms_scraper.py "https://public.powerdms.com/ExampleSite/tree/12345"

# The script will output its progress and create two files:
# -> ExampleSite_documents.csv
# -> download_ExampleSite.sh

# Step 2: Make the downloader executable
chmod +x download_ExampleSite.sh

# Step 3: Run the downloader
./download_ExampleSite.sh

# This will create a folder named 'downloaded_ExampleSite'
# and save all the PDF files inside it.
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
