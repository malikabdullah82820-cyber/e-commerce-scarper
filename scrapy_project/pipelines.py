"""
Scrapy pipelines for job data processing
"""
import re
from datetime import datetime
from logging import getLogger
from scrapy.exceptions import DropItem


logger = getLogger(__name__)


class DuplicateRemovalPipeline:
    """Remove duplicate job entries based on URL"""
    
    def __init__(self):
        self.ids_seen = set()
    
    def process_item(self, item, spider):
        job_url = item.get('job_url', '').strip()
        
        if not job_url:
            raise DropItem(f"Job with no URL dropped")
        
        if job_url in self.ids_seen:
            raise DropItem(f"Duplicate job found: {job_url[:50]}")
        
        self.ids_seen.add(job_url)
        return item


class JobPipeline:
    """Main pipeline for cleaning and processing job data"""
    
    def process_item(self, item, spider):
        """Process and clean job item"""
        
        # Clean job title
        if 'job_title' in item:
            item['job_title'] = self.clean_text(item['job_title'])
            if not item['job_title']:
                raise DropItem("Job with no title dropped")
        
        # Clean company name
        if 'company' in item and item['company']:
            item['company'] = self.clean_text(item['company'])
        
        # Clean location
        if 'location' in item and item['location']:
            item['location'] = self.clean_text(item['location'])
        
        # Clean department
        if 'department' in item and item['department']:
            item['department'] = self.clean_text(item['department'])
        
        # Normalize employment type
        if 'employment_type' in item and item['employment_type']:
            item['employment_type'] = self.normalize_employment_type(item['employment_type'])
        
        # Clean and truncate description
        if 'job_description' in item and item['job_description']:
            item['job_description'] = self.clean_text(item['job_description'])
            if len(item['job_description']) > 5000:
                item['job_description'] = item['job_description'][:5000]
        
        # Process skills
        if 'required_skills' in item:
            if isinstance(item['required_skills'], list):
                item['required_skills'] = '; '.join(item['required_skills'])
            elif item['required_skills']:
                item['required_skills'] = self.clean_text(item['required_skills'])
        
        # Add metadata
        if 'scraped_date' not in item:
            item['scraped_date'] = datetime.now().isoformat()
        
        # Set default source if not provided
        if 'source' not in item:
            item['source'] = 'Unknown'
        
        return item
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to string if needed
        text = str(text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep important ones
        text = re.sub(r'[\t\n\r]', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def normalize_employment_type(emp_type):
        """Normalize employment type values"""
        emp_type = emp_type.lower().strip()
        
        if 'full' in emp_type:
            return 'Full-time'
        elif 'part' in emp_type:
            return 'Part-time'
        elif 'contract' in emp_type:
            return 'Contract'
        elif 'intern' in emp_type or 'intern' in emp_type:
            return 'Internship'
        elif 'temp' in emp_type:
            return 'Temporary'
        else:
            return emp_type.title()
