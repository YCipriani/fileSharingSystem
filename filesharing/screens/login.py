import threading
import time
import datetime
from tkinter import *
from threading import Thread
import tkinter as tk
import sys

import os
import requests

from filesharing.common.globals import credentials, admin_email
from filesharing.common.logger import get_logger
from filesharing.app import start_app

from tkinter import messagebox

from filesharing.utils.current_time import (
    get_current_date_and_time,
    get_seconds_diff,
    write_service_started_time_to_file,
    write_number_of_checks_made,
    number_of_checks_made,
    service_started_time,
)
from filesharing.utils.notifications import (
    send_email,
    log_syslog,
    start_snmp_trap_receiver,
    send_snmp_trap,
)
from filesharing.utils.port import read_port_from_file

lock = threading.Lock()

log_file_path = sys.path[0].replace("screens", "").replace("/base_library.zip", "") + "/logs/demo.log"

def login(my_request):
    global log
    log = get_logger()
    global thread
    global thread1
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
            log.info(get_current_date_and_time() + "Login Successful")
            return user_menu(my_request)
    if user_found_flag:
        log.error(get_current_date_and_time() + "Password not recognized")
        return password_not_recognised()
    else:
        log.error(get_current_date_and_time() + "User not found")
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
    if my_request.request_type == "Tx":
        Button(
            user_menu_screen,
            text="Show Time Left Until Next Request",
            command=lambda: show_time(my_request),
        ).pack()
    if my_request.request_type == "Rx":
        Button(
            user_menu_screen,
            text="Show Number of Checks Made",
            command=show_number_of_checks_made,
        ).pack()
    Button(
        user_menu_screen,
        text="Start Service",
        command=lambda: start_service(my_request),
    ).pack()
    Button(
        user_menu_screen, text="Stop Service", command=lambda: stop_service(my_request)
    ).pack()
    Button(user_menu_screen, text="Show Logs", command=show_logs).pack()
    Button(user_menu_screen, text="Clear Logs", command=clear_logs).pack()
    Button(user_menu_screen, text="Close Program", command=close_program).pack()


def reset():
    now = datetime.datetime.now()  # current date and time
    end = now.strftime("%Y-%m-%d %H:%M:%S")
    date1_obj = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    write_service_started_time_to_file(date1_obj.strftime("%Y-%m-%d %H:%M:%S"), 0)
    write_number_of_checks_made(0)


def close_program():
    reset()
    with lock:
        open(log_file_path, "w").close()
        sys.exit()


def start_service(my_request):
    thread = Thread(target=start_app)
    thread.daemon = True
    thread.start()
    send_email(my_request, admin_email, True)
    start_message = "Service has started"
    if my_request.request_type == "Rx":
        log_syslog(start_message)
        th = Thread(target=start_snmp_trap_receiver)
        th.daemon = True
        th.start()
        send_snmp_trap(start_message)
    messagebox.showinfo("SUCCESS", start_message)
    log.info(get_current_date_and_time() + start_message)
    send_request(my_request)


def stop_service(my_request):
    try:
        requests.get("http://127.0.0.1:5000/shutdown")
    except:
        print("Connection max Retries")
    finally:
        if my_request.request_type == "Tx":
            send_email(my_request, admin_email, False)
        reset()
    messagebox.showinfo("SUCCESS", "Service has stopped")
    log.info(get_current_date_and_time() + "Service has stopped")


def send_tx_request(request_string, my_request):
    while True:
        requests.post(request_string)
        time.sleep(my_request.time)


def send_rx_request(request_string, my_request):
    message = None
    k = None
    for i in range(my_request.number_of_checks):
        k = i + 1
        if requests.post(request_string) == 'SUCCESS':
            message = (
                get_current_date_and_time()
                + "File "
                + my_request.file_name_and_extension
                + " was found in collection "
                + my_request.file_location
            )
            log.info(message + " (Check #" + str(k) + ")")
        else:
            message = (
                get_current_date_and_time()
                + "File "
                + my_request.file_name_and_extension
                + " was NOT found in collection "
                + my_request.file_location
            )
            log.error(message + " (Check #" + str(k) + ")")
        write_number_of_checks_made(k)
    log_syslog(message + ", " + str(k) + " times.")
    send_snmp_trap(message + " " + str(k) + " times.")
    send_email(my_request, admin_email, False)


def send_request(my_request):
    request_string = (
        "http://127.0.0.1:"
        + read_port_from_file()
        + "/send_request?request_type="
        + my_request.request_type
        + "&file_name="
        + my_request.file_name_and_extension
        + "&file_location="
        + my_request.file_location
    )
    with lock:
        now = datetime.datetime.now()  # current date and time
        end = now.strftime("%Y-%m-%d %H:%M:%S")
        date1_obj = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        write_service_started_time_to_file(date1_obj.strftime("%Y-%m-%d %H:%M:%S"), 1)
        if my_request.request_type == "Tx":
            thread1 = Thread(target=send_tx_request, args=(request_string, my_request))
            thread1.daemon = True
            thread1.start()
        if my_request.request_type == "Rx":
            thread1 = Thread(target=send_rx_request, args=(request_string, my_request))
            thread1.daemon = True
            thread1.start()


def show_time(my_request):
    d = service_started_time()
    if d["started"]:
        sec = get_seconds_diff(my_request.time)
        messagebox.showinfo("TIME LEFT UNTIL NEXT REQUEST", str(sec) + " Seconds")
    else:
        messagebox.showerror("ERROR", "NO TIME LEFT SINCE SERVICE HAS NOT BEEN STARTED")


def show_number_of_checks_made():
    n = number_of_checks_made()
    if n:
        messagebox.showinfo("NUMBER OF CHECKS MADE", str(n))
        log.info(get_current_date_and_time() + "Number of checks made: " + str(n))
    else:
        messagebox.showerror("ERROR", "NO CHECKS MADE. MAKE SURE YOU START THE SERVICE")
        log.info(get_current_date_and_time() + "No checks made yet.")


def show_logs():
    with open(log_file_path, "r") as f:
        master = tk.Tk()
        master.title(string="Logs")
        text_widget = tk.Text(master, height=50, width=100)
        text_widget.pack()
        text_widget.insert(tk.END, f.read())
        tk.mainloop()


def clear_logs():
    open(log_file_path, "w").close()
    messagebox.showerror("SUCCESS", "Logs have been cleared")


def password_not_recognised():
    messagebox.showerror("ERROR", "Invalid Password")


def user_not_found():
    messagebox.showerror("ERROR", "User Not Found")
