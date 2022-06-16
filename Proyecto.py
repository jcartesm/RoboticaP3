
from traceback import print_tb
import matplotlib.pyplot as plt
import math as mt
import pygame
import numpy as np
import random as RA

###########################################
nALPHA = 0.1             # Tasa de Aprendizaje
nGAMMA = 0.98            # Factor de Descuento
nMAX_EPISODIOS = 1000   
aList_A = ['N','S','E','O']
Epsilon = 0.1

# Acciones
nNORTE = 0 ; nESTE  = 2 
nSUR   = 1 ; nOESTE = 3

# Meta
aMETA = [10,4]

# Mapa 
aMapa = [   # 0  1  2  3  4  5  6  7
            [ 1, 1, 1, 1, 1,-1, 1, 1], # 0
            [ 1,-1,-1,-1, 1,-1, 1, 1], # 1
            [ 1,-1, 1,-1, 1, 1, 1, 1], # 2
            [ 1,-1, 1, 1, 1,-1,-1,-1], # 3
            [ 1, 1, 1, 1, 1, 1, 1, 1], # 4
            [-1,-1,-1, 1,-1,-1,-1, 1], # 5
            [ 1, 1, 1, 1, 1, 1,-1, 1], # 6
            [ 1,-1,-1, 1,-1, 1,-1, 1], # 7
            [ 1, 1,-1, 1,-1, 1, 1, 1], # 8
            [-1, 1,-1, 1,-1, 1,-1, 1], # 9
            [-1, 1,-1, 1, 1, 1,-1,-1], # 10
            [ 1, 1,-1, 1,-1, 1, 1, 1]  # 11
        ] 

#aMapa = [   # 0  1  2  3  4  5  6  7
#            [ 0, 0, 0, 0, 0,-1, 0, 0], # 0
#            [ 0,-1,-1,-1, 0,-1, 0, 0], # 1
#            [ 0,-1, 0,-1, 0, 0, 0, 0], # 2
#            [ 0,-1, 0, 0, 0,-1,-1,-1], # 3
#            [ 0, 0, 0, 0, 0, 0, 0, 0], # 4
#            [-1,-1,-1, 0,-1,-1,-1, 0], # 5
#            [ 0, 0, 0, 0, 0, 0,-1, 0], # 6
#            [ 0,-1,-1, 0,-1, 0,-1, 0], # 7
#            [ 0, 0,-1, 0,-1, 0, 0, 0], # 8
#            [-1, 0,-1, 0,-1, 0,-1, 0], # 9
#            [-1, 0,-1, 0, 1, 0,-1,-1], # 10
#            [ 0, 0,-1, 0,-1, 0, 0, 0]  # 11
#        ] 

aEstados = [    #  0   1  2   3   4   5   6   7
                [  0,  1,  2,  3,  4, -1,  5,  6], # 0
                [  7, -1, -1, -1,  8, -1,  9, 10], # 1
                [ 11, -1, 12, -1, 13, 14, 15, 16], # 2
                [ 17, -1, 18, 19, 20, -1, -1, -1], # 3
                [ 21, 22, 23, 24, 25, 26, 27, 28], # 4
                [ -1, -1, -1, 29, -1, -1, -1, 30], # 5
                [ 31, 32, 33, 34, 35, 36, -1, 37], # 6
                [ 38, -1, -1, 39, -1, 40, -1, 41], # 7
                [ 42, 43, -1, 44, -1, 45, 46, 47], # 8
                [ -1, 48, -1, 49, -1, 50, -1, 51], # 9
                [ -1, 52, -1, 53, 54, 55, -1, -1], # 10
                [ 56, 57, -1, 58, -1, 59, 60, 61]  # 11
        ] 

##################################################################

#                   Funciones Principales

##################################################################

# Genera QTABLE -> nS = Estados , nA = Acciones
def InitQ_Table(nS,nA):
    aQ = [[0.0 for i in range(nA)] for i in range(nS)]
    return aQ

# Estado Inicial del Robot
def Init_State():
    aPosRM = [0,0]
    return aPosRM # Poicion del RObot en el mapa

def Get_Greedy_Action(nS):
    if RA.random() > Epsilon:
        a = Get_Max_Action(nS)
    else:
        a = RA.randint(0,3)
    return a

