import socket
import requests
import whois
import sys
from urllib.parse import urlparse

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def check_url(url):
    # Perform DNS lookup
    try:
        print(f"Performing DNS lookup for {url}...")
        parsed_uri = get_domain(url)
        ip = socket.gethostbyname(parsed_uri)
        print(f"IP address: {ip}")
    except socket.gaierror:
        print("Invalid URL")
        return

    # Verify SSL certificate
    print(f"Verifying SSL certificate for {url}...")
    try:
        response = requests.get(url, timeout=10, verify=True)
        print(f"SSL certificate for {url} is valid.")
    except requests.exceptions.SSLError:
        print(f"SSL certificate for {url} is not valid.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to {url}: {e}")
        return

    # Perform WHOIS lookup
    print(f"Performing WHOIS lookup for {url}...")
    try:
        w = whois.whois(url)
        print(f"WHOIS information for {url}: {w}")
    except Exception as e:
        print(f"Could not perform WHOIS lookup for {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    check_url(sys.argv[1])
