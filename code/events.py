from enum import Enum

# message is an event broadcast to all listeners 
# (all active windows or listener fnctions)
class Message:
    def __init__(self, sender, message, params=None):
        self.sender=sender
        self.message=message
        self.params=params

# ... all other messages are sent to widgets with focus only

class MouseDown:
    def __init__(self,x,y):
        self.x=x
        self.y=y

click_time=100
# MouseDown followed by MouseUp within click_time ms is MouseClick
# Either MouseUp or MouseClick are generated, not both 
# x,y are coordinates of original MouseDown event
class MouseClick:
    def __init__(self,x,y):
        self.x=x
        self.y=y

mouse_long_time=1000
mouse_long_distance=10
drag_tick=50

# MouseDown with no MouseUp and when motion is less then mouse_long_distance
# is MouseLong
# If mouse is moved more than mouse_long_distance before MouseUp,Dragging starts
# Then Dragging event is generated every drag_tick seconds unless that is 0
# Once mouse is up, MouseLongEnd is generated 
class MouseLong:
    def __init__(self,x,y,mouse_down_event):
        self.x=x
        self.y=y
        self.mouse_down_event=mouse_down_event

class MouseLongEnd:
    def __init__(self,x,y,mouse_down_event):
        self.x=x
        self.y=y
        self.mouse_down_event=mouse_down_event

class Dragging:
    def __init__(self,mouse_down_event,x,y):
        self.start_event=mouse_down_event
        self.x=x
        self.y=y

slide_speed=500
# MouseLong followed by MouseLongEnd such that distance divided by time 
# is > slide_speed generates slide event
class Slide:
    def __init__(self,drag_start,drag_end,direction):
        self.start=drag_start
        self.end=drag_end
        self.direction=direction


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

# Keyboard event use pygame keys names
# https://www.pygame.org/docs/ref/key.html

class KeyDown:
    def __init__(self,key,uni_code):
        self.key=key
        self.unicode=uni_code


class KeyUp:
    def __init__(self,key,uni_code):
        self.key=key
        self.unicode=uni_code