# Retorna otra accion aleatoria a partir 
# de la acción de parametro
# nA: Accion de origen
# fil: numero de fila actual
# col: numero de columna actual
def Other_Action(nA,fil,col):
    nDado_A = RA.random()
    #--------NORTE---------------
    if nA == nNORTE:
        if col > 0 and col < 7:
            if nDado_A >= 0.0 and nDado_A < 0.5:
                return nESTE
            else:
                return nOESTE
        if col == 0:
            return nESTE
        if col == 7:
            return nOESTE
    #--------SUR---------------
    if nA == nSUR:
        if col > 0 and col < 7:
            if nDado_A >= 0.0 and nDado_A < 0.5:
                return nESTE
            else:
                return nOESTE
        if col == 0:
            return nESTE
        if col == 7:
            return nOESTE
    #--------ESTE---------------
    if nA == nESTE:
        if fil > 0 and fil < 11:
            if nDado_A >= 0.0 and nDado_A < 0.5:
                return nNORTE
            else:
                return nSUR
        if fil == 0:
            return nSUR
        if fil == 11:
            return nNORTE
    #--------OESTE---------------
    if nA == nOESTE:
        if fil > 0 and fil < 11:
            if nDado_A >= 0.0 and nDado_A < 0.5:
                return nNORTE
            else:
                return nSUR
        if fil == 0:
            return nSUR
        if fil == 11:
            return nNORTE

# Samplear la mejor opcion
def Get_Max_Action(nS):
    return Q[nS].index(max(Q[nS]))

# Calcular la rewards
def Get_Rw(aPosRM):
    if aMETA == aPosRM:
        return +5
    else:
        return -1

# Q(.) = State(1), a=Accion, r=Reward, sp=State
def UpDateQ(s,a,r,sp):
    maxQ = max(Q[sp])
    Q[s][a] = (1-nALPHA) * Q[s][a] + nALPHA * (r + nGAMMA * maxQ ) 
    #Q[s][a] = Q[s][a] + nALPHA * (r + nGAMMA * maxQ - Q[s][a]) #<- Segun pseudocodigo

# Simulando navegación
def Run_Action(a,nEXITO):
    global aPosRM
    global next_state
    nDado = RA.random() # Se Tira el dado
    i = aPosRM[0] # Fila Posicion del RObot Mapa
    j = aPosRM[1] # Columna Posicion del RObot Mapa
    #if nDado >= 0.0 and nDado <= nEXITO: # Probabilidad de exito
    ############################################
    if a == nNORTE: # El robot Sube
        if i > 0: # Bordes del Mapa
            if aMapa[i-1][j] != -1:  # Hay una muralla?
                #------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nEXITO: # <-------------- Probabilidad de moverse
                    aPosRM = [i-1,j] 
                    next_state = aEstados[i-1][j]# Actualizar nuevo Estado
                    return next_state,a
                else:
                    newAction = Other_Action(a,i,j)
                    next_state = Run_Action(newAction,1)
                    return next_state,newAction
                #------------------------------------------
            else: # Si hay una muralla...
                aPosRM = [i,j] 
                next_state = aEstados[i][j]
                return next_state,a
        else: # Si esta al borde del mapa...
            aPosRM = [i,j] 
            #print(aPosRM)
            next_state = aEstados[i][j]# Actualizar nuevo Estado
            return next_state,a
    ############################################
    if a == nSUR: # El robot baja
        if i < 11: # Bordes del Mapa
            if aMapa[i+1][j] != -1:  # Hay una muralla?
                #------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nEXITO: # <-------------- Probabilidad de moverse
                    aPosRM = [i+1,j] 
                    next_state = aEstados[i+1][j]# Actualizar nuevo Estado
                    return next_state,a
                else:
                    newAction = Other_Action(a,i,j)
                    next_state = Run_Action(newAction,1)
                    return next_state,newAction
                #------------------------------------------
            else: # Si hay una muralla...
                aPosRM = [i,j] 
                next_state = aEstados[i][j]
                return next_state,a
        else: # Si esta al borde del mapa...
            aPosRM = [i,j] 
            next_state = aEstados[i][j]
            return next_state,a
    ############################################
    if a == nESTE: # El robot va a la derecha
        if j < 7: # Bordes del Mapa
            if aMapa[i][j+1] != -1:  # Hay una muralla?
                #------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nEXITO: # <-------------- Probabilidad de moverse
                    aPosRM = [i,j+1] 
                    next_state = aEstados[i][j+1]# Actualizar nuevo Estado
                    return next_state,a
                else:
                    newAction = Other_Action(a,i,j)
                    next_state = Run_Action(newAction,1)
                    return next_state,newAction
                #------------------------------------------
            else: # Si hay una muralla...
                aPosRM = [i,j] 
                next_state = aEstados[i][j]
                return next_state,a
        else: # Si esta al borde del mapa...
            aPosRM = [i,j] 
            next_state = aEstados[i][j]
            return next_state,a
    ############################################
    if a == nOESTE: # El robot va a la izquierda
        if j > 0: # Bordes del Mapa
            if aMapa[i][j-1] != -1:  # Hay una muralla?
                #------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nEXITO: # <-------------- Probabilidad de moverse
                    aPosRM = [i,j-1] 
                    next_state = aEstados[i][j-1]# Actualizar nuevo Estado
                    return next_state,a
                else:
                    newAction = Other_Action(a,i,j)
                    next_state = Run_Action(newAction,1)
                    return next_state,newAction
                #------------------------------------------
            else: # Si hay una muralla...
                aPosRM = [i,j] 
                next_state = aEstados[i][j]
                return next_state,a
        else: # Si esta al borde del mapa...
            aPosRM = [i,j] 
            next_state = aEstados[i][j]
            return next_state,a
    return next_state,a

