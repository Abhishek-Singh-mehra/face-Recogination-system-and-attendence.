from sklearn.neighbors import KNeighborsClassifier


import cv2 
import pickle 
import numpy as np 
import os 
import csv
import time 
from datetime import datetime 
from win32com.client import Dispatch

def main(): 
    '''code to speak attendance taken.''' 
   
    def speak(str1):
        speak=Dispatch(("SAPI.spVoice"))
        speak.speak(str1)



    face_cap = cv2.CascadeClassifier('C:/Users/12345/AppData/Roaming/Python/Python313/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    video_cap = cv2.VideoCapture(0) 


    with open('projects/names.pkl' ,"rb")as f: 
           LABELS =pickle.load(f)

    with open('projects/faces_data.pkl' ,"rb")as f: 
          FACES =pickle.load(f)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES , LABELS)
    
    COL_NAMES = ['NAMES' , 'TIME']

    while True:
        ret , frame = video_cap.read()
        color = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        faces = face_cap.detectMultiScale(
            color,
            scaleFactor=1.1,
            minNeighbors= 5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        ) 
        ''' now to create the bex .'''
        for(x,y,w,h)in faces: 
           crop_image =  frame[y:y+h , x:x+w , :] 
           resize_image = cv2.resize(crop_image,(50 ,50)).flatten().reshape(1,-1) 
           output =knn.predict(resize_image) 
           ts =time.time() 
           date =datetime.fromtimestamp(ts).strftime("%d-%m-%y")
           timestmp= datetime.fromtimestamp(ts).strftime("%H-%M-%S") 
           exist =os.path.isfile("projects/attendence_"+date+".csv")
           cv2.putText(frame ,str(output[0]), (x,y-15) ,cv2.FONT_HERSHEY_COMPLEX , .8, (255 ,255 ,255) ,1)
           
           cv2.rectangle(frame , (x,y) , (x+w ,y+h) , (0,255,0),2)
           attendance =[str(output[0] ), str(timestmp)] 
        '''output frame.'''
        cv2.imshow("video_live", frame) 
        if(cv2.waitKey(1)== ord("p")):
            speak("attendance taken.")
            time.sleep(3)
            ''' if exist:
                 with open("attendence/attendence_"+date+".csv" , "+a" ,newline='')as csvfile:     
                     writer = csv.writer(csvfile)
                     writer.writerow(attendance)
                 csvfile.close()  
            else:
                 with open("attendence/attendence_"+date+".csv", "+a")as csvfile:     
                     writer = csv.writer(csvfile)
                     writer.writerow(COL_NAMES)
                     writer.writerow(attendance)'''
            if not os.path.exists("attendence"):
                os.makedirs("attendence")

            with open(f"projects/attendance_{date}.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not exist:
                    writer.writerow(COL_NAMES)
                writer.writerow(attendance)
                csvfile.close()
        
        if cv2.waitKey(1) == ord('a'):
         break
    video_cap.release()  
    








main()