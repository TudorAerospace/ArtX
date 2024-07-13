from tkinter import *
from tkinter import ALL, colorchooser, filedialog, PhotoImage
from PIL import *
from PIL import Image, ImageDraw, ImageColor, ImageTk, ImageEnhance, ImageFilter
import os
import random
import time
import shelve

class App:
    def __init__(self):
        self.width = 1540
        self.height = 720
        self.WIN = Tk()
        self.WIN.title("ArtX")
        self.WIN.geometry(f"{self.width}x{self.height}")
        self.WIN.resizable(False, False)
        self.WIN.config(bg="white")

        self.directories = ['ArtX', 'Assets']
        self.filename = 'rectangle.png'
        self.current_directory = os.getcwd()

        self.x0, self.y0, self.x1, self.y1 = None, None, None, None

        self.d1 = ["blue", "red", "yellow", "green", "big", "small", "little", "long", "white", "black", "sad", "happy", "sleepy", "motorized", "tall", "smart", "huge", "clean", "dirty", "bright", "dark", "ornate", "festive", "glowing"]
        self.d2 = ["cat", "dog", "plane", "iguana", "fish", "bird", "car", "planet", "book", "elephant", "star", "computer", "building", "bee", "ant", "hat", "object", "lion", "shark", "ball", "tank", "ship", "trumpet", "tree", "robot"]
        self.d3 = ["assembling", "eating", "building", "demolishing", "using", "selling", "placing", "gathering", "smelling", "tasting", "attacking", "planting", "seeing", "hiding", "burying", "decorating", "drawing"]
        self.d4 = ["a building", "a phone", "a home", "a guitar", "a piano", "a pizza", "a flower", "a treasure", "a letter", "an essay", "a laptop", "a tractor", "a fork", "a hat", "an entity(?)", "a fish", "a bat", "a poster", "a toy"]

        self.Colour = "#000000"
        self.Colour2 = ImageColor.getrgb("black")

        self.canvas_name = "canvas"
        self.image_states = [("rectangle0", 2, 2, 1001, 717, "rectangle", "#ffffff", ImageColor.getrgb("white"))]

        self.bkgr_clr = "#ffffff"
        self.image = Image.new("RGB", (1000, 720), "#ffffff")
        self.image_backup = None
        self.draw = ImageDraw.Draw(self.image)

        self.brush_size = 10
        self.brush_shape = "ellipse"
        self.brush_type = "brush"
        self.entry_suggestion = Entry(self.WIN, width=40)
        self.entry_suggestion.place(x=10, y=350)

        self.CVS_width_default = 1000
        self.CVS_height_default = 720
        self.CVS_width = 1000
        self.CVS_height = 720

        self.CVS = Canvas(self.WIN, width=1000, height=720)
        self.CVS.create_rectangle(2, 2, 1001, 717, fill="#ffffff", outline="#000000")
        self.CVS.config(cursor="pencil")

        self.CLR = Canvas(self.WIN, width=250, height=310)
        self.CLR.place(x=1280, y=400)

        self.menu = Menu(self.WIN)
        self.WIN.config(menu=self.menu)
        self.bs_sub_menu = Menu(self.menu, tearoff=0)
        self.sp_sub_menu = Menu(self.menu, tearoff=0)

        self.filter_type = None
        self.brightness_factor = 1.0

        self.rect_num = 1
        self.ellipse_num = 0
        self.line_num = 0
        self.bg_num = 0
        self.brush_num = 0
        self.filter_num = 0
        self.colour_num = 0

        self.artx_directory = os.path.abspath(__file__)
        self.path = self.artx_directory.replace('ArtX.py', 'Assets\\rectangle.png')
        self.artx_directory = self.artx_directory.replace('ArtX.py', '')

        # Import images for buttons
        self.photo_rectangle = PhotoImage(file=self.path)
        self.path = self.path.replace('rectangle.png', 'ellipse.png')
        self.photo_ellipse = PhotoImage(file=self.path)
        self.path = self.path.replace('ellipse.png', 'line.png')
        self.photo_line = PhotoImage(file=self.path)
        self.path = self.path.replace('line.png', 'pick_clr.png')
        self.photo_pick_clr = PhotoImage(file=self.path)
        self.path = self.path.replace('pick_clr.png', 'check.png')
        self.photo_check = PhotoImage(file=self.path)
        self.path = self.path.replace('check.png', 'eraser.png')
        self.photo_eraser = PhotoImage(file=self.path)
        self.path = self.path.replace('eraser.png', 'brush.png')
        self.photo_brush = PhotoImage(file=self.path)
        self.path = self.path.replace('brush.png', 'bucket.png')
        self.photo_bucket = PhotoImage(file=self.path)
        self.path = self.path.replace('bucket.png', 'lighten.png')
        self.photo_lighten = PhotoImage(file=self.path)
        self.path = self.path.replace('lighten.png', 'darken.png')
        self.photo_darken = PhotoImage(file=self.path)
        self.path = self.path.replace('darken.png', 'icon.png')
        self.photo_icon = PhotoImage(file=self.path)
        self.path = self.path.replace('icon.png', 'trophy.png')
        self.photo_trophy = PhotoImage(file=self.path)
        self.path = self.path.replace('trophy.png', 'achievement_1_inc.png')
        self.photo_ach_1_inc = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_1_inc.png', 'achievement_1_com.png')
        self.photo_ach_1_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_1_com.png', 'achievement_2_inc.png')
        self.photo_ach_2_inc = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_2_inc.png', 'achievement_2_com.png')
        self.photo_ach_2_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_2_com.png', 'achievement_3_inc.png')
        self.photo_ach_3_inc = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_3_inc.png', 'achievement_3_com.png')
        self.photo_ach_3_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_3_com.png', 'achievement_4_inc.png')
        self.photo_ach_4_inc = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_4_inc.png', 'achievement_4_com.png')
        self.photo_ach_4_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_4_com.png', 'achievement_5_com.png')
        self.photo_ach_5_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_5_com.png', 'achievement_5_inc.png')
        self.photo_ach_5_inc = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_5_inc.png', 'achievement_6_com.png')
        self.photo_ach_6_com = PhotoImage(file=self.path)
        self.path = self.path.replace('achievement_6_com.png', 'achievement_6_inc.png')
        self.photo_ach_6_inc = PhotoImage(file=self.path)
        
        self.WIN.iconphoto(False, self.photo_icon)
        self.start_time = time.time()
        
        self.ach_1_complete = False
        self.ach_1_complete_shown = False
        self.ach_2_complete = False
        self.ach_2_complete_shown = False
        self.ach_3_complete = False
        self.ach_3_complete_shown = False
        self.ach_4_complete = False
        self.ach_4_complete_shown = False
        self.ach_5_complete = False
        self.ach_5_complete_shown = False
        self.ach_6_complete = False
        self.ach_6_complete_shown = False

    def paint(self, event ): #Functia care se activeaza cand dai click/drag ca sa pictezi
        if self.brush_type == "brush" or self.brush_type == "eraser":   #pentru pensula
            self.x0, self.y0, self.x1, self.y1 = ( event.x - self.brush_size/2 ),( event.y- self.brush_size/2), ( event.x + self.brush_size/2 ), ( event.y + self.brush_size/2 )
            if self.brush_shape == "ellipse":
                self.CVS.create_oval( self.x0, self.y0, self.x1, self.y1, fill = self.Colour, outline= self.Colour, tags=f"brush{self.brush_num}")
                self.draw.ellipse([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, outline=self.Colour2)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "ellipse", self.Colour, self.Colour2))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
            elif self.brush_shape == "rectangle":
                self.CVS.create_rectangle( self.x0, self.y0, self.x1, self.y1, fill = self.Colour, outline= self.Colour,  tags=f"brush{self.brush_num}")
                self.draw.rectangle([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, outline=self.Colour2)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "rectangle", self.Colour, self.Colour2))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
            elif self.brush_shape == "pen":
                self.x0, self.y0, self.x1, self.y1 = ( event.x ),( event.y), ( event.x + self.brush_size ),( event.y + self.brush_size )
                self.CVS.create_line( self.x0, self.y0, self.x1, self.y1, fill = self.Colour,  tags=f"brush{self.brush_num}", width=self.brush_size )
                self.draw.line([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, width=self.brush_size)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "line", (self.Colour, self.Colour2), self.brush_size))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
        else: #pentru forme
            if self.x0 == None and self.y0 == None:
                self.x0, self.y0 = event.x, event.y
                self.disable_click()
                self.CVS.after(400, self.enable_click)
            elif self.x1 == None and self.y1 == None:
                self.x1, self.y1 = event.x, event.y
                if self.brush_type == "rectangle":
                    if self.x1 < self.x0:
                        self.x0, self.x1 = self.x1, self.x0
                    if self.y1 < self.y0:
                        self.y0, self.y1 = self.y1, self.y0
                    self.create_rectangle(self.x0, self.y0, self.x1, self.y1)
                    self.x0,self.y0, self.x1, self.y1 = None, None, None, None
                    self.disable_click()
                    self.CVS.after(400, self.enable_click)
                elif self.brush_type == "ellipse":
                    if self.x1 < self.x0:
                        self.x0, self.x1 = self.x1, self.x0
                    if self.y1 < self.y0:
                        self.y0, self.y1 = self.y1, self.y0
                    self.create_ellipse(self.x0, self.y0, self.x1, self.y1)
                    self.x0, self.y0, self.x1, self.y1 = None, None, None, None
                    self.CVS.after(400, self.enable_click)
                elif self.brush_type == "line":
                    self.create_line(self.x0, self.y0, self.x1, self.y1)
                    self.x0,self. y0, self.x1, self.y1 = None, None, None, None
                    self.disable_click()
                    self.CVS.after(400, self.enable_click)
            self.achievements['ach_2'] += 0.5
            self.handle_achievements(1)
        if self.achievements['ach_1'] == 0:
            self.achievements['ach_1'] = 1
            self.handle_achievements(1)
    
    def create_rectangle(self, x0, y0, x1, y1):
        tag = f"rectangle{self.rect_num}"
        self.image_states.append((tag, x0, y0, x1, y1, "rectangle", self.Colour, self.Colour2))
        self.rect_num += 1
        self.CVS.create_rectangle(x0, y0, x1, y1, fill=self.Colour, outline=self.Colour, tags=tag)
        self.draw.rectangle([x0, y0, x1, y1], fill=self.Colour2, outline=self.Colour2)

    def create_ellipse(self, x0, y0, x1, y1):
        tag = f"ellipse{self.ellipse_num}"
        self.image_states.append((tag, x0, y0, x1, y1, "ellipse", self.Colour, self.Colour2))
        self.ellipse_num += 1
        self.CVS.create_oval(x0, y0, x1, y1, fill=self.Colour, outline=self.Colour, tags=tag)
        self.draw.ellipse([x0, y0, x1, y1], fill=self.Colour2, outline=self.Colour2)

    def create_line(self, x0, y0, x1, y1):
        tag = f"line{self.line_num}"
        self.image_states.append((tag, x0, y0, x1, y1, "line", (self.Colour, self.Colour2), self.brush_size))
        self.line_num += 1
        self.CVS.create_line(x0, y0, x1, y1, fill=self.Colour, tags=tag, width=self.brush_size)
        self.draw.line([x0, y0, x1, y1], fill=self.Colour2, width=self.brush_size)


    def disable_click(self):   #Functia care da disable la click si drag (pentru forme)
        self.CVS.unbind('<Button-1>')
        self.CVS.unbind( "<B1-Motion>")

    def enable_click(self):     
        self.CVS.bind('<Button-1>', self.paint)
        self.CVS.bind( "<B1-Motion>", self.paint )
        
    def clr_test(self, event ):  #Test culori
        self.x0, self.y0, self.x1, self.y1 = ( event.x - 20 ),( event.y - 20), ( event.x + 20 ), ( event.y + 20 )
        self.CLR.create_oval( self.x0, self.y0, self.x1, self.y1, fill = self.Colour, outline= self.Colour )
        
    def pick_color(self):
        clr = colorchooser.askcolor()[1]
        if clr:
            self.Colour = clr
            self.Colour2 = ImageColor.getrgb(clr)
            
            if self.filter_type == "grs":
                grayscale_value = int((0.299 * self.Colour2[0] + 0.587 * self.Colour2[1] + 0.114 * self.Colour2[2]))
                self.Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'
                self.Colour2 = (grayscale_value)

    def assign_colour(self, x):  # Click pe butoanele de culoare
        self.Colour = x
        self.CVS.config(cursor="pencil") 
        try:
            self.Colour2 = ImageColor.getrgb(x)
            if self.filter_type == "grs":
                grayscale_value = int((0.299 * self.Colour2[0] + 0.587 * self.Colour2[1] + 0.114 * self.Colour2[2]))
                self.Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'
                self.Colour2 = (grayscale_value)
        except ValueError:
            self.Colour2 = ImageColor.getrgb("black")
            self.Colour =  "#000000000"
            if self.filter_type == "grs":
                grayscale_value = int((0.299 * self.Colour2[0] + 0.587 * self.Colour2[1] + 0.114 * self.Colour2[2]))
                self.Colour = f'#{grayscale_value:02x}{grayscale_value:02x}{grayscale_value:02x}'
                self.Colour2 = (grayscale_value)
        self.achievements['ach_4'] += 1
        self.handle_achievements(1)

    def set_type(self, shape_type): #Seteaza tipul de pensula (pensula, dreptunghi, elipsa, linie)
        self.brush_type = shape_type
        self.CVS.config(cursor="pencil") 
        if self.Colour == self.bkgr_clr:
            self.Colour = "black"
        
    def paint_background(self): #Da fill la background cu culoarea selectata
        self.CVS.create_rectangle(2, 2, 1001, 717, fill = self.Colour, outline="black", tags=f"bkgr{self.bg_num}")
        self.image_states.append((f"rectangle{self.rect_num}", 2, 2, 1001, 717, "rectangle", self.Colour, self.Colour2))
        self.rect_num += 1
        self.draw.rectangle([0, 0, 1001, 720], fill=self.Colour2, outline=self.Colour2)
        self.bkgr_clr = self.Colour

    def new_file(self): #Acelasi lucru dar da fill cu alb (si face un canvas nou in Pillow)
        self.CVS.config(height=self.CVS_height_default, width=self.CVS_width_default)
        self.CVS.create_rectangle(2, 2, 1001, 717, fill = "#ffffff", outline="#000000")
        self.image = Image.new("RGB", (1000, 720), "#ffffff")
        self.draw = ImageDraw.Draw(self.image)

    def get_idea(self): #Generator idei
        num = random.randint(0, 100)
        w = self.d1[random.randint(0, len(self.d1) - 1)]
        x = self.d2[random.randint(0, len(self.d2) - 1)]
        y = self.d3[random.randint(0, len(self.d3) - 1)]
        z = self.d4[random.randint(0, len(self.d4) - 1)]
        self.entry_suggestion.delete(0, END)
        idea = f"a {w} {x} {y} {z}."
        if num == 42:
            idea = "the meaning of life."
            CVS.config(cursor="question_arrow") 
        elif num == 53:
            idea = "a detective and his robot partner."
            CVS.config(cursor="man")
        elif  num == 99:
            idea = "a Lord using the Force."
            CVS.config(cursor="star")
        elif num == 79:
            idea = "a whale, above the surface of an alien planet."
            CVS.config(cursor="boat")
        elif num == 66:
            idea = "somewhere where no man has ever gone before!"
            CVS.config(cursor="trek") 
        self.entry_suggestion.insert(0, idea)
        return

    def save_image_as(self, action): #Salveaza imaginea ca...
        if action == 0:
            file_path = filedialog.asksaveasfilename(title="Save Image File", defaultextension=".png", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
            if file_path:
                self.image.save(file_path)
        else:
            file_path = filedialog.asksaveasfilename(title="Save Image File", defaultextension=".png", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
            if file_path:
                self.image.save(file_path)
            self.WIN.destroy()
            self.CLS.destroy()

    def open_image(self):  #Dialogul pentru deschis poze
        global brightness_factor, CVS
        self.brightness_factor = 1.0
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path:
            self.display_image(file_path)

    def revert_state(self):
        global image, draw, image_states, rect_num, ellipse_num, line_num, filter_num
        if self.image_states:

            last_state_tag = self.image_states.pop()[0]

            self.image_states = [state for state in self.image_states if state[0] != last_state_tag]

            self.CVS.delete("all")
            self.CVS.config(bg="white")
            self.image = Image.new("RGB", (self.CVS_width, self.CVS_height), "white")
            self.draw = ImageDraw.Draw(self.image)

            for state in self.image_states:
                try:
                    tag, x0, y0, x1, y1, shape_type, clr, clr2 = state
                except ValueError:
                    del state
                if tag.startswith("background"):
                    self.CVS.create_rectangle(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                    self.draw.rectangle([x0, y0, x1, y1], fill=clr2, outline=clr2)
                elif tag == "image":
                    self.draw = ImageDraw.Draw(self.image_backup)
                    self.tk_image = ImageTk.PhotoImage(self.image_backup)
                    self.CVS.config(height=self.image.height, width=self.image.width)
                    self.CVS.delete(ALL)
                    self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
                    self.CVS.image = self.tk_image
                elif shape_type == "rectangle":
                    self.CVS.create_rectangle(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                    self.draw.rectangle([x0, y0, x1, y1], fill=clr2, outline=clr2)
                elif shape_type == "ellipse":
                    self.CVS.create_oval(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                    self.draw.ellipse([x0, y0, x1, y1], fill=clr2, outline=clr2)
                elif shape_type == "line":
                    self.CVS.create_line(x0, y0, x1, y1, fill=clr[0], tags=tag, width=clr2)
                    self.draw.line([x0, y0, x1, y1], fill=clr[1], width=clr2)
                elif tag.startswith("filter"):
                    self.image = self.image.convert("RGB")
                    self.filter_type = None
                elif shape_type.startswith("brush"):
                    if shape_type == "ellipse":
                        self.CVS.create_oval(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                        self.draw.ellipse([x0, y0, x1, y1], fill=clr2, outline=clr2)
                    elif shape_type == "rectangle":
                        self.CVS.create_rectangle(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                        self.draw.rectangle([x0, y0, x1, y1], fill=clr2, outline=clr2)
                    elif shape_type == "pen":
                        self.CVS.create_line(x0, y0, x1, y1, fill=clr[0], tags=tag, width=clr2)
                        self.draw.line([x0, y0, x1, y1], fill=clr[1], width=clr2)

            self.rect_num = sum(1 for state in self.image_states if state[5] == "rectangle")
            self.ellipse_num = sum(1 for state in self.image_states if state[5] == "ellipse")
            self.line_num = sum(1 for state in self.image_states if state[5] == "line")



    def on_key_press(self, event):   #Eventuri
        if event.state == 4 and event.keysym == 'n':  # 4 -> Ctrl
            self.new_file()
        elif event.state == 4 and event.keysym == 'o':
            self.open_image()
        elif event.state == 4 and event.keysym == 'p':
            self.pick_color()
        elif event.state == 4 and event.keysym == 's':
            self.save_image_as(0)
        elif event.state == 4 and event.keysym == 'z':
            self.revert_state()
        
    def release(self, event=None):
        if self.brush_type == "brush" or self.brush_type == "eraser":
            self.image_states.append(f"brush{self.brush_num}")
            self.brush_num += 1

    def display_image(self, file_path):   #Incarca imaginea aleasa in open_image
        self.image_states = []
        loaded_image = Image.open(file_path)
        while loaded_image.width > self.CVS_width_default or loaded_image.height > self.CVS_height_default:
            loaded_image = loaded_image.resize((loaded_image.width - loaded_image.width//10, loaded_image.height - loaded_image.height//10))
        self.image = loaded_image
        self.image_backup = self.image
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = ImageTk.PhotoImage(loaded_image)
        self.CVS.config(height=self.image.height, width=self.image.width)
        self.CVS.delete(ALL)
        self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
        self.CVS.image = self.tk_image
        self.CVS_width, self.CVS_height = self.image.width, self.image.height
        self.image_states.append(("image", None, None, None, None, None, None, None))

    def pick_size(self, x):   #Marimea pensulei
        self.brush_size = int(x)

    def pick_shape(self, x):  #Forma pensulei
        global brush_shape, brush_type
        if x == "ellipse":
            self.brush_shape = "ellipse"
            self.brush_type = "brush"
        elif x == "rectangle":
            self.brush_shape = "rectangle"
            self.brush_type = "brush"
        elif x == "pen":    #Pentru forme interesante
            self.brush_shape = "pen"
            self.brush_type = "brush"

    def eraser(self): #Guma de sters (seteaza culoarea pensulei la culoarea backgrounduli)
        self.CVS.config(cursor="circle") 
        self.Colour = self.bkgr_clr
        self.Colour2 = ImageColor.getrgb(self.Colour)

    #Filtre
    def filter(self, _type): 
        if _type == "bnw":
            self.image = self.image.convert("1")
            self.Colour = 'black'
            self.Colour2 = 0
        elif _type == "grs":
            self.image = self.image.convert("L")
            self.Colour = 'black'
            self.Colour2 = 0
        elif _type == None:
            self.image = self.image.convert("RGB")
            self.Colour = 'black'
            self.Colour2 = 0
        elif _type == 'uex':
            self.brightness_factor = 0.5
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(self.brightness_factor)
            self.brightness_factor = 1.0
        elif _type == 'oex':
            self.brightness_factor = 1.5
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(self.brightness_factor)
            self.brightness_factor = 1.0
        elif _type == "spn":
            sharpened_image = self.image.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Sharpness(sharpened_image)
            sharpened_image = enhancer.enhance(2.0) 
            self.image = sharpened_image
        elif _type in ["SMOOTH", "BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE"]:
            self.image = self.image.filter(eval(f"ImageFilter.{_type}"))
        
        self.filter_type = _type
        self.image_states.append((f"filter", None, None, None, None, self.filter_type, None, None))
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.CVS.delete(ALL)
        self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image) 
        self.CVS.image = self.tk_image

    def brightness(self, _type):
        if _type == 0:
            self.brightness_factor -= 0.1
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(self.brightness_factor)
        elif _type == 1:
            self.brightness_factor += 0.1
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(self.brightness_factor)
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.CVS.delete(ALL)
        self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image) 
        self.CVS.image = self.tk_image
        self.brightness_factor = 1.0

    def open_achievement_window(self):
        ACH = Toplevel(self.WIN)
        ACH.title("Achievements")
        ACH.geometry("500x300")
        ACH.resizable(False, False)
        ACH.iconphoto(False, self.photo_trophy)

        self.canvas = Canvas(ACH, width=480, height=300)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(ACH, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=frame, anchor="nw")

        achievements_status = [self.ach_1_complete, self.ach_2_complete,self.ach_3_complete, self.ach_4_complete, self.ach_5_complete, self.ach_6_complete]

        achievements_images_inc = [self.photo_ach_1_inc, self.photo_ach_2_inc, self.photo_ach_3_inc, self.photo_ach_4_inc, self.photo_ach_5_inc, self.photo_ach_6_inc]

        achievements_images_com = [self.photo_ach_1_com, self.photo_ach_2_com, self.photo_ach_3_com, self.photo_ach_4_com, self.photo_ach_5_com, self.photo_ach_6_com]

        for i in range(0, 6):
            image = achievements_images_com[i] if achievements_status[i] else achievements_images_inc[i]
            button = Button(frame, command=lambda: self.handle_achievements(0), image=image)
            button.config(width=470, height=80)
            button.grid(row=i if i < 2 else i + 1, column=0, pady=5)

        frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def handle_achievements(self, action):
        shelf_path = os.path.join(self.artx_directory, "Assets", "achievement_progress")

        if action == 0:
            with shelve.open(shelf_path) as db:
                self.achievements = db.get('achievements', {'ach_1': 0, 'ach_2': 0, 'ach_3': 0, 'ach_4': 0, 'ach_6': 0})

            if self.achievements['ach_1'] >= 1:
                self.ach_1_complete_shown = True
            if self.achievements['ach_2'] >= 100:
                self.ach_2_complete_shown = True
            if self.achievements['ach_3'] >= 3600:
                self.ach_3_complete_shown = True
            if self.achievements['ach_4'] >= 20:
                self.ach_4_complete_shown = True
            if self.achievements['ach_2'] >= 500:
                self.ach_5_complete_shown = True
            if self.achievements['ach_6'] >= 1:
                self.ach_6_complete_shown = True

        elif action == 1:
            self.end_time = time.time()
            self.achievements['ach_3'] = int(self.end_time - self.start_time)
            with shelve.open(shelf_path) as db:
                db['achievements'] = self.achievements

            self.handle_achievements(2)

        elif action == 2:
            if self.achievements['ach_1'] == 1:
                self.ach_1_complete = True
                self.achievement_notification(1)
                self.ach_1_complete_shown = True
            if self.achievements['ach_2'] > 100:
                self.ach_2_complete = True
                self.achievement_notification(2)
                self.ach_2_complete_shown = True
            if self.achievements['ach_3'] > 3600:
                self.ach_3_complete = True
                self.achievement_notification(3)
                self.ach_3_complete_shown = True
            if self.achievements['ach_4'] > 20:
                self.ach_4_complete = True
                self.achievement_notification(4)
                self.ach_4_complete_shown = True
            if self.achievements['ach_2'] > 500:
                self.ach_5_complete = True
                self.achievement_notification(5)
                self.ach_5_complete_shown = True
            if self.achievements['ach_6'] == 1:
                self.ach_6_complete = True
                self.achievement_notification(6)
                self.ach_6_complete_shown = True
  
    def achievement_notification(self, action):
        achievements_complete_shown = [self.ach_1_complete_shown, self.ach_2_complete_shown, self.ach_3_complete_shown, self.ach_4_complete_shown, self.ach_5_complete_shown, self.ach_6_complete_shown]
        if action in range(1, 7) and not achievements_complete_shown[action - 1]:
            ACH_N = Toplevel(self.WIN)
            ACH_N.title("Achievement Got!")
            ACH_N.geometry("500x100")
            ACH_N.resizable(False, False)
            ACH_N.iconphoto(False, self.photo_trophy)
            achievements_complete_shown = [ self.ach_1_complete_shown, self.ach_2_complete_shown, self.ach_3_complete_shown, self.ach_4_complete_shown, self.ach_5_complete_shown, self.ach_6_complete_shown]           
            achievements_images_com = [self.photo_ach_1_com, self.photo_ach_2_com, self.photo_ach_3_com, self.photo_ach_4_com, self.photo_ach_5_com, self.photo_ach_6_com]
            image = None
            if action in range(1, 7) and not achievements_complete_shown[action - 1]:
                image = achievements_images_com[action - 1]
            achievement = Button(ACH_N, command=lambda: self.handle_achievements(0), image=image)
            achievement.config(width=470, height=80)
            achievement.grid(row=0, column=0, pady=5, padx=15)

    #Functia care creeaza butoanele
    def draw_buttons(self):
        global spinbox_brush_size
        #butoane stanga
        #seteaza marimea pensulei
        spinbox_brush_size = Spinbox(self.WIN, from_= 1, to=2000, width=5, command= lambda: self.pick_size(spinbox_brush_size.get()))
        spinbox_brush_size.insert(1, 0)
        spinbox_brush_size.place(x=2, y = 5)
        #confirma marimea 
        button_check = Button(self.WIN, image=self.photo_check)
        button_check.place(x=50, y=5)                                                                                   #Foloseste lambda ca sa dea call la functie doar cand apesi pe buton
        button_check.config(width=28, height=20, cursor="hand2", command = lambda: self.revert_state()) #Altfel ii da call doar cand creaza butonul
        #guma
        button_eraser = Button(self.WIN, image=self.photo_eraser)
        button_eraser.place(x=90, y=5)
        button_eraser.config(width=74, height=20, cursor="hand2", command = self.eraser)
        #pensula
        button_brush = Button(self.WIN, image=self.photo_brush)
        button_brush.place(x=176, y=5)
        button_brush.config(width=72, height=20, cursor="hand2", command = lambda: self.set_type("brush"))
        #sugestii de desen
        button_suggestion = Button(self.WIN, text="Draw:")
        button_suggestion.place(x=10, y=300)
        button_suggestion.config(width=10, height=2, cursor="hand2", command = self.get_idea)
        #dreptunghi
        button_rectangle = Button(self.WIN, image = self.photo_rectangle, compound = LEFT)
        button_rectangle.place(x=5, y=35)
        button_rectangle.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("rectangle"))
        #elipsa
        button_ellipse = Button(self.WIN, image = self.photo_ellipse, compound = LEFT)
        button_ellipse.place(x=90, y=35)
        button_ellipse.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("ellipse"))
        #linie
        button_ellipse = Button(self.WIN, image = self.photo_line, compound = LEFT)
        button_ellipse.place(x=175, y=35)
        button_ellipse.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("line"))
        #darken
        button_darken = Button(self.WIN, image = self.photo_darken, compound = LEFT)
        button_darken.place(x=5, y=85)
        button_darken.config(width=115, height=36, cursor="hand2", command = lambda: self.brightness(0))
        #lighten
        button_lighten = Button(self.WIN, image = self.photo_lighten, compound = LEFT)
        button_lighten.place(x=133, y=85)
        button_lighten.config(width=115, height=36, cursor="hand2", command = lambda: self.brightness(1))

        #butoane dreapta
        #clr/bgr
        button_pick = Button(self.WIN, image=self.photo_pick_clr)
        button_pick.place(x=1283, y=185)
        button_pick.config(width=120, height=36, cursor="hand2", command = self.pick_color)
        color_button = Button(self.WIN, image=self.photo_bucket)
        color_button.place(x=1412, y=185)
        color_button.config(width=110, height=36, cursor="hand2", command = self.paint_background)
        #rgb
        button_r = Button(self.WIN,bg="#ff0000")
        button_r.place(x=1283, y=5)
        button_r.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ff0000"))
        button_g = Button(self.WIN, bg="#228b22")
        button_g.place(x=1365, y=5)
        button_g.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#228b22"))
        button_b = Button(self.WIN, bg="#00008b")
        button_b.place(x=1447, y=5)
        button_b.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#00008b"))
        #yop
        button_y = Button(self.WIN, bg="#e6cc00")
        button_y.place(x=1283, y=50)
        button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#e6cc00"))
        button_o = Button(self.WIN, bg="#fca510")
        button_o.place(x=1365, y=50)
        button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#fca510"))
        button_p = Button(self.WIN, bg="#8a00c2")
        button_p.place(x=1447, y=50)
        button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#8a00c2"))
        #bpb
        button_y = Button(self.WIN, bg="#724a24")
        button_y.place(x=1283, y=95)
        button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#724a24"))
        button_o = Button(self.WIN, bg="#f98cb9")
        button_o.place(x=1365, y=95)
        button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#f98cb9"))
        button_p = Button(self.WIN, bg="#d2b48c")
        button_p.place(x=1447, y=95)
        button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#d2b48c"))
        #wbg
        button_w = Button(self.WIN, bg="#ffffff")
        button_w.place(x=1283, y=140)
        button_w.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ffffff"))
        button_blk = Button(self.WIN, bg="#000000000")
        button_blk.place(x=1365, y=140)
        button_blk.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#000000000"))
        button_gry = Button(self.WIN, bg="#808080")
        button_gry.place(x=1447, y=140)
        button_gry.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#808080"))


    def draw_menu(self):    #Creaza butoanele din meniu
        file_menu: Menu = Menu(self.menu)
        tool_menu: Menu = Menu(self.menu)
        filter_menu: Menu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New          Ctrl+N', command=self.new_file)
        file_menu.add_command(label='Open...      Ctrl+O', command=self.open_image)
        file_menu.add_command(label='Save As...   Ctrl+S', command = lambda: self.save_image_as(0))
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.WIN.quit)

        self.menu.add_cascade(label='Tools', menu=tool_menu)
        tool_menu.add_cascade(label='Brush Shape', menu=self.bs_sub_menu)
        self.bs_sub_menu.add_command(label='Ellipse', command= lambda: self.pick_shape("ellipse"))
        self.bs_sub_menu.add_command(label='Rectangle', command= lambda: self.pick_shape("rectangle"))
        self.bs_sub_menu.add_command(label='Pen', command= lambda: self.pick_shape("pen"))

        tool_menu.add_cascade(label="Shapes", menu=self.sp_sub_menu)
        self.sp_sub_menu.add_command(label='Rectangle', command = lambda: self.set_type("rectangle"))
        self.sp_sub_menu.add_command(label='Ellipse', command = lambda: self.set_type("ellipse"))
        self.sp_sub_menu.add_command(label='Line', command = lambda: self.set_type("line"))

        self.menu.add_cascade(label='Filters', menu=filter_menu)
        filter_menu.add_command(label='Grayscale', command= lambda: self.filter("grs"))
        filter_menu.add_command(label='Black and White', command= lambda: self.filter("bnw"))
        filter_menu.add_command(label='RGB', command= lambda: self.filter(None))
        filter_menu.add_command(label='Underexpose', command= lambda: self.filter("uex"))
        filter_menu.add_command(label='Overexpose', command= lambda: self.filter("oex"))
        filter_menu.add_command(label='Sharpen', command= lambda: self.filter("spn"))
        filter_menu.add_command(label='Smoothen', command= lambda: self.filter("SMOOTH"))
        filter_menu.add_command(label='Blur', command= lambda: self.filter("BLUR"))
        filter_menu.add_command(label='Contour', command= lambda: self.filter("CONTOUR"))
        filter_menu.add_command(label='Detail', command= lambda: self.filter("DETAIL"))
        filter_menu.add_command(label='Edge Enhance', command= lambda: self.filter("EDGE"))

        self.menu.add_cascade(label='Achievements', command= lambda: self.open_achievement_window())
        self.menu.add_cascade(label='Competition', command= lambda: self.competition())


    def draw_label(self):   #Text + Notes
        label_test_clr = Label(self.WIN, text="Compare Colors", font=("Arial", 16, "bold"), fg="black", bg="white")
        label_test_clr.place(x=1310, y=370)
        label_notes = Label(self.WIN, text="Notes", font=("Arial", 16, "bold"), fg="black", bg="white")
        label_notes.place(x=95, y=370)
        notes = Text(self.WIN, width=30, height=19, bg="grey94")
        notes.place(x=10, y=400)
    
    def competition(self):
        if self.achievements['ach_6'] == 0:
            self.achievements['ach_6'] = 1
            self.handle_achievements(1)
        CON = Tk()
        competition = Competition(CON)
        CON.mainloop()


    def on_closing(self):
        self.CLS = Tk()
        self.CLS.title("Quit? ")
        label = Label(self.CLS, text="Do you want to quit?")
        label.grid(row=0, column= 1)
        cancel = Button(self.CLS, text="Cancel", command= lambda: self.CLS.destroy())
        cancel.grid(row=1, column=0)
        save = Button(self.CLS, text="Save & Quit", command= lambda: self.save_image_as(1))
        save.grid(row=1, column=1)
        quit = Button(self.CLS, text="Quit", command= lambda: self.quit_app())
        quit.grid(row=1, column=2)

        self.handle_achievements(1)

    def quit_app(self):
            self.WIN.destroy()
            self.CLS.destroy()      

class Competition:
    def __init__(self, root):
        self.COM = root
        self.COM.title("Drawing Competition")
        
        self.player_left = Canvas(root, width=500, height=500, bg='white')
        self.player_left.grid(row=1, column=0)
        self.player_right = Canvas(root, width=500, height=500, bg='white')
        self.player_right.grid(row=1, column=1)
        self.challenges = ["a cat", "a dog", "a bird", "a house", "a tree", "each other", "a cow", "a landscape", "an apple", "a bottle", "a bowl", "a space ship", "a flower", "a river"]
        
        self.x0, self.y0 = 250, 250 
        self.x1, self.y1 = 250, 250 
        self.line_width = 3

        self.button_draw = Button(root, width=70, height=1, text="Draw: ", command= self.suggestion)
        self.button_draw.grid(row=0, column=0)

        self.entry_suggestion = Entry(root, width=70)
        self.entry_suggestion.grid(row=0, column=1)

        self.player_left.create_oval(self.x0-2, self.y0-2, self.x0+2, self.y0+2, fill='blue')
        self.player_right.create_oval(self.x1-2, self.y1-2, self.x1+2, self.y1+2, fill='red')
        
        self.key_state_left = {'w': False, 'a': False, 's': False, 'd': False}
        self.key_state_right = {'Up': False, 'Left': False, 'Down': False, 'Right': False}

        self.COM.bind('<KeyPress>', self.key_press)
        self.COM.bind('<KeyRelease>', self.key_release)
        
        self.update()

    def key_press(self, event):
        if event.char in self.key_state_left:
            self.key_state_left[event.char] = True
        elif event.keysym in self.key_state_right:
            self.key_state_right[event.keysym] = True
    
    def key_release(self, event):
        if event.char in self.key_state_left:
            self.key_state_left[event.char] = False
        elif event.keysym in self.key_state_right:
            self.key_state_right[event.keysym] = False

    def update(self):
        move_mapping_wasd = {
            'w': (0, -5),
            'a': (-5, 0),
            's': (0, 5),
            'd': (5, 0)
        }

        move_mapping_arrow = {
            'Up': (0, -5),
            'Left': (-5, 0),
            'Down': (0, 5),
            'Right': (5, 0)
        }

        for key, pressed in self.key_state_left.items():
            if pressed:
                dx, dy = move_mapping_wasd[key]
                self.player_left.create_rectangle(self.x0, self.y0, self.x0 + dx, self.y0 + dy, width=self.line_width, fill="blue", outline="blue")
                self.x0 += dx
                self.y0 += dy
        for key, pressed in self.key_state_right.items():
            if pressed:
                dx, dy = move_mapping_arrow[key]
                self.player_right.create_rectangle(self.x1, self.y1, self.x1 + dx, self.y1 + dy, width=self.line_width, fill="red", outline="red")
                self.x1 += dx
                self.y1 += dy
        self.COM.after(50, self.update)

    def suggestion(self):
        challenge = random.choice(self.challenges)
        self.entry_suggestion.delete(0, END)
        self.entry_suggestion.insert(0, challenge)
        self.player_left.delete(ALL)
        self.player_right.delete(ALL)
        self.x0, self.y0 = 250, 250 
        self.x1, self.y1 = 250, 250 

app : App = App()
#Eventuri
app.CVS.bind( "<B1-Motion>", app.paint )
app.CVS.bind( "<Button-1>", app.paint )
app.CVS.bind( "<ButtonRelease-1>", app.release )
app.CVS.pack()

app.CLR.bind( "<Button-1>", app.clr_test )
app.WIN.bind( "<KeyPress>", app.on_key_press )

app.draw_label()
app.draw_menu()
app.draw_buttons()
app.handle_achievements(0)
app.handle_achievements(2)
app.WIN.protocol('WM_DELETE_WINDOW', app.on_closing)
mainloop()