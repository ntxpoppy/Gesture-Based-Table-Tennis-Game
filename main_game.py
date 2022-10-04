#importing libraries

import cv2
import numpy as np
import cvzone
import time
import os #rerun
import sys #rerun
import subprocess #rerun
from cvzone.HandTrackingModule import HandDetector


#had to resize game over sign to TT size.
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height

#importing images required
imgBackground = cv2.imread("TT_corr.png")
imgintro2 = cv2.imread("test.png", cv2.IMREAD_UNCHANGED)
imgball = cv2.imread("ball_small.png", cv2.IMREAD_UNCHANGED) #transparency
imgracket1 = cv2.imread("TT_next_resize.png", cv2.IMREAD_UNCHANGED) #transparency
imgracket2 = cv2.imread("TT_re size.png", cv2.IMREAD_UNCHANGED) #transparency
imgscore_p1 = cv2.imread("score_p1_re.png", cv2.IMREAD_UNCHANGED) #transparency
imgscore_p2 = cv2.imread("score_p2.png", cv2.IMREAD_UNCHANGED) #transparency
imgHighscore_notif = cv2.imread("Highscore_notif.png", cv2.IMREAD_UNCHANGED) #transparency
imgGameover = cv2.imread("GO_bg_retry.png", cv2.IMREAD_UNCHANGED) #transparency

#hand detection
detector = HandDetector(detectionCon=0.8, maxHands=2)

#keeping ball at a particular location
ballPos = [300,100] #y,x
speedx = 20 #speed of ball in x-axis
speedy = 20 #speed of ball in y-axis
Gameover = False #Gameover to be False to allow game to start
score = [0,0] #initialising score of both players

#Game LOOP
while True:
    _, img = cap.read()
    img = cv2.flip(img,1) # 1 for horizontal flip

#finding hands/detecting
    hands, img = detector.findHands(img, flipType= False) #draw hands
    img = cv2.addWeighted(img, 0.1, imgBackground, 0.9, 0) #TT background image
    #countdown
    # Specify the countdown

    # check for hands + Game working
    if hands:
        for hand in hands:
            x,y,w,h = hand['bbox']
            h1, w1, _ = imgracket1.shape #fixing bat position
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 500) #(y, ymin, ymax)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgracket1, (80, y1))
                #img3 = cvzone.overlayPNG(img,imgscore_p1, (300,300))
                if 80 < ballPos[0] < 80+w1 and y1 < ballPos[1] < y1+h1:  #has hit the left bat
                    speedx = -speedx
                    ballPos[0] += 80  # avoid bounces
                    score[0] +=1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgracket2, (1118,y1))
                if 1118 < ballPos[0] < 1118+w1 and y1 < ballPos[1] < y1+h1: #has hit the right bat
                    speedx = -speedx
                    ballPos[0] -= 80  # avoid bounces
                    score[1] += 1
        # BALL starting location and start of the game w/h ball
        img = cvzone.overlayPNG(img, imgball, ballPos)
        if ballPos[1] >= 500 or ballPos[1] <= 5:  #yaxis ~1
            speedy = -speedy

        ballPos[0] += speedx
        ballPos[1] += speedy

        #score display for each player
        cv2.putText(img, "P2: " + str(score[0]), (300, 650), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        cv2.putText(img, "P1: " + str(score[1]), (900, 650), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

    else: #display rules when no hands are detected!
        text1 = "THE RULES OF GESTURE BASED TT GAME: "
        text5 = "* The RIGHT player will start first!"
        text2 = "* The goal of the game is to hit the ball with your bats!"
        text3 = "* Player 1 will play with their RIGHT hand"
        text4 = "* Player 2 will play with their LEFT hand"
        text6 = "* Remove ANY hand from screen to read rules"
        text7 = "* Game starts if ANY hand appears! "
        cv2.putText(img, text1, (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 3)
        cv2.putText(img, text2, (250, 72), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, text3, (250, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, text4, (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, text5, (250, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, text6, (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, text7, (250, 550), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    # When the Game is OVER
    if ballPos[0] < 90 or ballPos[0] > 1160:
        Gameover = True
        if Gameover:
            img = imgGameover #GAMEOVER IMAGE as background
            if score[0] > score[1]: #Player 1 winning condition
                cv2.putText(img, "PLAYER 1 WINS BY " + str(score[0]) + " POINTS!", (100, 650), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255),
                            3)
                time.sleep(6)
                # rerun trial
                #subprocess.call([sys.executable, os.path.realpath(__file__)] +sys.argv[1:])

            if score[0] < score[1]: #Player 2 winning condition
                cv2.putText(img, "PLAYER 2 WINS by " + str(score[1]) + " POINTS!", (100, 650), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255),
                            3)
                time.sleep(6)
                # rerun trial
                #subprocess.call([sys.executable, os.path.realpath(__file__)] +sys.argv[1:])

            if score[0] == score[1]: #TIE condition
                cv2.putText(img, "IT IS A TIE by " + str(score[1]) + " POINTS!", (100, 650), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255),
                            3)
                time.sleep(6) #pause the screen to read
                # rerun trial
                #subprocess.call([sys.executable, os.path.realpath(__file__)] +sys.argv[1:])


    cv2.imshow("TT GAME", img)
    cv2.waitKey(1)  # opening webcam