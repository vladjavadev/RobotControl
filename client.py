from client import gui


if __name__ == "__main__":
    try:
        gui.run_gui()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")