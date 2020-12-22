from tkinter import *
from tkinter import ttk
import psycopg2


class Funcionalidades:
    def clean_forms(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.block_entry.delete(0, END)
        self.number_entry.delete(0, END)
        self.phone_entry.delete(0, END)

    def clean_forms2(self):
        self.pay_clientid_entry.delete(0, END)
        self.date_pay_entry.delete(0, END)
        self.value_pay_entry.delete(0, END)
        self.penalty_pay_entry.delete(0, END)

    def connect_db(self):
        self.conn = psycopg2.connect(
            database='payment_manager',
            user='postgres',
            password='941215',
            host='localhost',
            port='5433'
        )

        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def variables(self):
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.block = self.block_entry.get()
        self.number = self.number_entry.get()
        self.phone = self.phone_entry.get()

    def new_client(self):
        self.variables()
        self.connect_db()

        self.cursor.execute(f"""
            INSERT INTO cliente (nome, email, quadra, num_casa, telefone)
            VALUES ('{self.name}', '{self.email}', '{self.block}', '{self.number}', '{self.phone}')""")
        self.conn.commit()
        self.disconnect_db()
        self.clean_forms()

    def new_payment(self):
        self.pay_clientid = self.pay_clientid_entry.get()
        self.date_pay = self.date_pay_entry.get()
        self.value_pay = self.value_pay_entry.get()
        self.penalty_pay = self.penalty_pay_entry.get()
        self.connect_db()

        self.cursor.execute(f"""
            INSERT INTO mensalidade (clienteid, datapago, valorpago, multa)
            VALUES ('{self.pay_clientid}', '{self.date_pay}', '{self.value_pay}', '{self.penalty_pay}')""")
        self.conn.commit()
        self.disconnect_db()
        self.clean_forms2()

    def show_list(self):
        self.clients_list.delete(*self.clients_list.get_children())
        self.connect_db()
        self.cursor.execute("""
            SELECT clienteid, nome, email, quadra, num_casa, telefone
            FROM cliente
            ORDER BY quadra, nome ASC""")
        lista = self.cursor.fetchall()

        for i in lista:
            self.clients_list.insert("", END, values=i)

        self.disconnect_db()

    def show_payments(self):
        self.payments_list.delete(*self.payments_list.get_children())
        self.clientid = self.clientid_entry.get()
        self.connect_db()
        self.cursor.execute(f"""
            SELECT cliente.clienteid, mensalidade.mensalidadeid, mensalidade.datapago, 
            mensalidade.valorpago, mensalidade.multa
            FROM cliente
            INNER JOIN mensalidade
            ON cliente.clienteid = '{self.clientid}' AND mensalidade.clienteid = '{self.clientid}'""")
        lista = self.cursor.fetchall()

        for i in lista:
            self.payments_list.insert("", END, values=i)

        self.disconnect_db()

    def search_id(self):
        self.variables()
        self.clientid = self.clientid_entry.get()
        self.clean_forms()
        self.connect_db()

        self.clientid_entry.get()
        self.cursor.execute(f"""
            SELECT clienteid, nome, email, quadra, num_casa, telefone
            FROM cliente
            WHERE clienteid = '{self.clientid}'""")
        search_id = self.cursor.fetchall()

        for i in search_id:
            self.name_entry.insert(END, i[1])
            self.email_entry.insert(END, i[2])
            self.block_entry.insert(END, i[3])
            self.number_entry.insert(END, i[4])
            self.phone_entry.insert(END, i[5])

        self.disconnect_db()

    def search_paymentid(self):
        self.payid = self.payid_entry.get()
        self.date = self.date_entry.get()
        self.value = self.value_entry.get()
        self.penalty = self.penalty_entry.get()
        self.connect_db()

        self.payid_entry.get()
        self.cursor.execute(f"""
                    SELECT mensalidadeid, datapago, valorpago, multa
                    FROM mensalidade
                    WHERE mensalidadeid = '{self.payid}'""")
        search_payid = self.cursor.fetchall()

        for i in search_payid:
            self.date_entry.insert(END, i[1])
            self.value_entry.insert(END, i[2])
            self.penalty_entry.insert(END, i[3])

        self.disconnect_db()

    def delete_client(self):
        self.variables()
        self.connect_db()

        self.cursor.execute(f"""
            DELETE FROM cliente WHERE nome = '{self.name}'""")
        self.conn.commit()

        self.disconnect_db()
        self.show_list()
        self.clean_forms()

    def delete_payment(self):
        self.payid = self.payid_entry.get()
        self.date = self.date_entry.get()
        self.value = self.value_entry.get()
        self.penalty = self.penalty_entry.get()
        self.connect_db()

        self.cursor.execute(f"""
            DELETE FROM mensalidade WHERE mensalidadeid = '{self.payid}'""")
        self.conn.commit()

        self.disconnect_db()
        self.show_payments()
        self.clean_forms()

    def update_client(self):
        self.variables()
        self.clientid = self.clientid_entry.get()
        self.connect_db()

        self.cursor.execute(f"""
            UPDATE cliente
            SET nome = '{self.name}', 
            email = '{self.email}', 
            quadra = '{self.block}', 
            num_casa = '{self.number}', 
            telefone = '{self.phone}'
            WHERE clienteid = '{self.clientid}'""")

        self.conn.commit()
        self.disconnect_db()
        self.show_list()
        self.clean_forms()

    def update_payment(self):
        self.payid = self.payid_entry.get()
        self.date = self.date_entry.get()
        self.value = self.value_entry.get()
        self.penalty = self.penalty_entry.get()
        self.clientid = self.clientid_entry.get()
        self.connect_db()

        self.cursor.execute(f"""
            UPDATE mensalidade
            SET datapago = '{self.date}', 
            valorpago = '{self.value}', 
            multa = '{self.penalty}'
            WHERE mensalidadeid = '{self.payid}'""")

        self.conn.commit()
        self.disconnect_db()
        self.show_payments()
        self.clean_forms()

    def search_client(self):
        self.connect_db()

        self.clients_list.delete(*self.clients_list.get_children())

        self.search_entry.insert(END, '%')
        search = self.search_entry.get()
        self.cursor.execute("""
            SELECT clienteid, nome, email, quadra, num_casa, telefone
            FROM cliente
            WHERE nome ILIKE '%s' ORDER BY nome ASC""" % search)
        search_nome = self.cursor.fetchall()

        for i in search_nome:
            self.clients_list.insert("", END, values=i)

        self.search_entry.delete(0, END)

        self.disconnect_db()

    def clean(self):
        self.body.destroy()
        self.body = Frame(self.window, bg="#3b3b3b", bd=4,
                          highlightbackground="#a9a9a9", highlightthickness=3)
        self.body.place(relx=0.12, rely=0, relwidth=0.88, relheight=1)

    def exit(self):
        self.window.destroy()


class Main(Funcionalidades):
    def __init__(self):
        self.window = Tk()
        self.window_config()
        self.frames()

        # Static Icons
        self.icons()

        # Bar menu static
        self.widgets_bar_menu()

        # Home Page
        self.widgets_home()

        self.window.mainloop()

    def window_config(self):
        # Standard Settings from window
        self.window.title("Gerenciador de mensalidade")
        self.window.geometry("750x600+350+50")
        self.window.resizable(0, 0)
        self.window.config(bg="#3b3b3b")

    def frames(self):
        # Standard Frames from application
        self.bar_menu = Frame(self.window, bg="#d3d3d3")
        self.bar_menu.place(relx=0, rely=0, relwidth=0.12, relheight=1)

        self.body = Frame(self.window, bg="#3b3b3b", bd=4,
                          highlightbackground="#a9a9a9", highlightthickness=3)
        self.body.place(relx=0.12, rely=0, relwidth=0.88, relheight=1)

    def icons(self):
        # Constructing icons
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
        # Standard widgets from bar menu
        self.home_button = Button(self.bar_menu, image=self.icon_home,
                                  bg="#d3d3d3", bd=0, command=self.widgets_home)
        self.home_button.place(relx=0, rely=0.03, relwidth=1)

        self.clients_button = Button(self.bar_menu, image=self.icon_client,
                                     bg="#d3d3d3", bd=0, command=self.widgets_clients)
        self.clients_button.place(relx=0, rely=0.18, relwidth=1)

        self.new_button = Button(self.bar_menu, image=self.icon_new,
                                 bg="#d3d3d3", bd=0, command=self.widgets_new_client)
        self.new_button.place(relx=0, rely=0.33, relwidth=1)

        self.close_button = Button(self.bar_menu, image=self.icon_close,
                                   bg="#d3d3d3", bd=0, command=self.exit)
        self.close_button.place(relx=0, rely=0.85, relwidth=1)

    def widgets_home(self):
        # Constructing home page
        self.clean()
        self.home_button.configure(background="#a9a9a9")
        self.clients_button.configure(background="#d3d3d3")
        self.new_button.configure(background="#d3d3d3")

        self.header = Label(self.body, text="Seja bem-vindo",
                            bg="#3b3b3b", fg="#d3d3d3",
                            font="Arial 60", justify="left")
        self.header.place(relx=0.035, rely=0.1, relwidth=0.95)

        self.content = Label(self.body, text="Esse é um sistema de gerenciamento de mensalidades,\n"
                                             "onde você poderá fazer o controle de pagamento das\n"
                                             "mensalidades do seu negócio. Além de poder adicionar\n"
                                             "novos clientes, editar os já existentes, enviar emails\n"
                                             "e muito mais!",
                             bg="#3b3b3b", fg="#d3d3d3",
                             font="Arial 17", justify="left")
        self.content.place(relx=0.035, rely=0.5, relwidth=0.95)

    def widgets_clients(self):
        # Listing customers
        self.clean()
        self.home_button.configure(background="#d3d3d3")
        self.new_button.configure(background="#d3d3d3")
        self.clients_button.configure(background="#a9a9a9")

        self.header = Label(self.body, text="Lista de clientes",
                            bg="#3b3b3b", fg="#d3d3d3",
                            font="Arial 25 bold", justify="left")
        self.header.place(relx=0.02, rely=0.02, relwidth=0.46)

        # Search field
        self.search_entry = Entry(self.body, relief="groove", font="Arial 20",
                                  bg="#d3d3d3", fg="#3b3b3b")
        self.search_entry.place(relx=0.043, rely=0.16, relwidth=0.35)

        self.search_bt = Button(self.body, image=self.icon_search,
                                bg="#a9a9a9", bd=2, command=self.search_client)
        self.search_bt.place(relx=0.41, rely=0.16)

        # Manage customers
        self.manager_bt = Button(self.body, image=self.icon_manager,
                                 bg="#a9a9a9", bd=1, command=self.manager)
        self.manager_bt.place(relx=0.83, rely=0.16)

        # Register payment
        self.payment_bt = Button(self.body, image=self.icon_pay,
                                 bg="#8fbc8f", bd=1, command=self.pay)
        self.payment_bt.place(relx=0.90, rely=0.16)

        # Clients list
        self.clients_list = ttk.Treeview(self.body, height=3,
                                         column=("col1", "col2", "col3", "col4", "col5", "col6"))

        self.clients_list.heading("#0", text="#")
        self.clients_list.heading("#1", text="ID")
        self.clients_list.heading("#2", text="Nome")
        self.clients_list.heading("#3", text="E-mail")
        self.clients_list.heading("#4", text="Quadra")
        self.clients_list.heading("#5", text="Nº")
        self.clients_list.heading("#6", text="Telefone")

        self.clients_list.column("#0", width=1)
        self.clients_list.column("#1", width=10)
        self.clients_list.column("#2", width=120)
        self.clients_list.column("#3", width=100)
        self.clients_list.column("#4", width=12)
        self.clients_list.column("#5", width=3)
        self.clients_list.column("#6", width=40)

        self.clients_list.place(relx=0.02, rely=0.25, relwidth=0.93, relheight=0.7)

        self.scroll_list = Scrollbar(self.body, orient="vertical")
        self.clients_list.configure(yscroll=self.scroll_list.set)
        self.scroll_list.place(relx=0.95, rely=0.25, relwidth=0.03, relheight=0.7)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 11))
        self.show_list()

    def widgets_new_client(self):
        # Register new client
        self.clean()
        self.home_button.configure(background="#d3d3d3")
        self.clients_button.configure(background="#d3d3d3")
        self.new_button.configure(background="#a9a9a9")

        self.header = Label(self.body, text="Novo cliente",
                            bg="#3b3b3b", fg="#d3d3d3",
                            font="Arial 25 bold", justify="left")
        self.header.place(relx=0.02, rely=0.02, relwidth=0.36)

        # Field Name
        self.name_label = Label(self.body, text="Nome:",
                                bg="#3b3b3b", fg="#d3d3d3",
                                font="Arial 15", justify="left")
        self.name_label.place(relx=0.035, rely=0.2)

        self.name_entry = Entry(self.body, relief="groove", font="Arial 20",
                                bg="#d3d3d3", fg="#3b3b3b")
        self.name_entry.place(relx=0.038, rely=0.26, relwidth=0.92)

        # Field E-mail
        self.email_label = Label(self.body, text="E-mail:",
                                 bg="#3b3b3b", fg="#d3d3d3",
                                 font="Arial 15", justify="left")
        self.email_label.place(relx=0.035, rely=0.37)

        self.email_entry = Entry(self.body, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.email_entry.place(relx=0.038, rely=0.43, relwidth=0.92)

        # Blcok Field
        self.block_label = Label(self.body, text="Quadra:",
                                 bg="#3b3b3b", fg="#d3d3d3",
                                 font="Arial 15", justify="left")
        self.block_label.place(relx=0.035, rely=0.54)

        self.block_entry = Entry(self.body, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.block_entry.place(relx=0.038, rely=0.60, relwidth=0.38)

        # Number house Field
        self.number_label = Label(self.body, text="Nº da casa:",
                                  bg="#3b3b3b", fg="#d3d3d3",
                                  font="Arial 15", justify="left")
        self.number_label.place(relx=0.58, rely=0.54)

        self.number_entry = Entry(self.body, relief="groove", font="Arial 20",
                                  bg="#d3d3d3", fg="#3b3b3b")
        self.number_entry.place(relx=0.58, rely=0.60, relwidth=0.38)

        # Phone field
        self.phone_label = Label(self.body, text="Telefone:",
                                 bg="#3b3b3b", fg="#d3d3d3",
                                 font="Arial 15", justify="left")
        self.phone_label.place(relx=0.035, rely=0.71)

        self.phone_entry = Entry(self.body, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.phone_entry.place(relx=0.038, rely=0.77, relwidth=0.50)

        # Buttons
        self.clean_form_bt = Button(self.body, text="Limpar", font="Arial 13",
                                    bg="#a9a9a9", bd=1, width=8, height=1,
                                    command=self.clean_forms)
        self.clean_form_bt.place(relx=0.68, rely=0.91)

        self.save_form_bt = Button(self.body, text="Salvar", font="Arial 13",
                                   bg="#8fbc8f", bd=1, width=8, height=1,
                                   command=self.new_client)
        self.save_form_bt.place(relx=0.83, rely=0.91)

    def manager(self):
        self.manager_win = Toplevel()
        self.manager_win.title("Gerenciar cliente")
        self.manager_win.geometry("616x570+435+80")
        self.manager_win.resizable(0, 0)
        self.manager_win.config(bg="#a9a9a9")
        self.manager_win.transient(self.window)
        self.manager_win.focus_force()
        self.manager_win.grab_set()

        # Frame for manager window
        self.manager_frame = Frame(self.manager_win, bg="#a9a9a9", bd=4,
                                   highlightbackground="#d3d3d3", highlightthickness=3)
        self.manager_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Contents
        self.header = Label(self.manager_frame, text="Perfil do cliente",
                            bg="#a9a9a9", fg="#3b3b3b",
                            font="Arial 18 bold", justify="left")
        self.header.place(relx=0.02, rely=0.02, relwidth=0.37)

        # Entrys
        ## Field ID
        self.clientid_label = Label(self.manager_frame, text="ID:",
                                    bg="#a9a9a9", fg="#3b3b3b",
                                    font="Arial 15", justify="left")
        self.clientid_label.place(relx=0.035, rely=0.1)

        self.clientid_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                    bg="#d3d3d3", fg="#3b3b3b")
        self.clientid_entry.place(relx=0.09, rely=0.1, relwidth=0.07)

        self.searchid_button = Button(self.manager_frame, image=self.icon_search,
                                      bg="#a9a9a9", bd=2, command=self.search_id)
        self.searchid_button.place(relx=0.2, rely=0.1)

        ## Field name
        self.name_label = Label(self.manager_frame, text="Nome:",
                                bg="#a9a9a9", fg="#3b3b3b",
                                font="Arial 15", justify="left")
        self.name_label.place(relx=0.035, rely=0.17)

        self.name_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                bg="#d3d3d3", fg="#3b3b3b")
        self.name_entry.place(relx=0.038, rely=0.23, relwidth=0.85)

        ## Field E-mail
        self.email_label = Label(self.manager_frame, text="E-mail:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 15", justify="left")
        self.email_label.place(relx=0.035, rely=0.33)

        self.email_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.email_entry.place(relx=0.038, rely=0.40, relwidth=0.92)

        ## Blcok Field
        self.block_label = Label(self.manager_frame, text="Quadra:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 15", justify="left")
        self.block_label.place(relx=0.035, rely=0.51)

        self.block_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.block_entry.place(relx=0.038, rely=0.57, relwidth=0.38)

        ## Number house Field
        self.number_label = Label(self.manager_frame, text="Nº da casa:",
                                  bg="#a9a9a9", fg="#3b3b3b",
                                  font="Arial 15", justify="left")
        self.number_label.place(relx=0.58, rely=0.51)

        self.number_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                  bg="#d3d3d3", fg="#3b3b3b")
        self.number_entry.place(relx=0.58, rely=0.57, relwidth=0.38)

        ## Phone field
        self.phone_label = Label(self.manager_frame, text="Telefone:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 15", justify="left")
        self.phone_label.place(relx=0.035, rely=0.68)

        self.phone_entry = Entry(self.manager_frame, relief="groove", font="Arial 20",
                                 bg="#d3d3d3", fg="#3b3b3b")
        self.phone_entry.place(relx=0.038, rely=0.74, relwidth=0.50)

        # Buttons
        self.update_cli = Button(self.manager_frame, image=self.icon_edit,
                                 bg="#8fbc8f", bd=1, command=self.update_client)
        self.update_cli.place(relx=0.77, rely=0.88)

        self.delete_cli = Button(self.manager_frame, image=self.icon_delete,
                                 bg="#dc143c", bd=1, command=self.delete_client)
        self.delete_cli.place(relx=0.85, rely=0.88)

        self.payments_cli = Button(self.manager_frame,
                                   text="Mensalidades pagas...",
                                   font="Arial 14", bg="#d3d3d3",
                                   fg="#3b3b3b", bd=1, command=self.payments)
        self.payments_cli.place(relx=0.05, rely=0.88)

    def payments(self):
        self.payments_win = Toplevel()
        self.payments_win.title("Mensalidades Pagas")
        self.payments_win.geometry("600x500+450+100")
        self.payments_win.resizable(0, 0)
        self.payments_win.config(bg="#a9a9a9")
        self.payments_win.transient(self.window)
        self.payments_win.focus_force()
        self.payments_win.grab_set()

        self.payments_frame = Frame(self.payments_win, bg="#a9a9a9", bd=4,
                                    highlightbackground="#d3d3d3", highlightthickness=3)
        self.payments_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.header_payments = Label(self.payments_frame, text="Mensalidades Pagas",
                                     bg="#a9a9a9", fg="#3b3b3b",
                                     font="Arial 15 bold", justify="left")
        self.header_payments.place(relx=0.02, rely=0.02, relwidth=0.4)

        # Manager payments
        self.manager_pay_bt = Button(self.payments_frame, image=self.icon_manager,
                                     bg="#d3d3d3", bd=1, command=self.manager_payments)
        self.manager_pay_bt.place(relx=0.92, rely=0.13)

        # Clients list
        self.payments_list = ttk.Treeview(self.payments_frame, height=3,
                                         column=("col1", "col2", "col3", "col4", "col5"))

        self.payments_list.heading("#0", text="#")
        self.payments_list.heading("#1", text="ID")
        self.payments_list.heading("#2", text="ID men.")
        self.payments_list.heading("#3", text="Data pagamento")
        self.payments_list.heading("#4", text="Valor pago")
        self.payments_list.heading("#5", text="Multa")


        self.payments_list.column("#0", width=1)
        self.payments_list.column("#1", width=10)
        self.payments_list.column("#2", width=10)
        self.payments_list.column("#3", width=100)
        self.payments_list.column("#4", width=100)
        self.payments_list.column("#5", width=10)

        self.payments_list.place(relx=0.02, rely=0.25, relwidth=0.93, relheight=0.7)

        self.scroll_list2 = Scrollbar(self.payments_frame, orient="vertical")
        self.payments_list.configure(yscroll=self.scroll_list2.set)
        self.scroll_list2.place(relx=0.95, rely=0.25, relwidth=0.03, relheight=0.7)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 11))
        self.show_payments()

    def manager_payments(self):
        self.manager_pay_win = Toplevel()
        self.manager_pay_win.title("Gerenciar mensalidades")
        self.manager_pay_win.geometry("250x500+660+110")
        self.manager_pay_win.resizable(0, 0)
        self.manager_pay_win.config(bg="#a9a9a9")
        self.manager_pay_win.transient(self.window)
        self.manager_pay_win.focus_force()
        self.manager_pay_win.grab_set()

        # Frame for manager payments window
        self.manager_pay_frame = Frame(self.manager_pay_win, bg="#a9a9a9",
                                       bd=4, highlightbackground="#d3d3d3",
                                       highlightthickness=3)
        self.manager_pay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Entrys
        ## Field ID
        self.payid_label = Label(self.manager_pay_win, text="ID:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 20", justify="left")
        self.payid_label.place(relx=0.05, rely=0.05)

        self.payid_entry = Entry(self.manager_pay_win, relief="groove",
                                 font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.payid_entry.place(relx=0.24, rely=0.05, relwidth=0.25)

        self.search_payid_button = Button(self.manager_pay_win,
                                          image=self.icon_search, bg="#d3d3d3",
                                          bd=2, command=self.search_paymentid)
        self.search_payid_button.place(relx=0.58, rely=0.05)

        # Date Field
        self.date_label = Label(self.manager_pay_win, text="Data:",
                                bg="#a9a9a9", fg="#3b3b3b",
                                font="Arial 20", justify="left")
        self.date_label.place(relx=0.05, rely=0.15)

        self.date_entry = Entry(self.manager_pay_win, relief="groove",
                                font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.date_entry.place(relx=0.08, rely=0.24, relwidth=0.8)

        # Value Field
        self.value_label = Label(self.manager_pay_win, text="Valor:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 20", justify="left")
        self.value_label.place(relx=0.05, rely=0.35)

        self.value_entry = Entry(self.manager_pay_win, relief="groove",
                                 font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.value_entry.place(relx=0.08, rely=0.44, relwidth=0.8)

        # Penalty Field
        self.penalty_label = Label(self.manager_pay_win, text="Multa:",
                                   bg="#a9a9a9", fg="#3b3b3b",
                                   font="Arial 20", justify="left")
        self.penalty_label.place(relx=0.05, rely=0.57)

        self.penalty_entry = Entry(self.manager_pay_win, relief="groove",
                                   font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.penalty_entry.place(relx=0.08, rely=0.66, relwidth=0.8)

        # Buttons
        self.update_pay = Button(self.manager_pay_win, image=self.icon_edit,
                                 bg="#8fbc8f", bd=1,
                                 command=self.update_payment)
        self.update_pay.place(relx=0.3, rely=0.82)

        self.delete_pay = Button(self.manager_pay_win, image=self.icon_delete,
                                 bg="#dc143c", bd=1, command=self.delete_payment)
        self.delete_pay.place(relx=0.5, rely=0.82)

    def pay(self):
        self.pay_win = Toplevel()
        self.pay_win.title("Gerenciar cliente")
        self.pay_win.geometry("250x450+660+110")
        self.pay_win.resizable(0, 0)
        self.pay_win.config(bg="#a9a9a9")
        self.pay_win.transient(self.window)
        self.pay_win.focus_force()
        self.pay_win.grab_set()

        # Frame for manager payments window
        self.pay_frame = Frame(self.pay_win, bg="#a9a9a9",
                                       bd=4, highlightbackground="#d3d3d3",
                                       highlightthickness=3)
        self.pay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Entrys
        ## Field ID
        self.pay_clientid_label = Label(self.pay_win, text="ID:",
                                        bg="#a9a9a9", fg="#3b3b3b",
                                        font="Arial 20", justify="left")
        self.pay_clientid_label.place(relx=0.05, rely=0.05)

        self.pay_clientid_entry = Entry(self.pay_win, relief="groove",
                                        font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.pay_clientid_entry.place(relx=0.24, rely=0.05, relwidth=0.25)

        # Date Field
        self.date_pay_label = Label(self.pay_win, text="Data:",
                                bg="#a9a9a9", fg="#3b3b3b",
                                font="Arial 20", justify="left")
        self.date_pay_label.place(relx=0.05, rely=0.15)

        self.date_pay_entry = Entry(self.pay_win, relief="groove",
                                font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.date_pay_entry.place(relx=0.08, rely=0.24, relwidth=0.8)

        # Value Field
        self.value_pay_label = Label(self.pay_win, text="Valor:",
                                 bg="#a9a9a9", fg="#3b3b3b",
                                 font="Arial 20", justify="left")
        self.value_pay_label.place(relx=0.05, rely=0.35)

        self.value_pay_entry = Entry(self.pay_win, relief="groove",
                                 font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.value_pay_entry.place(relx=0.08, rely=0.44, relwidth=0.8)

        # Penalty Field
        self.penalty_pay_label = Label(self.pay_win, text="Multa:",
                                   bg="#a9a9a9", fg="#3b3b3b",
                                   font="Arial 20", justify="left")
        self.penalty_pay_label.place(relx=0.05, rely=0.57)

        self.penalty_pay_entry = Entry(self.pay_win, relief="groove",
                                   font="Arial 20", bg="#d3d3d3", fg="#3b3b3b")
        self.penalty_pay_entry.place(relx=0.08, rely=0.66, relwidth=0.8)

        # Buttons
        self.save_pay = Button(self.pay_win, text="Salvar",
                               bg="#8fbc8f", bd=1, font="Arial 15",
                               command=self.new_payment)
        self.save_pay.place(relx=0.35, rely=0.82)


Main()
