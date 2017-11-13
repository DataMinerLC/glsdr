# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:05:25 2017

@author: LC
"""
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

def getDate(review):
    
    date='NA' # initialize critic and text 
    dateChunk=review.find('div',{'class':re.compile('floatLt')})
    if dateChunk: date=dateChunk.text#.encode('ascii','ignore')
        
    return date

def getPros(review):
    
    pros='NA' # initialize critic and text 
    prosChunk=review.find('p',{'class':re.compile(' pros mainText truncateThis wrapToggleStr')})
    if prosChunk: pros=prosChunk.text#.encode('ascii','ignore')
        
    return pros

def getCons(review):
    
    cons='NA' # initialize critic and text 
    consChunk=review.find('p',{'class':re.compile(' cons mainText truncateThis wrapToggleStr')})
    if consChunk: cons=consChunk.text#.encode('ascii','ignore')
        
    return cons


def glsdr(compy, indx, pg):
    
    dates=[]
    pross=[]
    conss=[]
    ratingss=[]

    for i in range(1, pg):
        url='https://www.glassdoor.com/Reviews/'+ compy +'-Reviews-'+ indx+'_P'+str(i)+'.htm?sort.sortType=RD&sort.ascending=false'
        response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        html=response.content # get the html
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        #'lxml' tells what type of data. 'ascii': ignore non_ascii characters (eg, Chinese, Japanese)
        reviews=soup.findAll('div', {'class': 'hreview'})
        ratings=soup.findAll('span', {'class': 'value-title'})

        for review in reviews:
            dates.append(getDate(review)),
            pross.append(getPros(review)),
            conss.append(getCons(review))
    
        for rating in ratings:
            ratingss.append(rating.get('title'))

        review_list = pd.DataFrame(
            {'Date': dates,
             'Pros': pross,
             'Cons': conss,
             'Rating': ratingss[1:]})
    
        review_list.to_csv(compy +'.csv', index=False)
        
if __name__=='__main__':
    glsdr('Prudential', 'E2944', 3)        
