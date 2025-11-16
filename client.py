from client import grid_gui,gui_init_dim,gui_conect_server
from client import client_websocket as cw


if __name__ == "__main__":
    try:
        connect_gui = gui_conect_server.GUI_ConnectServer()
        connect_gui.run_game()
        init_gui = gui_init_dim.Gui_InitDim()
        init_gui.run_game()
        dim = (cw.dim_grid.x_dim, cw.dim_grid.y_dim)
        main_gui = grid_gui.Animation(x_dim=dim[0], y_dim=dim[1])
        main_gui.run_game()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")