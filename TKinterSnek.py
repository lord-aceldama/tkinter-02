import random
import tkinter as tk


#-- Defined Constants
BLOCK_SIZE = 15
WORLD_WIDTH = 40
WORLD_HEIGHT = 30
SNEK_SPEED = 5
TICK = 1000
REVERSE = (set(["Up", "Down"]), set(["Left", "Right"]))


class Snek(tk.Canvas):
    """ Inhertit the tkinter Cnvas class
    """
    def __init__(self):
        """ Init variables
        """
        self.width = WORLD_WIDTH * BLOCK_SIZE
        self.height = WORLD_HEIGHT * BLOCK_SIZE

        super().__init__(width=self.width, height=self.height, background="black", highlightthickness=0)
        self.bind_all("<Key>", self.on_keypress)

        #-- Set default values
        self.reset()

        #-- Draw the world
        self.draw_world()

        #-- Start the ticks
        self.after(self.game_speed, self.tick)


    def reset(self):
        """ Inits default values
        """
        self.score = 0
        self.direction = "Right"
        self.snekpos = [(5 * BLOCK_SIZE, 5 * BLOCK_SIZE), (4 * BLOCK_SIZE, 5 * BLOCK_SIZE), (3 * BLOCK_SIZE, 5 * BLOCK_SIZE)]
        self.foodpos = self.drop_nom()
        self.snek_speed = SNEK_SPEED
        self.game_speed = TICK // self.snek_speed


    def drop_nom(self):
       """ Reurns a random location on the map
       """
       pos = (random.randint(1, WORLD_WIDTH - 2) * BLOCK_SIZE, random.randint(1, WORLD_HEIGHT - 2) * BLOCK_SIZE)
       while pos in self.snekpos:
           pos = (random.randint(1, WORLD_WIDTH - 2) * BLOCK_SIZE, random.randint(1, WORLD_HEIGHT - 2) * BLOCK_SIZE)

       return pos


    def draw_world(self):
        """ Display our world and everything in it
        """
        #-- Draw the world's edge
        self.create_rectangle(7, 27, self.width - 7, self.height - 7, outline="#666")

        #-- Draw the snek
        for x, y in self.snekpos:
            self.create_rectangle(x, y, x+BLOCK_SIZE, y+BLOCK_SIZE, outline="#0f0", fill="#080", tag="snek")

        #-- Draw food
        self.create_rectangle(
            self.foodpos[0], self.foodpos[1], self.foodpos[0] + BLOCK_SIZE, self.foodpos[1] + BLOCK_SIZE, 
            outline="#ff0", fill="#880", tag="food"
        )

        #-- Draw the score
        self.create_text(
            45, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=("TkDefaultFont", 14)
        )

    
    def move_snek(self):
        """ Move snek and update canvas snek segment positions
        """
        x, y = self.snekpos[0]
        if self.direction == "Left":
            x = x - BLOCK_SIZE
        elif self.direction == "Right":
            x = x + BLOCK_SIZE
        elif self.direction == "Up":
            y = y - BLOCK_SIZE
        else: #-- Down
            y = y + BLOCK_SIZE

        #-- Trim snek tail, add snek head
        self.snekpos = [(x, y)] + self.snekpos[:-1]

        #-- Move the canvas elements
        for seg, pos in zip(self.find_withtag("snek"), self.snekpos):
            self.coords(seg, pos[0], pos[1], pos[0] + BLOCK_SIZE, pos[1] + BLOCK_SIZE)


    def check_collisions(self):
        """ Return True if snek deaded
        """
        x, y = self.snekpos[0]
        return (
            (x <= 0) or (x >= (self.width - BLOCK_SIZE)) or     #-- X boundary
            (y <= 0) or (y >= (self.height - BLOCK_SIZE)) or    #-- Y boundary
            self.snekpos[0] in self.snekpos[1:]                 #-- Head of snek eats self
        )


    def check_nom(self):
        """ Check if snek nommed food
        """
        if self.snekpos[0] == self.foodpos:
            #-- Inc score
            self.score = self.score + 1
            self.itemconfigure(self.find_withtag("score"), text=f"Score: {self.score}")

            #-- Add extra tail so snek can stretch
            x, y = self.snekpos[-1]
            self.create_rectangle(x, y, x+BLOCK_SIZE, y+BLOCK_SIZE, outline="#0f0", fill="#080", tag="snek")
            self.snekpos.append(None) #-- Can be nothing, because move_snek strips last element

            #-- Move food
            self.foodpos = self.drop_nom()
            nom = self.find_withtag("food")
            self.coords(nom, self.foodpos[0], self.foodpos[1], self.foodpos[0] + BLOCK_SIZE, self.foodpos[1] + BLOCK_SIZE)


    def tick(self):
        """ Main timing engine
        """
        if self.check_collisions():
            return
        else:
            self.check_nom()
            self.move_snek()
            self.after(self.game_speed, self.tick)


    def on_keypress(self, e):
        """ Handle keypresses
        """
        if not ((self.direction == e.keysym) or (set([self.direction, e.keysym]) in REVERSE)) :
            self.direction = e.keysym


#-- Init main window
root=tk.Tk()
root.title = "Snek"
root.resizable = False

#-- Init Snek (Canvas)
board = Snek()

#-- Add Snek to window and run
board.pack()
root.mainloop()
