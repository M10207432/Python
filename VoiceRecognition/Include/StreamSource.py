from time import time
import cv2

ex_file=['1','2','3']

class streamsource(object):
    def __init__(self):
        self.success=False
        self.frames = [open('..//'+f+'.jpg','rb').read() for f in ex_file]
        
    def get_frame(self):
        return self.frames[int(time())%len(ex_file)]

    def get_video(self):
        if self.success==False:
            self.vidcap=cv2.VideoCapture('2.mp4')
            self.success, self.video_img=self.vidcap.read()
            self.success=True
            
            self.success, self.video_img=self.vidcap.read()
            cv2.imwrite("tmp.jpg", self.video_img)

        self.success, self.video_img=self.vidcap.read()
        cv2.imwrite("tmp.jpg", self.video_img)
        f=open('tmp.jpg','rb')
        source=f.read()
        f.close()
        return source
