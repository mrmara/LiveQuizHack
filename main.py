import sys
import cv2
from include.image import image
from include.webScraper import webScraper
from sys import argv
from include.webScraper import browserOpener
if __name__ == '__main__':
    debug=int(argv[1])
    key=0
    if len(argv)>2:
        numSites=int(argv[2])
    else:
        numSites=7
    my_image=image(debug) #debug 1=tutte info su pc 2 poche info su pc 3=tutte info su cell
    help=webScraper(debug,numSites)
    while key!=2:
        iter=0
        while iter<=4:
            iter+=1
            question,answears,err = my_image.newQuest()
            if not err:
                browser=browserOpener("https://www.google.com/search?q="+question)
                browser.setDaemon(True)
                browser.start()
                help.searchQuestion(question,answears)
                break

        key=0
        while not (key==1 or key==2):
            print("Attendo comandi: ")
            try:
                key=int(input())
            except:
                pass
