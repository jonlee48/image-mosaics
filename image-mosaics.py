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

    for i in range(len(im1_pts)):
        x = im1_pts[i][0]
        y = im1_pts[i][1]

        xp = im2_pts[i][0]
        yp = im2_pts[i][1]

        P.append(np.array([-1*x, -1*y, -1,    0,    0,  0, x*xp, y*xp, xp]))
        P.append(np.array([   0,    0,  0, -1*x, -1*y, -1, x*yp, y*yp, yp]))

    # TODO: Compute PH = 0    
    zeros = np.zeros_like(P)
    zeros = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    H = np.linalg.lstsq(P, zeros, rcond=None)

    return H

if __name__ == '__main__':
    im1_pts = [(1, 1), (2, 2)]
    im2_pts = [(1, 1), (2, 2)]

    H = computeH(im1_pts, im2_pts)

    print(H)