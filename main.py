import argparse
import cv2
import numpy as np
from vanishing_points import VP
from homography import *
from get_perspective_images import get_perspectives

parser = argparse.ArgumentParser(prog = '2D to 3D Perspective Converter')
counter = 0
def click_event(event, x, y, flags, params):
    global points
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        counter+=1
        cv2.circle(img_dummy, (x,y), 2, (255, 255, 255), 3)
        cv2.putText(img_dummy, ('C{}'.format(counter)), (x,y), font,
                    1, (255, 0, 0), 2)   #str(x) + ',' + str(y)    
        cv2.imshow('image', img_dummy)
    if event == cv2.EVENT_MBUTTONDOWN:
        coordinates = np.array([[[points[0],points[1]],[points[3],points[4]]], 
                                [[points[0],points[2]],[points[3],points[5]]],
                                [[points[0],points[3]],[points[1],points[4]]]])

        vanishing_points = VP.points(coordinates)
        Hxy,Hyz,Hxz = Homography.mat(points[0],[points[1],points[2],points[3]],vanishing_points)
        P = get_perspectives(image,Hxy,Hyz,Hxz,points)
        P.warped()

if __name__=="__main__":
    parser.add_argument('filename')
    parser.add_argument('-r','--resize',default=0,choices=[0,1],required=False,type=int)
    args = parser.parse_args()
    points = []
    image = cv2.imread(args.filename, 1)
    if args.resize==1:
        image = cv2.resize(image, (round(image.shape[1]/2),round(image.shape[0]/2)))
    img_dummy = image.copy()
    cv2.imshow('image', img_dummy)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.imwrite('annotated.jpg',img_dummy)
    cv2.destroyAllWindows()
