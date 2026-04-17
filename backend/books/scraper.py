from selenium import webdriver
from selenium.webdriver.common.by import By
from .ai_utils import generate_summary
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
        try:
            title = book.find_element(By.TAG_NAME, "h3").text

            # ⭐ Rating
            rating_class = book.find_element(By.CLASS_NAME, "star-rating").get_attribute("class")
            if rating_class:
                rating_text = rating_class.split()[-1]
                rating = rating_map.get(rating_text, None)
            else:
                rating = None

            # 🔗 Link
            link = book.find_element(By.TAG_NAME, "a").get_attribute("href")
            if not link:
                continue

            # 👉 Open detail page
            driver.get(link)
            time.sleep(1)

            try:
                description = driver.find_element(By.ID, "product_description")\
                    .find_element(By.XPATH, "following-sibling::p").text
            except:
                description = "No description available"

            data.append({
                "title": title,
                "author": "Unknown",
                "description": description,
                "rating": rating,
                "url": link
            })

            driver.back()
            time.sleep(1)

        except Exception as e:
            print("Error scraping book:", e)
            continue

    driver.quit()

    # Generate summaries
    for book in data:
        book['summary'] = generate_summary(book.get('description', ''))

    return data