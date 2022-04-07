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


## Results


## Augmented Reality

The goal for this feature was to simulate the idea of having a painting on a wall. 

![](videos/original-vid.gif)

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

![](videos/out-movie.gif)