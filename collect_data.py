#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import cv2
import os
import tkinter as tk  # 使用Tkinter前需要先导入


def CollectData():
    # root='/media/arl/ssd2/collect_data_code'
    root = ''
    # root='/media/liang/ssd22/collect_data_code'
    video_name = os.listdir(root + 'collect_data')
    begin = 0
    if len(video_name) == 0:
        begin = 0
    else:
        for i in range(len(video_name)):
            num_video = int(video_name[i].split('.')[0])
            if begin < num_video:
                begin = num_video
    win_row = 600
    win_col = 1820
    start_all_time = time.time()

    # Create a new VideoCapture object
    cam = cv2.VideoCapture(0)

    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    # codec = cv2.VideoWriter_fourcc((*'png '))
    # codec = cv2.VideoWriter_fourcc(*'mjpg')

    fps = 30.0  # 指定写入帧率为30
    frameSize = (640, 480)  # 指定窗口大小
    # 创建 VideoWriter对象
    out = cv2.VideoWriter(root + 'collect_data/' + str(begin + 1) + '.avi', codec, fps, frameSize)
    print("按键Q-结束视频录制")

    rat, img = cam.read()
    # Initialise variables to store current time difference as well as previous time call value
    previous = time.time()
    cost_control_time = time.time() - start_all_time
    # Keep looping
    rat5 = True
    wash_time = 10
    while True:
        cv2.namedWindow("guide", cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow("guide", 70, 0)

        # Show the image and keep streaming
        rat, img = cam.read()

        if rat == False:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!cannot read camera!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            break
        if cost_control_time > wash_time:
            print(f'time used: {cost_control_time}')
            break
        out.write(img)
        cost_control_time = time.time() - start_all_time
        black = [0, 0, 0]  # ---Color of the border---
        img = cv2.resize(img, dsize=(int(win_col / 2), int(win_row)), interpolation=cv2.INTER_CUBIC)

        #        cv2.putText(back_ground,"Step: " ,(int(back_ground.shape[0]/2.5),  int(back_ground.shape[1]/3)), font, 2,(0,0,0), 2, 0)   #(col,row) begin
        cv2.imshow("guide", cv2.flip(img, -1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            out.release()
            cv2.destroyAllWindows()
            print(cost_control_time)
            break

    cam.release()
    out.release()
    cv2.destroyAllWindows()

# # 第1步，实例化object，建立窗口window
# window = tk.Tk()
#
# # 第2步，给窗口的可视化起名字
# window.title('wash hand monitor project')
#
# # 第3步，设定窗口的大小(长 * 宽)
# window.geometry('1000x600')  # 这里的乘是小x
#
# # 第4步，在图形界面上设定标签
# l = tk.Label(window, text='Want to wash hand?', bg='green', font=('Arial', 30), width=30, height=3)#, width=30, height=2
# # 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
#
# # 第5步，放置标签
# l.pack()    # Label内容content区域放置位置，自动调节尺寸
# # 放置lable的方法有：1）l.pack(); 2)l.place();
# B = tk.Button(window, text ="yes,click here", command = CollectData,bg='white',width=30, height=3)
#
# B.pack()
# # 第6步，主窗口循环显示
# window.mainloop()
# # 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# # 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。
