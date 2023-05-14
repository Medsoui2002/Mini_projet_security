from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            message = [(ord(i)-5) for i in msg]
            msg = [chr(i) for i in message]
            msg_list.insert(tkinter.END, msg)
        except OSError: 
            break


def send(event=None): 
    msg = my_msg.get()
    msgquit=msg
    message = [(ord(i)+5) for i in msg]
    msg = [chr(i) for i in message]
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msgquit == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()
top = tkinter.Tk('300x900')
top.title("projet")

messages_frame = tkinter.Frame(top) 
my_msg = tkinter.StringVar() 
my_msg.set("créer votre nom.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, background='#063579', fg='White', width=50, yscrollcommand=scrollbar.set, font=("Calibri",14))
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width=30,font=("Calibri",14))
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="envoyer", command=send,background='#063579', fg='White', font=("Calibri",14))
send_button.pack()

top.protocol("dlt penetre", on_closing)


HOST = '127.0.0.1'
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()



