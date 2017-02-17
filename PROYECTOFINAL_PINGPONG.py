#ESCUELA POLITECNICA NACIONAL
#ESCUELA DE FORMACION DE TECNOLOGOS
#PROYECTO FINAL PROGRAMACION AVANZADA
#INTEGRANTES: FERNANDA USHCASINA, JESSICA CARRILLO
import pygame
from pygame.locals import *
import os
import sys
from random import randint

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMG_DIR = "im"
BLANCO = (255, 255, 255)
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0,0,2,2)

    def actualizar (self):
        self.left,self.top=pygame.mouse.get_pos()
        

class Boton (pygame.sprite.Sprite):
    def __init__(self, inicio1, x=200, y=200): #    Constructor
        self.boton_Normal= inicio1
        ancho, alto = self.boton_Normal.get_size()
        self.boton_Seleccion=pygame.transform.scale(self.boton_Normal, (int(ancho*1.1), int(alto*1.1)))
        self.boton_actual=self.boton_Normal

        self.rect=self.boton_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)


    def actualizar (self, pantalla, cursor): #  Funcion para verificar si existe colicion entre el rectangulo que sigue al mouse y el boyon iniciar
        if cursor.colliderect(self.rect):
            self.boton_actual=self.boton_Seleccion
        else:
            self.boton_actual=self.boton_Normal
        pantalla.blit(self.boton_actual, self.rect) 


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ball.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [3, 3] #velocidad de movimiento
        
#actualizar y sumar puntos
    def update(self,puntos):
        if self.rect.left <= 0: 
          puntos[1] += 1 
        if self.rect.right >= SCREEN_WIDTH: 
          puntos[0] += 1

#ubicacion de la pelota (centro)      
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx = SCREEN_WIDTH / 2
            self.rect.centery = SCREEN_HEIGHT / 2
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
        return puntos
        
        
    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0] = -self.speed[0]
            

class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT / 2
       
    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

def texto(texto, tam=20, color=(0, 0, 0)):
    fuente = pygame.font.Font(None, tam)
    return fuente.render(texto, True, color)

def main():
    pygame.init()
    size = width, height = 800, 600
    pantalla = pygame.display.set_mode(size)
    pantalla2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Pygame")
    reloj= pygame.time.Clock()
    fondo_inicio=pygame.image.load("inicio1.png")
    boton_iniciar=pygame.image.load("jugar.png")
    boton1=Boton(boton_iniciar, 350, 250)
    cursor1= Cursor()
    boton_juego2=pygame.image.load("jugar2.png")
    boton2=Boton(boton_juego2, 350, 350)
    fuente = pygame.font.SysFont("arial", 20, True)

    sonido_1 = pygame.mixer.music.load("musica_Inicio1.mp3") #sonido de fondo de juego primer nivel 
    sonido_1 = pygame.mixer.music.play(1)
    sonido_1=pygame.mixer.music.stop()

    fuente1 = pygame.font.SysFont("wendy", 32, True)
    texto_Puntaje=fuente1.render("MARCADOR ", True,((255,255,255))) # Texto para puntaje
    texto_Tiempo=fuente.render("Tiempo: ", True, (255,255,255)) # Texto tiempo
    texto_jugador1=fuente1.render("Jugador1 ", True,((255,255,255)))
    texto_jugador2=fuente1.render("Jugador2 ", True,((255,255,255)))
    fuente2 = pygame.font.SysFont("algerian", 50,True)
    texto_inicio=fuente2.render("PING PONG ",True,((100,50,150)))
    texto_play=fuente2.render("JUGAR ",True,((255,50,120)))
    
    
    try:
        filename = os.path.join(
        os.path.dirname(__file__),

        
        'fo.png')
        fon = pygame.image.load(filename)
             
##convert.- conversion del formato de los pixeles de formato canvas
        fondo = fon.convert()
    except pygame.error as e:
        print ('Cannot load image: ', filename)
        raise SystemExit(str(e))

##codiciones del puntaje
  
    
    bola = Pelota()
    jugador1 = Paleta(40)
    jugador2=Paleta(SCREEN_WIDTH - 40)
    clock = pygame.time.Clock()
    fps=60
    pygame.key.set_repeat(1,fps)
    puntos=[0,0]
    salir=False
    while salir!=True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir=True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    sonido_1=pygame.mixer.music.play(1)
                  
                    while True:
                        clock.tick(60)

                    # Actualizamos los obejos en pantalla
                        jugador1.humano()
                        jugador2.humano()
                        bola.update(puntos)
                        
                      
        # Comprobamos si colisionan los objetos
                        bola.colision(jugador1)
                        bola.colision(jugador2)
                        
        # Posibles entradas del teclado y mouse
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit(0)
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_UP:
                                    jugador1.rect.centery -= 20
                                elif event.key == K_DOWN:
                                    jugador1.rect.centery += 20
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_w:
                                        jugador2.rect.centery -= 20
                                    elif event.key == pygame.K_s:
                                        jugador2.rect.centery += 20
                            elif event.type == pygame.KEYUP:
                                if event.key == K_UP:
                                    jugador1.rect.centery += 0
                                elif event.key == K_DOWN:
                                    jugador1.rect.centery += 0
                          
                        segundos=pygame.time.get_ticks()/1000 # Variable de segundos
                        contador=fuente.render(str(segundos), True, (255,255,255))
                        pantalla.blit(fondo, (0, 0))
                        pantalla.blit(bola.image, bola.rect)
                        pantalla.blit(jugador1.image, jugador1.rect)
                        pantalla.blit(jugador2.image, jugador2.rect)
                        pantalla.blit(texto_jugador1, (100, 570))
                        pantalla.blit(texto_jugador2, (600, 570))
                        pantalla.blit(texto_Tiempo, (600, 3))
                        pantalla.blit(texto_Puntaje, (330, 8))
                        pantalla.blit(contador, (700,3))
                        pantalla.blit(texto(str(puntos[0]),100,BLANCO),(SCREEN_WIDTH/4,10))
                        pantalla.blit(texto(str(puntos[1]),100,BLANCO),((SCREEN_WIDTH*3/4)-20,10))
                        pygame.display.flip()
                        pygame.display.update()
                    pygame.display.update()
                elif cursor1.colliderect(boton2.rect):
                    sonido_1=pygame.mixer.music.play(1)
                    import PingPong_Proyecto
                    PingPong_Proyecto.main()
     
            pantalla.blit(fondo_inicio, (0, 0))
            pantalla.blit(texto_inicio, (250,150))
            pantalla.blit(texto_play, (300,200))
            cursor1.actualizar()
            boton1.actualizar(pantalla,cursor1)
            boton2.actualizar(pantalla,cursor1)
            pygame.display.update()
        pygame.display.update()
      





if __name__ == "__main__":
    main()
