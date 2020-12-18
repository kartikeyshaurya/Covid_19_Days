import pygame

def load_image(name):
    '''
    Loading the image 
    '''
    try:
        image = pygame.image.load(name)
        if image.get_alpha() == None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error :
        print("Could not load tje image")
    return image, image.get_rect()