import requests
from pyfiglet import Figlet
from tqdm import tqdm
import socket
import time
import re
from urllib.parse import urlparse  # Used to extract the domain
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Function to check if the URL is valid
def is_valid_url(url):
    regex = re.compile(r'^(?:http|ftp)s?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b(?:/[\w\.-]*)*$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to get the IP address of the URL
def get_ip_from_url(url):
    try:
        # Extract domain name from URL (ignoring http:// or https://)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path  # fallback for non-standard input
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        print(f"Error: Unable to resolve URL '{url}'. Please check the URL and try again.")
        return None

# Function to get geolocation info using IPinfo API
def get_geolocation_info(ip):
    try:
        # Get the API key from environment variables
        api_key = os.getenv("IPINFO_API_KEY")
        if not api_key:
            print("Error: API key not found in environment variables.")
            return None, None

        # Make an API request to IPinfo
        url = f"https://ipinfo.io/{ip}/json?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Check if latitude and longitude are available
        location = data.get("loc", None)
        if location:
            latitude, longitude = location.split(',')
            return latitude, longitude
        else:
            print(f"Error: Location data is not available for IP {ip}.")
            return None, None
    except Exception as e:
        print(f"Error: Failed to fetch geolocation data for IP '{ip}': {e}")
        return None, None

# Function to generate Google Maps link with coordinates
def get_google_maps_link(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

# Main function to execute the script
def main():
    f = Figlet(font='slant')  # You can also use '3-d'
    print(f.renderText('Ip2tools'))

    # Get URL input
    url = input('Enter a URL: ').strip()

    # Validate the URL format
    if not is_valid_url(url):
        print(f"Error: '{url}' is not a valid URL.")
        return

    # Get the IP address from the URL
    ip = get_ip_from_url(url)
    if ip is None:
        return

    # Fetch geolocation info for the IP using IPinfo
    latitude, longitude = get_geolocation_info(ip)
    if latitude is None or longitude is None:
        return

    # Display progress using tqdm
    print("Fetching information, please wait...")
    for _ in tqdm(range(100), desc="Loading", ncols=100):
        time.sleep(0.1)

    # Print the results
    print(f'IP: {ip}')
    time.sleep(0.1)
    print(f'Latitude: {latitude}')
    time.sleep(0.1)
    print(f'Longitude: {longitude}')
    time.sleep(0.1)

    # Generate Google Maps link
    google_maps_link = get_google_maps_link(latitude, longitude)
    print(f'Google Maps Link: {google_maps_link}')

if __name__ == "__main__":
    main()

