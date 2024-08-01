from konlpy.tag import Okt
from newspaper import Article

import time
import json 
import threading

import boto3

import requests


sqs = boto3.client('sqs')

start = time.time()
# okt = Okt()

def check_url_exists(url):
    try:
        # URL에 HEAD 요청을 보냅니다.
        response = requests.head(url, allow_redirects=True, timeout=5)
        
        # 상태 코드가 200대면 URL이 존재한다고 판단합니다.
        if 200 <= response.status_code < 300:
            #print(f"URL {url} 존재합니다.")
            return True
        else:
            #print(f"URL {url} 존재하지 않습니다. 상태 코드: {response.status_code}")
            return False
    except requests.RequestException as e:
        #print(f"URL {url} 확인 중 오류 발생: {e}")
        return False
 
def get_news_pages(url, page_num):
    
    page_url = url + page_num
    
    a = Article(page_url, language='ko')
    a.download()
    a.parse()


    print(f"[Page] {page_num} : {a.title}")
    
    try:
        response = sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/637423653538/news-queue",
            MessageBody=json.dumps(page_url)
        )
    except Exception as e:
        print(f"Error sending message to SQS: {str(e)}")

        
    # tokens = okt.morphs(a.text)
    # token_count = len(tokens)


    # print('-'*50)
    # print(a.authors)
    # print('-'*50)
    # print(a.publish_date)    
    # print('-'*50)
    # print(a.text[1:50])    

threads = []
i = 0

while i < 100:
    # url = 'https://www.energy-news.co.kr/news/articleView.html?idxno='
    #t=threading.Thread(target=get_news_pages, args=(url,str(203727+i)))
    
    url = "https://wikidocs.net/"
    page_url = url + str(124143+i)
    
    if check_url_exists(page_url) == True:
        t=threading.Thread(target=get_news_pages, args=(url,str(124143+i)))

        t.start()
        threads.append(t)

        i += 1

for t in threads:
    t.join()

end = time.time()

print(f"수행시간: {end - start} 초")

