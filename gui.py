from tkinter import Text, Tk

from screeninfo import get_monitors


class GUI:
    def __init__(self, width=0.2, height=0.8):
        width *= get_monitors()[0].width
        height *= get_monitors()[0].height
        self.__root = Tk()
        self.__root.geometry(f"{int(width)}x{int(height)}")
        self.__chatbox = Text(self.__root, height=5, width=52)
        self.__chatbox.insert("end", "Hello.....")
        self.__chatbox.config(state="disabled")
        self.__chatbox.pack()

    def start(self):
        self.__root.mainloop()

    def add_line(self, line):
        self.__chatbox.insert("end", "\n" + line)


if __name__ == "__main__":
    gui = GUI()
    gui.start()
