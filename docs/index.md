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
Image mosaics are created by compositing multiple images together by computing the perspective transformation between images. 
We captured our own photographs and implemented a GUI so that users could select features to map between images. 
We also implemented three bells and whistles. 
The code is available at [github.com/jonlee48/image-mosaics](https://github.com/jonlee48/image-mosaics)

### Sections
1. [Shoot and choose good pictures](#1---shoot-and-choose-good-pictures)
2. [Recover homographies](#2---recover-homographies)
3. [Warp the images](#3---warp-the-images)
4. [Blend images into a mosaic](#4---blend-images-into-a-mosaic)
5. [Bells and whistles](#5---bells-and-whistles)
   1. [Implemented perspective warping using our own math.](#51---implemented-perspective-warping-using-our-own-math)
   2. [Image blending](#52---image-blending)
   3. [Augmented reality](#53---augmented-reality)

## 1 - Shoot and choose good pictures
We selected a photo of a car on the highway and a stock image of a license plate. We could do some interesting things, 
such as warping the photo of the car to make the license plate easier to read, or map the photo of the license plate onto the car's license plate.

{% include image names="imgs/license1.jpg,imgs/license2.jpg" caption="Photos to test rectification of the numbers on a license plate." height="130" %}

We chose the following photos because they were visually appealing - showing a landscape scene that would make for a nice panorama. 
Additionally, each set of images had unique features which made it easier to find 4 corresponding points in the photos.
For example, the corners of the windows of the ski lodge would make good points to solve for a homography. 

{% include image names="imgs/lodge2.jpg,imgs/lodge1.jpg" caption="Photos of an empty ski lodge captured over Spring break." height="350" %}

{% include image names="imgs/bk-bridge-1.jpg,imgs/bk-bridge-2.jpg,imgs/bk-bridge-3.jpg," caption="Photos of the Brooklyn Bridge." height="250" %}

{% include image names="imgs/bk-and-manhattan-bridge-1.jpg,imgs/bk-and-manhattan-bridge-2.jpg,imgs/bk-and-manhattan-bridge-3.jpg,imgs/bk-and-manhattan-bridge-4.jpg" caption="Sequence of panoramic photos of NYC." height="110" %}


## 2 - Recover homographies

We chose to compute the homography ourselves for this project rather than use any Python libraries. The general idea is to solve the following equation:

$$
Ah = 0
$$

Let us first define a point correspondence. A point correspondence is a pair of coordinates (x,y) and (x', y') that represent the matching two locations in image one and two.

$h$ is the homography and is a 1x9 matrix that will later be shaped into a 3x3 matrix, and $A$ is a 2n x 9 matrix where n is the number of point correspondences between the two images.

For each point correspondence between a pair of images, the following two rows are appended to matrix $A$:

$$
[-x, -y, -1,    0,    0,  0, x*x', y*x', x'] \\
[   0,    0,  0, -x, -y, -1, x*y', y*y', y']
$$

We then use single value decomposition to solve $Ah=0$ for $h$. 

$$
A = U \Sigma V^T
$$

The last column of $V$ contains the vectorized entries of $H$. We simply reshape the column vector into a 3x3 matrix to get $H$.

Here is our implementation in python.
```python
def computeH(im1_pts, im2_pts):
    '''
        Computes and returns the homography between two images.

        im1_pts and im2_pts are n-by-2 matrices holding the 
        (x,y) locations of n point correspondences from the two images
        
        Returns H, the recovered 3x3 homography matrix
    '''
    A = [] 

    assert(len(im1_pts) == len(im2_pts))

    for im1, im2 in zip(im1_pts,im2_pts):
        x = im1[0]
        y = im1[1]

        xp = im2[0]
        yp = im2[1]

        A.append(np.array([-1*x, -1*y, -1,    0,    0,  0, x*xp, y*xp, xp]))
        A.append(np.array([   0,    0,  0, -1*x, -1*y, -1, x*yp, y*yp, yp]))

    A = np.array(A)

    # use single value decomposition to solve for H
    u, s, v = np.linalg.svd(A)

    # H is last column of v
    H = v[8].reshape((3,3))
    # normalize H
    H = (1 / H.item(8)) * H

    return H
```

## 3 - Warp the images

## 4 - Blend images into a mosaic
{% include image names="imgs/lodge12.png" caption="lodge" height="300" %}
{% include image names="imgs/bk-and-manhattan-bridge-123.png" caption="NYC" height="300" %}
{% include image names="imgs/bk-bridge-123.png" caption="Brooklyn Bridge" height="300" %}

## 5 - Bells and whistles

### 5.1 - Implemented perspective warping using our own math.

### 5.2 - Image blending
In order to demonstrate the blending process the best we wanted to have images that had similar features but differnet levels of contrast. 

We decided to use a whiteboard with writing as the light can reflect off of interesting angles to create differnet contrasts.

![2 pictures of the same board with differnt levels of contrast](boardside.png)

Our naive approach to blend these two images is just to write the first image over the second one. 

![Mosaic with writing the first picture over the first one](noblur.png)

In this photo, we clearly see the lines where the two images are. 

Next, we tried to identify the overlap of the two images for example: 

![Mosaic with the overlap idenfied](overlap.png)

In pseudocode this would be: 

``` sh
while writing second image pixel: 
    if (pixels are already present)
        overlap[pixel] = true
```

Once we know where the overlap is we tried to just take 50% from each image in this region, again in pseudocode: 

``` sh
while writing second image pixel: 
    if (pixels are already present)
        newpixel = (0.5 * curpixel) + (0.5 * oldpixel)
```

This would give us the result: 

![Mosaic with 50% in overlap](halfblur.png)

In this mosaic, we can still see an edge, but there is more of a gradual difference between the two images.

Finally, as we move across the overlap region the values that we are trying to approximate change. 

![2 regions of the overlap labeled](overlap_label.png)

For example, in this image we would want the region in black to repersent more of the left image and the region in blue to repersent more of the right image. Because of this we can change the weight of each image as we move across the border region, again in pseudocode:

``` sh
while writing second image pixel: 
    if (pixels are already present)
        w = (current_width / total_width)
        newpixel = (w * curpixel) + ((1-w) * oldpixel)
```

This would give us the result: 

![Changing weight blur](boardblur.png)

As we can see this result is a lot better and the transition feels smooth.


### 5.3 Augmented Reality

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
