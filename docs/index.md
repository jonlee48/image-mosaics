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

## Background

## Main Algorithm
Some inline $math$.
$$
C_D=\frac{2D}{\rho V ^2 A}
$$

### Recover Homographies
```python
if (this is code):
    return syntax_highlighting
```

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

## Results


## Augmented Reality

The goal for this feature was to simulate the idea of having a painting on a wall. 

![](/videos/original-vid.gif)

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

![](/videos/out-movie.gif)