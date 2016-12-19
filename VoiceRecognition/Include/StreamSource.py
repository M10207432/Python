from time import time

ex_file=['1','2','3']

class streamsource(object):
    def __init__(self):
        self.frames = [open('..//'+f+'.jpg','rb').read() for f in ex_file]
        
    def get_frame(self):
        return self.frames[int(time())%len(ex_file)]

