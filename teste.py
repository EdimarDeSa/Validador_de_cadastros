# from tkinter import *
# import time
# from tkinter.ttk import Notebook
#
#
# ws=Tk()
#
# ws.config(width=330,height=250)
#
# notebook=Notebook(ws)
# notebook.place(x=0,y=0)
#
# Tablist=[]
# i=0
# while i<6:
#      Tablist.append(Frame(ws))
#      Tablist[i].config(width=330,height=200,background='white')
#      i+=1
#
# i=0
# while i<6:
#     notebook.add(Tablist[i],text='tab'+str(i))
#     i+=1
#
# def LoopTabs():
#     i=0
#     while i<6:
#          notebook.select(i)
#          time.sleep(2)
#          i+=1
#
# button=Button(ws,text='Click here',command=LoopTabs)
# button.place(x=20,y=180)
# ws.mainloop()
#
# import winreg
# import tkinter as tk
#
#
# def is_dark_mode_enabled():
#     try:
#         # Abre a chave de registro relacionada ao modo escuro no Windows 10
#         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
#         value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
#
#         # 1 significa que o modo claro está ativado, 0 significa que o modo escuro está ativado
#         return value == 0
#     except Exception as e:
#         print("Erro ao verificar o modo escuro:", str(e))
#         return False
#
#
# # Verifica se o modo escuro está ativado
# if is_dark_mode_enabled():
#     theme = "dark"
# else:
#     theme = "light"
#
# # Crie e configure sua janela do Tkinter com o tema apropriado
# root = tk.Tk()
# root.title("Exemplo de Tkinter com base no modo escuro")
# label = tk.Label(root, text='Testando o tema:')
# label.pack(fill='x', ipady=10)
# root.geometry("400x300")
#
# if theme == "dark":
#     # Use o tema escuro
#     label.configure(bg="black", fg="white")
# else:
#     # Use o tema claro
#     label.configure(bg="white", fg="black")
#
# # Adicione widgets à janela aqui
#
# root.mainloop()

from ttkbootstrap import *

def ativa_dialog_box():
    s = Image(root, [200, 400])
    print(s)


icon = 'C:/Users/Edimar/Documents/GitHub/Validador_de_cadastros/icons/icons8-lottery-50.png'
root = Window(title='Testes', iconphoto=icon, size=(400, 400))
root.place_window_center()

Label(text='Teste de fonte selector', name='bt_1').pack(pady=50, anchor='center')
bt = Button(text='Click aqui', command=ativa_dialog_box)
bt.pack(pady=50, anchor='center')

root.mainloop()