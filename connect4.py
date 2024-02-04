import tkinter as tk
from tkinter import PhotoImage,ttk,scrolledtext,messagebox
import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
cell_size = 50
circle_radius = cell_size // 2 - 5

class Connect4Board:
    def __init__(self, master, rows, columns):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.current_player = 1  # Player 1 starts
        self.board_array =  [[0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]]
        self.move_no = 1
        self.iswin = False
        self.isdraw = False
    
        self.frame_for_board = tk.Frame(self.master, width=columns * cell_size + 10, height=rows * cell_size + 60,bg='blue')
        self.frame_for_board.place(x=120, y=20)
        self.canvas_for_droping_ball = tk.Canvas(self.frame_for_board, width=columns * cell_size, height=cell_size)
        self.canvas_for_droping_ball.pack()

        self.canvas = tk.Canvas(self.frame_for_board, width=columns * cell_size, height=rows * cell_size)
        self.canvas.pack()
        self.turn_label = tk.Label(self.master, text="Player's Turn:", font=("Helvetica", 16),bg='#8ab7aa')
        self.turn_label.place(x='150',y='390')
        self.turn_label_value = tk.Label(self.master, text="", font=("Helvetica", 16),bg='#8ab7aa')
        self.turn_label_value.place(x='290',y='390')

        self.move_label = tk.Label(self.master, text="Move Number:", font=("Helvetica", 16),bg='#8ab7aa')
        self.move_label.place(x='150',y='430')
        self.move_label_value = tk.Label(self.master, text="", font=("Helvetica", 16),bg='#8ab7aa')
        self.move_label_value.place(x='290',y='430')


        self.draw_board()

    def move_ball(self, event):
        # Move the ball horizontally with the mouse motion
        x = event.x
        y = cell_size // 2  # Lock the y-coordinate to the center of the canvas
        self.canvas_for_droping_ball.coords(self.ball_id, x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius)

    def drop_ball(self, event):
        # Determine the column based on the mouse click position
        column = event.x // cell_size
        print(f"Clicked on column {column + 1}")
        row = self.get_next_empty_row(column)
        if row is not None:
            self.update_board(row, column)
            self.move_no = self.move_no+1
            if self.check_win(row, column):
                print(f"Player {self.current_player} wins!")
                self.iswin = True
                self.winning_player = self.current_player  
            elif self.move_no == 43:
                self.isdraw = True
            else:
                self.switch_player()
            self.draw_board()
            if self.iswin:
                if self.winning_player ==1:
                    messagebox.showinfo('Win','Player 1 wins!')
                else:
                    messagebox.showinfo('Win','Player 2 wins!')
                self.reset_board()
            if self.isdraw:
                messagebox.showinfo('Draw','Nobody won. Game has been drawn!')
                self.reset_board()    

    def get_next_empty_row(self, column):
        for row in range(self.rows - 1, -1, -1):
            if self.board_array[row][column] == 0:
                return row
        return None

    def update_board(self, row, column):
        self.board_array[row][column] = self.current_player

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas_for_droping_ball.delete("all")
        # Initially position the ball in the center of the 4th column
        initial_column = 3
        initial_x = (initial_column * cell_size) + (cell_size // 2)
        initial_y = cell_size // 2
        self.ball_id = self.canvas_for_droping_ball.create_oval(
            initial_x - circle_radius, initial_y - circle_radius, initial_x + circle_radius, initial_y + circle_radius,
            fill='red' if self.current_player == 1 else 'yellow', outline='red' if self.current_player == 1 else 'yellow',
            tags="ball"
        )

        self.canvas_for_droping_ball.bind("<Motion>", self.move_ball)
        self.canvas_for_droping_ball.bind("<Button-1>", self.drop_ball)

        for row in range(self.rows):
            for col in range(self.columns):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Draw rectangle
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='white', fill='blue')

                # Draw circle slot in the center of the rectangle
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                player_color = 'red' if self.board_array[row][col] == 1 else 'yellow' if self.board_array[row][col] == 2 else 'white'
                self.canvas.create_oval(center_x - circle_radius, center_y - circle_radius,
                                        center_x + circle_radius, center_y + circle_radius, fill=player_color, outline=player_color)
        
        if self.current_player == 1:
            self.turn_label_value.config(text='Player 1 (Red Player)')
        else:
            self.turn_label_value.config(text='Player 2 (Yellow Player)')

        self.move_label_value.config(text=str(self.move_no))


    def check_win(self, row, col):
        # Check for a win in the horizontal row
        if self.check_horizontal_row(row):
            return True
        # Check for a win in the vertical column
        if self.check_vertical_column(col):
            return True
        # Checking diagonally 
        if self.check_diagonal_topleft_to_bottomright(row,col):
            return True
        # Checking diagonally 
        if self.check_diagonal_topright_to_bottomleft(row,col):
            return True
        # Check for a win in the diagonal (top-left to bottom-right)
        if self.check_line([self.board_array[i][i] for i in range(min(self.rows, self.columns))]):
            return True
        # Check for a win in the diagonal (top-right to bottom-left)
        if self.check_line([self.board_array[i][self.columns - 1 - i] for i in range(min(self.rows, self.columns))]):
            return True
        #if no win i.e no 4 consecutive matches
        return False
    
    #logic for checking horizontally
    def check_horizontal_row(self,row):
        return self.check_line(self.board_array[row])
    
    #logic for checking veritcalyy
    def check_vertical_column(self,col):
        line_array = []
        for i in range(self.rows):
            line_array.append(self.board_array[i][col])
        return self.check_line(line_array)
    
    #logic for checking top left to bottom right for win
    def check_diagonal_topleft_to_bottomright(self,row,col):
        line_array = []
        if row-col >= 0:
            new_row,new_col = abs(row-col),0 # new starting position of row and column for checking
        else:
            new_row,new_col = 0,abs(row-col)

        while(new_row<=5 and new_col<=6):
            line_array.append(self.board_array[new_row][new_col])
            new_row = new_row+1 #to increment row and column diagonally
            new_col = new_col+1

        return self.check_line(line_array)
    
    #logic for checking top right to bottom left for win
    def check_diagonal_topright_to_bottomleft(self,row,col):
        line_array = []
        if row+col <= 6:
            new_row,new_col = 0,row+col # new starting position of row and columns for checking
        
        else:
            new_row,new_col = (row+col)%6,6
    
        while(new_row<=5 and new_col>=0):
            line_array.append(self.board_array[new_row][new_col])
            new_row = new_row+1 # to increment row and col diagonally
            new_col = new_col-1
        return self.check_line(line_array)
    
    #logic for checking line if there are four consecutive ball 
    def check_line(self, line):
        count = 0
        for i in line:
            if i == self.current_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switch player between 1 and 2

    def reset_board(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.board_array[i][j] = 0
        self.current_player = 1
        self.move_no = 1
        self.iswin = False
        self.isdraw = False

        self.draw_board()

def play():
    pygame.mixer.Sound.play(click_sound)
    menu_screen.destroy()
    global play_menu
    play_menu = tk.Tk()
    screen_width = play_menu.winfo_screenwidth()
    screen_height = play_menu.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    play_menu.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    play_menu.resizable(False, False)
    play_menu.title("Play")
    play_menu.configure(bg="#8ab7aa")
    
    back_path = "buttons/back_arrow.png"
    back_icon = PhotoImage(file=back_path)
    back_button = tk.Button(play_menu, image=back_icon,command=back_clicked3, bd=0, relief=tk.FLAT)
    back_button.place(x ='10',y='10')

    reset_path = "buttons/reset.png"
    reset_icon = PhotoImage(file=reset_path)
    reset_button = tk.Button(play_menu, image=reset_icon,command=reset_clicked, bd=0, relief=tk.FLAT)
    reset_button.place(x ='10',y='50')


    connect4_board = Connect4Board(play_menu, rows=6, columns=7)
    play_menu.mainloop()

def reset_clicked():
        pygame.mixer.Sound.play(click_sound)
        Connect4Board(play_menu, rows=6, columns=7).reset_board()

def option():
    
    pygame.mixer.Sound.play(click_sound)
    menu_screen.destroy()
    global option_menu
    option_menu = tk.Tk()
    screen_width = option_menu.winfo_screenwidth()
    screen_height = option_menu.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    option_menu.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    option_menu.resizable(False, False)
    option_menu.title("Settings")

    background_image_path = "buttons/background4.png"
    background_img = PhotoImage(file=background_image_path)

    # Create a Label to display the background image
    background_label = tk.Label(option_menu, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Set the volume for music 
    def set_volume_music(volume):
      
        pygame.mixer.music.set_volume(volume)

    #set volume for button 
    def set_volume_button(volume):
        click_sound.set_volume(volume)

    

    style = ttk.Style()
    style.configure("TScale", thickness=30, troughcolor="blue", sliderlength=30)

    music_volume_label = tk.Label(option_menu, text="Music Volume:", font=("Helvetica", 20))
    music_volume_label.place(x='100',y='100')
    
    # Create a Scale widget for volume control using ttk
    music_volume_scale = ttk.Scale(option_menu, from_=0.0, to=1.0, length=200, orient=tk.HORIZONTAL,
                             command=lambda volume: set_volume_music(float(volume)), style="TScale")

    music_volume_scale.place(x='300',y='105')
    
    #create scale widget for button volume

    button_volume_label = tk.Label(option_menu, text="Button Volume:", font=("Helvetica", 20))
    button_volume_label.place(x='100',y='200')
    
    button_volume_scale = ttk.Scale(option_menu, from_=0.0, to=1.0, length=200, orient=tk.HORIZONTAL,
                             command=lambda volume: set_volume_button(float(volume)), style="TScale")

    button_volume_scale.place(x='300',y='205')

    back_path = "buttons/back_arrow.png"
    back_icon = PhotoImage(file=back_path)
    back_button = tk.Button(option_menu, image=back_icon,command=back_clicked1, bd=0, relief=tk.FLAT)
    back_button.place(x ='10',y='10' )
    
    option_menu.mainloop()

def back_clicked1():
    pygame.mixer.Sound.play(click_sound)
    option_menu.destroy()
    main_menu()

def back_clicked2():
    pygame.mixer.Sound.play(click_sound)
    help_menu.destroy()
    main_menu()

def back_clicked3():
    pygame.mixer.Sound.play(click_sound)
    play_menu.destroy()
    main_menu()

    
def help():
    pygame.mixer.Sound.play(click_sound)
    menu_screen.destroy()
    global help_menu
    help_menu = tk.Tk()
    screen_width = help_menu.winfo_screenwidth()
    screen_height = help_menu.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    help_menu.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    help_menu.resizable(False, False)
    help_menu.title("How to play?")

    background_image_path = "buttons/background4.png"
    background_img = PhotoImage(file=background_image_path)

    # Create a Label to display the background image
    background_label = tk.Label(help_menu, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    back_path = "buttons/back_arrow.png"
    back_icon = PhotoImage(file=back_path)
    back_button = tk.Button(help_menu, image=back_icon,command=back_clicked2, bd=0, relief=tk.FLAT)
    back_button.place(x ='10',y='10')
    # Instructions text
    instructions_text = (
        "Objective:\n"
        "Connect Four is a classic two-player connection game in which the players take turns dropping colored discs "
        "from the top into a vertically suspended grid. The objective is to connect four of one's own discs of the same "
        "color vertically, horizontally, or diagonally before the opponent.\n\n"
        
        "Game Setup:\n"
        "1. The game is played on a vertical grid with six rows and seven columns.\n"
        "2. Each player is assigned a color, typically red or yellow.\n"
        "3. The game begins with an empty grid.\n\n"

        "Player Turns:\n"
        "1. Players take turns to drop one of their colored discs into any of the seven columns.\n"
        "2. The disc will occupy the lowest available space within the selected column.\n\n"

        "Winning the Game:\n"
        "1. The game is won by the first player to connect four of their discs in a row.\n"
        "2. The connection can be vertical, horizontal, or diagonal.\n"
        "3. Once a player achieves a Connect Four, they win the game.\n\n"

        "Draw:\n"
        "1. If the entire grid is filled with discs and no player has connected four in a row, the game is a draw.\n\n"

        "Game Controls:\n"
        "1. You can move the disc on top of columns.\n"
        "2. To drop a disc, click on the top of column where you want to place it.\n\n"

        "Tips:\n"
        "1. Plan ahead and try to block your opponent's potential connections.\n"
        "2. Pay attention to both horizontal and diagonal possibilities.\n"
        "3. Be strategic in creating opportunities for yourself while hindering your opponent's progress.\n\n"

        "Enjoy playing Connect Four!"
    )
    # Create a scrolled text widget
    instructions_text_widget = scrolledtext.ScrolledText(help_menu, wrap=tk.WORD, width=60, height=30)
    instructions_text_widget.insert(tk.END, instructions_text)
    instructions_text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
    instructions_text_widget.pack(pady=100)

    help_menu.mainloop()


def quit():
    exit()
    

def main_menu():
    global menu_screen
    menu_screen = tk.Tk()
    screen_width = menu_screen.winfo_screenwidth()
    screen_height = menu_screen.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    menu_screen.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    menu_screen.resizable(False, False)
    menu_screen.title("Connect Four")

    background_image_path = "buttons/background4.png"
    background_img = PhotoImage(file=background_image_path)

    # Create a Label to display the background image
    background_label = tk.Label(menu_screen, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load icons
    play_path = "buttons/play_new.png"
    play_icon = PhotoImage(file=play_path)

    option_path = "buttons/option.png"
    option_icon = PhotoImage(file=option_path)

    help_path = "buttons/help_new.png"
    help_icon = PhotoImage(file=help_path)

    exit_path = "buttons/exit_new.png"
    exit_icon = PhotoImage(file=exit_path)

    # Create buttons with icons and arrange them using grid
    play_button = tk.Button(menu_screen, image=play_icon,command=play, bd=0, relief=tk.FLAT)
    option_button = tk.Button(menu_screen, image=option_icon,command=option, bd=0, relief=tk.FLAT)
    help_button = tk.Button(menu_screen, image=help_icon,command=help, bd=0, relief=tk.FLAT)
    exit_button = tk.Button(menu_screen, image=exit_icon,command=quit, bd=0, relief=tk.FLAT)

    # Pack buttons to center them vertically
    play_button.pack(side=tk.TOP, pady=(80, 20))
    option_button.pack(side=tk.TOP, pady=20)
    help_button.pack(side=tk.TOP, pady=20)
    exit_button.pack(side=tk.TOP, pady=20)

    

    

    # Use after() to delay starting the music after Tkinter main loop has started
    #menu_screen.after(100, start_music)

    menu_screen.mainloop()

if __name__ == "__main__":
    pygame.mixer.init()
    def start_music():
        # Load the background music
        pygame.mixer.music.load("music/musicMain.ogg")
        pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
        pygame.mixer.music.set_volume(0.2)
    start_music()
    global click_sound
    click_sound = pygame.mixer.Sound("music/ClickChess.wav")
    main_menu()
