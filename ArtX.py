from tkinter import *
from tkinter import ALL, colorchooser, filedialog, PhotoImage
from PIL import *
from PIL import Image, ImageDraw, ImageColor, ImageTk, ImageEnhance
import os
import random

width, height = 1540, 720

WIN = Tk()
WIN.title("ArtX")
WIN.geometry(f"{width}x{height}")
WIN.resizable(False, False)
WIN.config(bg="white")

directories = ['ArtX', 'Assets']
filename = 'rectangle.png'
current_directory = os.getcwd()

x0, y0, x1, y1 = None, None, None, None

#liste de cuvinte pt generator
d1 = ["blue", "red", "yellow", "green", "big", "small", "little", "long", "white", "black", "sad", "happy", "sleepy", "motorized", "tall", "smart", "huge", "clean", "dirty", "bright", "dark", "ornate", "festive", "glowing"]
d2 = ["cat", "dog", "plane", "iguana", "fish", "bird", "car", "planet", "book", "elephant", "star", "computer", "building", "bee", "ant", "hat", "object", "lion", "shark", "ball", "tank", "ship", "trumpet", "tree"]
d3 = ["assembling", "eating", "building", "demolishing", "using", "selling", "placing", "gathering", "smelling", "tasting", "atacking", "planting", "seeing", "hiding", "burying", "decorating", "drawing"]
d4 = ["a building", "a phone", "a home", "a guitar", "a piano", "a pizza", "a flower", "a tresure", "a letter", "an essay", "a laptop", "a tractor", "a fork", "a hat", "an entity(?)", "a fish", "a bat", "a poster", "a toy"]

Colour : str = "#000000"
Colour2 = ImageColor.getrgb("black")

canvas_name = "canvas"

bkgr_clr : str = "#ffffff"
image = Image.new("RGB", (1000, 720), "#ffffff")
draw = ImageDraw.Draw(image)

#Creeaza canvasul si il face alb
CVS_width, CVS_height = 1000, 720
CVS = Canvas(WIN, width = 1000, height = 720) 
CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")
CVS.config(cursor="pencil") 

CLR = Canvas(WIN, width = 250, height = 310) 
CLR.place(x=1280, y=400)

menu = Menu(WIN)
WIN.config(menu=menu)
bs_sub_menu = Menu(menu, tearoff=0)
sp_sub_menu = Menu(menu, tearoff=0)

brush_size : int = 10
brush_shape : str = "ellipse"
brush_type : str = "brush"
entry_suggestion = Entry(WIN, width=40)
entry_suggestion.place(x=10, y=350)

filter_type : None
brightness_factor : float = 1.0

def find_artx_directory(directory): #gasete locatia folderuli ArtX
    for dirpath, dirnames, filenames in os.walk(directory):
        if 'ArtX' in dirnames:
            return os.path.join(dirpath)

artx_directory = find_artx_directory(current_directory)

if artx_directory:
    path = os.path.join(artx_directory, *directories, filename)
    print(path)

#Importeaza imaginile pentru butoane
photo_rectangle = PhotoImage(file = path) 
path = path.replace('rectangle.png', 'ellipse.png')
photo_ellipse = PhotoImage(file = path) 
path = path.replace('ellipse.png', 'line.png')
photo_line = PhotoImage(file = path) 
path = path.replace('line.png', 'pick_clr.png')
photo_pick_clr = PhotoImage(file = path) 
path = path.replace('pick_clr.png', 'check.png')
photo_check = PhotoImage(file = path) 
path=path.replace('check.png', 'eraser.png')
photo_eraser = PhotoImage(file = path) 
path = path.replace('eraser.png', 'brush.png')
photo_brush = PhotoImage(file = path) 
path = path.replace('brush.png', 'bucket.png')
photo_bucket = PhotoImage(file = path) 
path = path.replace('bucket.png', 'lighten.png')
photo_lighten = PhotoImage(file = path) 
path = path.replace('lighten.png', 'darken.png')
photo_darken = PhotoImage(file = path) 

