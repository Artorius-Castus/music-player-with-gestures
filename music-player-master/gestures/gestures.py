import cv2
import pygame
import numpy as np
import mediapipe as mp

#intialize Pygame Mixer
pygame.mixer.init()

#Load Music Files
music_files = ['song1.mp3', 'song2.mp3','song3.mp3']
current_song_index = 0
pygame.mixer.music.load(music_files[current_song_index])

#Start Webcam
cap = cv2.VideoCapture(0) #0 for default webcam

#Define Hand Gesture recognition functions
def is_wave_left(landmarks):
    wrist = landmarks.landmark[0]
    finger_tips = [landmarks.landmark[4],landmarks.landmark[8],landmarks.landmark[12],landmarks.landmark[16],landmarks.landmark[20]]
    return all(tip.x <wrist.x - 0.1 for tip in finger_tips) #adjusted threshold

def is_wave_right(landmarks):
    wrist = landmarks.landmark[0]
    finger_tips = [landmarks.landmark[4],landmarks.landmark[8],landmarks.landmark[12],landmarks.landmark[16],landmarks.landmark[20]]
    return all(tip.x > wrist.x + 0.1 for tip in finger_tips) #adjusted threshold

def is_palm_up(landmarks):
    wrist = landmarks.landmark[0]
    palm = landmarks.landmark[5]
    return palm.y < wrist.y

def is_palm_down(landmarks):
    wrist = landmarks.landmark[0]
    palm = landmarks.landmark[5]
    return palm.y > wrist.y


#hand gesture recognition loop
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)


#guidline
print("guideline:")
print("-Wave left to play the next song")
print("-Waveright to play the previous song")
print("-Move you palm up to increase volume")
print("-Move you palm down to deccrease volume")

while True:
    ret,frame = cap.read()
    frame = cv2# 5;33

    