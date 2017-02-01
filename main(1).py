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

    
def main():

##creacion del fondo del juego
    
    pygame.init()
    size = width, height = 800, 600
    pantalla = pygame.display.set_mode(size)
    pygame.display.set_caption('Pong Pygame')
    salir=False

    reloj= pygame.time.Clock()
    sonido_1 = pygame.mixer.music.load("musica.mp3") #sonido de fondo de juego primer nivel 
    sonido_1 = pygame.mixer.music.play(1)

    player1=Pad() # Instanciamos un objeto de clase  Player
    
    #auxiliares para el movimiento
    izq_apretada,der_apretada,arriba_apretada,abajo_apretada=False,False,False,False
    t=0
##Carga la imagen
    try:
        filename = os.path.join(
        os.path.dirname(__file__),
        'graficos',
        'fondo.png')
        fon = pygame.image.load(filename)
        
##convert.- conversion del formato de los pixeles de formato canvas
        fondo = fon.convert()
    except pygame.error as e:
        print ('Cannot load image: ', filename)
        raise SystemExit(str(e))

##codiciones del puntaje
    if not pygame.font:
        raise SystemExit('Pygame does not support fonts')

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'graficos',
            'wendy.ttf')
        font = pygame.font.Font(filename, 90)
    except pygame.error as e:
        print ('Cannot load font: ', filename)
        raise SystemExit(str(e))

    left_score = Score(font, (width/3, height/8))
    right_score = Score(font, (2*width/3, height/8))
    left = pygame.Rect(0, 0, 5, height)
    right = pygame.Rect(width-5, 0, 5, height)
    
##posiciona cada una de las raquetas en la pantalla   
    pad_left = Pad((width/6, height/4))
    pad_right = Pad((5*width/6, 3*height/4))
    clock = pygame.time.Clock()
    fps = 60
##continúe registrando eventos del teclado mientras mantenemos
##presionada una determinada tecla.
    pygame.key.set_repeat(1,fps)
    
##ubicacion de la pelota
    ball = Ball((width/2, height/2))
    
##agrupacion sprotes.- raquetas y pelota
    sprites = pygame.sprite.Group(pad_left, pad_right)
    sprites = pygame.sprite.Group(pad_left, pad_right, ball)
    sprites = pygame.sprite.Group(pad_left, pad_right, ball, left_score, right_score)
    
##limitar el movimiento de la pelota
    top = pygame.Rect(0, 0, width, 5)
    bottom = pygame.Rect(0, height-5, width, 5)


## bucle infinito
    while 1:
        
        clock.tick(fps)
##hacemos que las raquetas se detengan usando funcion stop
        pad_left.stop()
        pad_right.stop()
        
##imprimirle movimiento a la pelota
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
##movimiento de las raquetas
## teclas w y s .- jugador izquierda
## teclas desplazamiento .- jugador derecha

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                pad_left.move_up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pad_left.move_down()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                pad_right.move_up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                pad_right.move_down()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
##velocidad aleatoria tanto en el eje X como en el eje Y            
                ball.start(randint(1, 3), randint(1, 3))
##                
        if ball.rect.colliderect(left):
            right_score.score_up()
            ball.reset()
            ball.stop()
        elif ball.rect.colliderect(right):
            left_score.score_up()
            ball.reset()
            ball.stop()
    
        sprites.update()
##copia pixeles contenidos en la imagen de fondo
        pantalla.blit(fondo, (0, 0))
        
##draw(screen).- actualice y dibuje en pantalla todos los sprites
        sprites.draw(pantalla)
        
##cambio de buffers 
        pygame.display.flip()

##detectar las colisiones entre la pelota y los rectángulos superior e inferior que creamos con anterioridad
        if ball.rect.colliderect(top) or ball.rect.colliderect(bottom):
            ball.change_y()
        elif (ball.rect.colliderect(pad_left.rect) or
            ball.rect.colliderect(pad_right.rect)):
            ball.change_x()
            
##si movemos las raquetas hacia arriba o hacia abajo lo suficiente, notaremos que desaparecerán de la pantalla.
## Limitamos el movimiento de las raquetas dentro de los confines del rectángulo que acabamos de crear, usando
##para esto la función clamp_ip() de la clase Rect de Pygame.            
        screen_rect = pantalla.get_rect().inflate(0, -10)
        pad_left.rect.clamp_ip(screen_rect)
        pad_right.rect.clamp_ip(screen_rect)


  

if __name__ == '__main__':
    main()



