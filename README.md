# 2D-to-3D-converter

This project is for my deeper understanding of Projection and Homography.
This is a simple API which takes a 2D image and gives a 3D perspective. 

## #Installation
`pip3 install -r requirements.txt`

## #Overview
![Annotated image](images/annotated_image.jpg)

* XY plane

![XY plane](images/Perspective_2.jpg)
  
* YZ plane

![YZ plane](images/Perspective_1.jpg)

* XZ plane

![XZ plane](images/Perspective_3.jpg)

## #Steps to run
`python3 main.py <file name> -r <0,1>` #(if you the image doesn't fit in the screen)
* Click the points on the image in same sequence shown in [annotated image](images/annotated_image.jpg) with the 'LEFT MOUSE BUTTON'.
* Once the annotation is done, click the 'MOUSE SCROLL BUTTON' to get the 3D perspectives.
