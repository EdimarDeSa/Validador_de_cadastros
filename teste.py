from ttkbootstrap import *


class CustomNoteBook(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self._quadro_de_botoe = Frame(self, style=kwargs.get('style'), border=DOTBOX)
        self._quadro_de_botoe.pack(fill=X, expand=True, side=TOP)


if __name__ == '__main__':
    root = Window()
    CustomNoteBook(root)
    root.mainloop()