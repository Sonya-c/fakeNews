
import csv
from pynvim import encoding
import requests
from requests import Response
from bs4 import BeautifulSoup
from typing import List, Dict


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
        page: Response = requests.get(url, headers)

        if page.ok:
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup

    except Exception:
        print(f"[ERROR]: web_scraping.scrap page_url = {url}")

    return None


def save_page(id: int, soup: BeautifulSoup) -> None:
    """Save the page data and the page content

    Args:
        soup (BeautifulSoup): soup oject
    """

    # Write the date to the cvs file
    csv_file = csv.writer(open("./data/main.csv", "a"))

    title: str = "TITLE_ERROR"

    for title_tag in soup.find_all("title"):
        if title_tag.string is not None:
            title = title_tag.string

    csv_file.writerow([
        title.replace(",", "")
    ])

    # Write the page content to a file
    file_name: str = "data/pages/page_" + str(id) + ".txt"

    with open(file_name, "w", encoding="utf-8") as text_file:
        text_file.write(
            soup.find_all("body")[0].get_text()
        )


def get_url_list(soup: BeautifulSoup, url_list: List[str]) -> List[str]:
    """Get the links of a page

    Args:
        soup (BeautifulSoup): the soup object
        url_list (List[str]): url list

    Returns:
        List[str]:
    """
    for a in soup.select("a"):  # For each anchor in the page

        if a.has_attr("href"):
            href: str = a.attrs["href"]  # Get the link of the anchor

            if (len(href) >= 1 and href[0] != "#"):  # If the url is correct
                url_list.append(href)  # Ad the url to the list of url

    return url_list


def scrape(num: int, url: str) -> None:
    """Scrape a website 

    Args:
        num (int): Number of pages
        url (str): main url
    """
    csv_file = csv.writer(open("./data/main.csv", "w"))
    csv_file.writerow(["Titulo, "])

    url_list: List[str] = [url]  # Init the url list
    i: int = 0  # Interator
    j: int = 0  # Number of correct pages

    while (i <= num and i < len(url_list)):
        soup = get_page(url_list[i])  # Get the soup object

        if (soup != None):
            j += 1  # New correct page
            save_page(j, soup)  # Save the page content to a txt
            url_list = get_url_list(soup, url_list)  # Add new elements to the liss

        i += 1
