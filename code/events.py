# mouse buttons are numbered n=0 is left, n=1 is right, the rest we'll see

class MouseDown:
    def __init__(self,n,x,y):
        self.n=n
        self.x=x
        self.y=y

class MouseUp:
    def __init__(self,n,x,y,down_event):
        self.n=n
        self.x=x
        self.y=y
        self.down_event=down_event   

click_time=100

# MouseDown followed by MouseUp within click_time ms is MouseClick
# Either MouseUp or MouseClick are generated, not both 
# x,y are coordinates of original MouseDown event
class MouseClick:
    def __init__(self,n,x,y):
        self.n=n
        self.x=x
        self.y=y

dbl_click_time=100

# Two MouseClick event within dbl_click_time are a DoubleClick
# If DoubleClick event is generated, the second MouseClick is not
class DoubleClick:
    def __init__(self,n,x,y):
        self.n=n
        self.x=x
        self.y=y

class Direction(Enum):
    up=0
    down=1
    left=2
    right=3

# For scrollwheels
class Scroll:
    def __init__(self,x,y,direction):
        self.x=x
        self.y=y
        self.direction=direction

drag_time=500
drag_tick=50

# MouseDown with no MouseUp after drag_time is DragStart
# Then Dragging event is generated every drag_tick seconds unless that is 0
# until MouseUp when DragEnd is generated
class DragStart:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Dragging:
    def __init__(self,start_event,x,y):
        self.start_event=start_event
        self.x=x
        self.y=y

class DragEnd:
    def __init__(self,start_event,x,y):
        self.start_event=start_event
        self.x=x
        self.y=y

slide_speed=500
# DragStart followed by DragEnd such that distance divided by time 
# is > slide_speed generates slide event

class Slide:
    def __init__(self,drag_start,drag_end,direction):
        self.start=drag_start
        self.end=drag_end
        self.direction=direction


# Keyboard event use pygame keys names
# https://www.pygame.org/docs/ref/key.html

class KeyDown:
    def __init__(self,key):
        self.key=key


class KeyUp:
    def __init__(self,key):
        self.key=key

