from threading import Thread
from threading import Lock
from threading import currentThread
from bs4 import BeautifulSoup
import requests
import urllib
from termcolor import colored
import colorama
from include.image import image
import webbrowser
import os
class webScraper():

    def __init__(self,debug,numSites):
        self.debug=debug
        self.numSites=numSites
        self.lockPrint=Lock()
        colorama.init()
    def getLinks(self):
        body=requests.get("https://www.google.com/search?q="+self.question)
        if self.debug==1 or self.debug==3:
            print ("Io ho cercato questo URL:\n","https://www.google.com/search?q="+self.question)
        soup=BeautifulSoup(body.text,"lxml")
        linksList=[]
        for link in soup.find_all('a'):
            if "/url?q=" in link.get("href"):
                linksList.append(link.get("href")[7:].split("&")[0].replace("%25","%"))
                if len(linksList)>self.numSites-1:
                    break
        if self.debug==1 or self.debug==3:
            print(linksList)
        return linksList

    def searchQuestion(self,question,answears):
        self.question=question
        self.answears=answears
        links = self.getLinks()
        threads = []
        for i in range(min(len(links),self.numSites)):
            name='numero'+str(i)
            thread = openAndCount(name,links[i],self.question,self.answears,self.lockPrint)
            thread.setDaemon(True)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join(10)

class openAndCount (Thread):
    def __init__(self,name,link,question,answears,lockPrint):
        Thread.__init__(self,name=name)
        self.link = link
        self.answears=answears
        self.question=question
        self.lockPrint=lockPrint
        f = open(os.getcwd()+"\\include\\stopwords.txt",'r')
        self.stopwords = f.read().splitlines()
        f.close()
        f = open(os.getcwd()+"\\include\\stopchars.txt",'r')
        self.stopchars = f.read().splitlines()
        f.close()
    def searchEntire(self,body):
        c0=body.upper().count(self.answears[0].upper())
        c1=body.upper().count(self.answears[1].upper())
        c2=body.upper().count(self.answears[2].upper())
        return c0,c1,c2
    def searchSplitted(self,body):
        c=[0,0,0]
        for i in range(3):
            c[i]=0
            for word in self.answears[i].replace("'",' ').split(" "):
                if word.lower() not in self.stopwords:
                    c[i]=c[i]+body.lower().count(word)
        return c
    def run(self):
        body=requests.get(self.link).text
        c0,c1,c2=self.searchEntire(body)
        c=self.searchSplitted(body)
        self.lockPrint.acquire()
        buff="Thread "+currentThread().getName()+" sta cercando in: "+self.link
        print (colored(buff,'red'))
        try:
            buff=str(c0)+"\t"+str(c1)+"\t"+str(c2)+"\n"+str(c[0])+"\t"+str(c[1])+"\t"+str(c[2])
            print(colored(buff,'white'))
        finally:
            self.lockPrint.release()
            buff="\n-------"+"Thread "+currentThread().getName()+" rilascia il lock"+"------------\n"
            print(colored(buff,'green'))
class browserOpener(Thread):
    def __init__(self,url):
        Thread.__init__(self)
        self.url=url
    def run(self):
        webbrowser.open(self.url)
