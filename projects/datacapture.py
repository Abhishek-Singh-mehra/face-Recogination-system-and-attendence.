import cv2 
import pickle 
import numpy as np 
import os
def main():
    face_cap = cv2.CascadeClassifier('C:/Users/12345/AppData/Roaming/Python/Python313/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    video_cap = cv2.VideoCapture(0) 


    faces_data = []
    i=0
    name = input("enter your name:")


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
           resize_image = cv2.resize(crop_image,(50 ,50))  
           if len(faces_data)<100 and i%10==0:
            faces_data.append(resize_image)
           cv2.rectangle(frame , (x,y) , (x+w ,y+h) , (0,255,0),2)
           cv2.putText(frame , str(len(faces_data)) , (50,50) , cv2.FONT_HERSHEY_COMPLEX , 1 ,(50, 50 ,255),1)
           i+=1
        '''output frame.'''
        cv2.imshow("video_live", frame)
        if cv2.waitKey(1) == ord('a') or len(faces_data)==100:
         break
    video_cap.release()  
    

    faces_data = np.asarray(faces_data)
    faces_data = faces_data.reshape(100 ,-1)
    '''now we have converted into the numpy array''' 
    '''now wee will store the names'''
    if'names.pickle'not in os.listdir('projects/'): 
        names = [name]*100
        with open('projects/names.pkl'  ,"wb")as f: 
          pickle.dump(names ,f)
    else:
        with open('projects/names.pkl' ,"rb")as f: 
           names =pickle.load(f)
        names = names + [name]*100
        with open('projects/names.pkl' ,"wb")as f: 
          pickle.dump(names ,f)



    '''now for the faces  '''
    if'faces_data.pickle'not in os.listdir('projects/'): 
        with open('projects/faces_data.pkl' ,"wb")as f: 
          pickle.dump(faces_data ,f)
    else:
        with open('projects/faces_data.pkl' ,"rb")as f: 
          face_data_load =pickle.load(f)
          face_data_load = np.concatenate(face_data_load , faces_data , axis =0)
        with open('projects/faces_data.pkl' ,"wb")as f: 
          pickle.dump(face_data_load ,f)








main()