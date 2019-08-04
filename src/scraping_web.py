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
        # Get start url
        response = req.get(_url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # concat results
        job_list.extend([job.text.strip() for job in soup.select('.jobtitle')])
        #prepare next link
        last_page_url = soup.select('.pagination a')[-1]['href']
        last_page = int(last_page_url.split('=')[-1])
        if( last_page > current_page):
            next_url = f'{base_link}{last_page_url}'
            next_page_search(next_url)

    # Executing logic for first time is diferent from next calls
    response = req.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    job_list.extend([job.text.strip() for job in soup.select('.jobtitle')])
    last_page_url = soup.select('.pagination a')[-1]['href']
    last_page_url = f'{base_link}{last_page_url}'

    #next_page_search(last_page_url)
    return job_list


if __name__ == "__main__":
    get_all_job_titles()