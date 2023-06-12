import turtle
t = turtle.Turtle()
def turtleGraphics(nameF, value):
        if nameF == "OPEN":
            pass
        elif nameF == "END":
            turtle.done()
        elif nameF == "PENUP":
            t.penup()
        elif nameF == "PENDOWN":
            t.pendown()
        elif nameF == "FORWARD":
            t.forward(value)
        elif nameF == "BACKWARD":
            t.backward(value)
        elif nameF == "LEFT":
            t.left(value)
        elif nameF == "RIGHT":
            t.right(value)
        elif nameF == "SPEED":
            t.speed(value)
        elif nameF == "PENSIZE":
            t.pensize(value)
        elif nameF == "CIRCLE":
            t.circle(value)

turtleGraphics("OPEN", None)
turtleGraphics("FORWARD", 50)
turtleGraphics("LEFT", 90)
turtleGraphics("FORWARD", 50)
turtleGraphics("LEFT", 90)
turtleGraphics("FORWARD", 50)
turtleGraphics("LEFT", 90)
turtleGraphics("FORWARD", 50)
turtleGraphics("LEFT", 90)

print("hola")