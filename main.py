import pymongo
from lib import lib
import time

def main():

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = client['otzovik_reviews']
    collection = mydb['reviews']
    for i in range(1,21):
        url = 'https://otzovik.com/lastreviews/' + str(i) + '/'
        content = lib.getContent(url)
        if content != False:
            reviews  = lib.getReviews(content)
            for review in reviews:
                q = {'review_url': review['review_url']}
                doc = collection.find_one(q)
                if type(doc) != dict:
                    collection.insert_one(review)
                else:
                    print(review['review_url'] + ' already has in db')



if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))