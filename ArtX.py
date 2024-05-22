from tkinter import *
from tkinter import ALL, EventType, colorchooser, filedialog, PhotoImage
from PIL import *
from PIL import Image, ImageDraw, ImageColor, ImageTk
import os
import random

width, height = 1540, 720

WIN = Tk()
WIN.title("ArtX")
WIN.geometry(f"{width}x{height}")
WIN.resizable(False, False)
WIN.config(bg="white")

x1, y1, x2, y2 = None, None, None, None

d1 = ["blue", "red", "yellow", "green", "big", "small", "little", "long", "white", "black", "sad", "happy", "sleepy", "motorized", "tall", "smart"]
d2 = ["cat", "dog", "plane", "iguana", "fish", "bird", "car", "planet", "book", "elephant", "star", "computer", "building", "bee", "ant", "hat"]
d3 = ["assembling", "eating", "building", "demolishing", "using", "selling", "placing", "gathering", "smelling", "tasting", "atacking", "planting", "seeing", "hiding"]
d4 = ["a building", "a phone", "a home", "a guitar", "a piano", "a pizza", "a flower", "a tresure", "a letter", "an essay", "a laptop", "a tractor", "a fork", "a hat", "an entity(?)", "a fish", "a bat", "a poster"]

Colour = "#000000"
Colour2 = ImageColor.getrgb("black")

canvas_name = "canvas"

bkgr_clr = "#ffffff"
image = Image.new("RGB", (1000, 720), "#ffffff")
draw = ImageDraw.Draw(image)

#Creeaza canvasul si il face alb
CVS = Canvas(WIN, width = 1000, height = 720) 
CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")
CVS.config(cursor="pencil") 

CLR = Canvas(WIN, width = 250, height = 310) 
CLR.place(x=1280, y=400)

menu = Menu(WIN)
WIN.config(menu=menu)
bs_sub_menu = Menu(menu, tearoff=0)

path = os.path.join('Img')

brush_size = 5
brush_shape = "ellipse"
brush_type = "brush"
entry_suggestion = Entry(WIN, width=40)
entry_suggestion.place(x=10, y=350)

def paint( event ):
    global x1, y1, x2, y2
    if brush_type == "brush":
        x1, y1, x2, y2 = ( event.x - brush_size/2 ),( event.y- brush_size/2), ( event.x + brush_size/2 ),( event.y + brush_size/2 )
        if brush_shape == "ellipse":
            CVS.create_oval( x1, y1, x2, y2, fill = Colour, outline= Colour )
            draw.ellipse([x1, y1, x2, y2], fill=Colour2, outline=Colour2)
            x1, y1, x2, y2 = None, None, None, None
        elif brush_shape == "rectangle":
            CVS.create_rectangle( x1, y1, x2, y2, fill = Colour, outline= Colour )
            draw.rectangle([x1, y1, x2, y2], fill=Colour2, outline=Colour2)
            x1, y1, x2, y2 = None, None, None, None
        elif brush_shape == "pen":
            x1, y1, x2, y2 = ( event.x ),( event.y), ( event.x + brush_size ),( event.y + brush_size )
            CVS.create_line( x1, y1, x2, y2, fill = Colour )
            draw.rectangle([x1, y1, x2, y2], fill=Colour2, outline=Colour2)
            x1, y1, x2, y2 = None, None, None, None
    elif brush_type == "rectangle":
        if x1 == None and y1 == None:
            x1, y1 = event.x, event.y
        elif x2 == None and y2 == None:
            x2, y2 = event.x, event.y
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1
            CVS.create_rectangle( x1, y1, x2, y2, fill = Colour, outline= Colour )
            draw.rectangle([x1, y1, x2, y2], fill=Colour2, outline=Colour2)
            x1, y1, x2, y2 = None, None, None, None

    
def clr_test( event ):
    x1, y1, x2, y2 = ( event.x - 20 ),( event.y - 20), ( event.x + 20 ), ( event.y + 20 )
    CLR.create_oval( x1, y1, x2, y2, fill = Colour, outline= Colour )
    
