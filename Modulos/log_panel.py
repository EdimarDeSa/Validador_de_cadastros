from Modulos import Toplevel, Tk, Text, Scrollbar


class LogPanel:
    def __init__(self, master: Tk, kw: dict):
        kw.pop('master')
        kw['state'] = 'disabled'
        kw['wrap'] = 'word'
        top_level = Toplevel(master)
        top_level.geometry(f'800x500+{top_level.winfo_rootx()+600}+{top_level.winfo_rooty()}')
        
        self._tela1 = Text(master=top_level, **kw)
        scrollbar1 = Scrollbar(master=top_level, command=self._tela1.yview)
        self._tela1.place(relx=0, rely=0, relheight=1, relwidth=0.485)
        self._tela1.configure(yscrollcommand=scrollbar1.set)
        scrollbar1.place(relx=0.485, rely=0, relheight=1, relwidth=0.015)

        self._tela2 = Text(master=top_level, **kw)
        scrollbar2 = Scrollbar(master=top_level, command=self._tela2.yview)
        self._tela2.place(relx=0.5, rely=0, relheight=1, relwidth=0.485)
        self._tela2.configure(yscrollcommand=scrollbar2.set)
        scrollbar2.place(relx=0.985, rely=0, relheight=1, relwidth=0.015)
        
    def log_impressora(self, info, screen_number: int):
        tela = None
        if not screen_number:
            tela = self._tela1
        else:
            tela = self._tela2
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
