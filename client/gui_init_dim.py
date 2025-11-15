import pygame
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

class Gui_InitDim:
    def __init__(self, 
                 title="Set Dimension", 
                 width=400, 
                 height=600,
                 x_dim=10,
                 y_dim=10):
        self.width = width
        self.height = height
        self.x_dim = x_dim
        self.y_dim = y_dim


        self.running = True

        pygame.init()
        window_size = [width,height]
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(title)
        pygame.font.SysFont('Comic Sans MS', 36)
        self.font = pygame.font.Font(None, 48)

        self.inputX = InputField(50,80,80,80)
        self.inputY  = InputField(150,80,80,80)
        self.sX = InputField(50,200,60,40)
        self.sY = InputField(50,300,60,40)
        self.gX = InputField(150,200,60,40)
        self.gY = InputField(150,300,60,40)
        self.input_ok_btn = InputField(160,400,60,40)
        self.clock = pygame.time.Clock()

    def run_game(self):
        inputX = self.inputX
        inputY = self.inputY
        sX=self.sX
        sY=self.sY
        gX=self.gX
        gY=self.gY
        okBtn = self.input_ok_btn
        okBtn.text = "OK"
        while self.running:
            m_pos = pygame.mouse.get_pos()
            m_click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    self.running = False
                
                elif pygame.mouse.get_pressed()[0]:
                    
                    if inputX.field.collidepoint(m_pos):
                        inputX.active = True
                        inputY.active = False
                        sX.active = False
                        sY.active = False
                        gX.active = False
                        gY.active = False

                    elif inputY.field.collidepoint(m_pos):
                        inputY.active = True
                        inputX.active = False
                        sX.active = False
                        sY.active = False
                        gX.active = False
                        gY.active = False
                    elif sX.field.collidepoint(m_pos):
                        inputY.active = False
                        inputX.active = False
                        sX.active = True
                        sY.active = False
                        gX.active = False
                        gY.active = False
                    elif sY.field.collidepoint(m_pos):
                        inputY.active = False
                        inputX.active = False
                        sX.active = False
                        sY.active = True
                        gX.active = False
                        gY.active = False
                    elif gX.field.collidepoint(m_pos):
                        inputY.active = False
                        inputX.active = False
                        sX.active = False
                        sY.active = False
                        gX.active = True
                        gY.active = False
                    elif gY.field.collidepoint(m_pos):
                        inputY.active = False
                        inputX.active = False
                        sX.active = False
                        sY.active = False
                        gX.active = False
                        gY.active = True
                    else:
                        inputX.active = False
                        inputY.active = False
                        sX.active = False
                        sY.active = False
                        gX.active = False
                        gY.active = False


                    inputX.color = inputX.clr_edit if inputX.active else inputX.clr_lock
                    inputY.color = inputY.clr_edit if inputY.active else inputY.clr_lock
                    inputY.color = inputY.clr_edit if inputY.active else inputY.clr_lock

                    sX.color = sX.clr_edit if sX.active else sX.clr_lock
                    sY.color = sY.clr_edit if sY.active else sY.clr_lock
                    gX.color = gX.clr_edit if gX.active else gX.clr_lock
                    gY.color = gY.clr_edit if gY.active else gY.clr_lock


                elif event.type == pygame.KEYDOWN:
                    if inputX.active:
                        if event.key == pygame.K_RETURN:
                            print(f"Введено: {inputX.text}")
                            inputX.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            inputX.text = inputX.text[:-1]
                        else:
                            if event.unicode.isdigit():
                                inputX.text += event.unicode
                    elif inputY.active:
                        if event.key == pygame.K_RETURN:
                            print(f"Введено: {inputY.text}")
                            inputY.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            inputY.text = inputY.text[:-1]
                        else:
                            if event.unicode.isdigit():
                                inputY.text += event.unicode

                    for field in [sX, sY, gX, gY]:
                        if field.active:
                            if event.key == pygame.K_RETURN:
                                print(f"Введено: {field.text}")
                                field.text = ''
                            elif event.key == pygame.K_BACKSPACE:
                                field.text = field.text[:-1]
                            else:
                                if event.unicode.isdigit():
                                    field.text += event.unicode

            self.screen.fill((255, 255, 255))
            text_inputX = self.font.render(inputX.text, True, (0, 0, 0))
            text_inputY = self.font.render(inputY.text, True, (0, 0, 0))
            self.screen.blit(text_inputX, (inputX.x,inputX.y))
            self.screen.blit(text_inputY, (inputY.x,inputY.y))

            text_sX = self.font.render(sX.text, True, (0, 0, 0))
            text_sY = self.font.render(sY.text, True, (0, 0, 0))
            text_gX = self.font.render(gX.text, True, (0, 0, 0))
            text_gY = self.font.render(gY.text, True, (0, 0, 0))

            self.screen.blit(text_sX, (sX.x, sX.y))
            self.screen.blit(text_sY, (sY.x, sY.y))
            self.screen.blit(text_gX, (gX.x, gX.y))
            self.screen.blit(text_gY, (gY.x, gY.y))
            
            is_hovered = okBtn.field.collidepoint(m_pos)

                # Check click
            if is_hovered and m_click[0]:  # Left mouse button
                print("Button clicked!")
                x_dim = int(inputX.text)
                y_dim = int(inputY.text)
                start = (int(sX.text),
                         int(sY.text))
                goal = (int(gX.text),
                         int(gY.text))
                cw.dim_grid.x_dim = x_dim
                cw.dim_grid.y_dim = y_dim

                cw.send_dim_grid((x_dim, y_dim),start,goal)
                self.running = False

            # Draw
            btn_text = self.font.render(okBtn.text,True,(0,0,0))
            pygame.draw.rect(self.screen, okBtn.clr_edit if is_hovered else okBtn.clr_lock, okBtn.field)
            self.screen.blit(btn_text, (okBtn.x, okBtn.y))


            pygame.draw.rect(self.screen, inputX.color, inputX.field, 2)
            pygame.draw.rect(self.screen, inputY.color, inputY.field, 2)

            pygame.draw.rect(self.screen, sX.color, sX.field, 2)
            pygame.draw.rect(self.screen, sY.color, sY.field, 2)
            pygame.draw.rect(self.screen, gX.color, gX.field, 2)
            pygame.draw.rect(self.screen, gY.color, gY.field, 2)
            self.clock.tick(30)
            pygame.display.flip()


if __name__ == "__main__":
    gui_dim = Gui_InitDim(x_dim = 20, y_dim=20)                
    gui_dim.run_game()