def pick_color():
    global Colour, Colour2
    clr = colorchooser.askcolor()[1]  #Deschide interfata de selectare a culorii
    if clr:
        Colour = clr
        Colour2 = ImageColor.getrgb(clr)

def set_type(shape_type):
    global brush_type
    brush_type = shape_type
    
def paint_background():
    global bkgr_clr
    CVS.create_rectangle(2, 2, 1001, 717, fill = Colour, outline="black")
    draw.rectangle([0, 0, 1001, 720], fill=Colour2, outline=Colour2)
    bkgr_clr = Colour

def new_file():
    global image, draw
    CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")
    image = Image.new("RGB", (1000, 720), "#ffffff")
    draw = ImageDraw.Draw(image)

def get_idea():
    w = d1[random.randint(0, len(d1) - 1)]
    x = d2[random.randint(0, len(d2) - 1)]
    y = d3[random.randint(0, len(d3) - 1)]
    z = d4[random.randint(0, len(d4) - 1)]
    entry_suggestion.delete(0, END)
    idea = f"a {w} {x} {y} {z}."
    entry_suggestion.insert(0, idea)
    return

def assign_colour(x):
    global Colour, Colour2
    Colour = x
    try:
        Colour2 = ImageColor.getrgb(x)
    except ValueError:
        Colour2 = ImageColor.getrgb("black")
        Colour =  "#000000000"

def save_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = f"{script_dir}/Img"  
    save_path = os.path.join(script_dir, f'{canvas_name}.png')
    image.save(save_path)

def save_image_as():
    file_path = filedialog.asksaveasfilename(
        title="Save Image File",
        defaultextension=".png",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
    )
    if file_path:
        image.save(file_path)

def open_image():
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if file_path:
        display_image(file_path)

def on_key_press(event):
    if event.state == 4 and event.keysym == 's':  # 4 -> Ctrl
        save_image()
    elif event.state == 4 and event.keysym == 'n':
        new_file()
    elif event.state == 4 and event.keysym == 'o':
        open_image()
    elif event.state == 4 and event.keysym == 'p':
        pick_color()
    elif (event.state & 0x4) and (event.state & 0x1) and event.keysym == 'S': #1 -> shift
        save_image_as()

def display_image(file_path):
    pass

def pick_size(x):
    global brush_size
    brush_size = int(x)

def pick_shape(x):
    global brush_shape, brush_type
    if x == "ellipse":
        brush_shape = "ellipse"
        brush_type = "brush"
    elif x == "rectangle":
        brush_shape = "rectangle"
        brush_type = "brush"
    elif x == "pen":
        brush_shape = "pen"
        brush_type = "brush"

def eraser():
    global bkgr_clr, Colour, Colour2
    Colour = bkgr_clr
    Colour2 = ImageColor.getrgb(Colour)

