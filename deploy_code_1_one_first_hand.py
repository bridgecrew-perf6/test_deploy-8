# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:19:18 2021

@author: asabater
"""


import numpy as np

from skel_aug import skele_augmentation
import pickle

np.random.seed(0)

# for this file ,get the skeleton of kaggle dataset and try test
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
import re

def Feedback():
    f= open('store.pckl','rb')
    model_params=pickle.load(f)
    f.close()


    f = open('classifier.pckl', 'rb')
    classifier = pickle.load(f)
    f.close()


    def Completion_matrix(new_sample):
        zero_row = np.where(~new_sample.any(axis=1))[0]
        if (len(zero_row) != 0):
            new_sample[zero_row, :] = 1
        return new_sample


    # 50 guys do 6 action
    def process_output_skelenton_to_array(results):
        # not sure the type of mediapipe output ,I use this function convert it to array
        out = ['0'] * 63
        # Print handedness and draw hand landmarks on the image.
        if not results.multi_hand_landmarks:
            out = out
            # can not find a hand ,initialize to 0
        else:
            # only choose the first one hand
            hand_landmarks = str(results.multi_hand_landmarks[0])
            hand_landmarks = re.split('\n}\nlandmark {\n  x: |\n  y: |\n  z: |\n}\n|landmark {\n  x: ', hand_landmarks)
            out = hand_landmarks[1:64]
        return out

    test_frames=[]
    # For static images:
    result_max = "begin"

    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    #/media/liang/ssd2/wash_hand_3/Domain-and-View-point-Agnostic-Hand-Action-Recognition-main/datasets/HandWashDataset_self/Step6/Step6_24.avi
        cap = cv2.VideoCapture(0)
    #    cap = cv2.VideoCapture("/media/liang/ssd2/wash_hand_3/collect_data_all_recent_used!!!!!!!!!!/collect_data/11.avi")


        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



            if len(test_frames)<29:# maybe need over the tcn length?
                test_frames.append(image)
            elif len(test_frames) > 29:
                print("error ,max is 1+1=2 but now is over 2+1=3")
            elif len(test_frames)==29:
                test_frames.append(image)
                predict_data=[]
                for i in range(len(test_frames)):
                    predict_data.append(process_output_skelenton_to_array(hands.process(image)))


                # here the input is a two frames .but only use the first one
                data= np.float64(np.array(predict_data))

                new_sample = Completion_matrix(data)
                data_AUG = np.float64(skele_augmentation(new_sample, model_params))
                print("Generate a prediction")

                data_AUG=np.expand_dims(data_AUG ,axis=0)

    #            prediction = model.predict(data_AUG)
                prediction = classifier.predict(data_AUG)

                print(prediction.shape)
    #            print(prediction)
    #            print(np.argmax(prediction))

                test_frames.pop(0)

      #          result_max=str(np.argmax(prediction))
                result_max=str(prediction[0])

            cv2.putText(image,result_max ,(100,100), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0), 2, 0)   #(col,row) begin
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



        cap.release()
        cv2.destroyAllWindows()


