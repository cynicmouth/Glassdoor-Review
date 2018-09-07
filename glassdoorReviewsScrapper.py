#import necessary libraries
import time
import requests
from bs4 import  BeautifulSoup
import pandas as pd
#from urllib.request import urlopen
from userAgents import user_agents, randomUserAgents
import lxml

url = 'https://www.glassdoor.com/Reviews/Apple-Reviews-E1138.htm'
#store randomized user agent headers in head variable
head = randomUserAgents()
start = time.time()

#function which returns whole text content of a page in lxml format
def soup(url,headers):
    ''' scrape text content of page and return that lxml text content for every page iteration'''
    #instantiate session object
    session = requests.Session()
    #pass url and headers to get response
    req = session.get(url, headers=headers)
    #print('req variable: ', req)
    #parse text content response using .text and it is lxml formartting (for fastness). you can use html_parser
    # as you wish
    bs = BeautifulSoup(req.text, 'lxml')
    #print('bs variable: ', bs)
    return bs

#use this function in order to automate everything. However it is time taken process if you want to scrape
#all page reviews. For accenture, it is having 2000+ pages which may take around 6 hrs to complete
#this function gets all page links till the end of last page reviews for company
'''
pages = set()
def getPages(url, head):
        
    global pages
    bs = soup(url, head)
    nextPage = bs.find('div',{'class',"flex-grid tbl margTop"})
    print(nextPage)
    for link in nextPage.findAll('a'):
        if 'href' in link.attrs:
            url = 'https://glassdoor.com{}'.format(link.attrs['href'])
            if url not in pages:
            #new page
                pages.add(url)
    #get last page
    for lastPage in nextPage.findAll('li',{'class':'page last'}):
        lastPage = 'https://glassdoor.com{}'.format(lastPage.a['href'])
        getPages(lastPage, head)
    return pages
#soup(url, head)
#getPages(url, head)
'''
#startTime = start - time.time()
#intiate empty list variables
a=[]
date=[]
revNo=[]
employee=[]
position = []
summ=[]
pro=[]
con=[]
advice=[]
review = []
subReviews = []
workLife = []
culture = []
careerOpp = []
compBenefits = []
srManagement = []
# recommend=[]
# outlook=[]
# ceo=[]
link=[]

#pages = getPages(url, head)
pages = [url]
#hardcoded page links to 99 pages. Can be increased till last page if u know how many pages are there.
#more number of pages, more time taken
page_ranges = range(2,13000) #get reviews from 99 pages
#generating page links till 99 pages
for pageNumber in page_ranges:
    pages.append(url[:-4] + '_P' + str(pageNumber) + '.htm')
count = 1
for page in pages:
    #call the function and pass each page link and headers
    bs = soup(page,head)
    #employee reviews
    for x in bs.findAll('li',{'class',' empReview cf '}):

    # ## PK
        a.append(count)
        count += 1

    ## Rev Number
    #employee review number
        try:
            revNo.append(x.attrs['id'])
            # revNo.append(x.find('li',{'class':' empReview cf '}).attrs[' id'])
            # for emp in x.find(':
            #     print(emp.attrs[' id'])
        except:
            revNo.append('None')

        ## overall rating
    #rating given by user
        try:
            rating = x.find('span',{'class':'rating'})
            for y in rating:
                review.append(rating.find('span',{'class':'value-title'})\
                              .attrs['title'])
        except:
            review.append('None')

    ## subRatings list
    #sub rating like workculture, management etc., 5 sub ratings
        try:
            for rate in x.findAll('span',{'class':'gdBars gdRatings med '}):
                z = rate.attrs['title']
                subReviews.append(z)
        except:
            subReviews.append('None')

    ## Date
    #date review has been given
        try:
            date.append(x.find('time',{'class':'date subtle small'}).text)
        except:
            date.append('None')
    # Summary
    #summary title
        try:
            summar = x.a.text
            summar = summar.split('"')
            summ.append(summar[1])
        except:
            summ.append('None')
    ## Pros
    #pros of the company
        try:
            pro.append(x.find('p',{'class':' pros mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            pro.append('None')
    ## Cons
    #cons of the company
        try:
            con.append(x.find('p',{'class':' cons mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            con.append('None')
    ## Advice to Management

        try:
            advice.append(x.find('p',{'class':' adviceMgmt mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            advice.append('None')

    ## Employee Type
    #whether former employee or current employee
        try:
            employee.append(x.find('span',{'class':"authorJobTitle"}).text)
        except:
            employee.append('None')
    ## Position and Location
    #designation and location worked
        try:
            position.append(x.find('p',{'class':' tightBot mainText'}).text)
        except:
            position.append('None')
    ## Review Link
    #each employee review link
        link.append(url+(x.find('a',{'class':'reviewLink'}).attrs['href']))

    for x in range(len(subReviews)):
        if x==0 or x%5==0:
            workLife.append(subReviews[x])
        if x==1 or x%5==1:
            culture.append(subReviews[x])
        if x==2 or x%5==2:
            careerOpp.append(subReviews[x])
        if x==3 or x%5==3:
            compBenefits.append(subReviews[x])
        if x==4 or x%5==4:
            srManagement.append(subReviews[x])

#store all list information into dataframe and convert into csv file
df=pd.DataFrame(index=a)
df['date']=date
df['reviewNo']=revNo
df['employeeType']=employee
df['position']=position
df['summary']=summ
df['pro']=pro
df['con']=con
df['advice']=advice
df['overallStar']=review
#df['workLifeStar']=workLife
#df['cultureStar']=culture
#df['careerOppStar']=careerOpp
#df['comBenefitsStar']=compBenefits
#df['srManagementStar']=srManagement
df['reviewLink']=link

csvName = 'apple_review'
df.to_csv('{}.csv'.format(csvName), sep=',')
print('StartTime = {}\nEnd Time = {}'.format(start, time.time() - start))

