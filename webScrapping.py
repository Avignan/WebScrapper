import pandas as pd
import requests
from fake_useragent import UserAgent
import re
from bs4 import BeautifulSoup

ua = UserAgent()  # Use it only if request error occurs
url_to_hit = "https://www.zomato.com/kolkata/subway-sector-5-salt-lake/reviews"   # Some how this site is getting Connection Error
headers = {'User-Agent': str(ua.chrome)}


def scrap_data():
    print("Scrapping started...")
    while True:
        try:
            # Used another url to hit
            response = requests.get(url="https://www.yelp.com/biz/original-joes-san-francisco-3")
            site_html = BeautifulSoup(response.content, 'html.parser')
            consumer_name = []
            reviews_given = []

            # Gathering all the necessary data

            name_parent_tags = site_html.find_all('span', {'class': 'fs-block css-ux5mu6'})
            for parent_tag in name_parent_tags:
                child_tags = parent_tag.find_all("a", {'class': 'css-1m051bw'})
                for child_tag in child_tags:
                    consumer_name.append(child_tag.text)
            review_parent_tags = site_html.find_all('p', {'class': 'comment__09f24__gu0rG css-qgunke'})
            for parent_tag in review_parent_tags:
                child_tags = parent_tag.find_all("span", {'class': 'raw__09f24__T4Ezm'})
                for child_tag in child_tags:
                    reviews_given.append(child_tag.text)

            # Creating a DatSet with the data collected/scrapped
            print("Creating Data Set...")
            data_dict = {'Names': consumer_name, 'Reviews': reviews_given}
            dataframe = pd.DataFrame(data_dict)
            excel_name = 'Review_Data.xlsx'
            dataframe.to_excel(excel_name, index=False)
            print("Data Set Created!")
            return excel_name, dataframe
        except requests.exceptions.ConnectionError:
            print("Site unreachable")


def data_clean(ex_name, df):
    # This function simply cleans the data of any unnecessary character present in the raw data
    special_ch = r"[*|#|;|<|>|:]"
    review_lis = []
    for index, row in df['Reviews'].iteritems():
        if len(re.findall(special_ch, row)) > 0:
            for ch in re.findall(special_ch, row):
                row = row.replace(ch, "")
        review_lis.append(row)

    df['Reviews'] = review_lis
    df.to_excel(ex_name, index=False)


if __name__ == "__main__":
    name, data = scrap_data()
    data_clean(name, data)