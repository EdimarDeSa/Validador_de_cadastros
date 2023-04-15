from tkinter import Toplevel, Tk, Text, Scrollbar
from tkinter.ttk import Progressbar


class LogPanel(Toplevel):
    def __init__(self, master: Tk, kw: dict):
        kw['state'] = 'disabled'
        kw['wrap'] = 'word'
        Toplevel.__init__(self, master)
        self.geometry(f'800x500+{self.winfo_rootx()+600}+{self.winfo_rooty()}')
        
        self._tela1 = Text(master=self, **kw)
        scrollbar1 = Scrollbar(master=self, command=self._tela1.yview)
        self._tela1.place(relx=0, rely=0, relheight=1, relwidth=0.485)
        self._tela1.configure(yscrollcommand=scrollbar1.set)
        scrollbar1.place(relx=0.485, rely=0, relheight=1, relwidth=0.015)

        self._tela2 = Text(master=self, **kw)
        scrollbar2 = Scrollbar(master=self, command=self._tela2.yview)
        self._tela2.place(relx=0.5, rely=0, relheight=1, relwidth=0.485)
        self._tela2.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.place(relx=0.985, rely=0, relheight=1, relwidth=0.015)
        
    def log_impressora(self, info, screen_number: int):
        telas = {
            0: self._tela1,
            1: self._tela2
        }
        tela = telas[screen_number]
        tela.config(state='normal')
        tela.insert('end', f'{info}\n')
        tela.config(state='disabled')
    
    def log_clear(self, screen_number: int):
        tela = None
        if not screen_number:
            tela = self._tela1
        else:
            tela = self._tela2
        tela.config(state='normal')
        tela.delete('0.0', 'end')
        tela.config(state='disabled')
