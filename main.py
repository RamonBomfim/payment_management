from tkinter import *


class Home:
    def __init__(self):
        self.window = Tk()
        self.window.title("Payment Management")
        self.window.minsize(width=600, height=600)
        self.window.config(bg="#609")
        self.window.resizable(0, 0)

        self.bar_menu = Frame(self.window, bg="#3b3b3b", width=100)
        self.bar_menu.pack(fill="y", side="left")

        self.home_button = Button(self.bar_menu, text="  Home  ", bd=0, bg="#609",width=13, height=6, command=None)
        self.home_button.pack()

        self.management_button = Button(self.bar_menu, text="  Management  ", bd=1, bg="#3b3b3b",
                                        width=13, height=6, command=None)
        self.management_button.pack()

        self.new_client_button = Button(self.bar_menu, text="  New Client  ", bd=1,
                                        bg="#3b3b3b", width=13, height=6, command=None)
        self.new_client_button.pack()

        self.settings_button = Button(self.bar_menu, text="  Settings  ", bd=1,
                                      bg="#3b3b3b", width=13, height=6, command=None)
        self.settings_button.pack(side="bottom")

        self.body_title = Label(self.window, text="Olá,\nSeja bem-vindo", font="Arial 40 bold",
                                justify="left", anchor="e", pady=30)
        self.body_title.pack()

        self.body_text = Label(self.window, text="Este é um sistema de gerenciamento\nde mensalidade.\n",
                               font="Arial 20", justify="left")
        self.body_text.pack()

        self.body_text_complement = Label(self.window, text="Aqui você poderá gerenciar as mensalidades,\n"
                                                            "assim como adicionar novos clientes,\n"
                                                            "gerenciar os clientes já existentes\n"
                                                            "e muito mais!\n",
                                          font="Arial 17", justify="left")
        self.body_text_complement.pack()

        self.butotn_start = Button(self.window, text="Start!", bg="orange", width=15,
                                   pady=10, command=None).pack()

        self.window.mainloop()


Home()
