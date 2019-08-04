""" In this file we scrap a web page for job open positions in CRC"""

import requests as req
import bs4

from common import params

base_link = params.config()['web_sites']['indeed']['base_link']
url = params.config()['web_sites']['indeed']['url_tosearch']
user_agent = params.config()['web_sites']['indeed']['user_agent']

headers = {
    'User-Agent': user_agent,
}


def get_all_job_titles():
    """ Will go over the page getting all job titles"""
    # job list
    job_list = []

    def next_page_search(_url):
        # get the url number page
        current_page = int(_url.split('=')[-1])        
        last_page_url = visitingNextPage(job_list, _url)
        last_page = int(last_page_url.split('=')[-1])
        # if next page is less than currect page
        if( last_page > current_page):
            next_url = f'{base_link}{last_page_url}'
            next_page_search(next_url)

    # Executing logic for first time is diferent from next calls
    last_page_url = visitingNextPage(job_list, url)
    last_page_url = f'{base_link}{last_page_url}'

    #next_page_search(last_page_url)
    return job_list


def visitingNextPage(ls, _url):
    """ Visit the url and return next url page """
    response = req.get(_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    ls.extend([{
        'title': job.select('.title')[0].select('.jobtitle')[0].text.strip(), 
        'link':'{}{}'.format(base_link, job.select('.title')[0].select('.jobtitle')[0]['href']) ,
        'date': job.select('.jobsearch-SerpJobCard-footer')[0].select('.date')[0].text,
        } for job in soup.select('.jobsearch-SerpJobCard')])
    return soup.select('.pagination a')[-1]['href']

def visitingJobs():
    """ resultado final, un diccionario con el job title, company y descripcion """
    ls = []
    for job in get_all_job_titles():
        response = req.get(job['link'])
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # Company & location selector
        company = soup.select('.jobsearch-InlineCompanyRating')[0].text
        description = soup.select('#jobDescriptionText')[0].text
        ls.append({**job, 'company': company, 'description':description})

    return ls

if __name__ == "__main__":
    print(visitingJobs()[0])