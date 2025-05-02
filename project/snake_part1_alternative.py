# This implementation uses threading.Event and a shared task list instead of queue.Queue
# for inter-thread communication and synchronization, demonstrating an alternative
# multitasking synchronization approach.

import threading
from tkinter import Tk, Canvas, Button
import random
import time
from typing import List, Tuple, Dict, Optional, Any

class Gui:
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
        self.score: int = self.canvas.create_text(scoreTextXLocation, scoreTextYLocation, fill=textColour, 
                                            text='Your Score: 0', font=("Helvetica", "11", "bold"))
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self) -> None:
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton: Button = Button(self.canvas, text="Game Over!", height=3, width=10, font=("Helvetica", "14", "bold"), command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)

class TaskHandler:
    """
        Manages game tasks using a shared list and threading.Event for synchronization.
    
        This class replaces the original QueueHandler by using a shared list and threading.Event
        to manage tasks between the game thread and the GUI thread. It processes tasks like updating
        the snake's position, spawning new prey, updating the score, or ending the game.
    """
    def __init__(self, task_list: List[Dict[str, Any]], task_event: threading.Event) -> None:
        """
            Initializes the TaskHandler with a shared task list and event for synchronization.
        
            Args:
                task_list (List[Dict[str, any]]): A shared list to store tasks (e.g., move, prey, score updates).
                task_event (threading.Event): An event object to signal when new tasks are available.
        """
        # Store the shared task list where the game thread will append tasks
        self.task_list: List[Dict[str, Any]] = task_list
        # Store the threading.Event object used to signal when tasks are ready to process
        self.task_event: threading.Event = task_event
        # Reference to the GUI object to update the canvas and other elements
        self.gui: Gui = gui
        # Schedule the taskHandler method to run after 5 milliseconds using Tkinter's after method
        # This ensures non-blocking periodic checks for tasks in the main thread
        self.gui.root.after(5, self.taskHandler)

    def taskHandler(self) -> None:
        """
            Processes tasks from the shared list when signaled by the event.
        
            This method is called periodically (every 5ms) to check if there are tasks to process.
            It checks the threading.Event to see if the game thread has signaled new tasks, and if
            tasks are available in the list, it processes one task per call in a FIFO manner. After
            processing, it reschedules itself to run again, ensuring continuous task handling without
            blocking the Tkinter main loop.
        """
        # Check if the event is set (indicating new tasks) and if there are tasks in the list
        if self.task_event.is_set() and self.task_list:
            # Clear the event to indicate that we're handling the tasks
            # This prevents re-processing the same signal until the game thread sets it again
            self.task_event.clear()
            # Pop the first task from the list (FIFO behavior, similar to a queue)
            task: Dict[str, Any] = self.task_list.pop(0)
            # Process the task based on its type
            if "game_over" in task:
                # Debug: Confirm the "game_over" task is being processed
                print("Processing 'game_over' task")
                # If the task is "game_over", display the "Game Over!" button on the canvas
                self.gui.gameOver()
            elif "move" in task:
                # If the task is "move", update the snake's position on the canvas
                # Flatten the list of coordinates [(x1, y1), (x2, y2), ...] into [x1, y1, x2, y2, ...]
                points: List[int] = [x for point in task["move"] for x in point]
                # Update the snake icon's coordinates on the canvas using the flattened points
                self.gui.canvas.coords(self.gui.snakeIcon, *points)
            elif "prey" in task:
                # If the task is "prey", update the prey's position on the canvas
                # The task["prey"] value is a tuple (x1, y1, x2, y2) defining the prey rectangle
                self.gui.canvas.coords(self.gui.preyIcon, *task["prey"])
            elif "score" in task:
                # If the task is "score", update the displayed score on the canvas
                # Format the score text as "Your Score: N" where N is the new score
                self.gui.canvas.itemconfigure(self.gui.score, text=f"Your Score: {task['score']}")
        # Schedule the next call to taskHandler after 5 milliseconds
        # This ensures continuous checking for new tasks without blocking the GUI
        self.gui.root.after(5, self.taskHandler)