#Functia care creeaza butoanele
def draw_buttons():
    global spinbox_brush_size
    #butoane stanga
    spinbox_brush_size = Spinbox(WIN, from_= 1, to=2000, width=5)
    spinbox_brush_size.place(x=2, y = 5)
    button_pick = Button(WIN, text="Ok")
    button_pick.place(x=50, y=5)
    button_pick.config(width=5, height=1, cursor="hand2", command = lambda: pick_size(spinbox_brush_size.get()))
    button_pick = Button(WIN, text="Eraser")
    button_pick.place(x=100, y=5)
    button_pick.config(width=5, height=1, cursor="hand2", command = eraser)
    button_suggestion = Button(WIN, text="Draw:")
    button_suggestion.place(x=10, y=300)
    button_suggestion.config(width=10, height=2, cursor="hand2", command = get_idea)
    button_rectangle = Button(WIN, text="Rectangle")
    button_rectangle.place(x=5, y=35)
    button_rectangle.config(width=10, height=2, cursor="hand2", command = lambda: set_type("rectangle"))
    button_ellipse = Button(WIN, text="Rectangle")
    button_ellipse.place(x=5, y=35)
    button_ellipse.config(width=10, height=2, cursor="hand2", command = lambda: set_type("rectangle"))
    #butoane dreapta

    #clr/bgr
    button_pick = Button(WIN, text="Pick a colour")
    button_pick.place(x=1283, y=185)
    button_pick.config(width=15, height=2, cursor="hand2", command = pick_color)
    color_button = Button(WIN, text="Fill Background")
    color_button.place(x=1412, y=185)
    color_button.config(width=15, height=2, cursor="hand2", command = paint_background)
    #rgb
    button_r = Button(WIN,bg="#ff0000")
    button_r.place(x=1283, y=5)
    button_r.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#ff0000"))
    button_g = Button(WIN, bg="#228b22")
    button_g.place(x=1365, y=5)
    button_g.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#228b22"))
    button_b = Button(WIN, bg="#00008b")
    button_b.place(x=1447, y=5)
    button_b.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#00008b"))
    #yop
    button_y = Button(WIN, bg="#e6cc00")
    button_y.place(x=1283, y=50)
    button_y.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#e6cc00"))
    button_o = Button(WIN, bg="#fca510")
    button_o.place(x=1365, y=50)
    button_o.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#fca510"))
    button_p = Button(WIN, bg="#8a00c2")
    button_p.place(x=1447, y=50)
    button_p.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#8a00c2"))
    #bpb
    button_y = Button(WIN, bg="#724a24")
    button_y.place(x=1283, y=95)
    button_y.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#724a24"))
    button_o = Button(WIN, bg="#f98cb9")
    button_o.place(x=1365, y=95)
    button_o.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#f98cb9"))
    button_p = Button(WIN, bg="#d2b48c")
    button_p.place(x=1447, y=95)
    button_p.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#d2b48c"))
    #wbg
    button_w = Button(WIN, bg="#ffffff")
    button_w.place(x=1283, y=140)
    button_w.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#ffffff"))
    button_blk = Button(WIN, bg="#000000000")
    button_blk.place(x=1365, y=140)
    button_blk.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#000000000"))
    button_gry = Button(WIN, bg="#808080")
    button_gry.place(x=1447, y=140)
    button_gry.config(width=10, height=2, cursor="hand2", command = lambda: assign_colour("#808080"))

def draw_menu():
    filemenu = Menu(menu)
    toolmenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New          Ctrl+N', command=new_file)
    filemenu.add_command(label='Open...      Ctrl+O', command=open_image)
    filemenu.add_command(label='Save         Ctrl+S', command = save_image)
    filemenu.add_command(label='Save As...   Ctrl+Shift+S', command = save_image_as)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=WIN.quit)

    menu.add_cascade(label='Tools', menu=toolmenu)
    toolmenu.add_cascade(label='Brush Shape', menu=bs_sub_menu)
    bs_sub_menu.add_command(label='Ellipse', command= lambda: pick_shape("ellipse"))
    bs_sub_menu.add_command(label='Rectangle', command= lambda: pick_shape("rectangle"))
    bs_sub_menu.add_command(label='Pen', command= lambda: pick_shape("pen"))

def draw_label():
    label_test_clr = Label(WIN, text="Compare Colours", font=("Arial", 16, "bold"), fg="black", bg="white")
    label_test_clr.place(x=1310, y=370)
    label_notes = Label(WIN, text="Notes", font=("Arial", 16, "bold"), fg="black", bg="white")
    label_notes.place(x=95, y=370)
    notes = Text(WIN, width=30, height=19, bg="grey94")
    notes.place(x=10, y=400)

CVS.bind( "<B1-Motion>", paint )
CVS.bind( "<Button-1>", paint )
CVS.pack()

CLR.bind( "<Button-1>", clr_test )
WIN.bind('<KeyPress>', on_key_press)

draw_label()
draw_menu()
draw_buttons()
mainloop()