from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_books():
    driver = webdriver.Chrome()
    driver.get("https://books.toscrape.com")

    books = driver.find_elements(By.CLASS_NAME, "product_pod")

    data = []

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    for book in books[:10]:
        title = book.find_element(By.TAG_NAME, "h3").text
        
        # ⭐ Extract rating
        rating_class = book.find_element(By.CLASS_NAME, "star-rating").get_attribute("class")
        rating_text = rating_class.split()[-1]  # gets "Three", "Four", etc.
        rating = rating_map.get(rating_text, None)

        price = book.find_element(By.CLASS_NAME, "price_color").text

        data.append({
            "title": title,
            "author": "Unknown",
            "description": price,
            "rating": rating,
            "url": "https://books.toscrape.com"
        })

    driver.quit()
    return data