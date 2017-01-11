import os, sys, pygame
from random import randint

#creacion de raquetas
class Pad(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.max_speed = 5
        self.speed = 0

    def move_up(self):
        self.speed = self.max_speed * -1

    def move_down(self):
        self.speed = self.max_speed * 1

    def stop(self):
         self.speed = 0

    def update(self):
        self.rect.move_ip(0, self.speed)




def main():

   #creacion del fondo del juego
    pygame.init()

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Proyecto-Final')

    try:
        filename = os.path.join(
        os.path.dirname(__file__),
        'graficos',
        'fondo.png')
        fondo = pygame.image.load(filename)
        fondo = fondo.convert()
    except pygame.error as e:
        print ('Cannot load image: ', filename)
        raise SystemExit(str(e))
    
if __name__ == '__main__':
    main()
