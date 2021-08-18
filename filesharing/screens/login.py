from tkinter import *
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from os.path import dirname
import tkinter as tk
import tkinter.scrolledtext as tkscrolled

import requests

from filesharing.common.globals import scheduler, credentials
from filesharing.common.logger import get_logger
from filesharing.app import start_app

from tkinter import messagebox

from filesharing.db.mongodbDAL import mongodbDAL
from filesharing.utils.current_time import print_date_time


def login(my_request):
    global log
    log = get_logger()
    global thread
    global login_screen
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.eval(
        "tk::PlaceWindow %s center"
        % login_screen.winfo_pathname(login_screen.winfo_id())
    )
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
    password_login_entry = Entry(login_screen, textvariable=password_verify, show="*")
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(
        login_screen,
        text="Login",
        width=10,
        height=1,
        command=lambda: login_verify(
            my_request, username_verify.get(), password_verify.get()
        ),
    ).pack()

    login_screen.mainloop()


def login_verify(my_request, username, password):
    user_found_flag = False
    for c in credentials:
        if username == c["username"]:
            user_found_flag = True
        if username == c["username"] and password == c["password"]:
            log.info(print_date_time() + "Login Successful")
            return user_menu(my_request)
    if user_found_flag:
        log.error(print_date_time() + "Password not recognized")
        return password_not_recognised()
    else:
        log.error(print_date_time() + "User not found")
        return user_not_found()


def user_menu(my_request):
    login_screen.withdraw()
    messagebox.showinfo("SUCCESS", "Login Successful")
    global user_menu_screen
    user_menu_screen = Toplevel(login_screen)
    user_menu_screen.title("User Menu")
    w = login_screen.winfo_reqwidth()
    h = login_screen.winfo_reqheight()
    ws = login_screen.winfo_screenwidth()
    hs = login_screen.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    user_menu_screen.geometry("+%d+%d" % (x + 100, y + 100))
    user_menu_screen.geometry("300x175")
    Button(user_menu_screen, text="Show Logs", command=show_logs).pack()
    Button(user_menu_screen, text="Clear Logs", command=clear_logs).pack()
    if my_request.request_type == "Tx":
        Button(
            user_menu_screen,
            text="Show Time Left Until Next Request",
            command=show_time,
        ).pack()
    else:
        Button(
            user_menu_screen,
            text="Show Number of Checks Left",
            command=show_number_of_checks_left,
        ).pack()
    Button(
        user_menu_screen,
        text="Start Service",
        command=lambda: start_service(my_request),
    ).pack()
    Button(user_menu_screen, text="Shutdown Service", command=shutdown_service).pack()
    Button(user_menu_screen, text="Exit Program", command=exit_program).pack()


def start_service(my_request):
    thread = Thread(target=start_app)
    thread.start()
    file = {
        "file_name": my_request.file_name_and_extension,
        "file_location": my_request.file_location,
    }
    dal = mongodbDAL(my_request.request_type)
    dal.add_dummy_file_to_file_list(my_request.file_location)
    dal.list_of_files_to_send.append(file)
    messagebox.showinfo("SUCCESS", "Service has started")
    log.info(print_date_time() + "Service Started")
    if my_request.request_type == "Tx":
        scheduler.add_job(
            func=dal.add_dummy_file_to_file_list,
            trigger="interval",
            seconds=my_request.time,
            args=my_request.file_location,
        )
        scheduler.add_job(
            func=dal.add_files_to_collection,
            trigger="interval",
            seconds=my_request.time,
            args=my_request.file_location,
        )
        scheduler.start()
    if my_request.request_type == "Rx":
        for i in range(my_request.number_of_checks):
            k = i + 1
            if dal.find_file_by_collection(
                my_request.file_name_and_extension, my_request.file_location
            ):
                print("Round " + str(k) + ": File Found")
                log.info(print_date_time() +
                    "Round "
                    + str(k)
                    + ": "
                    + my_request.file_name_and_extension
                    + " found in collection "
                    + my_request.file_location
                    + "."
                )
            else:
                print(" Round " + str(k) + ": File Not Found")
                log.info(print_date_time() +
                    "Round "
                    + str(k)
                    + ": "
                    + my_request.file_name_and_extension
                    + " not found in "
                    "collection " + my_request.file_location + "."
                )


def show_time():
    pass


def show_number_of_checks_left():
    pass


def shutdown_service():
    requests.get("http://127.0.0.1:5000/shutdown")
    messagebox.showinfo("SUCCESS", "Service has shutdown")
    log.info(print_date_time() + "Service has Shutdown")
    return "Server shutting down..."


def show_logs():
    with open(dirname(dirname(__file__)) + "/logs/demo.log", "r") as f:
        log.info(print_date_time() + "Showing Logs...")
        master = tk.Tk()
        master.title(string="Logs")
        text_widget = tk.Text(master, height=50, width=100)
        text_widget.pack()
        text_widget.insert(tk.END, f.read())
        tk.mainloop()


def clear_logs():
    open(dirname(dirname(__file__)) + "/logs/demo.log", "w").close()


def exit_program():
    exit(0)


def password_not_recognised():
    messagebox.showerror("ERROR", "Invalid Password")


def user_not_found():
    messagebox.showerror("ERROR", "User Not Found")
