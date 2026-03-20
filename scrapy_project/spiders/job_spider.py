"""
Main Scrapy spider for extracting job details
"""
import scrapy
import csv
import os
from datetime import datetime
from pathlib import Path
from scrapy_project.items import JobItem


class JobSpider(scrapy.Spider):
    """Spider for crawling job listings and extracting structured data"""
    
    name = 'jobs'
    allowed_domains = []
    start_urls = []
    
    def __init__(self, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self.job_urls = []
        self.load_job_urls()
    
    def load_job_urls(self):
        """Load job URLs from the CSV file created by Selenium"""
        csv_file = os.path.join(os.path.dirname(__file__), '../../data/raw/job_links.csv')
        
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('job_url'):
                        self.job_urls.append(row['job_url'])
                        self.allowed_domains.append(self.get_domain(row['job_url']))
        
        # Remove duplicates
        self.allowed_domains = list(set(self.allowed_domains))
        
        # Set start URLs
        self.start_urls = self.job_urls[:50]  # Limit for demo
        
        self.logger.info(f'Loaded {len(self.job_urls)} job URLs from {csv_file}')
    
    @staticmethod
    def get_domain(url):
        """Extract domain from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    
    def parse(self, response):
        """Parse job listing page and extract data"""
        
        item = JobItem()
        
        try:
            # Extract job title - try multiple selectors
            title = self.extract_with_multiple_selectors(
                response,
                ['h1', 'h1.job-title', '.job-title h1', '[data-test="jobTitle"]', '.title']
            )
            item['job_title'] = title
            
            # Extract company name
            company = self.extract_with_multiple_selectors(
                response,
                ['company', '.company-name', '[data-company]', '.employer', '.organization']
            )
            item['company'] = company
            
            # Extract location
            location = self.extract_with_multiple_selectors(
                response,
                ['.location', '[data-location]', '.job-location', '.region']
            )
            item['location'] = location
            
            # Extract employment type
            emp_type = self.extract_with_multiple_selectors(
                response,
                ['.employment-type', '[data-employment-type]', '.job-type']
            )
            item['employment_type'] = emp_type
            
            # Extract posted date
            posted_date = self.extract_with_multiple_selectors(
                response,
                ['.posted-date', '[data-posted]', '.publish-date', 'time::attr(datetime)']
            )
            item['posted_date'] = posted_date
            
            # Extract job description - combined from multiple sections
            description = self.extract_description(response)
            item['job_description'] = description
            
            # Extract required skills
            skills = self.extract_skills(response)
            item['required_skills'] = skills
            
            # Extract experience level
            exp_level = self.extract_with_multiple_selectors(
                response,
                ['.experience-level', '[data-level]', '.seniority']
            )
            item['experience_level'] = exp_level
            
            # Extract salary if available
            salary = self.extract_with_multiple_selectors(
                response,
                ['.salary', '[data-salary]', '.compensation']
            )
            item['salary'] = salary
            
            # Set the job URL and metadata
            item['job_url'] = response.url
            item['scraped_date'] = datetime.now().isoformat()
            item['source'] = self.get_domain(response.url)
            
            # Generate internal ID
            item['internal_id'] = self.generate_id(response.url)
            
            # Add department if found
            item['department'] = self.extract_with_multiple_selectors(
                response,
                ['.department', '[data-department]', '.team']
            )
            
            return item
        
        except Exception as e:
            self.logger.error(f'Error parsing {response.url}: {e}')
            return None
    
    @staticmethod
    def extract_with_multiple_selectors(response, selectors):
        """Try multiple selectors to extract text"""
        for selector in selectors:
            try:
                if '::attr' in selector:
                    # Handle attribute extraction
                    parts = selector.split('::attr(')
                    css = parts[0]
                    attr = parts[1].rstrip(')')
                    text = response.css(f'{css}::attr({attr})').get('').strip()
                else:
                    text = response.css(f'{selector}::text').get('').strip()
                
                if text:
                    return text
            except:
                continue
        
        return ''
    
    @staticmethod
    def extract_description(response):
        """Extract complete job description"""
        # Try multiple common description containers
        description_selectors = [
            '.job-description',
            '[data-description]',
            '.description',
            '.job-content',
            'main',
            '.details'
        ]
        
        for selector in description_selectors:
            text = ' '.join(response.css(f'{selector}::text').getall())
            if text:
                return ' '.join(text.split())[:3000]  # Limit to 3000 chars
        
        return ''
    
    @staticmethod
    def extract_skills(response):
        """Extract required skills from the job posting"""
        skills = []
        
        # Try to find skills list
        skill_selectors = [
            '.skills li',
            '[data-skills] li',
            '.required-skills li',
            '.qualifications li'
        ]
        
        for selector in skill_selectors:
            skill_elements = response.css(selector)
            if skill_elements:
                for elem in skill_elements:
                    skill = ' '.join(elem.css('::text').getall()).strip()
                    if skill:
                        skills.append(skill)
        
        # If no structured skills found, try to extract from description
        if not skills:
            description = response.css('.job-description, [data-description], .description').get('')
            # Look for common technical terms (simplified)
            tech_keywords = ['Python', 'JavaScript', 'Java', 'C++', 'AWS', 'Docker', 'SQL', 'React', 'Node.js']
            for keyword in tech_keywords:
                if keyword.lower() in description.lower():
                    skills.append(keyword)
        
        return '; '.join(list(set(skills))) if skills else ''
    
    @staticmethod
    def generate_id(url):
        """Generate an internal ID from URL"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()[:12]
