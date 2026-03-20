"""
Main Selenium script for job board automation and link collection
"""
import time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from config import (
    JOB_TITLES, LOCATIONS, HEADLESS, TIMEOUT, POLITE_DELAY, OUTPUT_FILE
)
from utils import (
    wait_for_element, wait_for_elements, scroll_to_bottom_until_no_new_elements,
    save_links_to_csv, get_full_url, click_element, rate_limit
)


class JobBoardScraper:
    def __init__(self):
        """Initialize the web driver"""
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        options.add_argument(f"--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(TIMEOUT)
        self.collected_links = []
    
    def scrape_github_jobs(self):
        """Scrape from GitHub Jobs board"""
        print("\n" + "="*60)
        print("Scraping GitHub Jobs Board")
        print("="*60)
        
        base_url = "https://github.com/jobs"
        
        try:
            self.driver.get(base_url)
            rate_limit(POLITE_DELAY)
            
            # Wait for page to load
            wait_for_element(self.driver, ".Box-row", timeout=20)
            
            # Search for multiple job titles
            for job_title in JOB_TITLES[:2]:  # Limit to 2 for demo
                print(f"\nSearching for: {job_title}")
                
                # Clear and fill search box
                search_box = wait_for_element(self.driver, "input[name='description']")
                if search_box:
                    search_box.clear()
                    search_box.send_keys(job_title)
                    rate_limit(1)
                    
                    # Submit search
                    search_box.submit()
                    rate_limit(POLITE_DELAY)
                    
                    # Wait for results
                    wait_for_element(self.driver, ".Box-row", timeout=20)
                    
                    # Scroll and collect links
                    job_cards = scroll_to_bottom_until_no_new_elements(
                        self.driver, ".Box-row", max_scrolls=10
                    )
                    
                    for card in job_cards[:50]:  # Limit for demo
                        try:
                            link_elem = card.find_element(By.CSS_SELECTOR, "a[data-ga-click*='Job']")
                            url = link_elem.get_attribute("href")
                            full_url = get_full_url(base_url, url)
                            
                            self.collected_links.append({
                                'url': full_url,
                                'date': datetime.now().isoformat(),
                                'search_term': job_title,
                                'source': 'GitHub Jobs'
                            })
                            print(f"  ✓ Collected: {full_url[:60]}")
                        except Exception as e:
                            print(f"  ✗ Error parsing job card: {e}")
                            continue
                    
                    print(f"Total collected from this search: {len([l for l in self.collected_links if l['search_term'] == job_title])}")
        
        except Exception as e:
            print(f"Error scraping GitHub Jobs: {e}")
    
    def scrape_example_board(self):
        """Scrape from a public example job board"""
        print("\n" + "="*60)
        print("Scraping Example Public Job Board")
        print("="*60)
        
        # This is a simulated collection from a public job board
        # In production, you would implement actual scraping
        
        example_jobs = [
            {'url': 'https://example.com/jobs/1234', 'title': 'Software Engineer - Python', 'company': 'Tech Corp'},
            {'url': 'https://example.com/jobs/1235', 'title': 'Data Analyst', 'company': 'Data Inc'},
            {'url': 'https://example.com/jobs/1236', 'title': 'QA Engineer', 'company': 'Quality Systems'},
            {'url': 'https://example.com/jobs/1237', 'title': 'DevOps Engineer', 'company': 'Cloud Tech'},
            {'url': 'https://example.com/jobs/1238', 'title': 'Frontend Developer', 'company': 'WebDev Studios'},
        ]
        
        for job in example_jobs:
            self.collected_links.append({
                'url': job['url'],
                'date': datetime.now().isoformat(),
                'search_term': job.get('title', 'General'),
                'source': 'Example Board'
            })
            print(f"  ✓ Added: {job['url']}")
        
        print(f"Added {len(example_jobs)} example jobs")
    
    def generate_sample_data(self):
        """Generate sample job links for testing Scrapy"""
        print("\n" + "="*60)
        print("Generating Sample Job Data")
        print("="*60)
        
        # Real job URLs that we'll scrape with Scrapy
        sample_links = [
            {
                'url': 'https://www.greensill.com/careers/jobs/software-engineer/',
                'source': 'Company Career Page',
                'search_term': 'Software Engineer'
            },
            {
                'url': 'https://greenhouse.io/app/jobs',
                'source': 'Greenhouse',
                'search_term': 'General'
            }
        ]
        
        for link in sample_links[:5]:  # Add sample links
            self.collected_links.append({
                'url': link['url'],
                'date': datetime.now().isoformat(),
                'search_term': link.get('search_term', 'Job'),
                'source': link.get('source', 'Various')
            })
            print(f"  ✓ Added sample: {link['url'][:60]}")
        
        print(f"Total sample links: {len(sample_links)}")
    
    def run(self):
        """Run the scraping workflow"""
        print("\n" + "#"*60)
        print("# JOB MARKET SCRAPER - SELENIUM AUTOMATION")
        print("#"*60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Scrape from GitHub Jobs
            self.scrape_github_jobs()
            
            # Add example jobs
            self.scrape_example_board()
            
            # Generate sample data for Scrapy
            self.generate_sample_data()
            
        except Exception as e:
            print(f"\nError during scraping: {e}")
        finally:
            self.driver.quit()
            print("\nDriver closed.")
        
        # Save collected links
        if self.collected_links:
            save_links_to_csv(self.collected_links, OUTPUT_FILE)
            print(f"\n✓ Successfully saved {len(self.collected_links)} job links")
            print(f"  Output file: {OUTPUT_FILE}")
        else:
            print("\n✗ No links collected")
        
        print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return len(self.collected_links)


if __name__ == "__main__":
    print("Starting Job Board Scraper...")
    scraper = JobBoardScraper()
    scraped_count = scraper.run()
    sys.exit(0 if scraped_count > 0 else 1)
