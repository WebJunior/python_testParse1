import requests
from bs4 import BeautifulSoup
import random


def getContent(url):
    proxies = [
        {'https': '91.208.39.70:8080'},
        {'https': '188.216.17.170:8118'},
        {'https': '80.240.25.119:1080'}
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    proxy = random.choice(proxies)
    print(proxy)
    r = requests.get(url, proxies = proxy, timeout = 5, headers = headers)
    if r.status_code == 200:
        return r.text
    else:
        print('can`t get content', url)
        return False

def getReviews(content):
    soup = BeautifulSoup(content, 'lxml')
    reviews = soup.find_all('div', class_ = 'item mshow0')
    last_reviews = []
    for review in reviews:
        try:
            card_title = review.find('a', class_ = 'product-name').text
        except:
            card_title = 'empty card_title'
        try:
            card_url = review.find('a', class_ = 'product-name')['href']
        except:
            card_url = 'empty card_url'
        try:
            review_url = review.find('a', class_ = 'review-btn review-read-link')['href']
        except:
            review_url = 'empty review_url'

        if review_url == 'empty review_url':
            break
        content_review = getContent(review_url)
        if content_review != False:
            soup = BeautifulSoup(content_review, 'lxml')
            try:
                author_nickname = soup.find('div', class_ = 'login-col').find('a', class_ = 'user-login').find('span', attrs = {'itemprop':'name'}).text
            except:
                author_nickname = 'empty author_nickname'
            try:
                author_url = 'https://otzovik.com' + soup.find('div', class_ = 'login-col').find('a', class_ = 'user-login')['href']
            except:
                author_url = 'empty author_url'
            try:
                review_title = soup.find('h1').text
            except:
                review_title = 'epmty revie_title'
            try:
                review_date = soup.find('span', class_ = 'dtreviewed').find('abbr').get('title')
            except:
                review_date = 'empty review_date'
            try:
                review_text_plus = soup.find('div','review-plus').text
            except:
                review_text_plus = 'empty review_text_plus'
            try:
                review_text_minus = soup.find('div','review-plus').text
            except:
                review_text_minus = 'empty review_text_minus'
            try:
                review_body = soup.find('div', class_ = 'review-body').text
            except:
                review_body = 'empty review_body'
            try:
                review_footer = soup.find('table', class_ = 'product-props').text
            except:
                review_footer = 'empty review_footer'
            review_text = review_text_plus + '<br />' + review_text_minus + '<br />' + review_body + '<br />' + review_footer
            # print(card_title, card_url,review_url , author_nickname , author_url, review_title, review_date,review_text)
            last_reviews.append({'card_title': card_title,
                             'card_url': card_url,
                             'review_url': review_url,
                             'author_nickname': author_nickname,
                             'author_url': author_url,
                             'review_title': review_title,
                             'review_date': review_date,
                             'review_text': review_text})
        print(review_url, 'got it!')


    return last_reviews