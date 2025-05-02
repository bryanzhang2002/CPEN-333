# Group#: A37
# Student Names: Eric Lim, Bryan Zhang

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    def __init__(self, window:Tk):
        self.process_name = current_process().name      # get the client name e.g. Client1
        self.window:Tk = window
        self.gui()      # start the client GUI
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # initialize client TCP socket
        try:    # attempt to connect to server
            self.clientSocket.connect(('localhost', 12000)) # connect to server
            clientPort = self.clientSocket.getsockname()[1] # get the client port #
            self.clientLabel.config(text=f"{self.process_name} @port #{clientPort}")    # config the label to be of the form 'Client1 @port: #12345' to be filled with the appropriate data
        except Exception as e:  # in case of error, print the exception and gracefully return
            print(f"Exception connecting to server: {e}")
            return
        # this background thread activates the receive_message which contains an infinite loop that constantly listens for incoming messages from the server while maintaining GUI responsiveness.
        self.receiveThread = threading.Thread(target=self.receive_message, daemon=True)    # daemon so that the thread terminates when the client GUI is closed 
        self.receiveThread.start()
    
    def gui(self): 
        """
        This class takes care of the client's graphical user interface (GUI) creation and termination. 
        List of elements in the GUI:
            - window title: Chat Client
            - Client and port number
            - input box for user to send messages with label
            - Chat history box with scroll bar and label
        """
        self.window.title("Chat Client")

        # displays the client # and port # in the form 'Client1 @port: #12345'
        self.clientLabel = Label(self.window)  
        self.clientLabel.pack(side = TOP, anchor=W, padx=10, pady=(10,0))

        # creates the input box for sending chat messsages
        inputFrame = Frame(self.window)
        inputFrame.pack(padx=10, pady=5, fill='x')
        Label(inputFrame, text="Chat message: ").grid(row=0, column=0, sticky='w', padx=(0,5))
        self.entry = Entry(inputFrame, width=40)    # entry box is created 
        self.entry.grid(row=0, column=1, sticky='w')

        self.entry.bind('<Return>', self.return_key_pressed)    # bind the return key to the return_key_pressed method

        # 'Chat History:' label
        Label(self.window, text = "Chat History:").pack(side=TOP, anchor=W, padx=10)

        # Frame for chat history text box and scroll bar
        text_frame = Frame(self.window)
        text_frame.pack(padx=10, pady=5, fill='both', expand=True)

        # text box for chat history
        self.text_area = Text(text_frame, height=15, state=DISABLED)   # prevents user from manually modifying chat history
        self.text_area.tag_configure("right", justify="right")  # when you insert text with the "right" tag it will be right justified
        self.text_area.tag_configure("left", justify="left")    # when you insert text with the "left" tag it will be left justified
        self.text_area.pack(side=LEFT, expand=True, fill='both')

        # Scrollbar
        scrollbar = Scrollbar(text_frame, command=self.text_area.yview)
        scrollbar.pack(side=RIGHT,fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)     # syncs the scrollbar and text chat box

    def return_key_pressed(self, event):  
        """
        This method triggers whenever the user presses the return key, and calls the method send_message 
        """
        self.send_message()

    def send_message(self):
        """
        Send a chat message to the server and display it locally.
        
        Retrieves the message from the user through input entry box, validates it's non-empty, then:
        1. Inserts the client's process name to the front of the message
        2. Sends the full message to the server via the connected socket
        3. Clears the input entry box
        4. Calls method to display the sent message in the local chat history
        """
        message=self.entry.get().strip()    # get the user input from the entry box and strip the whitespace
        if message != "":   # if there is a non-empty message, attempt to send it 
            try:
                full_message = f"{self.process_name}: {message}" # append the client's name before the message 
                self.clientSocket.send(full_message.encode())   # send encoded full message to server
                self.entry.delete(0,END)    # clear message entry box
                self.display_message(f"{self.process_name}: {message}") # display message locally
            except Exception as e:
                print(f"Exception sending message: {e}")

    def receive_message(self):
        """
        Continuously listen for incoming messages from the server and display them.
        This method is meant to be ran in a daemon thread so that the loop automatically exits when the main thread terminates
        
        Runs in an infinite loop:
        1. .recv blocks the thread until data arrives from the server or an exception is raised
        3. Display non-empty messages in the chat history by invoking the method display_message()
        4. Handle and log any socket exceptions, breaking the loop on failure
        """
        while True:
            try:
                message = self.clientSocket.recv(1024).decode() # decode message received from server
                if message != "":   # if message is non empty, display it in the chat history
                    self.display_message(message)
            except Exception as e:
                print(f"Exception receiving message: {e}")
                break

    def display_message(self, message:str):
        """
        Display a chat message (inputted as a str) in the chat history text area with sender-based alignment.
        1. Temporarily enable the text area for modification
        2. Apply right-alignment for messages from the current client
        3. Apply left-alignment for messages from other clients
        4. Automatically scroll to show the latest message
        5. Disable modification of the text area
        """
        self.text_area.config(state=NORMAL) # allows chat history to be modified
        if message.startswith(f"{self.process_name}"):  # if the message is from the client itself display on the right side
            self.text_area.insert(END, f"{message}\n", "right")
        else:   # if the message is from another client, display on the left
            self.text_area.insert(END, f"{message}\n", "left")
        self.text_area.config(state=DISABLED)   # prevents chat history from being manually modified by user
        self.text_area.see(END) # automatically scrolls to the most recent message

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()