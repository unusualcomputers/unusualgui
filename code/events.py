from enum import Enum

# quit showing up in the event queue stops the application
# more general than pygame quit, can be put there by buttons for example
class Quit:
    def __init__(self):
        self.sender=None
        pass

# message is an event broadcast to all listeners 
# (all active windows or listener functions)
class Message:
    def __init__(self, sender, message, params=None, receivers=[]):
        self.sender=sender
        self.message=message
        self.params=params
        self.receivers=receivers

# ... all other messages are sent to widgets with focus only

class MouseDown:
    def __init__(self,pos):
        self.pos=pos

class MouseUp:
    def __init__(self,pos,mouse_down_pos,elapsed):
        self.pos=pos
        self.mouse_down_pos=mouse_down_pos
        self.elapsed=elapsed # milis since MouseDown

# config.mouse_long_time=1000
# MouseDown with no MouseUp within this time is MouseLong
class MouseLong:
    def __init__(self,mouse_down_pos):
        self.pos=mouse_down_pos

# config.drag_min_distance
# MouseMotion with one of the buttons pressed is Dragging  and 
#   distance covered is less than drag_min_distance
#   NOTE: once we move more than drag_min_distance subsequent moves can be 
#   smaller
class Dragging:
    def __init__(self,mouse_down_pos,pos):
        self.start_event=mouse_down_pos
        self.pos=pos

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

# config.key_repeat_start=1000
# config.key_repeat=500
# Keyboard event use pygame keys names
# https://www.pygame.org/docs/ref/key.html
# If a key is down for longer then key_repeat_start, start sending KeyUp every
# key_repeat milliseconds
# NOTE: this means that not every KeyUp is preceded by KeyDown
class KeyDown:
    def __init__(self,key,uni_code,mod):
        self.key=key
        self.unicode=uni_code
        self.mod=mod

class KeyUp:
    def __init__(self,key,uni_code,mod):
        self.key=key
        self.unicode=uni_code
        self.mod=mod

