import pygame
import numpy as np
from client import client_websocket as cw



class InputField:
    def __init__(self,pos_x,pos_y,width=60,height=40):
        self.x= pos_x
        self.y=pos_y
        self.field =  pygame.Rect(pos_x,pos_y,width,height)
        self.clr_lock = pygame.Color('lightskyblue3')
        self.clr_edit = pygame.Color('dodgerblue2')
        self.color = self.clr_lock
        self.active = False
        self.text=''

class GridGUI:
    def __init__(self, title="Init Dim GRID",
                 width=50, height=50, margin=2,
                 x_dim=10, y_dim=10):
        self.width = width
        self.height = height
        self.margin = margin
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.start = None
        self.goal = None

        self.gui_grid = np.ones((x_dim, y_dim, 3), dtype=np.uint8) * 255

        pygame.init()
        window_size = [(width + margin) * y_dim + margin,
                    (height + margin) * x_dim + margin+60]
        
        # после вычисления window_size
        win_w, win_h = window_size

        # кнопка OK внизу слева
        self.ok_btn = InputField(10, win_h - 50, 60, 40)
        self.ok_btn.text = "OK"

        # кнопка CLEAR рядом
        self.clear_btn = InputField(80, win_h - 50, 120, 40)
        self.clear_btn.text = "CLEAR"

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(title)
        pygame.font.SysFont('Comic Sans MS', 36)
        self.font = pygame.font.Font(None, 48)
        self.done = False
        self.clock = pygame.time.Clock()

    def run(self):
        
        while not self.done:
            m_pos = pygame.mouse.get_pos()
            m_click = pygame.mouse.get_pressed()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    raise KeyboardInterrupt("GUI closed by user")

                elif pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (self.width + 2)
                    row = pos[1] // (self.height + 2)
                    if row >= self.x_dim or column >= self.y_dim:
                        print("Clicked outside grid")
                        continue
                    
                    if self.start is None:
                        self.start = (row, column)
                        self.gui_grid[row][column] = [255, 0, 0]  # Green for start
                        print(f"Start position set to: {self.start}")
                    elif self.start == (row, column):
                        print("Start position already set here.")
                        continue
                    elif self.goal is None:
                        self.goal = (row, column)
                        self.gui_grid[row][column] = [0, 255, 0]  # Red for goal
                        print(f"Goal position set to: {self.goal}")
                        
            self.screen.fill((0, 0, 0))
            for row in range(self.gui_grid.shape[0]):
                for column in range(self.gui_grid.shape[1]):
                    color = self.gui_grid[row][column]
                    pygame.draw.rect(self.screen,
                                        color,
                                        [(self.width + 2) * column + 2,
                                        (self.height + 2) * row + 2,
                                        self.width,
                                        self.height])
                    

            okBtn_is_hovered = self.ok_btn.field.collidepoint(m_pos)
            clearBtn_is_hovered = self.clear_btn.field.collidepoint(m_pos)

            if okBtn_is_hovered and m_click[0]:  # Left mouse button
                print("Ok Button clicked!")
                if self.start and self.goal:
                    print(f"Final Start: {self.start}, Goal: {self.goal}")
                    cw.send_points(self.start,self.goal)
                    self.done = True

            if clearBtn_is_hovered and m_click[0]: 
                print("Clear Button clicked!")
                self.start = None
                self.goal = None
                self.gui_grid = np.ones((self.x_dim, self.y_dim, 3), dtype=np.uint8) * 255

            ok_btn_text = self.font.render(self.ok_btn.text,True,(0,0,0))
            pygame.draw.rect(self.screen, self.ok_btn.clr_edit if okBtn_is_hovered else self.ok_btn.clr_lock, self.ok_btn.field)
            self.screen.blit(ok_btn_text, (self.ok_btn.x, self.ok_btn.y))
            
            clr_btn_text = self.font.render(self.clear_btn.text,True,(0,0,0))
            pygame.draw.rect(self.screen, self.clear_btn.clr_edit if clearBtn_is_hovered else self.clear_btn.clr_lock, self.clear_btn.field)
            self.screen.blit(clr_btn_text, (self.clear_btn.x, self.clear_btn.y))


            self.clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    gui = GridGUI(x_dim=10, y_dim=10)
    gui.run()
    pygame.quit()