class App:

    def paint(self, event ): #Functia care se activeaza cand dai click/drag ca sa pictezi
        global x0, y0, x1, y1
        if brush_type == "brush":   #pentru pensula
            x0, y0, x1, y1 = ( event.x - brush_size/2 ),( event.y- brush_size/2), ( event.x + brush_size/2 ),( event.y + brush_size/2 )
            if brush_shape == "ellipse":
                CVS.create_oval( x0, y0, x1, y1, fill = Colour, outline= Colour )
                draw.ellipse([x0, y0, x1, y1], fill=Colour2, outline=Colour2)
                x0, y0, x1, y1 = None, None, None, None
            elif brush_shape == "rectangle":
                CVS.create_rectangle( x0, y0, x1, y1, fill = Colour, outline= Colour )
                draw.rectangle([x0, y0, x1, y1], fill=Colour2, outline=Colour2)
                x0, y0, x1, y1 = None, None, None, None
            elif brush_shape == "pen":
                x0, y0, x1, y1 = ( event.x ),( event.y), ( event.x + brush_size ),( event.y + brush_size )
                CVS.create_line( x0, y0, x1, y1, fill = Colour )
                draw.line([x0, y0, x1, y1], fill=Colour2)
                x0, y0, x1, y1 = None, None, None, None
        else: #pentru forme
            if x0 == None and y0 == None:
                x0, y0 = event.x, event.y
                self.disable_click()
                CVS.after(400, self.enable_click)
            elif x1 == None and y1 == None:
                x1, y1 = event.x, event.y
                if brush_type == "rectangle":
                    if x1 < x0:
                        x0, x1 = x1, x0
                    if y1 < y0:
                        y0, y1 = y1, y0
                    CVS.create_rectangle( x0, y0, x1, y1, fill = Colour, outline= Colour )
                    draw.rectangle([x0, y0, x1, y1], fill=Colour2, outline=Colour2)
                    x0, y0, x1, y1 = None, None, None, None
                    self.disable_click()
                    CVS.after(400, self.enable_click)
                elif brush_type == "ellipse":
                    if x1 < x0:
                        x0, x1 = x1, x0
                    if y1 < y0:
                        y0, y1 = y1, y0
                    CVS.create_oval( x0, y0, x1, y1, fill = Colour, outline= Colour )
                    draw.ellipse([x0, y0, x1, y1], fill=Colour2, outline=Colour2)
                    x0, y0, x1, y1 = None, None, None, None
                    self.disable_click()
                    CVS.after(400, self.enable_click)
                elif brush_type == "line":
                    CVS.create_line( x0, y0, x1, y1, fill = Colour)
                    draw.line([x0, y0, x1, y1], fill=Colour2)
                    x0, y0, x1, y1 = None, None, None, None
                    self.disable_click()
                    CVS.after(400, self.enable_click)

    def disable_click(self):   #Functia care da disable la click si drag (pentru forme)
        CVS.unbind('<Button-1>')
        CVS.unbind( "<B1-Motion>")

    def enable_click(self):     
        CVS.bind('<Button-1>', self.paint)
        CVS.bind( "<B1-Motion>", self.paint )
        
    def clr_test(self, event ):  #Testare culori
        x0, y0, x1, y1 = ( event.x - 20 ),( event.y - 20), ( event.x + 20 ), ( event.y + 20 )
        CLR.create_oval( x0, y0, x1, y1, fill = Colour, outline= Colour )
        
    def pick_color(self):
        global Colour, Colour2
        clr = colorchooser.askcolor()[1]  # Get the hex color
        if clr:
            Colour = clr
            Colour2 = ImageColor.getrgb(clr)  # For Pillow image
            
            # Convert to grayscale regardless of any external conditions
            if filter_type == "grs":
                grayscale_value = int((0.299 * Colour2[0] + 0.587 * Colour2[1] + 0.114 * Colour2[2]))
                Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'  # For Tkinter canvas
                Colour2 = (grayscale_value)

    def assign_colour(self, x):  #Functia pentru butoanele de culoare
        global Colour, Colour2
        Colour = x
        try:
            Colour2 = ImageColor.getrgb(x)
            if filter_type == "grs":
                grayscale_value = int((0.299 * Colour2[0] + 0.587 * Colour2[1] + 0.114 * Colour2[2]))
                Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'  # For Tkinter canvas
                Colour2 = (grayscale_value)
        except ValueError:
            Colour2 = ImageColor.getrgb("black")
            Colour =  "#000000000"
            if filter_type == "grs":
                grayscale_value = int((0.299 * Colour2[0] + 0.587 * Colour2[1] + 0.114 * Colour2[2]))
                Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'  # For Tkinter canvas
                Colour2 = (grayscale_value)

    def set_type(self, shape_type): #Seteaza tipul de pensula (pensula, dreptunghi, elipsa, linie)
        global brush_type, Colour
        brush_type = shape_type
        if Colour == bkgr_clr:
            Colour = "black"
        
    def paint_background(self): #Da fill la background cu culoarea selectata
        global bkgr_clr
        CVS.create_rectangle(2, 2, 1001, 717, fill = Colour, outline="black")
        draw.rectangle([0, 0, 1001, 720], fill=Colour2, outline=Colour2)
        bkgr_clr = Colour

    def new_file(self): #Acelasi lucru dar da fill cu alb (si face un canvas nou in Pillow)
        global image, draw
        CVS.config(height=CVS_height, width=CVS_width)
        CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")
        image = Image.new("RGB", (1000, 720), "#ffffff")
        draw = ImageDraw.Draw(image)

    def get_idea(self): #Generator idei
        num = random.randint(0, 1000)
        w = d1[random.randint(0, len(d1) - 1)]
        x = d2[random.randint(0, len(d2) - 1)]
        y = d3[random.randint(0, len(d3) - 1)]
        z = d4[random.randint(0, len(d4) - 1)]
        entry_suggestion.delete(0, END)
        idea = f"a {w} {x} {y} {z}."
        if num == 42:
            idea = "the meaning of life."
        entry_suggestion.insert(0, idea)
        return

    def save_image_as(self): #Salveaza imaginea ca...
        file_path = filedialog.asksaveasfilename(title="Save Image File", defaultextension=".png", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            image.save(file_path)

    def open_image(self):  #Dialogul pentru deschis poze
        global brightness_factor, CVS
        brightness_factor = 1.0
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            self.display_image(file_path)

    def on_key_press(self, event):   #Eventuri
        if event.state == 4 and event.keysym == 'n':  # 4 -> Ctrl
            self.new_file()
        elif event.state == 4 and event.keysym == 'o':
            self.open_image()
        elif event.state == 4 and event.keysym == 'p':
            self.pick_color()
        elif event.state == 4 and event.keysym == 's':
            self.save_image_as()

    def display_image(self, file_path):   #Incarca imaginea aleasa in open_image
        global image, draw, CVS, tk_image
        loaded_image = Image.open(file_path)
        while loaded_image.width > CVS_width or loaded_image.height > CVS_height:
            loaded_image = loaded_image.resize((loaded_image.width - loaded_image.width//10, loaded_image.height - loaded_image.height//10))
        image = loaded_image
        draw = ImageDraw.Draw(image)
        tk_image = ImageTk.PhotoImage(loaded_image)
        CVS.config(height=image.height, width=image.width)
        CVS.delete(ALL)
        CVS.create_image(0, 0, anchor=NW, image=tk_image)
        CVS.image = tk_image

    def pick_size(self, x):   #Marimea pensulei
        global brush_size
        brush_size = int(x)

    def pick_shape(self, x):  #Forma pensulei
        global brush_shape, brush_type
        if x == "ellipse":
            brush_shape = "ellipse"
            brush_type = "brush"
        elif x == "rectangle":
            brush_shape = "rectangle"
            brush_type = "brush"
        elif x == "pen":    #Pentru forme interesante
            brush_shape = "pen"
            brush_type = "brush"

    def eraser(self): #Guma de sters (seteaza culoarea pensulei la culoarea backgrounduli)
        global bkgr_clr, Colour, Colour2
        Colour = bkgr_clr
        Colour2 = ImageColor.getrgb(Colour)

    #Filtre
    def filter(self, _type): 
        global image, draw, tk_image, Colour, Colour2, filter_type, brightness_factor
        if _type == "bnw":
            image = image.convert("1")
            Colour = 'black'
            Colour2 = 0
        elif _type == "grs":
            image = image.convert("L")
            Colour = 'black'
            Colour2 = 0
        elif _type == None:
            image = image.convert("RGB")
            Colour = 'black'
            Colour2 = 0
        elif _type == 'uex':
            brightness_factor = 0.5
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
            brightness_factor = 1.0
        elif _type == 'oex':
            brightness_factor = 1.5
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
            brightness_factor = 1.0
        filter_type = _type

        draw = ImageDraw.Draw(image)
        tk_image = ImageTk.PhotoImage(image)
        CVS.delete(ALL)
        CVS.create_image(0, 0, anchor=NW, image=tk_image) 
        CVS.image = tk_image

    def brightness(self, _type):
        global brightness_factor, image, tk_image, draw
        if _type == 0:
            brightness_factor -= 0.1
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
        elif _type == 1:
            brightness_factor += 0.1
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_factor)
        draw = ImageDraw.Draw(image)
        tk_image = ImageTk.PhotoImage(image)
        CVS.delete(ALL)
        CVS.create_image(0, 0, anchor=NW, image=tk_image) 
        CVS.image = tk_image
        brightness_factor = 1.0

    #Functia care creeaza butoanele
    def draw_buttons(self):
        global spinbox_brush_size

        #butoane stanga
        #seteaza marimea pensulei
        spinbox_brush_size = Spinbox(WIN, from_= 1, to=2000, width=5)
        spinbox_brush_size.place(x=2, y = 5)
        #confirma marimea 
        button_check = Button(WIN, image=photo_check)
        button_check.place(x=50, y=5)                                                                                   #Foloseste lambda ca sa dea call la functie doar cand apesi pe buton
        button_check.config(width=28, height=20, cursor="hand2", command = lambda: self.pick_size(spinbox_brush_size.get())) #Altfel ii da call doar cand creaza butonul
        #guma
        button_eraser = Button(WIN, image=photo_eraser)
        button_eraser.place(x=90, y=5)
        button_eraser.config(width=74, height=20, cursor="hand2", command = self.eraser)
        #pensula
        button_brush = Button(WIN, image=photo_brush)
        button_brush.place(x=176, y=5)
        button_brush.config(width=72, height=20, cursor="hand2", command = lambda: self.set_type("brush"))
        #sugestii de desen
        button_suggestion = Button(WIN, text="Draw:")
        button_suggestion.place(x=10, y=300)
        button_suggestion.config(width=10, height=2, cursor="hand2", command = self.get_idea)
        #dreptunghi
        button_rectangle = Button(WIN, image = photo_rectangle, compound = LEFT)
        button_rectangle.place(x=5, y=35)
        button_rectangle.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("rectangle"))
        #elipsa
        button_ellipse = Button(WIN, image = photo_ellipse, compound = LEFT)
        button_ellipse.place(x=90, y=35)
        button_ellipse.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("ellipse"))
        #linie
        button_ellipse = Button(WIN, image = photo_line, compound = LEFT)
        button_ellipse.place(x=175, y=35)
        button_ellipse.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("line"))
        #darken
        button_darken = Button(WIN, image = photo_darken, compound = LEFT)
        button_darken.place(x=5, y=85)
        button_darken.config(width=115, height=36, cursor="hand2", command = lambda: self.brightness(0))
        #lighten
        button_lighten = Button(WIN, image = photo_lighten, compound = LEFT)
        button_lighten.place(x=133, y=85)
        button_lighten.config(width=115, height=36, cursor="hand2", command = lambda: self.brightness(1))

        #butoane dreapta
        #clr/bgr
        button_pick = Button(WIN, image=photo_pick_clr)
        button_pick.place(x=1283, y=185)
        button_pick.config(width=120, height=36, cursor="hand2", command = self.pick_color)
        color_button = Button(WIN, image=photo_bucket)
        color_button.place(x=1412, y=185)
        color_button.config(width=110, height=36, cursor="hand2", command = self.paint_background)
        #rgb
        button_r = Button(WIN,bg="#ff0000")
        button_r.place(x=1283, y=5)
        button_r.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ff0000"))
        button_g = Button(WIN, bg="#228b22")
        button_g.place(x=1365, y=5)
        button_g.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#228b22"))
        button_b = Button(WIN, bg="#00008b")
        button_b.place(x=1447, y=5)
        button_b.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#00008b"))
        #yop
        button_y = Button(WIN, bg="#e6cc00")
        button_y.place(x=1283, y=50)
        button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#e6cc00"))
        button_o = Button(WIN, bg="#fca510")
        button_o.place(x=1365, y=50)
        button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#fca510"))
        button_p = Button(WIN, bg="#8a00c2")
        button_p.place(x=1447, y=50)
        button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#8a00c2"))
        #bpb
        button_y = Button(WIN, bg="#724a24")
        button_y.place(x=1283, y=95)
        button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#724a24"))
        button_o = Button(WIN, bg="#f98cb9")
        button_o.place(x=1365, y=95)
        button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#f98cb9"))
        button_p = Button(WIN, bg="#d2b48c")
        button_p.place(x=1447, y=95)
        button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#d2b48c"))
        #wbg
        button_w = Button(WIN, bg="#ffffff")
        button_w.place(x=1283, y=140)
        button_w.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ffffff"))
        button_blk = Button(WIN, bg="#000000000")
        button_blk.place(x=1365, y=140)
        button_blk.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#000000000"))
        button_gry = Button(WIN, bg="#808080")
        button_gry.place(x=1447, y=140)
        button_gry.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#808080"))


    def draw_menu(self):    #Creaza butoanele din meniu
        file_menu = Menu(menu)
        tool_menu = Menu(menu)
        filter_menu = Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New          Ctrl+N', command=self.new_file)
        file_menu.add_command(label='Open...      Ctrl+O', command=self.open_image)
        file_menu.add_command(label='Save As...   Ctrl+S', command = self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=WIN.quit)

        menu.add_cascade(label='Tools', menu=tool_menu)
        tool_menu.add_cascade(label='Brush Shape', menu=bs_sub_menu)
        bs_sub_menu.add_command(label='Ellipse', command= lambda: self.pick_shape("ellipse"))
        bs_sub_menu.add_command(label='Rectangle', command= lambda: self.pick_shape("rectangle"))
        bs_sub_menu.add_command(label='Pen', command= lambda: self.pick_shape("pen"))

        tool_menu.add_cascade(label="Shapes", menu=sp_sub_menu)
        sp_sub_menu.add_command(label='Rectangle', command = lambda: self.set_type("rectangle"))
        sp_sub_menu.add_command(label='Ellipse', command = lambda: self.set_type("ellipse"))
        sp_sub_menu.add_command(label='Line', command = lambda: self.set_type("line"))

        menu.add_cascade(label='Filters', menu=filter_menu)
        filter_menu.add_command(label='Grayscale', command= lambda: self.filter("grs"))
        filter_menu.add_command(label='Black and White', command= lambda: self.filter("bnw"))
        filter_menu.add_command(label='RGB', command= lambda: self.filter(None))
        filter_menu.add_command(label='Underexpose', command= lambda: self.filter("uex"))
        filter_menu.add_command(label='Overexpose', command= lambda: self.filter("oex"))


    def draw_label(self):   #Text + Notes
        label_test_clr = Label(WIN, text="Compare Colours", font=("Arial", 16, "bold"), fg="black", bg="white")
        label_test_clr.place(x=1310, y=370)
        label_notes = Label(WIN, text="Notes", font=("Arial", 16, "bold"), fg="black", bg="white")
        label_notes.place(x=95, y=370)
        notes = Text(WIN, width=30, height=19, bg="grey94")
        notes.place(x=10, y=400)

app = App()
print(artx_directory)
#Eventuri
CVS.bind( "<B1-Motion>", app.paint )
CVS.bind( "<Button-1>", app.paint )
CVS.pack()

CLR.bind( "<Button-1>", app.clr_test )
WIN.bind('<KeyPress>', app.on_key_press)

app.draw_label()
app.draw_menu()
app.draw_buttons()
mainloop()