tesseract_cmd = r'C:\Users\a.marangi\AppData\Local\Tesseract-OCR\tesseract.exe' #inserire percorso a tesseract.exe
config = ('-l ita+eng --oem 2 --psm 1') #parametri di configurazione tesseract
imgName = 1 #starting number for screen naming
imgFormat = ".png" #formati degli screen
cellScreenPath = "/storage/emulated/0/liveq/" #percorso salbvataggio screen su telefono
cellScreenCmd = "adb shell screencap -p " #comando adb per catturare screen
cellPullCmd =  "adb pull " #comando adb per copiare screen da cell
