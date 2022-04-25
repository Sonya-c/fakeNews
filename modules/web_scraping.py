import csv
import requests
from requests import Response
from bs4 import BeautifulSoup, Tag
from typing import List, Dict
from modules.to_csv import save_table
import urllib.parse


def get_page(url: str) -> BeautifulSoup:
    """Given an url, returns the BeautifullSoup object

    Args:
        url (str): url to request

    Returns:
        BeautifulSoup: the beautifulSoup object (None if error)
    """

    headers: Dict[str, str] = {
        "User-Agent": "Sonya Castro, sonya-c.github.io",
        "From": "sonyac@uninorte.edu.co"
    }

    try:
        page: Response = requests.get(url, headers)  # request the page

        if page.ok:
            soup = BeautifulSoup(page.content, "html.parser")  # parse the page
            return soup

    except Exception:
        print(f"[ERROR]: web_scraping.scrap page_url = {url}")

    return None


def get_data(soup: BeautifulSoup) -> List[str]:
    """Save the page data and the page content

    Args:
        soup (BeautifulSoup): soup oject
    """
    try:
        title: str = soup.select("head title")[0].string
        title = title.replace("BBC", "").replace(
            "Home", "").replace("News", "").replace("Sports", "")
        if (title == ""):
            return []

    except Exception:
        title: str = "TITLE_ERROR"

    try:
        time: str = soup.select("time")[0].attrs["datetime"]
        time = time[:10]
    except Exception:
        time: str = "TIME ERROR"

    return [title, time]


def get_url_list(soup: BeautifulSoup, url_list: List[str], parent_url: str) -> List[str]:
    """Get the links of a page

    Args:
        soup (BeautifulSoup): the soup object
        url_list (List[str]): url list

    Returns:
        List[str]:
    """
    for a in soup.select("#site-container a, #main-content a"):  # For each anchor in the page

        if a.has_attr("href"):
            href: str = a.attrs["href"]  # Get the link of the anchor

            if (len(href) >= 1 and href[0] != "#"):  # If the url is correct

                # It's a relative URL
                if not urllib.parse.urlparse(href).netloc:
                    href = urllib.parse.urljoin(parent_url, href)

                url_list.append(href)  # Ad the url to the list of url

    return url_list


def scrape(num: int) -> None:
    """Scrape a website 

    Args:
        num (int): Number of pages
    """

    url_list: List[str] = ["https://www.bbc.com/news"]  # Init the url list

    i: int = 0  # Number of page to scrape
    j: int = 0  # Number of correct pages

    rows: List[List[str, str]] = []

    # while when neew more pages and there still page to scrape
    while (j < num and i < len(url_list)):
        soup: BeautifulSoup = get_page(url_list[i])  # Get the soup object

        if (soup != None):
            j += 1  # New correct page

            row = get_data(soup)  # Save the page content to a txt

            if (row != []):
                rows.append(row)
            # Update the list (get more pages)
            url_list = get_url_list(soup, url_list, url_list[i])

        i += 1  # Scrape the next page

    save_table("./data/exp_1/data.csv", ["Title", "Date"], rows)
    print(f"Total de páginas revisadas = {i}")
    print(f"Total de páginas obtenidas = {j}")
