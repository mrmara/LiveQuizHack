import sys
import cv2
from image import image
from webScraper import webScraper
if __name__ == '__main__':
    debug=1
    key=0
    numSites=5
    my_image=image(debug)
    help=webScraper(debug,numSites)
    while key!=2:
        question,answears = my_image.newQuest()
        help.searchQuestion(question,answears)
        key=0
        while not (key==1 or key==2):
            print("Attendo comandi: ")
            key=int(input())
