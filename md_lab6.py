import numpy as np
from PIL import Image
import pygame
import random

# Wczytanie obrazu
image = Image.open("obrazek.bmp").convert("RGB")

# Konwersja obrazu na tablicę numpy
img_array = np.array(image)

board_height = img_array.shape[0]   # wysokość planszy, czyli liczbę wierszy kwadratów na planszy
board_width = img_array.shape[1]    # szerokość planszy, czyli liczbę kolumn kwadratów na planszy

size = 7    # rozmiar małego kwadratu
matrix= []
matrix = [[[0,0,0,0] for x in range(board_width)] for y in range(board_height)]

number_of_squares = 1000

tick = 0

def generate_random_position():
    return random.randint(0, 24), random.randint(0, board_height - 1)

def initialize_matrix():
    for i in range(number_of_squares):
        x, y = generate_random_position()
        matrix[y][x] = [0, 0, 0, 0]
        dir = random.randint(0,3)
        matrix[y][x][dir] = 1

#matrix[2][2] = [0,1,0,0]
#matrix[2][8] = [0,0,0,1]

initialize_matrix()

new_matrix = [[[0,0,0,0] for x in range(board_width)] for y in range(board_height)]

def rysuj():
    temp = np.copy(image)
    for x in range(board_width):
        for y in range(board_height):
            if np.all(img_array[x][y] == [0,0,0]):
                color = [0,0,0]
            else:    
                color = [255,255,255]
                for i in range(4):
                    if matrix[x][y][i] == 1:
                        color = [0,0,255]
                        break
            
            pygame.draw.rect(screen, color, (y*size, x*size, size, size))
            temp[x,y] = color
    img_save =  Image.fromarray(temp)
    img_save.save(f"./gif/frame{tick}.bmp")

Direction = {
    0:[0,-1],   #gora
    1:[1,0],    #prawo
    2:[0,1],    #dol
    3:[-1,0]    #lewo
}

def chodzenie():
    for x in range(board_width):
        for y in range(board_height):
            if np.all(img_array[x][y] != [0,0,0]):
                for i in range(4):
                    if matrix[x][y][i] > 0:
                        #print(f"Przed ruchem: Pozycja ({x}, {y}), Kierunek: {i}")
                        if np.all(img_array[(x+Direction[i][1])][(y+Direction[i][0])] == [0,0,0]): 
                            new_matrix[(x - Direction[i][1])][(y - Direction[i][0])][(i+2)%4] += matrix[x][y][i]
                        else:  
                            new_matrix[(x + Direction[i][1])][(y + Direction[i][0])][i] += matrix[x][y][i]
                        matrix[x][y][i] = 0

    for x in range(board_width):
        for y in range(board_height):
            matrix[x][y]=[0,0,0,0]
            if np.all(img_array[x][y] != [0,0,0]): 
                for i in [0,1]:
                    if new_matrix[x][y][i] + new_matrix[x][y][i+2] >= 2:
                        if new_matrix[x][y][i] == 0:
                            new_matrix[x][y][i+2] -= 2
                        elif new_matrix[x][y][i+2] == 0:
                            new_matrix[x][y][i] -= 2
                        else:
                            new_matrix[x][y][i] -= 1
                            new_matrix[x][y][i+2] -= 1
                        matrix[x][y][i+1] += 1
                        matrix[x][y][(i+3)%4] += 1

                for i in range(4):
                    if new_matrix[x][y][i] > 0:  
                        matrix[x][y][i] += new_matrix[x][y][i]
                        new_matrix[x][y][i]= 0    

                new_matrix[x][y] = [0,0,0,0] 
             


if __name__ == "__main__":
 
    pygame.init()
    global screen
    screen = pygame.display.set_mode((board_width*size, board_height*size))  
    # wyświetlenie okna gry
    pygame.display.set_caption("LGA")
    clock = pygame.time.Clock()
    run = True
    # pętla główna

    rysuj()
    while run:
        clock.tick(60)

        chodzenie()
        rysuj()        
        tick += 1
        pygame.time.delay(1) 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed() 


        pygame.display.flip()
