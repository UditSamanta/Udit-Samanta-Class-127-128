from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("D:\Class 127\chromedriver_win32\chromedriver")
browser.get(start_url)
time.sleep(10)
headers = ['name', 'light_years_from_earth', 'planet_mass', 'stellar_magnitude', 'discovery_date', 'hyperlink', 'planet_type', 'planet_radius', 'orbital_radius', 'orbital_period', 'eccentricity']
planet_data = []

new_planet_data = []

def scrap():
    for i in range(0, 3):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            for ul_tag in soup.find_all('ul', attrs = {'class', 'exoplanet'}):
                li_tags = ul_tag.find_all('li')
                temp_list = []
                for index, li_tag in enumerate(li_tags):
                    if index == 0:
                        temp_list.append(li_tag.find_all('a')[0].contents[0])
                    else:
                        try:
                            temp_list.append(li_tag.contents[0])
                        except:
                            temp_list.append("")
                hyperlink_li_tag = li_tags[0]
                temp_list.append('https://exoplanets.nasa.gov' + hyperlink_li_tag.find_all('a', href = True)[0]['href'])
                planet_data.append(temp_list)
            browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            print('page' + i + 'done')
        
def scrap_more_data(hyperlink):
    try:
        page = request.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp_list = []
        for tr_tag in soup.find_all('tr', attrs = {'class' : 'fact_row'}):
            td_tags = tr_tag.find_all('td')
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tags.find_all('div', attrs = {'class' : 'value'})[0].contents[0])
                except:
                    temp_list.append('')
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

scrap()
for index, data in enumerate(planet_data):
    scrap_more_data(data[5])

final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace('\n', '') for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

 with open('scrapper.csv', 'w') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(headers)
            csvWriter.writerows(final_planet_data)
