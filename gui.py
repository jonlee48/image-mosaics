import pygame
import cv2
import numpy as np
from mosaics import computeH

def resize_img(im, display_width, display_height):
    '''
    Scale the image to fit within display size, maintain aspect ratio
        im: pygame image
        display_width, display_height: ints
        returns: resized img
    '''
    width_scale = display_width / im.get_width()
    height_scale = display_height / im.get_height()
    scale = min(width_scale, height_scale)

    resize = (im.get_width() * scale, im.get_height() * scale)
    img_resize = pygame.transform.scale(im, resize)
    return img_resize

def resize_to_fit(im_width, im_height, display_width, display_height):
    '''
    Return dimensions of the image to fit within display size while maintaining aspect ratio
        im_width, im_height: dimensions of image
        display_width, display_height: dimensions of display
        returns: (int_width, int_height)
    '''
    width_scale = display_width / im_width
    height_scale = display_height / im_height
    scale = min(width_scale, height_scale)

    resize = (int(im_width * scale), int(im_height * scale))
    return resize


# TODO: input images to align
im1_path = 'imgs/lodge1.jpg'
im2_path = 'imgs/lodge2.jpg'

im2_path = 'imgs/license1.jpg'
im1_path = 'imgs/license2.jpg'

# start the pygame interface
pygame.init()
clock = pygame.time.Clock()


''' Resize images to fit on the screen '''
im1_raw = cv2.imread(im1_path)
im2_raw = cv2.imread(im2_path)

# get screen dimensions
info = pygame.display.Info()
display_width = int(info.current_w / 2)
display_height = info.current_h - 100

im1_new_size = resize_to_fit(im1_raw.shape[1], im1_raw.shape[0], display_width, display_height)
im1_resize = cv2.resize(im1_raw, im1_new_size)
im2_new_size = resize_to_fit(im2_raw.shape[1], im2_raw.shape[0], display_width, display_height)
im2_resize = cv2.resize(im2_raw, im2_new_size)

# save back to file so it can be opened by pygame
name, format = im1_path.split('.')
im1_newpath = name + '_resized.' + format
name, format = im2_path.split('.')
im2_newpath = name + '_resized.' + format

cv2.imwrite(im1_newpath, im1_resize)
cv2.imwrite(im2_newpath, im2_resize)

state = 0
features = []
colors = [(255,0,0), (0,255,0), (0,0,255), (255,0,255)]


# load images into pygame
im1 = pygame.image.load(im1_newpath)
im2 = pygame.image.load(im2_newpath)



# start display with first image
screen = pygame.display.set_mode((im1.get_width(), im1.get_height())) # window dimensions same as image
# Show the image
screen.blit(im1, (0,0))


quit = False
while not quit:

    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        # mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == 4:
                # transition to next image
                screen = pygame.display.set_mode((im2.get_width(), im2.get_height()))
                # Show the image
                screen.blit(im2, (0, 0))


            elif state < 9:
                # one of the 8 features manually selected
                pos = pygame.mouse.get_pos()
                print(pos)

                # draw a dot where clicked
                color = colors[len(features)%4]
                pygame.draw.circle(screen, color, pos, radius=3)

                # save the position
                features.append(pos)

            elif state == 9:

                # create two 4x2 matrix for set of features
                im1_pts = np.array(features[:4])
                im2_pts = np.array(features[4:])

                # convert to homogeneous coordinates (x,y,1)
                im1_pts = np.hstack((im1_pts, np.ones((4,1))))
                im2_pts = np.hstack((im2_pts, np.ones((4,1))))
                print(im1_pts)
                print(im2_pts)

                # compute the homography from im1 to im2
                H = computeH(im1_pts, im2_pts)
                print('H:')
                print(H)

                # TODO: show mosaic
                ''' Compute size of np array needed to fit mosaic '''
                # get coords of corners of im1 after mapping
                corners = [(0,0,1),
                           (im1.get_width(),0,1),
                           (0,im1.get_height(),1),
                           (im1.get_width(),im1.get_height(),1)]

                corners_mapped = np.zeros((4,2))
                for i,c in enumerate(corners):
                    cp = H@c
                    # normalize by 3rd coordinate
                    cp = cp/cp[2]
                    corners_mapped[i] = cp[0:2]

                #print(corners_mapped)


                # get lower and upper bounds of im1 and 2
                w_low = min(np.amin(corners_mapped[:,0]), 0)
                w_up  = max(np.amax(corners_mapped[:,0]), im2.get_width())
                h_low = min(np.amin(corners_mapped[:,1]), 0)
                h_up  = max(np.amax(corners_mapped[:,1]), im2.get_height())


                # get coordinates of origin (top,left corner) for im2
                origin_w = int(-w_low)
                origin_h = int(-h_low)


                # setup empty array for mosaic
                width = int(w_up-w_low)
                height = int(h_up-h_low)
                mosaic = np.zeros((height,width,3))
                print(mosaic.shape)
                print(im2.get_width())
                print(im2.get_height())


                ''' add image 2 to mosaic '''
                # image 2 needs to be same dimensions as mosaic
                im2 = cv2.imread(im2_newpath)
                print(im2.shape)

                im2_width = im2.shape[1]+origin_w
                im2_height = im2.shape[0]+origin_h
                pad_width = ((int(origin_h), int(mosaic.shape[0] - im2_height)), (int(origin_w), int(mosaic.shape[1] - im2_width)),(0,0))
                print('pad_width')
                print(pad_width)
                im2_padded = np.pad(im2,
                                    pad_width=pad_width,
                                    mode='constant',
                                    constant_values=0)
                # TODO: the width and height may still differ by 1 (due to rounding)
                print('padded shape')
                print(im2_padded.shape)

                print('mosaic shape')
                print(mosaic.shape)

                mosaic += im2_padded


                ''' add image 1 on top '''
                im1 = cv2.imread(im1_newpath)
                for w in range(im1.shape[1]):
                    for h in range(im1.shape[0]):
                        p = (w,h,1)
                        pp = H @ p
                        # normalize by 3rd coordinate
                        pp = pp / pp[2]
                        wp, hp, _ = pp
                        wp = round(wp+origin_w) # use round instead of int
                        hp = round(hp+origin_h)
                        # set the patch of n pixels around mapped coordinates to the pixel color (to account for rounding error)
                        # TODO: increase this number if patches in the image appear blank
                        n = 0
                        mosaic[hp:hp+n+1,wp:wp+n+1,:] = im1[h,w,:]

                ''' save the result '''
                mosaic_path = 'imgs/mosaic.png'
                cv2.imwrite(mosaic_path,mosaic)
                pygame_mosaic = pygame.image.load(mosaic_path)

                ''' display the result '''
                # resize result to fit to screen
                pygame_mosaic = resize_img(pygame_mosaic, display_width, display_height)

                screen = pygame.display.set_mode((pygame_mosaic.get_width(), pygame_mosaic.get_height()))
                screen.fill((0, 0, 0))
                screen.blit(pygame_mosaic, (0, 0))

                scale = 1
                scale = pygame_mosaic.get_width()/mosaic.shape[1]

                # Show the mapped 4 points from im1
                for i, p in enumerate(im1_pts):
                    pp = H @ p
                    # normalize by 3rd coordinate
                    pp = pp / pp[2]
                    w, h, _ = pp
                    w = round(scale * (w + origin_w))
                    h = round(scale * (h + origin_h))
                    color = colors[i % 4]
                    pygame.draw.circle(screen, color, (w, h), radius=3)

            state += 1


    # update the display
    pygame.display.flip()
    clock.tick(30)