# Q-Learning
def QL(ms = 100):
    s = aEstados[0][0]  # numero del estado [1.2.3.4....145]
    pasos = 0 ; tl_rw = 0
    for n in range(0,ms):
        a = Get_Greedy_Action(s)
        #print(a)
        sp, a = Run_Action(a,0.8)
        rw = Get_Rw(aPosRM)
        tl_rw += rw
        pasos += 1
        if type(sp)==tuple:
            sp = sp[1]
            
        UpDateQ(s,a,rw,sp)
        s = sp
        if aPosRM == aMETA:
            break
    return tl_rw, pasos

##################################################################

#                           MAIN

##################################################################

Q = InitQ_Table(62,4)

#f = open('pc.txt','w')
nl = 0
for xx in range(0,2):
    print(xx)
    for nl in range(1000):
        #print(nl)
        aPosRM = [0,0] ; total_rw = 0 ; ns = 0
        total_rw , ns = QL(1000)
        #print("Episodio = ",nl," , Steps = ",ns," , Reward = ",total_rw," , Epsilon = ", Epsilon)
        #if total_rw > 0:
            #print("Meta llegada en ",ns," pasos")
        Epsilon = Epsilon * 0.9
        sL = ''
        for n in range(62):
            sL += aList_A[Q[n].index(max(Q[n]))]
        #print(sL)
        
aOPTIMO = aEstados
# Crea un mapa con los movimientos optimos
for i in range(62):
    print(Q[i])
    #print(i," --> ",aList_A[Q[i].index(max(Q[i]))],'\n')
    for s in range(len(aOPTIMO)):#f , c = Q.index(i)
        for z in range(len(aOPTIMO[s])):
            if aOPTIMO[s][z] == i:
                aOPTIMO[s][z] = aList_A[Q[i].index(max(Q[i]))]
                continue
            if aOPTIMO[s][z] == -1:
                aOPTIMO[s][z] = '-'
                continue
    
    #print(i," --> ",aList_A[Q[i].index(max(Q[i]))],'\n')

opti = ''
for i in range(len(aOPTIMO)):
    for k in range(len(aOPTIMO[i])):
        if aOPTIMO[i][k] == -1:
            aOPTIMO[i][k] = '[-]'
        #opti += aOPTIMO[i][k]
        #if k % 16 == 0:
        #    opti += '\n'
        #if k == 0:
        #    opti = opti[::1]
    print(aOPTIMO[i])





######################################################################################

#                              PYGAME SIMULATION

######################################################################################
colEstados = len(aMapa[0])
filEstados = len(aMapa)

# Seteo de la ventana
pygame.init()
ventana = pygame.display.set_mode((colEstados*50, filEstados*50))
pygame.display.set_caption('The Intelligent Pacman')
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
            if aMapa[y][x] == -1:
                    ventana.blit(pared,[50*x,50*y])
    ventana.blit(moneda,[50*aMETA[0],50*aMETA[1]])
                    


def Mover(posActual,mov):
    x = posActual[0] * 50
    y = posActual[1] * 50
    if mov == "N":
        pacman = pygame.image.load("img/pacN.png")
        pacman = pygame.transform.scale(pacman, [50, 50])
        for i in range(11):
            y = y - 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = round(x/50)
        y = round(y/50)
        print("x = ",x," , y = ",y)
        return [x,y]
    if mov == "S":
        pacman = pygame.image.load("img/pacS.png")
        pacman = pygame.transform.scale(pacman, [50, 50])
        for i in range(10):
            y = y + 5
            #if y > 210:
            #    return [x,y-5]
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = round(x/50)
        y = round(y/50)
        print("x = ",x," , y = ",y)
        return [x,y]
    if mov == "E":
        pacman = pygame.image.load("img/pacE.png")
        pacman = pygame.transform.scale(pacman, [50, 50])
        for i in range(10):
            x = x + 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = round(x/50)
        y = round(y/50)
        print("x = ",x," , y = ",y)
        return [x,y]
    if mov == "O":
        pacman = pygame.image.load("img/pacO.png")
        pacman = pygame.transform.scale(pacman, [50, 50])
        for i in range(10):
            x = x - 5
            PrintFondo()
            ventana.blit(pacman,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        x = round(x/50)
        y = round(y/50)
        print("x = ",x," , y = ",y)
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
aMETA = [aMETA[1],aMETA[0]]

is_running = True
while is_running:
    print(posPacman)
    posPacman = Mover(posPacman,aOPTIMO[posPacman[1]][posPacman[0]])
    if posPacman == aMETA:
        while True:
            print("POTO")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

pygame.quit()