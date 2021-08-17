from tkinter import *
import json
from filesharing.common.read_credentials import get_all_credentials
from filesharing.app import start_app
from tkinter import messagebox


credentials = get_all_credentials()

def login():
    global login_screen
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.eval('tk::PlaceWindow %s center' % login_screen.winfo_pathname(login_screen.winfo_id()))
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command= lambda : login_verify(username_verify.get(), password_verify.get())).pack()

    login_screen.mainloop()


def login_verify(username, password):
    user_found_flag = False
    for c in credentials:
        if username == c['username']:
            user_found_flag = True
        if username == c['username'] and password == c['password']:
            return login_sucess()
    if user_found_flag:
        return password_not_recognised()
    else:
        return user_not_found()


def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Button(login_success_screen, text="OK", command=user_menu()).pack()

def user_menu():
    login_success_screen.withdraw()
    login_screen.withdraw()
    global user_menu_screen
    user_menu_screen = Toplevel(login_screen)
    user_menu_screen.title("User Menu")
    w = login_screen.winfo_reqwidth()
    h = login_screen.winfo_reqheight()
    ws = login_screen.winfo_screenwidth()
    hs = login_screen.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    user_menu_screen.geometry('+%d+%d' % (x+100, y+100))  ## this part allows you to only change the location
    user_menu_screen.geometry("300x100")
    Button(user_menu_screen, text="Show Logs", command=show_logs).pack()
    Button(user_menu_screen, text="Start Service", command=start_service).pack()
    messagebox.showinfo("SUCCESS", "Login Successful")


def start_service():
    global login_success_screen
    start_service_screen = Toplevel(user_menu_screen)
    start_service_screen.title("Success")
    start_service_screen.geometry("150x100")
    start_app()
    Button(start_service_screen, text="Stop Service", command=stop_service).pack()

def stop_service():
    pass

def show_logs():
    global show_logs
    show_logs = Toplevel(user_menu_screen)
    show_logs.title("Logs")
    show_logs.geometry("750x750")
    with open("demo.log", "r") as f:
        #show_logs.geometry("350x150+%d+%d" % (((show_logs.winfo_screenwidth() / 2.) - (350 / 2.)), ((show_logs.winfo_screenheight() / 2.) - (150 / 2.))))
        Label(show_logs, font=('consolas', '20', 'bold'), text=f.read()).pack(pady=(50, 0))


def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


login()
