import numpy as np

def isRegionBlack(mosaicpath):
    for i in range(len(mosaicpath)):
        for j in range(len(mosaicpath[0])):
            if np.array_equal(mosaicpath[i, j, :], [1, 1, 1]):
                return False
    return True
