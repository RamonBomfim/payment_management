from tkinter import *


class Main:
    def __init__(self):
        self.window = Tk()
        self.window_config()
        self.frames()

        self.icons()

        self.widgets_bar_menu()
        self.widgets_body()

        self.window.mainloop()

    def window_config(self):
        self.window.title("Gerenciador de mensalidade")
        self.window.geometry("700x600+350+50")
        self.window.resizable(0, 0)
        self.window.config(bg="#3b3b3b")

    def frames(self):
        self.bar_menu = Frame(self.window, bg="#d3d3d3")
        self.bar_menu.place(relx=0, rely=0, relwidth=0.12, relheight=1)

        self.body = Frame(self.window, bg="#3b3b3b", bd=4,
                          highlightbackground="#a9a9a9", highlightthickness=3)
        self.body.place(relx=0.12, rely=0, relwidth=0.88, relheight=1)

    def icons(self):
        self.icon_home = PhotoImage(file="assets/home.png")
        self.icon_client = PhotoImage(file="assets/cliente_b.png")
        self.icon_new = PhotoImage(file="assets/adicionar.png")
        self.icon_close = PhotoImage(file="assets/exit.png")
        self.icon_manager = PhotoImage(file="assets/engrenagem.png")
        self.icon_edit = PhotoImage(file="assets/editar.png")
        self.icon_delete = PhotoImage(file="assets/excluir.png")
        self.icon_pay = PhotoImage(file="assets/pagar.png")
        self.icon_search = PhotoImage(file="assets/lupa.png")

    def widgets_bar_menu(self):
        self.home_button = Button(self.bar_menu, image=self.icon_home,
                                  bg="#d3d3d3", bd=0, command=None)
        self.home_button.place(relx=0, rely=0.03, relwidth=1)
        self.home_button.configure(background="#a9a9a9")

        self.clients_button = Button(self.bar_menu, image=self.icon_client,
                                     bg="#d3d3d3", bd=0, command=None)
        self.clients_button.place(relx=0, rely=0.18, relwidth=1)

        self.new_button = Button(self.bar_menu, image=self.icon_new,
                                 bg="#d3d3d3", bd=0, command=None)
        self.new_button.place(relx=0, rely=0.33, relwidth=1)

        self.close_button = Button(self.bar_menu, image=self.icon_close,
                                   bg="#d3d3d3", bd=0, command=None)
        self.close_button.place(relx=0, rely=0.85, relwidth=1)

    def widgets_body(self):
        self.header = Label(self.body, text="Seja bem-vindo",
                            bg="#3b3b3b", fg="#d3d3d3",
                            font="Arial 60", justify="left")
        self.header.place(relx=0.035, rely=0.1, relwidth=0.95)

        self.header = Label(self.body, text="Esse é um sistema de gerenciamento de mensalidades,\n"
                                            "onde você poderá fazer o controle de pagamento das\n"
                                            "mensalidades do seu negócio. Além de poder adicionar\n"
                                            "novos clientes, editar os já existentes, enviar emails\n"
                                            "e muito mais!",
                            bg="#3b3b3b", fg="#d3d3d3",
                            font="Arial 17", justify="left")
        self.header.place(relx=0.035, rely=0.5, relwidth=0.95)



Main()
