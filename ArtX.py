from tkinter import *
from tkinter import colorchooser
from PIL import *
from PIL import Image, ImageDraw, ImageColor

WIN = Tk()
WIN.title("ArtX")
WIN.geometry("1560x720")
WIN.resizable(False, False)

global Colour
Colour = "#000000"
Colour2 = ImageColor.getrgb("black")

image = Image.new("RGB", (1000, 720), "#ffffff")
draw = ImageDraw.Draw(image)

#Creeaza canvasul si il face alb
CVS = Canvas(WIN, width = 1000, height = 720) 
CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")

def paint( event ):
    global Colour, Colour2
    x1, y1, x2, y2 = ( event.x ),( event.y), ( event.x + 5 ),( event.y + 5 ) 
    CVS.create_rectangle( x1, y1, x2, y2, fill = Colour, outline= Colour )
    draw.rectangle([x1, y1, x2, y2], fill=Colour2, outline=Colour2)

def pick_color():
    global Colour, Colour2
    clr = colorchooser.askcolor()[1]  #Deschide interfata de selectare a culorii
    if clr:
        Colour = clr
        Colour2 = ImageColor.getrgb(clr)

def paint_background():
    CVS.create_rectangle(2, 2, 1001, 717, fill = Colour, outline=Colour)
    draw.rectangle([0, 0, 1001, 720], fill=Colour2, outline=Colour2)

def assign_colour(x):
    global Colour, Colour2
    Colour = x
    if x == '#000000000':
        Colour2 = ImageColor.getrgb("black")
    else:
        Colour2 = ImageColor.getrgb(x)

def save_image():
    # Save the Pillow image
    image.save("canvas.png")
    print("Canvas saved as canvas.png")

#Functia care creeaza butoanele
def draw_buttons():
    #butoane stanga
    button_pick = Button(WIN, text="Save Image")
    button_pick.place(x=100, y=185)
    button_pick.config(width=15, height=2, cursor="hand2", command = save_image)

    #butoane dreapta

    #clr/bgr
    button_pick = Button(WIN, text="Pick a Color")
    button_pick.place(x=1283, y=185)
    button_pick.config(width=15, height=2, cursor="hand2", command = pick_color)
    color_button = Button(WIN, text="Fill Background")
    color_button.place(x=1412, y=185)
    color_button.config(width=15, height=2, cursor="hand2", command = paint_background)
    #rgb
    button_r = Button(WIN, text="Red")
    button_r.place(x=1283, y=5)
    button_r.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#ff0000"))
    button_g = Button(WIN, text="Green")
    button_g.place(x=1365, y=5)
    button_g.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#228b22"))
    button_b = Button(WIN, text="Blue")
    button_b.place(x=1447, y=5)
    button_b.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#00008b"))
    #yop
    button_y = Button(WIN, text="Yellow")
    button_y.place(x=1283, y=50)
    button_y.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#e6cc00"))
    button_o = Button(WIN, text="Orange")
    button_o.place(x=1365, y=50)
    button_o.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#fca510"))
    button_p = Button(WIN, text="Purple")
    button_p.place(x=1447, y=50)
    button_p.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#8a00c2"))
    #bpb
    button_y = Button(WIN, text="Brown")
    button_y.place(x=1283, y=95)
    button_y.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#724a24"))
    button_o = Button(WIN, text="Pink")
    button_o.place(x=1365, y=95)
    button_o.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#f98cb9"))
    button_p = Button(WIN, text="Beige")
    button_p.place(x=1447, y=95)
    button_p.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#d2b48c"))
    #wbg
    button_w = Button(WIN, text="White")
    button_w.place(x=1283, y=140)
    button_w.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#ffffff"))
    button_blk = Button(WIN, text="Black")
    button_blk.place(x=1365, y=140)
    button_blk.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#000000000"))
    button_gry = Button(WIN, text="Gray")
    button_gry.place(x=1447, y=140)
    button_gry.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#808080"))

CVS.bind( "<B1-Motion>", paint )
CVS.pack()

draw_buttons()
mainloop()