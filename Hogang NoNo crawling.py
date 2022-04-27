#!/usr/bin/env python
# coding: utf-8

# In[9]:


#호갱노노 사이트 아파트별 크롤링 
import urllib.request
import pandas as pd
import datetime
import re
from itertools import count
import time
from selenium import webdriver
from itertools import count


#아파트 크롤링 함수
def getApartment(url, result):
    
    
    #크롬 드라이버 연결
    wd = webdriver.Chrome('C:/chromedriver.exe')
    
    #URL로 아파트 리뷰 페이지 접속
    wd.get(url)
    wd.implicitly_wait(10)
    time.sleep(1)
    
    
    #회원 로그인
    
    #로그인 창 열기
    login = wd.find_element_by_css_selector('div.home-user-menu > a.btn-login') 
    login.click()
    time.sleep(1)
    
    #전화번호로 로그인
    tel_login = wd.find_element_by_css_selector('#react-root > div > div.dimmed-layer-container > div:nth-child(2) > div > div > div > div.css-1quwtqj > div.css-1pi75nk > span:nth-child(3)') #휴대전화로 로그인
    tel_login.click()
    time.sleep(1)
    
    #전화번호_비번 넣고 로그인
    wd.find_element_by_css_selector('div.css-70j7w6 > input.css-14q5jb5').send_keys('tel')
    wd.find_element_by_css_selector('div.css-1t8nnu8 > input.css-14q5jb5').send_keys('password')
    login_bt = wd.find_element_by_css_selector('div.css-1enkzm8 > form > a')
    login_bt.click() 
    time.sleep(1)
    
    wd.get(url) #사이트 재접속
    
    #총 리뷰수 추출
    review_num = wd.find_element_by_css_selector('div#base-header.css-9m7md2 > h2 > span') 
    review_num = re.sub(r'[^0-9]', '', review_num.text)
    review_num = int(review_num)
    
    for i in range(review_num):
        try: 
            #댓글 더보기가 있으면 클릭
            more = wd.find_element_by_xpath('//*[@id="container"]/div[4]/div[2]/div[2]/div/div[1]/div/div['+str(i+2)+']/div[1]/div[2]/a')
            more.click()
            
            #스크롤을 내리다 더보기가 있으면 클릭
            more2 = wd.find_element_by_xpath('//*[@id="container"]/div[4]/div[2]/div[2]/div/div[1]/a')
            more2.click()

        except:
            pass
        
        
        
        #리뷰 데이터 가져오기
        review = wd.find_element_by_xpath('//*[@id="container"]/div[4]/div[2]/div[2]/div/div[1]/div/div['+str(i+2)+']/div[1]/div[2]')
        #스크롤 내리기
        wd.execute_script("arguments[0].scrollIntoView(true);", review);
        
        #리뷰 데이터 저장하기
        result.append(review.text)
        
        print(str(i)+"번째 완료")

     


    

#사이트 url
url = ["https://hogangnono.com/apt/5dV10/0/8/review","https://hogangnono.com/apt/5eA98/0/3/review","https://hogangnono.com/apt/5dTd6/0/5/review"
    ,"https://hogangnono.com/apt/ayJdd/0/0/review","https://hogangnono.com/apt/b2L97/0/2/review","https://hogangnono.com/apt/b0fff/0/4/review"
    ,"https://hogangnono.com/apt/6di7b/0/8/review","https://hogangnono.com/apt/aYn67/0/4/review","https://hogangnono.com/apt/b2X24/0/11/review"]
apart = ["분당 한양", "분당 장미마을(현대)", "분당 우성"
         ,"동탄역 시범한화꿈에그린 프레스티지", "동탄2신도시 하우스디더레이크", "동탄 더샵 레이크에듀타운"
         ,"미사강변 골든센트로", "미사강변 센텀팰리스", "미사강변도시 8단지"]

crawling_num = 0

#크롤링함수 호출
for j in url:
    result = []
    print(apart[crawling_num]+'아파트 리뷰를 크롤링합니다.')
    
    #크롤링 함수 호출
    getApartment(url[crawling_num], result)

    # result를 pandas로 정리
    csv_table = pd.DataFrame(result, columns=(['리뷰']))
    
    # pandas를 csv 파일로 추출
    csv_table.to_csv(''+apart[crawling_num]+'.csv', encoding='utf-8-sig', mode='a',header=True, index=True)
    print(result)
    
    crawling_num+=1


# In[ ]:




