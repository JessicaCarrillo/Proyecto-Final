import pygame
from pygame.locals import *
import os
import sys

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
IMG_DIR = "im"
BLANCO = (255, 255, 255)
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
        self.speed = [5, 5]
  

    def update(self,puntos):
        if self.rect.left <= 0: 
          puntos[1] += 1 
        if self.rect.right >= SCREEN_WIDTH: 
          puntos[0] += 1
          
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

    def cpu(self, pelota):
        self.speed = [0, 5]
        if pelota.speed[0] >= 0 and pelota.rect.centerx >= SCREEN_WIDTH / 2:
            if self.rect.centery > pelota.rect.centery:
                self.rect.centery -= self.speed[1]
            if self.rect.centery < pelota.rect.centery:
                self.rect.centery += self.speed[1]


def texto(texto, tam=20, color=(0, 0, 0)):
    fuente = pygame.font.Font(None, tam)
    return fuente.render(texto, True, color)


def main():
    pygame.init()
    pygame.mixer.init()
    # creamos la ventana y le indicamos un titulo:
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Pygame")

    fuente = pygame.font.SysFont("arial", 20, True)

    sonido_1 = pygame.mixer.music.load("musica_Inicio1.mp3") #sonido de fondo de juego primer nivel 
    sonido_1 = pygame.mixer.music.play(1)
  

    fuente1 = pygame.font.SysFont("wendy", 32, True)
    texto_Puntaje=fuente1.render("MARCADOR ", True,((255,255,255))) # Texto para puntaje
    texto_Tiempo=fuente.render("Tiempo: ", True, (255,255,255)) # Texto tiempo
    texto_jugador1=fuente1.render("Jugador1 ", True,((255,255,255)))
    texto_jugador2=fuente1.render("Jugador2 ", True,((255,255,255)))
    fuente2 = pygame.font.SysFont("algerian", 50,True)
    texto_inicio=fuente2.render("PING PONG ",True,((100,50,150)))
    texto_play=fuente2.render("JUGAR ",True,((255,50,120)))

    # cargamos los objetos
    fondo = load_image("fo.png", IMG_DIR, alpha=False)
    bola = Pelota()
    jugador1 = Paleta(40)
    jugador2 = Paleta(SCREEN_WIDTH - 40)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    puntos=[0,0]
    # el bucle principal del juego
    while True:
        clock.tick(60)
        # Actualizamos los obejos en pantalla
        jugador1.humano()
        jugador2.cpu(bola)
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
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador1.rect.centery += 0
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 0
     
        # actualizamos la pantalla
        segundos=pygame.time.get_ticks()/1000 # Variable de segundos
        contador=fuente.render(str(segundos), True, (255,255,255))
        pantalla.blit(fondo, (0, 0))
        todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
        todos.draw(pantalla)
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


if __name__ == "__main__":
    main()