class Game:
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, task_list: List[Dict[str, Any]], task_event: threading.Event) -> None:
        self.task_list: List[Dict[str, Any]] = task_list
        self.task_event: threading.Event = task_event
        self.score: int = 0
        self.snakeCoordinates: List[Tuple[int, int]] = [(495, 55), (485, 55), (475, 55), (465, 55), (455, 55)]
        self.direction: str = "Left"
        self.gameNotOver: bool = True
        # Precompute valid positions for prey spawning
        self.THRESHOLD: int = 15
        self.valid_positions: List[Tuple[int, int]] = self._compute_valid_positions()
        self.prey: Tuple[int, int]  # Added to indicate the type of self.prey
        self.createNewPrey()
        # Initial snake position update
        self.task_list.append({"move": self.snakeCoordinates})
        self.task_event.set()

    def _compute_valid_positions(self) -> List[Tuple[int, int]]:
        """
            Precomputes a list of valid positions for prey spawning, excluding snake positions.
            This method creates a grid of possible positions on the canvas, stepped by SNAKE_ICON_WIDTH,
            and checks each position to ensure it doesn't overlap with the snake. The resulting list of
            valid positions is used by createNewPrey() to quickly select a spawn location, improving
            performance by avoiding trial-and-error random generation.
        """

        valid_positions: List[Tuple[int, int]] = []  # Create an empty list to store valid positions into
        step: int = SNAKE_ICON_WIDTH  # Use the snake width as the grid step for efficiency
        for x in range(self.THRESHOLD, WINDOW_WIDTH - self.THRESHOLD, step): # Iterate through the canvas
            for y in range(self.THRESHOLD, WINDOW_HEIGHT - self.THRESHOLD, step): # Iterate through the canvas
                too_close: bool = False
                for sx, sy in self.snakeCoordinates:
                    # Determine if the position (x, y) overlaps with the snake segment at (sx, sy)
                    # Overlap occurs if the distance in both x and y directions is less than SNAKE_ICON_WIDTH
                    # This creates a square exclusion zone around each snake segment
                    if abs(sx - x) < SNAKE_ICON_WIDTH and abs(sy - y) < SNAKE_ICON_WIDTH:  # If it is too close to the edge, disregard this coordinate
                        too_close = True
                        break
                if not too_close:       # If it isnt too close to the edge, count it in the valid positions list to use in future implementation below
                    valid_positions.append((x, y))
        return valid_positions

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
        if (abs(newHead[0] - prey_x) < SNAKE_ICON_WIDTH and abs(newHead[1] - prey_y) < SNAKE_ICON_WIDTH):  # If the snake's head is close enough to the prey
            self.score += 1
            self.task_list.append({"score": self.score})
            # Since the snake will grow (by not removing the tail), update the list of valid
            # prey spawn positions to account for the new snake segment
            self.valid_positions = self._compute_valid_positions()
            # Spawn a new prey at a random valid position
            self.createNewPrey()
        else:
            # If no prey is captured, remove the tail to keep the snake's length constant
            # This simulates the snake moving forward without growing
            self.snakeCoordinates.pop(0)
            # Update the valid prey spawn positions to account for the snake's new position
            # This ensures the next prey spawn avoids the updated snake body
            self.valid_positions = self._compute_valid_positions()
            
        # Check if the game should end due to the new head position (e.g., hitting a wall or itself)
        # This updates the gameNotOver flag and adds a "game_over" task if necessary    
        self.isGameOver(newHead)
        # If the game is still ongoing, add a "move" task to update the snake's position in the GUI
        if self.gameNotOver:
            self.task_list.append({"move": self.snakeCoordinates})
        # Signal the TaskHandler that new tasks are available to process
        # This sets the threading.Event, prompting the TaskHandler to update the GUI
        self.task_event.set()  # Signal task handler

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
                if self.gameNotOver:  # Prevent multiple calls
                    self.gameNotOver = False  # Stop the game loop
                    self.task_list.append({"game_over": True})
                    self.task_event.set()
                    # Ensure gameOver() is only called once from the main thread
                    gui.root.after(0, lambda: gui.gameOver())
                    
    def createNewPrey(self) -> None:
        """
            Creates a new prey at a random, snake-free location from precomputed positions.
            This method spawns a new prey by selecting a random position from the precomputed
            list of valid positions (valid_positions). If no valid positions are available, it
            recomputes the list or falls back to a random position within the canvas boundaries.
            The prey's coordinates are then used to define a rectangle for display, and a task
            is added to update the GUI.
        """
        # Check if the list of valid positions is empty
        # This can happen if the snake occupies most of the canvas or after initialization
        if not self.valid_positions:  
            # Recompute the valid positions to ensure we have a list to choose from
            # This calls _compute_valid_positions() to generate new spawn points
            self.valid_positions = self._compute_valid_positions()
        if self.valid_positions:
            # Select a random (x, y) position from the list of valid positions
            # random.choice ensures an even distribution of spawn points
            x: int
            y: int
            x, y = random.choice(self.valid_positions)
        else:
            # Fallback case: if no valid positions are available (e.g., snake covers most of the canvas)
            # Generate a random position within the canvas boundaries as a last resort
            # This ensures the game can continue even in rare edge cases
            x: int = random.randint(self.THRESHOLD, WINDOW_WIDTH - self.THRESHOLD)
            y: int = random.randint(self.THRESHOLD, WINDOW_HEIGHT - self.THRESHOLD)
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
        # Add a "prey" task to the task list to update the prey's position in the GUI
        # The task contains the rectangle coordinates for the TaskHandler to process
        self.task_list.append({"prey": prey_coords})
        # Signal the TaskHandler that a new task is available
        # This sets the threading.Event, prompting the TaskHandler to update the GUI
        self.task_event.set()

if __name__ == "__main__":
    WINDOW_WIDTH: int = 500
    WINDOW_HEIGHT: int = 300
    SNAKE_ICON_WIDTH: int = 15
    PREY_ICON_WIDTH: int = 10
    BACKGROUND_COLOUR: str = "green"
    ICON_COLOUR: str = "yellow"

    # Shared resources for task management
    game_tasks: List[Dict[str, Any]] = []
    task_event: threading.Event = threading.Event()

    # Instantiate the game object first to ensure it's defined before Gui tries to access it
    game: Game = Game(game_tasks, task_event)
    # Instantiate the GUI after the game object
    gui: Gui = Gui()
    TaskHandler(game_tasks, task_event)

    # Start a thread with the main loop of the game
    threading.Thread(target=game.superloop, daemon=True).start()

    # Start the GUI's own event loop
    gui.root.mainloop()