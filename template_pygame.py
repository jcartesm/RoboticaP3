import matplotlib.pyplot as plt
import math as mt
import pygame
import numpy as np
import random as ra

######################################################################################

#                              PYGAME SIMULATION

######################################################################################
colEstados = 15
filEstados = 12

# Seteo de la ventana
pygame.init()
ventana = pygame.display.set_mode((colEstados*50, filEstados*50))
pygame.display.set_caption('Insert NAME')
BLACK = (0, 0, 0)
ventana.fill(BLACK)
pygame.display.flip()

# Cargado de Imagenes a ocupar
pacman = pygame.image.load("img/pacE.png")
pacman = pygame.transform.scale(pacman, [50, 50])

pared = pygame.image.load("img/pared.png")
pared = pygame.transform.scale(pared, [50, 50])

moneda = pygame.image.load("img/money.png")
moneda = pygame.transform.scale(moneda, [50, 50])

def PrintFondo():
    ventana.fill(BLACK)
    ventana.blit(moneda,[50*0,50*5])
    for y in range(0,filEstados): 
        for x in range(0,colEstados):
            #  y representa la fila del mapa
            if y == 2:
                #  x representa la columan del mapa
                if x == 2 or x == 3 or x == 4 or x == 6 or x == 7 or x == 8 or x == 13:
                    ventana.blit(pared,[50*x,50*y])
            if y == 3:
                if x == 2 or x == 8 or x == 12 or x ==13:
                    ventana.blit(pared,[50*x,50*y])
            if y == 4:
                if x == 2 or x == 11 or x == 12 or x ==13:
                    ventana.blit(pared,[50*x,50*y])
            if y == 6:
                if x == 8 or x == 9:
                    ventana.blit(pared,[50*x,50*y])
            if y == 7:
                if x == 2 or x == 3 or x == 4 or x == 9 or x == 10 or x == 11 or x == 11 or x == 14:
                    ventana.blit(pared,[50*x,50*y])
                    


def Mover(posActual,mov):
    x = posActual[0] * 50
    y = posActual[1] * 50
    if mov == "N":
        pacman = pygame.image.load("img/pacN.png")
        for i in range(10):
            y = y - 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = x/50
        y = y/50
        return [x,y]
    if mov == "S":
        pacman = pygame.image.load("img/pacS.png")
        for i in range(10):
            y = y + 5
            if y > 210:
                return [x,y-5]
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = x/50
        y = y/50
        return [x,y]
    if mov == "E":
        pacman = pygame.image.load("img/pacE.png")
        for i in range(10):
            x = x + 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = x/50
        y = y/50
        return [x,y]
    if mov == "O":
        pacman = pygame.image.load("img/pacO.png")
        for i in range(10):
            x = x - 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = x/50
        y = y/50
        return [x,y]
    
PrintFondo()
# Musica de fondo
#pygame.mixer.music.load('song/fondo.mp3')
#pygame.mixer.music.play(-1)
# Posicion inicial aleatoria del robot
#indexIni =  ra.randint(2,6)
posPacman = [0,0]
ventana.blit(pacman,[0,0])

    
pygame.display.update()

is_running = True
while is_running:
    #posPacman = Mover(posPacman,aP[posPacman[1][posPacman[0]]])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

pygame.quit()