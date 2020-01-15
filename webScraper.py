from threading import Thread
from threading import Lock
from bs4 import BeautifulSoup
import requests
import urllib

class webScraper():

    def __init__(self,debug,numSites):
        self.debug=debug
        self.numSites=numSites
        self.lock=Lock()
    def getLinks(self):
        body=requests.get("https://www.google.com/search?q="+self.question)
        soup=BeautifulSoup(body.text,"lxml")
        linksList=[]
        for link in soup.find_all('a'):
            if "/url?q=" in link.get("href"):
                linksList.append(link.get("href")[7:].split("&")[0])
                if len(linksList)>self.numSites-1:
                    break
        return linksList

    def searchQuestion(self,question,answears):
        self.question=question
        self.answears=answears
        links = self.getLinks()
        threads = []
        for i in range(self.numSites):
            thread = openAndCount(links[i],self.question,self.answears,self.lock)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

class openAndCount (Thread):
    def __init__(self, link,question,answears,lock):
        Thread.__init__(self)
        self.link = link
        self.answears=answears
        self.question=question
        self.lock=lock
    def searchEntire(self,body):
        c0=body.upper().count(self.answears[0].upper())
        c1=body.upper().count(self.answears[1].upper())
        c2=body.upper().count(self.answears[2].upper())
        return c0,c1,c2
    def searchSplitted(self,body):
        c=[0,0,0]
        for i in range(3):
            c[i]=0
            for word in self.answears[i].split(" "):
                c[i]=c[i]+body.upper().count(word.upper())
        return c
    def run(self):
        body=requests.get(self.link).text
        c0,c1,c2=self.searchEntire(body)
        c00,c11,c22=self.searchSplitted(body)
        self.lock.acquire()
        try:
            print ("Cercando in: ", self.link)
            print(c0,c1,c2,"\n",c00,c11,c22,"\n-------------------------------------------------\n")
        finally:
            self.lock.release()
