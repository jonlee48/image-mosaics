import pygame

def resize_img(img, display_width, display_height):
    ''' Scale the image to fit within display size, maintain aspect ratio '''
    width_scale = display_width / img.get_width()
    height_scale = display_height / img.get_height()
    scale = min(width_scale, height_scale)

    resize = (img.get_width() * scale, img.get_height() * scale)
    img_resize = pygame.transform.scale(img, resize)
    return img_resize

# input images to align
img1_path = 'imgs/sea-lion.jpg'
img2_path = 'imgs/cat.jpg'

state = 0
features = []
colors = [(255,0,0), (0,255,0), (0,0,255), (255,0,255)]
display_height = 600
display_width = 600

# load images into pygame
img1_orig = pygame.image.load(img1_path)
img2_orig = pygame.image.load(img2_path)

# resize images
img1 = resize_img(img1_orig, display_width, display_height)
img2 = resize_img(img2_orig, display_width, display_height)

img1_resize = img1.get_size()
img2_resize = img2.get_size()

# Clock
clock = pygame.time.Clock()

# start the pygame interface
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

# Background Color
screen.fill((0, 0, 0))
# Show the image
screen.blit(img1, (0,0))


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
                screen.fill((0, 0, 0))
                screen.blit(img2, (0, 0))

            elif state < 9:
                # one of the 8 features manually selected
                pos = pygame.mouse.get_pos()

                # draw a dot where clicked
                color = colors[len(features)%4]
                pygame.draw.circle(screen, color, pos, radius=3)

                # save the position
                features.append(pos)

            elif state == 9:
                # show mosaic
                screen.fill((0, 0, 0))
                screen.blit(img1, (0, 0))

            state += 1


    # update the display
    pygame.display.flip()
    clock.tick(30)