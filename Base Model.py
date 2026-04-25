import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time

# Width/height of window
WIDTH = 600
HEIGHT = 400

# Number of rows/columns in the grid
ROWS = 2
COLS = 3

# Padding between squares
SQUARE_PADDING = 20

# Create the main application window
root = tk.Tk()
root.title("Music Recommendation")

# Create a canvas where shapes will appear
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# List to store user responses
responses = ["", "", "", "", "", ""]

# Each question is a string, to be displayed in a text box
questions = [
    "How stressed are you right now, on a scale of 1-5?",
    "How happy or content are you with life right now, on a scale of 1-5?",
    "How concerned or worried are you right now, on a scale of 1-5?",
    "How calm and relaxed do you feel at this moment, on a scale of 1-5?",
    "How overwhelmed do you feel right now, on a scale of 1-5?",
    "How energized or motivated do you feel right now on a scale of 1-5?"
]

# Store square IDs and square data
squares = []
square_data = {}

# Calculate width/height of each grid space
square_width = WIDTH // COLS
square_height = HEIGHT // ROWS

# Create grid layout
for row in range(ROWS):
    for col in range(COLS):

        # Calculate square coordinates
        x1 = col * square_width + SQUARE_PADDING
        y1 = row * square_height + SQUARE_PADDING
        x2 = (col + 1) * square_width - SQUARE_PADDING
        y2 = (row + 1) * square_height - SQUARE_PADDING

        # Draw the square
        square = canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="lightblue"
        )

        # Take one question from the shuffled list
        question = questions.pop(0)

        # Store information about this square and save it
        square_data[square] = {
            "question": question,
            "revealed": False 
        }
        squares.append(square)

def handle_click(event):
    """
    This function runs every time the user clicks
    on the canvas.
    The 'event' object contains information about
    where the mouse was clicked.
    """

    # Question asking logic
    clicked = canvas.find_closest(event.x, event.y)
    if not clicked:
        return

    square = clicked[0]
    if square not in square_data:
        return
    if square_data[square]["revealed"]:
        return
    
    question = square_data[square]["question"]
    responses[square - 1] = simpledialog.askstring("Evaluation Question", question)
    if responses[square - 1] is None:
        return

    # Save user answer and set box to green
    canvas.itemconfig(square, fill="lightgreen")
    messagebox.showinfo("Result", "Thank you!")
    square_data[square]["revealed"] = True

    if ("" not in responses):
        playlists = [["https://open.spotify.com/playlist/37i9dQZF1DWSkMjlBZAZ07", "Happy Folk"],
                    ["https://open.spotify.com/playlist/37i9dQZF1DX889U0CL85jj", "Mood Booster"],
                    ["https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0", "Chill Vibes"],
                    ["https://open.spotify.com/playlist/37i9dQZF1DWYoYGBbGKurt", "Lofi Chill"], 
                    ["https://open.spotify.com/playlist/37i9dQZF1DWVFeEut75IAL", "Calming Classical"]]
        for i in range(6):
            responses[i] = int(responses[i])
        happy_index = (responses[1] + responses[5]) / 2
        stressed_index = (responses[0] + responses[2] + responses[4]) / 3
        calm_index = responses[3]
        choice = 0
        # Boolean decision tree logic
        if (stressed_index <= 2):
            if (calm_index >= 3):
                if (happy_index >= 3):
                    choice = 3
                else:
                    choice = 2
            else:
                if (happy_index >= 3):
                    choice = 0
                else:
                    choice = 1
        else:
            if (calm_index >= 3):
                if (happy_index >= 3):
                    choice = 4
                else:
                    choice = 4
            else:
                if (happy_index >= 3):
                    choice = 3
                else:
                    choice = 2

    
        messagebox.showinfo("Result", "Thank you for responding to the mood evaluation questions!")
        time.sleep(0.1)
        messagebox.showinfo("Result", f"According to your responses, you should try listening to the '{playlists[choice][1]}' playlist: \n\n{playlists[choice][0]}")


# Run the handle_click function
canvas.bind("<Button-1>", handle_click)

# Main loop
root.mainloop()