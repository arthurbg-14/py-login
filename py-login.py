import time
from tkinter import messagebox
from tkinter import *
import json
import re


def mainPage():
    def createLabel(text, x, y, show=""):
        label = Label(root, text=text, font="Agency_FB")
        label.place(relx=x, rely=y, anchor=CENTER)
        input = Entry(root)
        input.place(width=300, relx=x, rely=(y+0.05), anchor=CENTER)
        input.config(show=show)

        return (label, input)

    def createButton(text, width, heigth, relx, rely, command):
        button = Button(
            root, text=text, command=command)
        button.place(width=width, height=heigth, relx=relx,
                     rely=rely, anchor=CENTER)

        return button

    def showPass():
        if pass_input.config()["show"][-1] == "*":
            pass_input.config(show="")
        else:
            pass_input.config(show="*")

    def login():
        try:
            if database[email_input.get()]["password"] == pass_input.get():
                def profileDestroy():
                    profile.destroy()
                    return_btn.destroy()
                    name.destroy()

                profile = Frame(root)
                profile.place(x=0, y=0, width=1000, height=1000)

                return_btn = createButton(
                    "Voltar", 100, 50, 0.1, 0.9, profileDestroy)

                name = Label(
                    root, text="Hello!, "+database[email_input.get()]["name"], font='Arial 30 bold')
                name.place(relx=0.5, rely=0.1, anchor=CENTER)
            else:
                messagebox.showerror("Error", "incorrect email or password")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "incorrect email or password")

    def register():
        def registerDestroy():
            frame.destroy()
            tittle.destroy()
            return_button.destroy()
            name_input.destroy()
            name_label.destroy()
            email_input.destroy()
            email_label.destroy()
            pass_input.destroy()
            pass_label.destroy()
            show_pass_btn.destroy()
            register_button.destroy()

        def noErrors():
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            email = email_input.get()
            password = pass_input.get()
            if not re.fullmatch(regex, email):
                error.config(text="INVALID EMAIL")
                return False
            elif not re.search("[a-z]", password):
                error.config(text="PASSWORD DONT HAVE LOWER CASE CHARS")
                return False
            elif not re.search("[A-Z]", password):
                error.config(text="PASSWORD DONT HAVE UPPER CASE CHARS")
                return False
            elif not re.search("[0-9]", password):
                error.config(text="PASSWORD DONT HAVE NUMBERS")
                return False
            try:
                account = database[email]
                error.config(text="USER ALREADY EXISTS")
                return False
            except:
                return True

        def registerUser():
            global database

            if noErrors():

                database[email_input.get()] = {
                    "name": name_input.get(),
                    "password": pass_input.get()
                }
                print(name_input.get() + " has been registered")
                saveDatabase()
                database = getDatabase()

        def showPass():
            if pass_input.config()["show"][-1] == "*":
                pass_input.config(show="")
            else:
                pass_input.config(show="*")

        frame = Frame(root)
        frame.place(x=0, y=0, width=1000, height=1000)

        tittle = Label(root, text="Registre-se", font='Arial 30 bold')
        tittle.place(relx=0.5, rely=0.1, anchor=CENTER)

        return_button = createButton(
            "Voltar", 100, 50, 0.1, 0.1, registerDestroy)
        (name_label, name_input) = createLabel(
            text="Digite seu nome:", x=0.5, y=0.2)
        (email_label, email_input) = createLabel(
            text="Digite seu e-mail:", x=0.5, y=0.3)
        (pass_label, pass_input) = createLabel(
            text="Digite sua senha:", x=0.5, y=0.4, show="*")
        show_pass_btn = createButton(
            text="Mostrar Senha", width=150, heigth=20, relx=0.5, rely=0.5, command=showPass)
        error = Label(root, text="", font='Arial 15 bold', fg="red")
        error.place(relx=0.5, rely=0.6, anchor=CENTER)
        register_button = createButton(
            text="Criar conta", width=300, heigth=50, relx=0.5, rely=0.7, command=registerUser)

    tittle = Label(root, text="LOGAR", font='Arial 30 bold')
    tittle.place(relx=0.5, rely=0.1, anchor=CENTER)

    email_input = createLabel(text="Digite seu e-mail:", x=0.5, y=0.3)[1]
    pass_input = createLabel(text="Digite sua senha:",
                             x=0.5, y=0.4, show="*")[1]

    show_pass_btn = createButton(
        text="Mostrar Senha", width=150, heigth=20, relx=0.5, rely=0.5, command=showPass)
    login_button = createButton(
        text="Logar", width=300, heigth=50, relx=0.5, rely=0.7, command=login)
    register_button = createButton(
        text="Registrar", width=300, heigth=50, relx=0.5, rely=0.8, command=register)


def getDatabase():
    try:
        with open("database.json") as f:
            data = json.load(f)
            print("database has been loaded")
            return data
    except Exception as e:
        print(e)
        with open("database.json", "a") as f:
            json.dump({}, f)
        getDatabase()


def saveDatabase():
    with open("database.json", "w") as f:
        json.dump(database, f, indent=4, sort_keys=True)


root = Tk()
root.geometry("500x600")

database = getDatabase()
mainPage()

root.mainloop()
