import sys
import cv2
from image import image
from webScraper import webScraper
from sys import argv
if __name__ == '__main__':
    debug=int(argv[1])
    key=0
    if len(argv)
    numSites=int(argv[2])
    my_image=image(debug)
    help=webScraper(debug,numSites)
    while key!=2:
        iter=0
        while iter<=4:
            iter+=1
            question,answears,err = my_image.newQuest()
            if not err:
                help.searchQuestion(question,answears)
                break

        key=0
        while not (key==1 or key==2):
            print("Attendo comandi: ")
            try:
                key=int(input())
            except:
                pass
