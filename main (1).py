import os, sys, pygame
from random import randint

#programando las raquetas
##clase pad.- hereda los atributos de la clase sprite.Sprite de pygame
class Pad(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 30)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.max_speed = 10
        self.speed = 0

    def move_up(self):
        self.speed = self.max_speed * -1

    def move_down(self):
        self.speed = self.max_speed * 1

    def stop(self):
         self.speed = 0
##permite actualizar la posicion de la raqueta
    def update(self):
        self.rect.move_ip(0, self.speed)


##creando la pelota
##Como en el caso de la clase Pad, la clase Ball también hereda los
##atributos de la clase sprite.Sprite de Pygame       
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
  
  
    
        self.image = pygame.Surface((10, 10)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
            
    

    
##velocidad de los ejes
        self.speed_x = 0
        self.speed_y = 0
        
##cambiar la direccion de la pelta
    def change_y(self):
        self.speed_y *= -1
    def change_x(self):
        self.speed_x *= -1
        
##mover la pelota
    def start(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
        
##detener la pelota
    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
        
##actualizar la posición de la pelota teniendo en cuenta la velocidad en cada eje.
    def update(self):
        
##imagen de cuadrado en blanco de la pelota
        self.rect.move_ip(self.speed_x, self.speed_y)
    def reset(self):
        self.rect = self.image.get_rect(center=self.pos)

    
##clase puntaje de cada jugador
class Score(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.score = 0
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)
        
## se encarga de ir sumando puntos al marcador 
    def score_up(self):
        self.score += 1
        
##actualice la imagen y el rectángulo
    def update(self):
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

