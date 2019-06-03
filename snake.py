import tkinter as tk
import random as rn
import requests
import spidev
import time
from datetime import datetime

BASE_URL = 'http://localhost:8080/'

MENU_OPTIONS = [
    'NEW GAME',
    'RANKING',
    'EXIT'
]

spi = spidev.Spidev()
spi.open(0, 1)
spi.mode=0b00
spi.lsbfirst=False
spi.max_speed_hz=25000

def get_list_of_the_best_players():
    return requests.get(url = BASE_URL + '/rank/sorted').json()

def save_game__to_database(login: str, points: int):
    payload = {'login': login,
        'date': datetime.now(),
        'points': points }

    return requests.post(url = BASE_URL + '/rank', data = payload)

def print_menu(current_position_index: int):
    options = MENU_OPTIONS[:]
    options[current_position_index] = MENU_OPTIONS[current_position_index] + ' <--'

    [print(x) for x in options]


dt = 100
def create_game():
	window = tk.Tk() 
	c_draw = tk.Canvas(window, width = 600, height = 400) 
	c_draw.pack() 

	class Snake:

		def __init__(self, width, height):

			self.width = int(width)

			self.height = int(height)

			self.msnake = [[self.width / 2, self.height / 2], [self.width / 2 + 1, self.height / 2], [self.width / 2 + 2, self.height / 2]] # snake elements

			self.move = 0 

			self.tmove = [[0,1],[1,0],[0,-1],[-1,0]] 

			self.size = 10

			self.col = False 

			self.food = [rn.randint(1, self.width - 2), rn.randint(1, self.height - 2)]

		def drawBox(self,x, y, color = 'green'):

			c_draw.create_rectangle([x, y, x + self.size, y + self.size], fill=color)

		def draw(self):

			c_draw.delete("all")

			if self.col:

				c_draw.create_text([self.width / 2 * self.size, self.height / 2 * self.size], text = "Przegrałeś")

			else:

				for i in range(self.width):

					self.drawBox(i * self.size, 0)

					self.drawBox(i * self.size, (self.height - 1) * self.size)

				for i in range(1, self.height):

					self.drawBox(0, i * self.size)

					self.drawBox((self.width - 1) * self.size, i * self.size)

				for i in self.msnake:

					self.drawBox(i[0] * self.size, i[1] * self.size)

				self.drawBox(self.food[0] * self.size, self.food[1] * self.size, color = 'red')

		def eat(self): 

			if self.msnake[0][0] == self.food[0] and self.msnake[0][1] == self.food[1]: 

				self.msnake.append([0,0]) 

				self.food = [rn.randint(1, self.width - 2), rn.randint(1, self.height - 2)]

		def move_snake(self):

			for i in range(len(self.msnake) - 1,0,-1):

				self.msnake[i][0] = self.msnake[i-1][0]

				self.msnake[i][1] = self.msnake[i-1][1]

			self.msnake[0][0] += self.tmove[self.move][0]

			self.msnake[0][1] += self.tmove[self.move][1]

			self.colision()

			self.eat()

			self.draw()

		def turnLeft(self):

			self.move = (self.move + 1) % len(self.tmove)

		def turnRight(self):

			self.move = (self.move - 1) if self.move > 0 else len(self.tmove) - 1

		def colision(self):

			if self.msnake[0][0] == 0 or self.msnake[0][1] == 0 or self.msnake[0][0] == self.width - 1 or self.msnake[0][1] == self.height - 1:

				self.col = True

			for i in self.msnake[1:]: 

				if self.msnake[0][0] == i[0] and self.msnake[0][1] == i[1]:

					self.col = True

		def reset(self):

			self.col = False

			self.msnake = [[self.width / 2, self.height / 2], [self.width / 2 + 1, self.height / 2], [self.width / 2 + 2, self.height / 2]] # snake elements

			self.move = 0 

			self.tmove = [[0,1],[1,0],[0,-1],[-1,0]] 

			self.size = 10

			self.col = False 

			self.food = [rn.randint(1, self.width - 2), rn.randint(1, self.height - 2)]

			window.after(dt, move)

	

	sn = Snake(600 / 10, 400 / 10)

	return window, sn

def move():
    snake.move_snake()

    if not snake.col:
        window.after(dt, move)
    else:
        window.quit()

def game_pad():
    response = spi.xfer([0x00, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    return response[3:4]

def display_rank():
    players = get_list_of_the_best_players()
    print(players)

if __name__ == '__main__':
    radix = 0
    while radix != 3:
        if window:
            window.quit()
        print_menu(radix)
        radix = int(input())
        if radix == 1:
            window, snake = create_game()
            window.after(dt, move)
            window.mainloop()
        elif radix == 2:
            #display rank
            print(display_rank())

        elif radix == 3:
            radix = 3
        else:
            radix = 0

