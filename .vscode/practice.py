# a=35
# print("%f"%a)

# def fun():
#     print('fun')
#     print(fun())
 
# a=2*2//2
# b=3//2*3
# print(a,b)

# a=3//2
# print(a)

# a,b,c="123"
# b,c,d="456"
# print( a,b,c,d)


from keras.models import load_model
from time import sleep
from keras.utils.image_utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + r'haarcascade_frontalface_default.xml')
classifier =load_model(r"C:\Users\veathavalli\Downloads\model.h5")

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,1.3,5)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
    
        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

         #make a prediction on the roi,then look the classes
            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)


        # Display the resulting frame
        cv2.imshow('Emotion detector', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

           # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()



    