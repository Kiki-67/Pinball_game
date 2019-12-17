from tkinter import *
import tkinter
import time

# create the interface
tk = tkinter.Tk()
tk.title("Pinball Game") # game title
tk.resizable(0,0) # make the interface unadjustable in both horizontal and vertical
tk.wm_attributes("-topmost",1) # place the interface in fromt of all other windows
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0) # create canvas
canvas.pack()
tk.update()

# show some instructions
game_start_guide = canvas.create_text(430,10,text="Press Down: Start", font = ('Arial',10), state = 'hidden')
game_end_guide = canvas.create_text(430,30,text="Press Up: End", font = ('Arial',10), state = 'hidden')
game_left = canvas.create_text(430,50,text="Press Left: Paddle move left", font = ('Arial',8), state = 'hidden')
game_right = canvas.create_text(430,70,text="Press Right: Paddle move right", font = ('Arial',8), state = 'hidden')

game_score = canvas.create_text(430,90, text = "Your Score: ", font = ('Arial',10),state = 'hidden')
game_start_text = canvas.create_text(430,110, text = "Game Start", font = ('Arial',10),state = 'hidden')
game_over_text = canvas.create_text(250,200, text = "Game over", font = ('Arial',30),state = 'hidden')



#create class ball
class Ball:
    def __init__(self,canvas,paddle,ball_speed,ball_color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10,10,25,25,fill = ball_color) # create a round ball
        self.canvas.move(self.id,250,120) # move the ball to middle of the canvas
        self.x = ball_speed # set up the horizontal speed of the ball
        self.y = -ball_speed # set up vertical speed of the ball
        # set up the height and width of the canvas, ensure the ball will not go out of the canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom =False

    def hit_paddle(self,pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
                # if paddle catch the ball
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                    return True
        return False

    def draw(self,ball_speed):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id) # get the position of the ball
        if pos[1] <=0: # determine if the ball hit the top
                self.y= ball_speed # the ball will change to positive vertical direction
        if pos[3] >=self.canvas_height:
                self.hit_bottom = True # if the ball hit the bottom, game over
        if self.hit_paddle(pos) == True:
                self.y = -ball_speed # if the ball hit the paddle, the ball will change the direction
                score.addscore() # and score will add 1
        if pos[0] <=0: # determine if the ball hit the left-most or right-most, then move the opposite direction
                self.x = ball_speed
        if pos[2] >= self.canvas_width:
                self.x = -ball_speed


# create paddle calss
class Paddle:
    def __init__(self, canvas, paddle_color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10, fill = paddle_color) # create a rectangle paddle
        self.canvas.move(self.id,200,300) # move the paddle to nearly bottom of the canvas
        self.started=False
        self.x = 0
        self.speed = value
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left) # enable user to control the paddle with the left-arrow key
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right) # enable user to control the paddle with the right-arrow key
        self.canvas.bind_all('<KeyPress-Down>',self.game_start) # enable user to start the game with down-arrow key
        self.canvas.bind_all('<KeyPress-Up>',self.game_end) # # enable user to pause the game with up-arrow key

    def draw(self):
        self.canvas.move(self.id,self.x,0)
        pos =self.canvas.coords(self.id)
        # if paddle moves to right-most or left-most, stop moving
        if pos[0] <=0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x =0

# set the speed of the paddle
    def turn_left(self,evt):
        self.x = -self.speed

    def turn_right(self,evt):
        self.x = self.speed

    def set_speed(self,value): # enable different speed of paddle
        self.speed = value

    def game_start(self,evt):
        self.started = True

    def game_end(self,evt):
        self.started = False


# calculate the user score
class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        canvas.itemconfig(game_score, state = 'normal')
        self.id = canvas.create_text(470,90,text=self.score, fill = color)

        canvas.itemconfig(game_start_guide, state = 'normal')
        canvas.itemconfig(game_end_guide, state = 'normal')
        canvas.itemconfig(game_left, state = 'normal')
        canvas.itemconfig(game_right, state = 'normal')

    def addscore(self):
        self.score += 1 # every time when the ball hit the paddle, the score will add 1
        self.canvas.itemconfig(self.id,text = self.score)


def getBallcolor(): # function that enables user to input ball's color
    ball_color = str(input("Enter ball color: "))
    return ball_color

def getPaddlecolor(): # function that enables user to input paddle's color
    paddle_color = str(input("Enter paddle color: "))
    return paddle_color

# enable user to change the difficulty
def getBallSpeed(): # function that enables user to input the speed of ball
    ball_speed = float(input("Enter ball speed: "))
    return ball_speed

def getPaddleSpeed(): # function that enables user to input the speed of paddle
    value = float(input("Enter paddle speed: "))
    return value

# get user input
ball_speed = getBallSpeed()
value = getPaddleSpeed()
ball_color = getBallcolor()
paddle_color = getPaddlecolor()

# call the class
paddle = Paddle(canvas, paddle_color)
ball = Ball(canvas,paddle, ball_speed, ball_color)
score = Score(canvas, 'black')




def main():
    while 1: # use while loop to prevent a dead loop
        if ball.hit_bottom == False and paddle.started  == True: # if the ball hit the paddle
            ball.draw(ball_speed) # call function draw() in class ball
            paddle.draw() # call function draw() in class paddle
            canvas.itemconfig(game_start_guide, state = 'normal')

        if ball.hit_bottom == True: # if the ball hit the bottom
            canvas.itemconfig(game_score, font = ('Arial',10), fill = 'red',state = 'normal') # show the final score
            canvas.itemconfig(game_over_text, state = 'normal') # show the text: game over
            canvas.itemconfig(game_start_text, state = 'hidden') # the game start text will vanish
            break
        tk.update_idletasks()
        tk.update() # update the canvas
        time.sleep(0.01)


main()
tk.mainloop()

