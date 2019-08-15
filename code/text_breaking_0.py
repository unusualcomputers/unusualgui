import pygame
import pdb
pygame.init()
width=100

font_name="comicsansms"
font_size=20
font=pygame.font.SysFont(font_name,font_size,False,False)

text='long, longer, verylongword,in an increasingly longer string.'

lines=[]

sz=len(text)

last_end=0
last_white=-1
last_delim=-1

def tail(l):
    if len(l): return l[-1]
    else: return ''
#pdb.set_trace()
dash_w=font.size('-')[0]
for i in range(sz):
    w=font.size(text[last_end:i])[0]
    if w > width:
        if last_white!=-1:
            if last_white+1<i:
                new_end=last_white+1
            else:
                new_end=last_white
            lines.append(text[last_end:new_end].lstrip())
        elif last_delim!=-1:
            if last_delim+1<i:
                new_end=last_delim+1
            else:
                new_end=last_delim
            lines.append(text[last_end:new_end].lstrip())
        elif i<3: 
            raise "Can't fold this"
        else:
            new_end=i-2
            if font.size(text[last_end:new_end])[0]+dash_w > width:
                new_end=i-3
            lines.append((text[last_end:new_end]+'-').lstrip())

             
        last_end=new_end
        i=last_end
        
        last_white=-1
        last_delim=-1   
    else: 
        c=text[i]
        if c.isspace(): 
            last_white=i
        elif not c.isalnum(): 
            last_delim=i

if last_end<sz:
    lines.append(text[last_end:sz])


print lines
print reduce(lambda a,b: a+b,lines)
print text
for w in lines:
    print w,font.size(w)
