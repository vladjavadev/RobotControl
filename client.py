from client import grid_gui,gui_init_dim
from client import client_websocket as cw


if __name__ == "__main__":
    try:
        init_gui = gui_init_dim.Gui_InitDim()
        init_gui.run_game()
        dim = (cw.dim_grid.x_dim, cw.dim_grid.y_dim)
        main_gui = grid_gui.Animation(x_dim=dim[0], y_dim=dim[1])
        main_gui.run_game()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")