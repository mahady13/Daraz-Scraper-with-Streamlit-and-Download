import streamlit as st
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

data={'Title':[],'Price':[],'Location':[],'Link':[],'ImageLink':[]}


def darazscrape(query, page):
    driver = uc.Chrome(headless=True)
    for i in range(1, page + 1):
        url = f'https://www.daraz.com.bd/catalog/?page={i}&q={query}&spm=a2a0e.tm80335411.search.d_go'
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('div', class_='Bm3ON')
        for item in items:
            try:
                title = item.find('div', class_='RfADt')
                p = item.find('span', class_='ooOxS')
                price = (p.text.split()[1])
                l = item.find('div', class_='_95X4G')
                li = l.find('a')
                link = li.get('href')
                img = item.find('div', class_='picture-wrapper jBwCF')
                imag = img.find('img')
                image = imag.get('src')
                loctn = item.find('span', class_='oa6ri')
                location = loctn.text

                data['Title'].append(title.text)
                data['Price'].append(price)
                data['Link'].append('https:' + link)
                data['ImageLink'].append(image)
                data['Location'].append(location)
            except Exception as e:
                continue
    return pd.DataFrame(data)
st.title('Daraz Web Scraper')
queryy=st.text_input('Enter what you want to search:')
pages=st.number_input('Enter how many pages you want to scrape:',step=1,value=1,min_value=1)

if st.button('Scrape'):
    with st.spinner('Please wait a little bit, our app is scraping...'):
        df=darazscrape(queryy,pages)
    if not df.empty:
        st.success('Scraping Completed!')
        st.dataframe(df)
        csv_data=df.to_csv(encoding='utf-8',index=False)
        st.download_button(data=csv_data,label='Download Scraped Data as CSV',file_name=f'Daraz_{queryy}.csv',mime='text/csv')
    else:
        st.error('Error,search results not available. Check the search query again.')