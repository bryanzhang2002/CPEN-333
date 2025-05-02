import threading
import queue
from tkinter import Tk, Canvas, Button
import random, time
from typing import Tuple, List, Dict, Any

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self) -> None:
        scoreTextXLocation: int = 60
        scoreTextYLocation: int = 15
        textColour: str = "white"
        self.root: Tk = Tk()
        self.canvas: Canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BACKGROUND_COLOUR)
        self.canvas.pack()
        self.snakeIcon: int = self.canvas.create_line((0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon: int = self.canvas.create_rectangle(0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        self.score: int = self.canvas.create_text(scoreTextXLocation, scoreTextYLocation, fill=textColour, text='Your Score: 0', font=("Helvetica", "11", "bold"))
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)
    
    def gameOver(self) -> None:
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton: Button = Button(self.canvas, text="Game Over!", height=3, width=10, font=("Helvetica", "14", "bold"), command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self) -> None:
        self.queue: queue.Queue[Dict[str, Any]] = gameQueue
        self.gui: Gui = gui
        self.queueHandler()
    
    def queueHandler(self) -> None:
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules 
            to call itself after a short delay.
        '''
        try:
            while True:
                task: Dict[str, Any] = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points: List[int] = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)

class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self) -> None:
        self.queue: queue.Queue[Dict[str, Any]] = gameQueue
        self.score: int = 0
        self.snakeCoordinates: List[Tuple[int, int]] = [(495, 55), (485, 55), (475, 55), (465, 55), (455, 55)]
        self.direction: str = "Left"
        self.gameNotOver: bool = True
        self.prey: Tuple[int, int]  # Added to indicate the type of self.prey
        self.createNewPrey()
    
    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED: float = 0.15
        while self.gameNotOver:
            self.move()
            time.sleep(SPEED)
    
    def whenAnArrowKeyIsPressed(self, e: Any) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection: str = self.direction
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym
    
    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """
        
        # Calculate the new head position based on the current direction
        # This uses calculateNewCoordinates() to determine where the snake moves next
        newHead: Tuple[int, int] = self.calculateNewCoordinates()
        # Add the new head to the snake's coordinate list, extending the snake's length
        self.snakeCoordinates.append(newHead)
        
        prey_x: int
        prey_y: int
        prey_x, prey_y = self.prey
        # Check if the snake's head overlaps with the prey within a tolerance
        # The condition checks if the distance between the head and prey center is less than
        # SNAKE_ICON_WIDTH (15 pixels) in both x and y directions, creating a square capture zone
        if (abs(newHead[0] - prey_x) < SNAKE_ICON_WIDTH and abs(newHead[1] - prey_y) < SNAKE_ICON_WIDTH): # If the snake's head is close enough to the prey
            self.score += 1
            self.queue.put({"score": self.score})
            # Spawn a new prey at a random valid position
            self.createNewPrey()
        else:
            # If no prey is captured, remove the tail to keep the snake's length constant
            # This simulates the snake moving forward without growing
            self.snakeCoordinates.pop(0)
        
        # Check if the game should end due to the new head position (e.g., hitting a wall or itself)
        # This updates the gameNotOver flag and adds a "game_over" task if necessary   
        self.isGameOver(newHead)
        # If the game is still ongoing, add a "move" task to update the snake's position in the GUI
        if self.gameNotOver:
            # This signals the program to update the GUI
            self.queue.put({"move": self.snakeCoordinates})
    
    def calculateNewCoordinates(self) -> Tuple[int, int]:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        
        lastX: int
        lastY: int
        lastX, lastY = self.snakeCoordinates[-1]
        if self.direction == "Left":
            return (lastX - SNAKE_ICON_WIDTH, lastY)
        elif self.direction == "Right":
            return (lastX + SNAKE_ICON_WIDTH, lastY)
        elif self.direction == "Up":
            return (lastX, lastY - SNAKE_ICON_WIDTH)
        elif self.direction == "Down":
            return (lastX, lastY + SNAKE_ICON_WIDTH)
    
    def isGameOver(self, snakeCoordinates: Tuple[int, int]) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        
        x: int
        y: int
        x, y = snakeCoordinates
        if (x < 0 or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT or 
            snakeCoordinates in self.snakeCoordinates[:-1]):
            self.gameNotOver = False
            self.queue.put({"game_over": True})
    
    def createNewPrey(self) -> None:
        """
            Creates a new prey at a random location not overlapping with snake.
            This method generates a random position for the new prey within the canvas boundaries,
            ensuring it respects a THRESHOLD distance from the walls and does not overlap with the
            snake's current position. The prey's position is then used to define a rectangle for
            display, and a task is added to the queue to update the GUI.
        """
        # Define the THRESHOLD (15 pixels) to keep the prey away from the canvas edges
        # This ensures the prey is fully visible and not too close to the walls
        THRESHOLD: int = 15
        # Iterate random positions until a valid one is found
        while True:
            # Generate a random x-coordinate within the canvas, respecting the THRESHOLD
            # Range: [THRESHOLD, WINDOW_WIDTH - THRESHOLD] (e.g., [15, 485] for a 500px width)
            x: int = random.randint(THRESHOLD, WINDOW_WIDTH - THRESHOLD)
            # Generate a random y-coordinate within the canvas, respecting the THRESHOLD
            # Range: [THRESHOLD, WINDOW_HEIGHT - THRESHOLD] (e.g., [15, 285] for a 300px height)
            y: int = random.randint(THRESHOLD, WINDOW_HEIGHT - THRESHOLD)
            # Check if new prey position doesn't overlap with snake
            too_close: bool = False   # Flag to track if the current (x, y) position overlaps with the snake
            # Check the current (x, y) position against each snake segment's coordinates (sx, sy)
            for sx, sy in self.snakeCoordinates:
                # Determine if the position (x, y) overlaps with the snake segment at (sx, sy)
                # Overlap occurs if the distance in both x and y directions is less than SNAKE_ICON_WIDTH
                # This creates a square exclusion zone around each snake segment (15x15 pixels)
                if abs(sx - x) < SNAKE_ICON_WIDTH and abs(sy - y) < SNAKE_ICON_WIDTH:
                    too_close = True
                    break
            # If the position does not overlap with any snake segment, it's a valid spawn point
            if not too_close:
                break  # Exit the loop since we found a valid position
                
        # Store the selected (x, y) position as the prey's center coordinates
        # This is used for prey capture detection in the move() method        
        self.prey = (x, y)
        # Calculate the prey's rectangle coordinates for display on the canvas
        # The prey is a square with side length PREY_ICON_WIDTH (10 pixels), centered at (x, y)
        # The rectangle is defined as (x1, y1, x2, y2) where:
        # x1 = x - PREY_ICON_WIDTH//2, y1 = y - PREY_ICON_WIDTH//2
        # x2 = x + PREY_ICON_WIDTH//2, y2 = y + PREY_ICON_WIDTH//2
        prey_coords: Tuple[int, int, int, int] = (x - PREY_ICON_WIDTH//2, y - PREY_ICON_WIDTH//2, 
                      x + PREY_ICON_WIDTH//2, y + PREY_ICON_WIDTH//2)
        # Add a "prey" task to the queue to update the prey's position in the GUI
        # The task contains the rectangle coordinates for the QueueHandler to process
        self.queue.put({"prey": prey_coords})

if __name__ == "__main__":
    WINDOW_WIDTH: int = 500
    WINDOW_HEIGHT: int = 300
    SNAKE_ICON_WIDTH: int = 15
    PREY_ICON_WIDTH: int = 10
    BACKGROUND_COLOUR: str = "green"
    ICON_COLOUR: str = "yellow"
    gameQueue: queue.Queue[Dict[str, Any]] = queue.Queue()       #instantiate a queue object using python's queue class
    game: Game = Game()                   #instantiate the game object
    gui: Gui = Gui()                     #instantiate the game user interface
    QueueHandler()                  #instantiate the queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target=game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()