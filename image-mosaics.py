import numpy as np


def computeH(im1_pts, im2_pts):
    '''
        Computes and returns the homography between two images.

        im1_pts and im2_pts are n-by-2 matrices holding the 
        (x,y) locations of n point correspondences from the two images
        
        Returns H, the recovered 3x3 homography matrix
    '''
    H = None
    P = [] 

    assert(len(im1_pts) == len(im2_pts))

    for im1, im2 in zip(im1_pts,im2_pts):
        x = im1[0]
        y = im1[1]

        xp = im2[0]
        yp = im2[1]

        P.append(np.array([-1*x, -1*y, -1,    0,    0,  0, x*xp, y*xp, xp]))
        P.append(np.array([   0,    0,  0, -1*x, -1*y, -1, x*yp, y*yp, yp]))

    P = np.array(P)
    print(P)

    u, s, v = np.linalg.svd(P)

    H = v[8].reshape((3,3))
    # normalize H
    H = (1 / H.item(8)) * H

    print(H)
    return H

if __name__ == '__main__':
    im1_pts = [(0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
    im2_pts = [(0, 0, 1), (2, 0, 1), (0, 2, 1), (2, 2, 1)]

    H = computeH(im1_pts, im2_pts)

    for p in im1_pts:
        p = np.array(p)
        print(H@p)

