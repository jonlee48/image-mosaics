---
title: "CSCI 3907: Computational Photography "
layout: post
mathjax: true
---
------
# Project 3: Image Mosaics

## Team Members
- Jonathan Lee
- Graham Schock
- Jack Umina

## Overview
Image mosaics are created by compositing multiple images together by computing the perspective transformation between images. We captured our own photographs and implemented a GUI so that users could select features to map between images. We also implemented three bells and whistles.



### Table of Contents
- [Project 3: Image Mosaics](#project-3-image-mosaics)
  - [Team Members](#team-members)
  - [Overview](#overview)
    - [Table of Contents](#table-of-contents)
  - [1 - Shoot and choose good pictures](#1---shoot-and-choose-good-pictures)
  - [2 - Recover homographies](#2---recover-homographies)
  - [3 - Warp the images](#3---warp-the-images)
  - [4 - Blend images into a mosaic](#4---blend-images-into-a-mosaic)
  - [5 - Bells and whistles](#5---bells-and-whistles)
  - [5.1 - Implemented perspective warping using our own math.](#51---implemented-perspective-warping-using-our-own-math)
  - [5.2 - Image blending](#52---image-blending)
  - [5.3 - Augmented reality](#53---augmented-reality)
  - [5.3 Augmented Reality](#53-augmented-reality)

## 1 - Shoot and choose good pictures
{% include image names="imgs/lodge2.jpg,imgs/lodge1.jpg" caption="Photos of an empty ski lodge captured over Spring break." height="350" %}

{% include image names="imgs/bk-bridge-1.jpg,imgs/bk-bridge-2.jpg,imgs/bk-bridge-3.jpg," caption="Photos of the Brooklyn Bridge." height="250" %}

{% include image names="imgs/bk-and-manhattan-bridge-1.jpg,imgs/bk-and-manhattan-bridge-2.jpg,imgs/bk-and-manhattan-bridge-3.jpg,imgs/bk-and-manhattan-bridge-4.jpg" caption="Sequence of panoramic photos of NYC." height="110" %}

{% include image names="imgs/license1.jpg,imgs/license2.jpg" caption="Photos to test rectification of the numbers on a license plate." height="130" %}

## 2 - Recover homographies

We chose to compute the homography ourselves for this project rather than use any Python libraries. The general idea is to solve the following equation:

$$
Ah = 0
$$

Let us first define a point correspondence. A point correspondence is a pair of coordinates (x,y) and (x', y') that represent the matching two locations in image one and two.

$h$ is the homograpgy and is a 1x9 matrix that will later be shaped into a 3x3 matrix, and $A$ is a 2n x 9 matrix where n is the number of point correspondences between the two images.

For each point correspondence between a pair of images, the following two lines are appended to matrix $A$:

$$
(-x, -y, -1,    0,    0,  0, x*x', y*x', x')
$$
$$
(   0,    0,  0, -x, -y, -1, x*y', y*y', y')
$$

We then use single value decompositon to solve $Ah=0$ for $h$.

## 3 - Warp the images

## 4 - Blend images into a mosaic
{% include image names="imgs/lodge12.png" caption="lodge" height="300" %}
{% include image names="imgs/bk-and-manhattan-bridge-123.png" caption="NYC" height="300" %}
{% include image names="imgs/bk-bridge-123.png" caption="Brooklyn Bridge" height="300" %}

## 5 - Bells and whistles

## 5.1 - Implemented perspective warping using our own math.

## 5.2 - Image blending


## 5.3 Augmented Reality

The goal for this feature was to simulate the idea of having a painting on a wall. 

{% include image names="videos/original-vid.gif" height="350" %}

We started with the video above, a video of a wall. On the wall was a sheet of paper that had a checkerboard printed on it. Using an OpenCV function, we were able to automatically find the 4 corners of the checkerboard so that they could be used in computing the homography between an individual frame of the video and an image of a paitning. We used Van Gogh's iconic Starry Night as the painting.

A high-level psuedocode algorithm for this feature is as follows:
```
for each frame in the video:
    1. use OpenCV to get the 4 corners of the checkerboard on the wall
    2. compute the homography between the frame and starry night 
    3. using the homography matrix, transform Starry Night to cover checkerboard

compress frames back into video
```

This produced the following result:

{% include image names="videos/out-movie.gif" height="350" %}