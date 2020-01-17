import cv2
import pytesseract
import os
from termcolor import colored
import colorama
from include.config import *
class image():
    """docstring for image."""

    def __init__(self,debug=0):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
          # Define config parameters.
          # '-l eng'  for using the English language
          # '--oem 1' for using LSTM OCR Engine
          # "--psm stays for page segmentation mode"
        self.config = config
        self.imgName = imgName
        self.imgFormat = imgFormat
        self.cellScreenPath = cellScreenPath
        self.cellScreenCmd = cellScreenCmd
        self.cellPullCmd =  cellPullCmd
        self.pcScreenPath = os.getcwd()+"\\test_images"
        self.debug=debug
        f = open(os.getcwd()+"\\include\\stopwords.txt",'r')
        self.stopwords = f.read().splitlines()
        f.close()
        f=open(os.getcwd()+"\\include\\stopchars.txt","r")
        self.stopchars=f.read().splitlines()
        f.close
        self.err=0
        colorama.init()
    def loadFromCell(self):
        err1 = os.system('cmd /c'+self.cellScreenCmd+self.cellScreenPath+str(self.imgName)+self.imgFormat)
        err2 = os.system('cmd /c'+self.cellPullCmd+self.cellScreenPath+str(self.imgName)+self.imgFormat+" "+self.pcScreenPath)
        if err1 or err2 !=0:
            print("Collega il cell")
            exit(1)
        self.img = cv2.imread(self.pcScreenPath+"\\"+str(self.imgName)+self.imgFormat,cv2.IMREAD_GRAYSCALE)
        if self.img is None:
            print ("Image is None")
            exit(2)

    def loadFromFile(self):
        fileName=str(input("Enter name of file: "))
        self.img = cv2.imread(self.pcScreenPath+"\\"+fileName,cv2.IMREAD_GRAYSCALE)
        if self.img is None:
            print ("Image is None")
            exit(2)

    def cutImg(self):
        S8Quest=[300,550,0,800]
        PcQuest=[300,550,0,1100] #[y1,y2,x1,x2]
        S8Ans=[550,1100,0,800]
        PcAns=[550,1100,0,1100]
        if self.debug==1 or self.debug==2:
            print("CURRENTLY on PC")
            currentQuest=PcQuest
            currentAns=PcAns
        else:
            currentQuest=S8Quest
            currentAns=S8Ans
        if self.debug==1 or self.debug==3:
            cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image',180,370)
            cv2.imshow('Image', self.img)
            cv2.waitKey(0)
        self.imgQuest = self.img[currentQuest[0]:currentQuest[1], currentQuest[2]:currentQuest[3]]
        self.imgQuest = cv2.threshold(self.imgQuest, 200, 255, cv2.THRESH_BINARY_INV)[1]
        if self.debug==1 or self.debug==3:
            cv2.namedWindow('Crop',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Crop',(currentQuest[3]-currentQuest[2]),(currentQuest[1]-currentQuest[0]))
            cv2.imshow('Crop', self.imgQuest)
            cv2.waitKey(0)
        self.imgAns = self.img[currentAns[0]:currentAns[1], currentAns[2]:currentAns[3]]
        self.imgAns = cv2.threshold(self.imgAns, 10, 255, cv2.THRESH_BINARY)[1]
        if self.debug==1 or self.debug==3:
            cv2.resizeWindow('Crop',(currentAns[3]-currentAns[2]),(currentAns[1]-currentAns[0]))
            cv2.imshow('Crop', self.imgAns)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def img2str(self,img):
        text = pytesseract.image_to_string(img, config=self.config)
        return text.replace("¢","è")
    def purgeQueries(self):
        for char in self.question:
            if char in self.stopchars:
                self.question=self.question.replace(char,'')
        querywords = self.question.split()
        resultwords  = [word for word in querywords if word.lower() not in self.stopwords]
        self.question = ' '.join(resultwords)

    def newQuest(self):
        if self.debug==1 or self.debug==2:
            self.loadFromFile()
            print()
        elif self.debug==3 or self.debug==0:
            self.loadFromCell()
        self.cutImg()
        self.question=self.img2str(self.imgQuest)
        self.answearsRaw=self.img2str(self.imgAns)
        print(colored(self.question,'yellow'))
        print(colored(self.answearsRaw,'yellow'))
        array = self.answearsRaw.split('\n')
        if self.debug==1 or self.debug==3:
            print("OCR returned:")
            print (self.question,"\n",array)
        for item in array:
            if len(item)==0:
                array.remove(item)
        for item in array:
            if item.isspace():
                array.remove(item)
        self.answears = []
        if len(array)==3:
            self.answears = array[-3:]
            self.err=0
        else:
            print("OCR HA FALLITO")
            self.err=1
            return self.question, self.answears, self.err
        if self.debug==1 or self.debug==3:
            print("question and asnwears are:")
            print (self.question)
            print (self.answears)
        self.imgName = self.imgName+1
        self.purgeQueries()
        if self.debug==1 or self.debug==3:
            print("PURGED question and asnwears are:")
            print(self.question)
            print(self.answears)
        return self.question,self.answears,self.err
