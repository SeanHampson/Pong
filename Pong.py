from tkinter import *
from tkinter import messagebox
import random, time

class Ball:
    def __init__(self, canvas, paddle01, paddle02, score01, score02, color):
        self.canvas = canvas
        self.id = canvas.create_oval(450, 450, 460, 460, fill=color)

        self.paddle01 = paddle01
        self.paddle02 = paddle02

        self.score01 = score01
        self.score02 = score02

        starts = [-3, -2, -1, 1, 2, 3]
        self.score = 0
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_A(self, pos):
        if pos[0] <= 0:
            return True
        return False

    def hit_B(self, pos):
        if pos[2] >= self.canvas_width:
            return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        if pos[1] <= 0:
            self.y = 3

        if self.hit_A(pos) == True:
            self.score01.hit()

        if self.hit_B(pos) == True:
            self.score02.hit()
            
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            if self.hit_bottom == True:
                self.y = -3
                
        if pos[0] <= 0:
            self.x = 3

        if self.hit_paddleA(pos) == True:
            self.x = 3

        if self.hit_paddleB(pos) == True:
            self.x = -3
            
        if pos[2] >= self.canvas_width:
            self.x = -3

    def hit_paddleA(self, pos):
        paddle_pos = self.canvas.coords(self.paddle01.id)

        if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
            if pos[0] <= paddle_pos[2] and pos[0] >= paddle_pos[0]:
                return True
        return False

    def hit_paddleB(self, pos):
        paddle_pos = self.canvas.coords(self.paddle02.id)

        if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
            if pos[2] >= paddle_pos[0] and pos[2] <= paddle_pos[2]:
                return True
        return False

def halt():
    Exit = messagebox.askokcancel(title="Exit Confirmation", message="Are you sure you would like to quit?")
    if Exit > 0:
        tk.destroy()
    else:
        time.sleep(1)

def timeout():
    messagebox.showinfo(title="Game Paused", message="Press ok to continue playing")
    time.sleep(1)


class Paddle:
    def __init__(self, canvas, color, x0, y0, y1, y2, control):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x0, y0, y1, y2, fill = color)
        self.y = 0

        self.up = 'enabled'
        self.down = 'enabled'

        if control == 'a':
            self.canvas.bind_all('<KeyPress-Up>', self.move_up)
            self.canvas.bind_all('<KeyPress-Down>', self.move_down)
        else:
            self.canvas.bind_all('<KeyPress-Right>', self.move_up)
            self.canvas.bind_all('<KeyPress-Left>', self.move_down)
            
        self.canvas_height = self.canvas.winfo_height()
        self.hit_bottom = False

    def draw(self):
        self.canvas.move(self.id, 0, self.y)
        pos = self.canvas.coords(self.id)
        
        if pos[1] <= 0:
            self.y = 0
            self.up = 'disabled'
        else:
            self.up = 'enabled'
            
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            if self.hit_bottom == True:
                self.y = 0
                self.down = 'disabled'
        else:
            self.down = 'enabled'

    def move_up(self, evt):
        if self.up == 'enabled':
            self.y = -5
        else:
            self.y = 0

    def move_down(self, evt):
        if self.down == 'enabled':
            self.y = +5
        else:
            self.y = 0
            
class Score:
    def __init__(self, canvas, x):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(x, 10, font='25', text=self.score, fill='black')

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)
        
tk = Tk()
w=900
h=500
tk.title("Pong")
tk.resizable(0, 0)
canvas = Canvas(tk, width=w, height=h)
canvas.pack()
tk.update()

colors = ['green', 'red', 'yellow', 'purple', 'blue']
random.shuffle(colors)

score_paddleB = Score(canvas, 225)
score_paddleA = Score(canvas, 675)

canvas.create_line(450, 0, 450, 500)

paddleA = Paddle(canvas, colors[0], 10, 175, 20, 130, 'a') 
paddleB = Paddle(canvas, colors[0], (w-10), (h-175), (w-20), (h-130), 'b') 
ball = Ball(canvas, paddleA, paddleB, score_paddleA, score_paddleB, colors[1])

destroy = Button(canvas, text="Exit", command=halt).place(x=(w-30), y=(h-30))
stop4moment = Button(canvas, text="Pause", command=timeout).place(x=5, y=(h-30))

while 1:
    ball.draw()
    paddleA.draw()
    paddleB.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
