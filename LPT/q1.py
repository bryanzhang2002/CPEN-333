class Stack:
    def __init__(self):
        """ initializes an empty stack and sets it size
            data fields: 
                stack: a python list as the internal data structure
                size: a counter to keep track of the size of the stack 
        """
        self.stack = list() # initialize empty list
        self.size = 0   # initial size is zero

    def push(self, item):
        """ puts the item on top of the stack and adjusts the stack size"""
        self.stack+=[item]  # add item to end of the list (top of the stack)
        self.size+=1    # increase size by 1

    def pop(self):
        """ removes and returns the item on top of the stack
            also adjusts the stack size accordingly
            if the stack is empty, an Exception should be raise
        """
        try:
            if self.size == 0:
                print("Error: Stack is empty, cannot pop.") # raise an exception if list is empty 
                return None # gracefully return None
            top_item = self.stack[self.size-1]  # store the top item of the stack to be returned
            self.stack = self.stack[0:self.size-1]  # re-assign everything other than the top item as the stack 
            self.size -=1   # decrement the size
            return top_item 
        except:
            return None 


    def peek(self):
        """ returns the item on top of the stack without affecting it
            if the stack is empty, returns None
        """
        if self.size == 0:
            return None
        else:
            return self.stack[self.size-1]

    def getSize(self):
        """ returns the size of the stack"""
        return self.size


#Testing: 
#   instantiate a stack object
myStack = Stack()
print(myStack.stack)

#   call push to push 1
myStack.push(1)
print(myStack.stack)

#   call push to push "one"
myStack.push("one")
print(myStack.stack)

#   call peek and print the returned item
print(myStack.peek())
print(myStack.stack)

#   call pop and print the returned item
print(myStack.pop())
print(myStack.stack)

#   call getSize and print the returned value
print(myStack.getSize())
print(myStack.stack)