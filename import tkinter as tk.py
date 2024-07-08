import tkinter as tk
from tkinter import messagebox
import random
import time

class NumberPuzzle(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Number Puzzle")
        self.geometry("500x500")
        self.resizable(False, False)

        self.colors = ["#FF6666", "#FFB266", "#FFFF66", "#B2FF66", "#66FF66", "#66FFB2", "#66FFFF", "#66B2FF",
                       "#6666FF", "#B266FF", "#FF66FF", "#FF66B2", "#FF6F61", "#6F61FF", "#616FFF", "#6FFF61"]
        self.numbers = list(range(1, 16)) + [""]
        random.shuffle(self.numbers)
        self.tiles = []
        self.total_clicks = 0
        self.start_time = time.time()  # Record the start time
        self.create_tiles()
        self.create_info_panel()

        self.bind_all("<Key>", self.key_press)  # Bind to all widgets
        self.update_timer()  # Start the timer

    def create_tiles(self):
        for i in range(4):
            row = []
            for j in range(4):
                number = self.numbers[i * 4 + j]
                tile = tk.Button(self, text=number, font=("Arial", 24), width=4, height=2,
                                 bg=self.colors[i * 4 + j] if number != "" else "#FFFFFF", fg="#000000")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def create_info_panel(self):
        self.info_frame = tk.Frame(self)
        self.info_frame.grid(row=4, column=0, columnspan=4, pady=10)

        self.click_count_label = tk.Label(self.info_frame, text="Total Clicks: 0", font=("Arial", 16))
        self.click_count_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(self.info_frame, text="Time: 0s", font=("Arial", 16))
        self.timer_label.pack(side=tk.LEFT, padx=10)

    def update_click_count_label(self):
        self.click_count_label.config(text=f"Total Clicks: {self.total_clicks}")

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.after(1000, self.update_timer)  # Update timer every second

    def key_press(self, event):
        key = event.keysym
        blank_pos = self.find_blank()
        if key == "Up" and blank_pos[0] < 3:
            self.swap_tiles(blank_pos, (blank_pos[0] + 1, blank_pos[1]))
        elif key == "Down" and blank_pos[0] > 0:
            self.swap_tiles(blank_pos, (blank_pos[0] - 1, blank_pos[1]))
        elif key == "Left" and blank_pos[1] < 3:
            self.swap_tiles(blank_pos, (blank_pos[0], blank_pos[1] + 1))
        elif key == "Right" and blank_pos[1] > 0:
            self.swap_tiles(blank_pos, (blank_pos[0], blank_pos[1] - 1))

        if self.check_win():
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Congratulations!", f"You've solved the puzzle in {elapsed_time} seconds and {self.total_clicks} clicks!")
            self.reset_game()

    def find_blank(self):
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j]["text"] == "":
                    return (i, j)
        return None

    def swap_tiles(self, pos1, pos2):
        self.total_clicks += 1  # Increment total click count
        self.update_click_count_label()  # Update the click count display

        tile1_text = self.tiles[pos1[0]][pos1[1]]["text"]
        tile2_text = self.tiles[pos2[0]][pos2[1]]["text"]
        self.tiles[pos1[0]][pos1[1]].config(text=tile2_text)
        self.tiles[pos2[0]][pos2[1]].config(text=tile1_text)

    def check_win(self):
        current = [self.tiles[i][j]["text"] for i in range(4) for j in range(4)]
        return current == list(map(str, range(1, 16))) + [""]

    def reset_game(self):
        self.numbers = list(range(1, 16)) + [""]
        random.shuffle(self.numbers)
        for i in range(4):
            for j in range(4):
                number = self.numbers[i * 4 + j]
                self.tiles[i][j].config(text=number,
                                        bg=self.colors[i * 4 + j] if number != "" else "#FFFFFF")

        self.total_clicks = 0
        self.update_click_count_label()
        self.start_time = time.time()  # Reset start time

if __name__ == "__main__":
    game = NumberPuzzle()
    game.mainloop()
