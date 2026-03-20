"""
Utility functions for Selenium automation
"""
import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import csv
from pathlib import Path


def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for an element to be present and return it"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {selector}")
        return None


def wait_for_elements(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for elements to be present and return them"""
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, selector))
        )
        return elements
    except TimeoutException:
        print(f"Timeout waiting for elements: {selector}")
        return []


def click_element(driver, element, retries=3):
    """Safely click an element with retry logic"""
    for attempt in range(retries):
        try:
            element.click()
            return True
        except StaleElementReferenceException:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise
        except Exception as e:
            print(f"Error clicking element: {e}")
            return False
    return False


def scroll_to_element(driver, element):
    """Scroll element into view"""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)


def scroll_page(driver, pause_time=1):
    """Scroll to bottom of page"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)


def scroll_to_bottom_until_no_new_elements(driver, selector, max_scrolls=20, pause_time=1):
    """Scroll until no new elements appear"""
    previous_count = 0
    scroll_count = 0
    
    while scroll_count < max_scrolls:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        current_count = len(elements)
        
        if current_count == previous_count:
            print(f"No new elements. Found {current_count} total.")
            break
        
        previous_count = current_count
        scroll_page(driver, pause_time)
        scroll_count += 1
        print(f"Scroll {scroll_count}: Found {current_count} elements")
    
    return driver.find_elements(By.CSS_SELECTOR, selector)


def save_links_to_csv(links, filename):
    """Save list of job links to CSV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_url', 'collected_date', 'search_term'])
        
        for link_data in links:
            writer.writerow([
                link_data.get('url', ''),
                link_data.get('date', datetime.now().isoformat()),
                link_data.get('search_term', '')
            ])
    
    print(f"Saved {len(links)} links to {filename}")


def get_full_url(base_url, relative_url):
    """Convert relative URL to absolute URL"""
    if relative_url.startswith('http'):
        return relative_url
    
    base = base_url.rstrip('/')
    relative = relative_url.lstrip('/')
    
    return f"{base}/{relative}"


def extract_text_safe(element, selector, by=By.CSS_SELECTOR):
    """Safely extract text from an element"""
    try:
        sub_elem = element.find_element(by, selector)
        return sub_elem.text.strip()
    except NoSuchElementException:
        return ""


def extract_attribute_safe(element, attribute, selector="", by=By.CSS_SELECTOR):
    """Safely extract attribute from an element"""
    try:
        if selector:
            elem = element.find_element(by, selector)
        else:
            elem = element
        return elem.get_attribute(attribute) or ""
    except NoSuchElementException:
        return ""


def clean_text(text):
    """Clean text by removing extra whitespace and line breaks"""
    return " ".join(text.split())


def rate_limit(delay_seconds=2):
    """Implement polite rate limiting"""
    time.sleep(delay_seconds)
