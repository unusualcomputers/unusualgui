from widget import Widget

class Widgets:
    def __init__(self):
        self.widgets={}
        self.active=None
        self.focus=None

    def add_widgets(self, name, widgets):
        if len(widgets)==0:
            raise Exception(u'Cannot add empty widget list')
        self.active=self.get_widgets(name)
        self.active+=widgets
        self.focus=widgets[0]

    def get_widgets(self,name):
        if name not in self.widgets: 
            self.widgets[name]=[]
        return self.widgets[name]
            
    def activate(self,surface,name):
        active=self.get_widgets(name)
        if self.active == active: return
        for w in self.active:
            w,unfocus()
            w.undraw(surface)
        
        self.active=active
        active[0].focus()
        for w in self.active:
            w.draw(surface)
     
    def handle(self,event):
        return self.get_focus().handle(event)
 
    def broadcast(self,message):
        for w in self.active:
            if w != message.sender: m.handle(message)

    def get_focus(self):
        return self.focus
 
    def find_focus(self,x,y):
        if len(self.widgets)==0: return None
        if self.focus.contains(x,y): return self.focus
        
        for w in self.active:
            if w.contains(x,y) and w.accepts_focus(): 
                self.focus.unfocus()
                self.focus=w
                w.focus()
                return w

    def set_focus(self,widget):
        if widget==self.focus: return
        for w in self.active:
            if w==widget:
                self.focus.unfocus()
                w.focus()
                self.focus=w
                return
        raise Exception('Widget not found')
