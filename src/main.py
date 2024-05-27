import os
import csv
import json
import time
from dotenv import load_dotenv
from serpapi import GoogleSearch
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
api_key = os.getenv('SERP_KEY')

def search_job_listings(job_id, max_retries=1, retry_delay=1):
    retries = 0
    while retries < max_retries:
        params = {
            "engine": "google_jobs_listing",
            "api_key": api_key,
            "q": job_id
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        apply_options = results.get('apply_options', [])
        
        if apply_options:
            return [{'link': convert_indeed_link(option['link']), 'text': option['title']} for option in apply_options[:1]]
        
        retries += 1
        time.sleep(retry_delay)
    
    return []

def clean_text(text):
    return text.replace('\n', ' ').strip()

def convert_indeed_link(link):
    if 'indeed.com/viewjob' in link:
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)
        job_key = query_params.get('jk', [''])[0]
        if job_key:
            listing_link = f'https://www.indeed.com/viewjob?jk={job_key}'
            return listing_link
    return link

def search_and_save_jobs(queries, filepath, num_listings=1):
    # Determine if the file already exists to decide on writing headers
    file_exists = os.path.exists(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Only write headers if the file does not exist
        if not file_exists:
            writer.writerow(['Title', 'Company', 'Location', 'Via', 'Related Links', 'Extensions'])

        for query in queries:
            params = {
                'api_key': api_key,
                'engine': 'google_jobs',
                'q': query,
                'location': 'Kalamazoo, Michigan, United States',
                'hl': 'en',
                'gl': 'us',
                'start': 0,
                'num': 1
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            if 'error' in results:
                print(f"Error for query '{query}': {results['error']}")
            else:
                google_jobs_results = results.get('jobs_results', [])
                job_ids = [job['job_id'] for job in google_jobs_results[:1]]

                with ThreadPoolExecutor() as executor:
                    futures = [executor.submit(search_job_listings, job_id) for job_id in job_ids]
                    apply_links = {job_id: future.result()[:num_listings] for job_id, future in zip(job_ids, as_completed(futures))}

                for job in google_jobs_results[:1]:
                    job_id = job['job_id']
                    related_links = apply_links.get(job_id, [])
                    
                    if related_links:
                        title = job.get('title', '')
                        company_name = job.get('company_name', '')
                        location = job.get('location', '')
                        via = job.get('via', '')
                        related_links_json = json.dumps(related_links)
                        extensions = ', '.join(job.get('extensions', []))
                        writer.writerow([title, company_name, location, via, related_links_json, extensions])

    print(f"Results appended to {filepath}")


# Example usage
jobs = ["Administrative Assistant","Sales Associate","Customer Service Representative","Nurse","Accountant","Teacher","Software Developer","Marketing Manager","Cashier","Project Manager","Executive Assistant","Analyst","Human Resources Manager","Graphic Designer","Mechanical Engineer","Data Analyst","Financial Analyst","Office Manager","Electrician","Product Manager","Operations Manager","IT Technician","Receptionist","Physical Therapist","Paralegal","Pharmacist","Security Officer","Bank Teller","Construction Worker","Chef","Bartender","Server","Delivery Driver","Taxi Driver","Retail Manager","Event Planner","Cleaner","Web Developer","Content Writer","Editor","Pharmacist","Consultant","Quality Assurance Specialist","Real Estate Agent","Social Media Manager","Business Analyst","Dental Assistant","Dentist","Pediatrician","Surgeon","Biologist","Chemist","Veterinarian","Civil Engineer","Electrical Engineer","Software Engineer","Systems Administrator","Network Engineer","Lawyer","Judge","Police Officer","Firefighter","Librarian","Archivist","Curator","Artist","Actor","Musician","Interior Designer","Fashion Designer","Pilot","Flight Attendant","Travel Agent","Fitness Trainer","Nutritionist","Psychologist","Counselor","Social Worker","Pastor","Photographer","Videographer","Filmmaker","Producer","News Reporter","Journalist","Public Relations Specialist","Advertising Manager","Copywriter","SEO Specialist","Data Scientist","AI Developer","Robotics Engineer","Economist","Statistician","Mathematician","School Principal","Academic Advisor","Tutor","Librarian","Childcare Worker"]

queries = [jobs[i] + " kalamazoo michigan" for i in range(len(jobs))]
filepath = 'outputs/single_link_run_1.csv'
search_and_save_jobs(queries, filepath, num_listings=1)