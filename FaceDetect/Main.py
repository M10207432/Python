import cv2
import numpy
import os

'''========================
    Load Default File
========================'''
face_cascade_path="./haarcascade_frontalface_default.xml"
face_cascade=cv2.CascadeClassifier(os.path.expanduser(face_cascade_path))

scale_factor=1.1
min_neighbors=3
min_size=(1,1)
flags=cv2.cv.CV_HAAR_SCALE_IMAGE

def faceDetect(img_file_path,outfname_path):
    img_path=os.path.expanduser(img_file_path)
    img=cv2.imread(img_path)

    #========Face detect opencv function
    faces=face_cascade.detectMultiScale(img,
                                        scaleFactor=scale_factor,
                                        minNeighbors=min_neighbors,
                                        minSize=min_size,
                                        flags=flags)
    #========Draw detect area
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,0), 2)
        cv2.imwrite(outfname_path,img)

    #========Show Img
    result_img=cv2.imread(outfname_path)
    cv2.imshow("Result",result_img)     #From [img pixel data] to show it
    cv2.waitKey(0)                      #Wait for keyboard event
    cv2.destroyAllWindows()             #Destroy all windows
        
def main():
    print "System Boot"
    resource_path="./img4.jpg"
    target_path="./faces.jpg"
    faceDetect(resource_path,target_path)
    
if __name__=="__main__":
    main()
