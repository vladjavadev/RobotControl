import pygame
from client import client_websocket as cw
from utils.connect_dto import Connection as con
import time
import threading

def check_loop(gui):
    while gui.running:
        cw.get_connection(cw.con)
        time.sleep(0.5)

class GUI_ConnectServer:
    def __init__(self, 
                 title="Connect Server", 
                 width=400, 
                 height=600,
                 x_dim=10,
                 y_dim=10):
        self.width = width
        self.height = height
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.text=cw.con.get_status()
        self.rect = pygame.Rect(50,230,200,150)
        self.running = True

        pygame.init()
        window_size = [width,height]
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(title)
        pygame.font.SysFont('Comic Sans MS', 36)
        self.font = pygame.font.Font(None, 48)

        self.clock = pygame.time.Clock()

    def run_game(self):
        thread = threading.Thread(target=check_loop, daemon=True,args=(self,))
        thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    self.running = False
                

            status = cw.con.get_status()

            self.screen.fill((255, 255, 255))
            text_connection = self.font.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_connection, (self.rect.x,self.rect.y))
            pygame.draw.rect(self.screen, (0,0,0), self.rect, 2)
            self.clock.tick(30)
            pygame.display.flip()
            if status=="connected":
                self.running = False
                time.sleep(2.0)


