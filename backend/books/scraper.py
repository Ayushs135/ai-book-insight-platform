from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from .ai_utils import generate_summary
import time
from selenium.webdriver.chrome.service import Service



def scrape_books():
    # Setup driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://books.toscrape.com/catalogue/category/books/history_32/index.html")

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
            title_element = book.find_element(By.CSS_SELECTOR, "h3 a")

            title = title_element.get_attribute("title")

# Fallback (VERY IMPORTANT)
            if not title:
                title = title_element.text

            print("Scraping:", title)

            # Rating
            rating_class = book.find_element(By.CLASS_NAME, "star-rating").get_attribute("class")
            if rating_class:
                rating_text = rating_class.split()[-1]
                rating = rating_map.get(rating_text, None)
            else:
                rating = None

            # Book link
            link = book.find_element(By.TAG_NAME, "a").get_attribute("href")
            if not link:
                continue

            # OPEN IN NEW TAB (stable approach)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            driver.get(link)
            time.sleep(1)

            # Description
            try:
                description = driver.find_element(By.ID, "product_description") \
                    .find_element(By.XPATH, "following-sibling::p").text
            except:
                description = "No description available"

            # Close tab and return
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # Save data
            data.append({
                "title": title,
                "author": "Unknown",
                "description": description,
                "rating": rating,
                "url": link
            })

        except Exception as e:
            print("Error scraping book:", e)
            continue

    driver.quit()

    # Generate summaries (can disable if slow)
    for book in data:
        try:
            book['summary'] = generate_summary(book.get('description', ''))
        except:
            book['summary'] = book.get('description', '')[:100]

    return data