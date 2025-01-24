#Lab 2 (part 2)
#student name: Bryan Zhang
#student number: 69238335

from __future__ import annotations  #helps with type hints
from tkinter import *
#do not import any more modules

#do not change the skeleton of the program. Only add code where it is requested. 
class Complex:
    """ 
        this class implements the Complex number type 
        it stores the Complex number in two data fields: 
            real and imaginary
        Operation: 
            add, subtract, multiply and divide
            toString
    """
    def __init__(self, real: float, imaginary: float) -> None:
        """ initializer stores the Complex number""" 

        #Complex number must be in the lowest form (real and imaginary have no other common factor other than 1)
        #real stores the sign of the Complex
        self.real = real
        self.imaginary = imaginary

    def add(self, secondComplex: Complex) -> Complex:
        """
           adds 'this' Complex to secondComplex
           returns the result as a Complex number (type Complex)
        """
        real = self.real + secondComplex.real
        imaginary = self.imaginary + secondComplex.imaginary
        return Complex(real, imaginary)
    
    def subtract(self, secondComplex: Complex) -> Complex:
        """
           subtracts secondComplex from 'this' Complex to 
           returns the result as a Complex number (type Complex)
        """ 
        real = self.real - secondComplex.real
        imaginary = self.imaginary - secondComplex.imaginary
        return Complex(real, imaginary)

    def multiply(self, secondComplex: Complex) -> Complex:
        """
           multiplies 'this' Complex to secondComplex
           returns the result as a Complex number (type Complex)
        """ 
        real = self.real * secondComplex.real - self.imaginary * secondComplex.imaginary
        imaginary = self.real * secondComplex.imaginary + self.imaginary * secondComplex.real
        return Complex(real, imaginary)

    def divide(self, secondComplex: Complex) -> Complex:
        """
           divides 'this' Complex by secondComplex
           returns the result as a Complex number (type Complex)
        """ 
        if secondComplex.real == 0 and secondComplex.imaginary == 0:
            return Complex(float('nan'), float('nan'))
        real = (self.real * secondComplex.real + self.imaginary * secondComplex.imaginary)/(secondComplex.real**2 + secondComplex.imaginary**2)
        imaginary = (self.imaginary * secondComplex.real - self.real * secondComplex.imaginary)/(secondComplex.real**2 + secondComplex.imaginary**2)
        return Complex(real, imaginary)

    def toString(self) -> str:
        """             
            returns a string representation of 'this' Complex
            the general output format is: (real) + (imaginary)i
            special cases:
                if 'this' Complex is a real number, it must not show any imaginary component 
                Divide by zero returns "NaN" (not a number)
                if real or the imaginary component is 1, do not display that 1
        """
        if self.real != self.real or self.imaginary != self.imaginary:  # check if either entry is NaN
            return "NaN"

        if self.real == 0 and self.imaginary == 0: # the entry is 0
            return "0"
        if self.imaginary == 0: # the entry is a real number
            return str(self.real)
        if self.real == 0:  # the entry is an imaginary number
            if self.imaginary == 1:
                return "i"
            if self.imaginary == -1:
                return "-i"
            else:
                return f"{self.imaginary}i"
        
        # the entry is a complex number
        result: str = str(self.real)
        if self.imaginary > 0:
            result += "+"
        result += f"{self.imaginary}i"

        return result
                
    
class GUI:
    """ 
        this class implements the GUI for our program
        use as is.
        The add, subtract, multiply and divide methods invoke the corresponding
        methods from the Complex class to calculate the result to display.
    """
    def __init__(self):
        """ 
            The initializer creates the main window, label and entry widgets,
            and starts the GUI mainloop.
        """
        window = Tk()
        window.title("Complex Numbers")
        window.geometry("190x180")
       
        # Labels and entries for the first Complex number
        frame1 = Frame(window)
        frame1.grid(row = 1, column = 1, pady = 10)
        Label(frame1, text = "Complex 1:").pack(side = LEFT)
        self.Complex1real = StringVar()
        Entry(frame1, width = 5, textvariable = self.Complex1real, 
              justify = RIGHT, font=('Calibri 13')).pack(side = LEFT)
        Label(frame1, text = "+").pack(side = LEFT)
        self.Complex1imaginary = StringVar()
        Entry(frame1, width = 5, textvariable = self.Complex1imaginary, 
              justify = RIGHT, font=('Calibri 13')).pack(side = LEFT)
        Label(frame1, text = "i").pack(side = LEFT)

        # Labels and entries for the second Complex number
        frame2 = Frame(window)
        frame2.grid(row = 3, column = 1, pady = 10)
        Label(frame2, text = "Complex 2:").pack(side = LEFT)
        self.Complex2real = StringVar()
        Entry(frame2, width = 5, textvariable = self.Complex2real, 
              justify = RIGHT, font=('Calibri 13')).pack(side = LEFT)
        Label(frame2, text = "+").pack(side = LEFT)
        self.Complex2imaginary = StringVar()
        Entry(frame2, width = 5, textvariable = self.Complex2imaginary, 
              justify = RIGHT, font=('Calibri 13')).pack(side = LEFT)
        Label(frame2, text = "i").pack(side = LEFT)
        
        # Labels and entries for the result Complex number
        # an entry widget is used as the output here
        frame3 = Frame(window)
        frame3.grid(row = 4, column = 1, pady = 10)
        Label(frame3, text = "Result:     ").pack(side = LEFT)
        self.result = StringVar()
        Entry(frame3, width = 10, textvariable = self.result, 
              justify = RIGHT, font=('Calibri 13')).pack(side = LEFT)

        # Buttons for add, subtract, multiply and divide
        frame4 = Frame(window) # Create and add a frame to window
        frame4.grid(row = 5, column = 1, pady = 5, sticky = E)
        Button(frame4, text = "Add", command = self.add).pack(
            side = LEFT)
        Button(frame4, text = "Subtract", 
               command = self.subtract).pack(side = LEFT)
        Button(frame4, text = "Multiply", 
               command = self.multiply).pack(side = LEFT)
        Button(frame4, text = "Divide", 
               command = self.divide).pack(side = LEFT)
               
        mainloop()
        
    def add(self): 
        (Complex1, Complex2) = self.getBothComplex()
        result = Complex1.add(Complex2)
        self.result.set(result.toString())
    
    def subtract(self):
        (Complex1, Complex2) = self.getBothComplex()
        result = Complex1.subtract(Complex2)
        self.result.set(result.toString())
    
    def multiply(self):
        (Complex1, Complex2) = self.getBothComplex()
        result = Complex1.multiply(Complex2)
        self.result.set(result.toString())
    
    def divide(self):
        (Complex1, Complex2) = self.getBothComplex()
        result = Complex1.divide(Complex2)
        self.result.set(result.toString())

    def getBothComplex(self):
        """ Helper method used by add, subtract, multiply and divide methods """
        try:
            real1 = float(self.Complex1real.get())
            imaginary1 = float(self.Complex1imaginary.get())
            Complex1 = Complex(real1, imaginary1)

            real2 = float(self.Complex2real.get())
            imaginary2 = float(self.Complex2imaginary.get())
            Complex2 = Complex(real2, imaginary2)
            return (Complex1, Complex2)
        except ValueError:
            return (Complex(float('nan'), float('nan')), Complex(float('nan'), float('nan'))) # if an entry value is missing, cause NaN
if __name__ == "__main__": GUI()