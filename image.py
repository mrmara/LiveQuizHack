import cv2
import pytesseract
import os

class image():
    """docstring for image."""

    def __init__(self,debug=0):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\a.marangi\AppData\Local\Tesseract-OCR\tesseract.exe'
          # Define config parameters.
          # '-l eng'  for using the English language
          # '--oem 1' for using LSTM OCR Engine
          # "--psm stays for page segmentation mode"
        self.config = ('-l ita --oem 1 --psm 3')
        self.imgName = 1
        self.imgFormat = ".png"
        self.cellScreenPath = "/storage/emulated/0/liveq/"
        self.cellScreenCmd = "adb shell screencap -p "
        self.cellPullCmd =  "adb pull "
        self.pcScreenPath = r"C:\Users\a.marangi\Desktop\LVH\test_images"
        self.debug=debug
        f = open("stopwords.txt",'r')
        self.stopwords = f.read().splitlines()
        f.close()
        f=open("stopchars.txt","r")
        self.stopchars=f.read().splitlines()
        print (self.stopchars)
        f.close

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
        S8=[300,1300,0,800]
        Pc1=[400,1300,0,1100] #[y1,y2,x1,x2]
        current=Pc1
        self.img = self.img[current[0]:current[1], current[2]:current[3]]
        if self.debug==1:
            cv2.namedWindow('Image',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image', 600,600)
            cv2.imshow('Image', self.img)
            cv2.waitKey(0)

    def img2str(self):
        self.text = pytesseract.image_to_string(self.img, config=self.config)
    def purgeQueries(self):
        querywords = self.question.split()
        resultwords  = [word for word in querywords if word.lower() not in self.stopwords]
        self.question = ' '.join(resultwords)
        for char in self.question:
            if char in self.stopchars:
                self.question=self.question.strip(char)
        for answear in self.answears:
            querywords = answear.split()
            resultwords  = [word for word in querywords if word.lower() not in self.stopwords]
            answear = ' '.join(resultwords)

    def newQuest(self):
        if self.debug>=1:
            self.loadFromFile()
            print()
        else:
            self.loadFromCell()
        self.cutImg()
        self.img2str()
        print(self.text)
        array = self.text.split('\n')
        if self.debug==1:
            print("OCR returned:")
            print (array)
        for item in array:
            if len(item)==0:
                array.remove(item)
        for item in array:
            if item.isspace():
                array.remove(item)
        self.question = ''
        self.answears = []
        self.answears = array[-3:]
        for item in array[0:-3]:
            self.question=self.question+' '+item
        if self.debug==1:
            print (self.question)
            print (self.answears)
        self.imgName = self.imgName+1
        self.purgeQueries()
        if self.debug==1:
            print(self.question)
            print(self.answears)
        return self.question,self.answears
