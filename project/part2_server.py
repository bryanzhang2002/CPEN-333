# Group#: A37
# Student Names: Eric Lim, Bryan Zhang

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sends 
    the message to the other client(s).  
    It uses the tkinter module to create the GUI for the server client.
    """
    def __init__(self, window:Tk):
        self.window:Tk = window
        self.clients:list = []       # list for keeping track of active clients' sockets
        self.clients_lock:threading.Lock = threading.Lock()    # only allows one thread to modify clients list at a time
        self.gui()      # start the server GUI
        self.start_server()    # initialize the server socket
    
    def gui(self):
        """
        This class takes care of the server's graphical user interface (GUI) creation and termination. 
        List of elements in the GUI:
            - window title: Chat Server
            - Chat history text box with scroll bar and label
        """
        self.window.title("Chat Server")

        # 'Chat history:' label
        Label(text = "Chat History:").pack(side = TOP, anchor=W)

        # Frame for chat history text box and scroll bar
        text_frame = Frame(self.window)
        text_frame.pack(padx=5, pady=(0,10), fill='both', expand=True)

        # text box for chat history
        self.text_area = Text(text_frame, height=15, state=DISABLED)   # prevents user from manually modifying chat history
        self.text_area.pack(side=LEFT, expand=True, fill='both')   

        # Scrollbar
        scrollbar = Scrollbar(text_frame, command=self.text_area.yview)
        scrollbar.pack(side=RIGHT,fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)

    def start_server(self):
        """
        This method: 
        1. Creates a TCP socket for the server
        2. Binds the socket to IP address 127.0.0.1 (known as loopback address or localhost) on port 12000
        3. Sets the server to listen for incoming connections with a backlog of 1
        4. Launches a daemon thread to handle incoming client connections while maintaining GUI responsiveness and clean program termination
        """
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # initialize TCP server socket
        self.serverSocket.bind(('127.0.0.1', 12000))    # bind to loopback addess with arbitrary port number
        self.serverSocket.listen(1)     # backlog of 1 allows there to be one client in the queue, can be increased if needed
        self.acceptThread = threading.Thread(target=self.accept_connection, daemon=True) # daemon so that the thread terminates when the GUI is closed
        self.acceptThread.start()

    def accept_connection(self):
        """
        Continuously accept incoming client connections and create threads to handle communication.

        This method runs in a dedicated daemon thread and performs the following in an infinite loop:
        1. Waits until a new connection arrives using serverSocket.accept() 
        2. Safely adds the new client socket to the clients list using clients_lock
        3. Initializes and starts a new daemon thread to handle client communication for every accepted client
        """
        while True:
            connectionSocket, addr = self.serverSocket.accept()
            with self.clients_lock:
                self.clients.append(connectionSocket)
            # Using a background thread to handle client maintains GUI responsiveness, making it daemon ensures thread terminates when the GUI is closed
            clientThread = threading.Thread(target=self.handle_client, args=(connectionSocket,), daemon=True) 
            clientThread.start()

    def handle_client(self, connectionSocket: socket):
        """
        This method is run in a daemon thread for each connected client.

        Performs the following in an infinite loop:
        1. recv blocks execution until the client sends a message
        2. Call display_message method to display the message in chat history
        3. Broadcasts the message to all OTHER connected clients
        4. If error occurs in broadcasting, remove the client from client list and close the client socekt safely
        
        Exception handling:
        - If client fails to send message (for example the client gracefully disconnects) or unexpected error occurs, it is safely removed from the clients list, and its socket is closed via the finally block
        """
        try:
            while True:
                message = connectionSocket.recv(1024).decode()  # wait until message is received from client and decode it
                self.display_message(message)   # display message in chat history
                with self.clients_lock:     # needed to safely modify client list
                    for client in self.clients:     # broadcast the message to every client EXCEPT the current client
                        if client != connectionSocket:
                            try: 
                                client.send(message.encode())
                            except:     # if there is an error in sending the message, remove client from client list and close the faulty client's socket
                                if client in self.clients:
                                    self.clients.remove(client)
                                client.close()
        except Exception as e:  
            print(f"Error occured: {e}")
        finally:    # whether an error occured or the client exited gracefully, ensure disconnected client is removed and its socket is closed
            with self.clients_lock:
                if connectionSocket in self.clients:
                    self.clients.remove(connectionSocket)   # safely remove the client from the list of clients if its still there
            connectionSocket.close()    # close the socket of the client

    def display_message(self,message:str):   # displays the message in the server GUI
        """
        Display a message from client (inputted as a str) in the chat history text area with left alignment.
        1. Temporarily enable the chat history for modification
        2. Insert message into text area on a new line
        4. Automatically scroll to show the latest message
        5. Disable modification of the chat history
        """
        self.text_area.config(state=NORMAL) # enables modification of chat history
        self.text_area.insert(END, f"{message}\n")  # adds the message on a new line to the end of Text box
        self.text_area.see(END) # auto scrolls to the last inserted text
        self.text_area.config(state=DISABLED)   # disables modification of chat history

def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()