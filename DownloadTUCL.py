import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Create a folder named "tucl" to store downloaded files
if not os.path.exists("tucl"):
    os.makedirs("tucl")

# Base URL
base_url = "https://elibrary.tucl.edu.np/collections/1f1fdc5f-96bf-41b1-b0d9-21ae72697297?cp.page="

# Function to download HTML and return parsed BeautifulSoup object
def download_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Function to download PDF
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Get the absolute path of the "tucl" folder
base_path = os.path.abspath("tucl")

# Step 1: Modify each page to have proper links to other pages in the page number widget
for page_num in range(1, 8):
    page_url = base_url + str(page_num)
    page_filename = f"tucl/page_{page_num}.html"
    if os.path.exists(page_filename):
        print(f"Skipped downloading page {page_num} as it already exists")
        continue
    # Output console message
    print(f"Downloaded page {page_num}")
    # Download page HTML
    page_soup = download_html(page_url)
    # Modify page HTML to have proper links to other pages
    page_links = page_soup.find_all('a', class_='page-link')
    for link in page_links:
        link['href'] = os.path.abspath(f"tucl/page_{link.text.strip().replace('(current)', '').strip()}.html")
    # Write modified HTML content to file
    with open(page_filename, "w", encoding="utf-8") as f:
        f.write(str(page_soup))

# Step 2: Download paper-page HTML and associated PDFs
counter = 0
paper_page_paths = {}  # Dictionary to store paper-page paths
for page_num in range(1, 8):
    page_filename = f"tucl/page_{page_num}.html"
    with open(page_filename, "r", encoding="utf-8") as f:
        page_soup = BeautifulSoup(f.read(), 'html.parser')
    paper_links = page_soup.find_all('a', href=lambda href: href and "items" in href)
    for link in paper_links:
        link_text = link.get_text().strip()
        # Replace illegal characters in filename
        modified_link_text = link_text.replace(":", "").replace("/", "-")
        paper_filename = f"tucl/{modified_link_text}.html"
        if os.path.exists(paper_filename):
            print(f"Skipped downloading {modified_link_text} as it already exists")
            # Increment counter
            counter += 1
            continue
        # Check if link text is not "No Thumbnail Available"
        if link_text != "No Thumbnail Available":
            paper_url = urljoin(base_url, link["href"])
            paper_soup = download_html(paper_url)
            with open(paper_filename, "w", encoding="utf-8") as f:
                f.write(str(paper_soup))
            # Increment counter
            counter += 1
            # Output console message
            print(f"Downloaded: Page-{page_num} File-{counter} {paper_filename}")
            # Download PDFs associated with paper-page
            pdf_links = paper_soup.find_all('a', href=lambda href: href and "bitstreams" in href)
            for pdf_link in pdf_links:
                pdf_url = urljoin(base_url, pdf_link["href"])
                pdf_filename = f"tucl/{modified_link_text}_{pdf_links.index(pdf_link) + 1}.pdf"
                download_pdf(pdf_url, pdf_filename)
                # Modify paper-page HTML to correctly open the PDF file
                pdf_relative_path = os.path.relpath(pdf_filename, base_path)
                with open(paper_filename, "r", encoding="utf-8") as f:
                    html_content = f.read()
                    html_content = html_content.replace(pdf_link["href"], f"tucl/{os.path.basename(pdf_filename)}")
                with open(paper_filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
            # Store paper-page path in dictionary with both modified and original link text
            paper_page_paths[modified_link_text] = {
                "modified_link_text": modified_link_text,
                "original_link_text": link_text,
                "path": os.path.relpath(paper_filename, base_path)
            }

# Step 3: Update links in all page HTML files to point to the correct paper-pages
for page_num in range(1, 8):
    page_filename = f"tucl/page_{page_num}.html"
    with open(page_filename, "r", encoding="utf-8") as f:
        page_soup = BeautifulSoup(f.read(), 'html.parser')
    for link in page_soup.find_all('a'): 
        # Check if the link text matches the modified paper-page link
        link_text = link.get_text().strip().replace(":", "").replace("/", "-")
        if link_text in paper_page_paths:
            # Replace the href attribute with the relative path of the paper-page
            link['href'] = paper_page_paths[link_text]["path"]
    # Write updated page HTML content to file
    with open(page_filename, "w", encoding="utf-8") as f:
        f.write(str(page_soup))
