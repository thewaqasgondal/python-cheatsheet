"""
Basic Web Scraping Examples in Python

This module demonstrates web scraping techniques using requests and BeautifulSoup.
It covers HTTP requests, HTML parsing, and data extraction.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Optional, Any
import re


def basic_http_request():
    """Demonstrate basic HTTP GET request."""
    print("=== Basic HTTP Request ===")

    url = "https://httpbin.org/get"
    response = requests.get(url)

    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {response.elapsed.total_seconds()} seconds")
    print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
    print(f"Response Size: {len(response.text)} characters")

    # Parse JSON response
    if response.headers.get('content-type', '').startswith('application/json'):
        data = response.json()
        print(f"JSON Response: {json.dumps(data, indent=2)[:200]}...")

    print()


def http_methods_demo():
    """Demonstrate different HTTP methods."""
    print("=== HTTP Methods Demo ===")

    base_url = "https://httpbin.org"

    # GET request
    get_response = requests.get(f"{base_url}/get", params={"key": "value", "foo": "bar"})
    print(f"GET: {get_response.url}")
    print(f"Status: {get_response.status_code}")

    # POST request
    post_data = {"username": "user", "password": "pass123"}
    post_response = requests.post(f"{base_url}/post", data=post_data)
    print(f"POST: Status {post_response.status_code}")

    # PUT request
    put_response = requests.put(f"{base_url}/put", json={"name": "test"})
    print(f"PUT: Status {put_response.status_code}")

    # DELETE request
    delete_response = requests.delete(f"{base_url}/delete")
    print(f"DELETE: Status {delete_response.status_code}")

    print()


def headers_and_user_agents():
    """Demonstrate custom headers and user agents."""
    print("=== Custom Headers and User Agents ===")

    # Custom headers
    headers = {
        'User-Agent': 'Python Web Scraper Example/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    url = "https://httpbin.org/user-agent"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"User-Agent sent: {data.get('user-agent', 'N/A')}")

    # Test different user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    for ua in user_agents:
        headers['User-Agent'] = ua
        response = requests.get("https://httpbin.org/user-agent", headers=headers)
        if response.status_code == 200:
            detected = response.json().get('user-agent', '')[:50]
            print(f"Detected: {detected}...")

    print()


def error_handling_and_timeouts():
    """Demonstrate error handling and timeouts."""
    print("=== Error Handling and Timeouts ===")

    urls = [
        "https://httpbin.org/delay/1",  # Normal response
        "https://httpbin.org/delay/5",  # Will timeout
        "https://httpbin-nonexistent.org/",  # DNS error
        "https://httpbin.org/status/404",  # 404 error
        "https://httpbin.org/status/500",  # 500 error
    ]

    for url in urls:
        try:
            print(f"Requesting: {url}")
            # Set timeout to 3 seconds
            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                print(f"  ✓ Success: {response.status_code}")
            else:
                print(f"  ⚠ HTTP Error: {response.status_code}")

        except requests.exceptions.Timeout:
            print("  ✗ Timeout Error")
        except requests.exceptions.ConnectionError:
            print("  ✗ Connection Error")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Request Error: {e}")

    print()


def basic_html_parsing():
    """Demonstrate basic HTML parsing with BeautifulSoup."""
    print("=== Basic HTML Parsing ===")

    # Sample HTML (in real scraping, this would come from requests.get().text)
    html_content = """
    <html>
    <head><title>Sample Page</title></head>
    <body>
        <h1>Welcome to My Website</h1>
        <div class="content">
            <p>This is a paragraph.</p>
            <p>This is another paragraph.</p>
        </div>
        <ul class="menu">
            <li><a href="/home">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
        <div class="articles">
            <article>
                <h2>Article 1</h2>
                <p>Content of article 1...</p>
            </article>
            <article>
                <h2>Article 2</h2>
                <p>Content of article 2...</p>
            </article>
        </div>
    </body>
    </html>
    """

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title = soup.find('title').get_text() if soup.find('title') else 'No title'
    print(f"Page Title: {title}")

    # Extract main heading
    h1 = soup.find('h1').get_text() if soup.find('h1') else 'No H1'
    print(f"Main Heading: {h1}")

    # Extract all paragraphs
    paragraphs = soup.find_all('p')
    print(f"Number of paragraphs: {len(paragraphs)}")
    for i, p in enumerate(paragraphs, 1):
        print(f"  Paragraph {i}: {p.get_text()}")

    # Extract menu items
    menu_items = soup.find_all('li')
    print(f"Menu items: {[li.get_text() for li in menu_items]}")

    # Extract article titles
    articles = soup.find_all('article')
    print(f"Articles found: {len(articles)}")
    for article in articles:
        title = article.find('h2')
        if title:
            print(f"  Article: {title.get_text()}")

    print()


def scraping_real_website():
    """Demonstrate scraping a real website (with caution)."""
    print("=== Scraping Real Website (Example) ===")

    # Note: Always check website's robots.txt and terms of service
    # This is just an example - in practice, be respectful and legal

    try:
        # Using a simple example site
        url = "https://quotes.toscrape.com/"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract quotes
            quotes = soup.find_all('div', class_='quote')

            print(f"Found {len(quotes)} quotes on the page:")

            for i, quote in enumerate(quotes[:3], 1):  # Show first 3
                text_elem = quote.find('span', class_='text')
                author_elem = quote.find('small', class_='author')

                text = text_elem.get_text() if text_elem else 'No text'
                author = author_elem.get_text() if author_elem else 'Unknown'

                print(f"{i}. \"{text}\" - {author}")

            # Extract tags
            tags = soup.find_all('a', class_='tag')
            unique_tags = list(set(tag.get_text() for tag in tags))
            print(f"\nPopular tags: {unique_tags[:10]}")  # Show first 10

        else:
            print(f"Failed to fetch website: HTTP {response.status_code}")

    except Exception as e:
        print(f"Error scraping website: {e}")

    print()


def api_data_extraction():
    """Demonstrate extracting data from JSON APIs."""
    print("=== API Data Extraction ===")

    # Example API endpoint
    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            print("API Response Data:")
            print(f"  User ID: {data.get('userId')}")
            print(f"  Post ID: {data.get('id')}")
            print(f"  Title: {data.get('title')}")
            print(f"  Body: {data.get('body', '')[:50]}...")

        else:
            print(f"API request failed: HTTP {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")

    print()


def form_submission():
    """Demonstrate form submission with POST requests."""
    print("=== Form Submission ===")

    # Using httpbin.org for testing
    url = "https://httpbin.org/post"

    # Form data
    form_data = {
        'username': 'testuser',
        'password': 'testpass123',
        'email': 'user@example.com',
        'remember': 'on'
    }

    try:
        response = requests.post(url, data=form_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print("Form submission successful!")
            print(f"Submitted data: {result.get('form', {})}")
        else:
            print(f"Form submission failed: HTTP {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Form submission error: {e}")

    print()


def rate_limiting_and_delays():
    """Demonstrate respectful scraping with delays."""
    print("=== Rate Limiting and Delays ===")

    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/uuid",
        "https://httpbin.org/ip"
    ]

    print("Making requests with delays to be respectful...")

    for i, url in enumerate(urls, 1):
        try:
            print(f"Request {i}: {url}")
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                if 'uuid' in url:
                    data = response.json()
                    print(f"  UUID: {data.get('uuid', 'N/A')}")
                elif 'ip' in url:
                    data = response.json()
                    print(f"  IP: {data.get('origin', 'N/A')}")
                else:
                    print("  ✓ Request successful"
            else:
                print(f"  ✗ HTTP {response.status_code}")

            # Add delay between requests (be respectful!)
            if i < len(urls):
                print("  Waiting 1 second...")
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error: {e}")

    print()


def main():
    """Run all web scraping demonstrations."""
    print("Python Web Scraping Examples")
    print("=" * 40)
    print()

    # Basic HTTP operations
    basic_http_request()
    http_methods_demo()
    headers_and_user_agents()
    error_handling_and_timeouts()

    # HTML parsing
    basic_html_parsing()

    # Real-world examples
    api_data_extraction()
    form_submission()
    rate_limiting_and_delays()

    # Note: scraping_real_website() is commented out to avoid potential issues
    # Uncomment only if you want to test with a real website
    # scraping_real_website()


if __name__ == "__main__":
    main()