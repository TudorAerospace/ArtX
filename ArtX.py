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
        self.CLS = None
        self.WIN_BTR = None
        self.NFW = None

        self.closing: bool = False
        self.compare_colors_open: bool = False
        self.buttons_right_open: bool = False
        self.main_focus: bool = True
        self.secondary_focus: bool = False

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

        self.canvas_name: str = "canvas"
        self.image_states = [("rectangle0", 2, 2, 1001, 717, "rectangle", "#ffffff", ImageColor.getrgb("white"))]

        self.bkgr_clr: str = "#ffffff"
        self.image = Image.new("RGB", (1000, 720), "#ffffff")
        self.image_backup = None
        self.draw = ImageDraw.Draw(self.image)

        self.brush_size: int = 10
        self.brush_shape: str = "ellipse"
        self.brush_type: str = "brush"
        self.entry_suggestion: Entry = Entry(self.WIN, width=40)
        self.entry_suggestion.place(x=10, y=350)

        self.CVS_width_default: int = 1000
        self.CVS_height_default: int = 720
        self.CVS_width: int = 1000
        self.CVS_height: int = 720
        self.CVS_width_extended: int = 1260
        self.CVS_height_extended: int = 720

        self.x_deviation = 0
        self.y_deviation = 0

        self.CVS = Canvas(self.WIN, width= self.CVS_width_default, height=self.CVS_height_default)
        self.CVS.create_rectangle(2, 2, self.CVS_width_default, self.CVS_height_default-3, fill="#ffffff", outline="#000000")
        self.CVS.config(cursor="pencil")

        self.first_click: bool = False
        self.first_click_2: bool = False

        self.menu = Menu(self.WIN)
        self.WIN.config(menu=self.menu)
        self.bs_sub_menu = Menu(self.menu, tearoff=0)
        self.sp_sub_menu = Menu(self.menu, tearoff=0)
        self.ct_sub_menu = Menu(self.menu, tearoff=0)

        self.filter_type: str = None
        self.brightness_factor: float = 1.0

        self.rect_num = 1
        self.ellipse_num = 0
        self.line_num = 0
        self.triangle_num = 0
        self.bg_num = 0
        self.brush_num = 0
        self.filter_num = 0
        self.colour_num = 0

        self.artx_directory = os.path.abspath(__file__)
        self.path = self.artx_directory.replace('ArtX.py', 'Assets\\rectangle.png')
        self.artx_directory = self.artx_directory.replace('ArtX.py', '')

        self.CVS.bind( "<B1-Motion>", self.paint )
        self.CVS.bind( "<Button-1>", self.paint )
        self.CVS.bind( "<Button-3>", self.cancel )
        self.CVS.bind( "<ButtonRelease-1>", self.release )
        self.CVS.bind( "<Motion>", self.update_mouse_position)
        self.CVS.pack()
        self.WIN.bind( "<Unmap>", self.on_minimize)
        self.WIN.bind( "<Map>", self.on_restore)

        image_names = [
    'rectangle.png', 'picker.png', 'ellipse.png', 'line.png', 'triangle.png',
    'pick_clr.png', 'check.png', 'eraser.png', 'brush.png', 'bucket.png',
    'lighten.png', 'darken.png', 'icon.png', 'trophy.png', 'zoom_out.png', 'load_text.png', 
    'save_text.png','zoom_in.png', 'draw.png', 'achievement_1_inc.png', 'achievement_1_com.png',
    'achievement_2_inc.png', 'achievement_2_com.png', 'achievement_3_inc.png',
    'achievement_3_com.png', 'achievement_4_inc.png', 'achievement_4_com.png',
    'achievement_5_com.png', 'achievement_5_inc.png', 'achievement_6_com.png',
    'achievement_6_inc.png', 'achievement_7_com.png', 'achievement_7_inc.png',
    'achievement_8_com.png', 'achievement_8_inc.png']
        photos = {}

        for name in image_names:
            var_name = name 
            path = self.path.replace('rectangle.png', name)
            photos[var_name] = PhotoImage(file=path)

        for attr in image_names:
            attr2 = attr.replace('.png', '')
            setattr(self, f'photo_{attr2}', photos[f'{attr}'])

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
        self.ach_7_complete = False
        self.ach_7_complete_shown = False
        self.ach_8_complete = False
        self.ach_8_complete_shown = False

    def on_minimize(self, event):
        if event.widget == self.WIN:
            self.cc_close()
            self.br_close()

    def on_restore(self, event):
        if event.widget == self.WIN:
            self.draw_buttons_right()
            self.compare_colors()
        
    def create_mark(self, x0, y0, x1, y1):
        self.CVS.delete("mark1")
        self.CVS.create_line(x0, y0, x1, y1, fill="blue", tags="mark1", width=2)
        self.CVS.create_line(x0 + 15, y0, x1 - 15, y1, fill="blue" , tags="mark1", width=2)
        self.CVS.create_line(x0 + 7.5, y0 + 7.5, self.x2, self.y2, fill="blue" if self.brush_type != "line" else self.Colour, tags="mark1", width=2 if self.brush_type != "line" else 5, dash= (4, 20))
        if self.brush_type != "line":
            self.CVS.create_line(x0 + 7.5, self.y2, self.x2, y0 + 7.5, fill="blue" if self.brush_type != "line" else self.Colour, tags="mark1", width=2, dash= (4, 20))
        if self.brush_type == "triangle":
            self.CVS.create_line(x0 + 7.5, y0 + 7.5, self.x2 - (self.x2 - x0)//2, self.y2, fill=self.Colour, tags="mark1", width=5, dash= (4, 20))
            self.CVS.create_line(self.x2, y0 + 7.5, self.x2 - (self.x2 - x0)//2, self.y2, fill=self.Colour, tags="mark1", width=5, dash= (4, 20))
        self.CVS.create_line(x0 + 7.5, y0 + 7.5, x0 + 7.5, self.y2, fill="blue"  if self.brush_type != "rectangle" else self.Colour, tags="mark1", width=2 if self.brush_type != "rectangle" else 5, dash= (4, 20))
        self.CVS.create_line(x0 + 7.5, y0 + 7.5, self.x2, y0 + 7.5, fill="blue" if self.brush_type != "rectangle" and self.brush_type != "triangle" else self.Colour, tags="mark1", width=5 if self.brush_type in ["triangle", "rectangle"] else 2, dash= (4, 20))
        self.CVS.create_line(self.x2, y0 + 7.5, self.x2, self.y2, fill="blue" if self.brush_type != "rectangle" else self.Colour, tags="mark1", width=2 if self.brush_type != "rectangle" else 5, dash= (4, 20))
        self.CVS.create_line(x0 + 7.5,  self.y2, self.x2, self.y2, fill="blue" if self.brush_type != "rectangle" else self.Colour, tags="mark1", width=2 if self.brush_type != "rectangle" else 5, dash= (4, 20))
        if self.brush_type == "ellipse":
            self.CVS.create_oval(x0 + 7.5, y0 + 7.5 , self.x2, self.y2,outline= self.Colour, tags="mark1", width=4)

    def update_marks(self, x0, y0, x1, y1):
        self.create_mark(x0, y0, x1, y1)
        self.update_mark_id = self.CVS.after(25, self.update_marks, x0, y0, x1, y1)

    def cancel_update_marks(self):
        if hasattr(self, 'update_mark_id'):
            self.CVS.after_cancel(self.update_mark_id)
            self.CVS.delete("mark1")

    def paint(self, event):
        if self.brush_type == "brush" or self.brush_type == "eraser":
            self.x0, self.y0, self.x1, self.y1 = (event.x - self.brush_size / 2), (event.y - self.brush_size / 2), (event.x + self.brush_size / 2), (event.y + self.brush_size / 2)
            if self.brush_shape == "ellipse":
                self.CVS.create_oval(self.x0, self.y0, self.x1, self.y1, fill=self.Colour, outline=self.Colour, tags=f"brush{self.brush_num}")
                self.draw.ellipse([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, outline=self.Colour2)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "ellipse", self.Colour, self.Colour2))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
            elif self.brush_shape == "rectangle":
                self.CVS.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.Colour, outline=self.Colour, tags=f"brush{self.brush_num}")
                self.draw.rectangle([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, outline=self.Colour2)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "rectangle", self.Colour, self.Colour2))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
            elif self.brush_shape == "pen":
                self.x0, self.y0, self.x1, self.y1 = (event.x), (event.y), (event.x + self.brush_size), (event.y + self.brush_size)
                self.CVS.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.Colour, tags=f"brush{self.brush_num}", width=self.brush_size)
                self.draw.line([self.x0, self.y0, self.x1, self.y1], fill=self.Colour2, width=self.brush_size)
                self.image_states.append((f"brush{self.brush_num}", self.x0, self.y0, self.x1, self.y1, "line", (self.Colour, self.Colour2), self.brush_size))
                self.x0, self.y0, self.x1, self.y1 = None, None, None, None
        elif self.brush_type == "picker":
            x, y = event.x, event.y
            rgb_color = self.image.getpixel((x, y))
            self.Colour = "#%02x%02x%02x" % rgb_color
            self.Colour2 = ImageColor.getrgb(self.Colour)
        else:
            if self.x0 is None and self.y0 is None:
                self.x0, self.y0 = event.x, event.y
                self.update_marks(self.x0 - 7.5, self.y0 - 7.5, self.x0 + 7.5, self.y0 + 7.5)
                self.disable_click()
                self.CVS.after(400, self.enable_click)
            elif self.x1 is None and self.y1 is None:
                self.x1, self.y1 = event.x, event.y
                self.cancel_update_marks()
                try:
                    if self.brush_type == "rectangle":
                        if self.x1 < self.x0:
                            self.x0, self.x1 = self.x1, self.x0
                        if self.y1 < self.y0:
                            self.y0, self.y1 = self.y1, self.y0
                        self.create_rectangle(self.x0, self.y0, self.x1, self.y1)
                        self.x0, self.y0, self.x1, self.y1 = None, None, None, None
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
                        self.x0, self.y0, self.x1, self.y1 = None, None, None, None
                        self.disable_click()
                        self.CVS.after(400, self.enable_click)
                    elif self.brush_type == "triangle":
                        if self.x1 < self.x0:
                            self.x0, self.x1 = self.x1, self.x0
                        if self.y1 > self.y0:
                            self.y0, self.y1 = self.y1, self.y0
                            self.create_triangle(self.x1, self.y1, self.x1 - (self.x1 - self.x0)//2, self.y0, self.x0, self.y1)
                        else:
                            self.create_triangle(self.x0, self.y0, self.x1 - (self.x1 - self.x0)//2, self.y1, self.x1, self.y0)
                        self.x0, self.y0, self.x1, self.y1 = None, None, None, None
                        self.CVS.after(400, self.enable_click)
                    self.achievements['ach_2'] += 0.5
                    self.handle_achievements(1)
                except TypeError:
                    print("ERROR")
                    print(self.x0, self.x1, self.y0, self.y1)
                    pass
        if self.achievements['ach_1'] == 0:
            self.achievements['ach_1'] = 1
            self.handle_achievements(1)

    def update_mouse_position(self, event):
        self.x2, self.y2 = event.x, event.y

    def cancel(self, event=None):
        self.x0, self.y0 = None, None
        self.cancel_update_marks()

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

    def create_triangle(self, x0, y0, x1, y1, x2, y2):
        tag = f"triangle{self.triangle_num}"
        vertices = [x0, y0, x1, y1, x2, y2]
        self.triangle_num += 1
        self.image_states.append((tag, vertices, None, None, None, "triangle", self.Colour, self.Colour2))
        self.CVS.create_polygon(vertices, outline=self.Colour, fill=self.Colour, width=2, tag=tag)
        self.draw.polygon([(x0, y0), (x1, y1), (x2, y2)], outline=self.Colour2, fill=self.Colour2)

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
                    self.image = self.image_backup.copy()  # Restore the backup image
                    self.draw = ImageDraw.Draw(self.image)
                    self.tk_image = ImageTk.PhotoImage(self.image)
                    self.CVS.config(height=self.image.height, width=self.image.width)
                    self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
                    self.CVS.image = self.tk_image
                    self.CVS_width, self.CVS_height = self.image.width, self.image.height
                elif shape_type == "rectangle":
                    self.CVS.create_rectangle(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                    self.draw.rectangle([x0, y0, x1, y1], fill=clr2, outline=clr2)
                elif shape_type == "ellipse":
                    self.CVS.create_oval(x0, y0, x1, y1, fill=clr, outline=clr, tags=tag)
                    self.draw.ellipse([x0, y0, x1, y1], fill=clr2, outline=clr2)
                elif shape_type == "triangle":
                    self.CVS.create_polygon(x0, fill=clr, outline=clr, tags=tag)
                    self.draw.polygon([(x0[0], x0[1]), (x0[2], x0[3]), (x0[4], x0[5])], outline=clr2, fill=clr2)
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
            self.open_new_file_window()
        elif event.state == 4 and event.keysym == 'o':
            self.open_image()
        elif event.state == 4 and event.keysym == 'p':
            self.pick_color()
        elif event.state == 4 and event.keysym == 's':
            self.save_image_as(0)
        elif event.state == 4 and event.keysym == 'z':
            self.revert_state()
        elif event.state == 4 and event.keysym == 'e':
            self.extend_canvas()
        
    def release(self, event=None):
        if self.brush_type == "brush" or self.brush_type == "eraser":
            self.image_states.append(f"brush{self.brush_num}")
            self.brush_num += 1

    def display_image(self, file_path):   #Incarca imaginea aleasa in open_image
        self.image_states = []
        loaded_image = Image.open(file_path)
        while loaded_image.width > self.CVS_width_default or loaded_image.height > self.CVS_height_default:
            loaded_image = loaded_image.resize((loaded_image.width - loaded_image.width // 10, loaded_image.height - loaded_image.height // 10))
        
        self.image = loaded_image
        self.image_backup = loaded_image.copy()  # Create a deep copy of the image
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = ImageTk.PhotoImage(loaded_image)
        self.CVS.config(height=self.image.height, width=self.image.width)
        self.CVS.delete(ALL)
        self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
        self.CVS.image = self.tk_image
        self.CVS_width, self.CVS_height = self.image.width, self.image.height
        self.image_states.append(("image", None, None, None, None, None, None, None))

    def handle_zoom(self, _type):
            zoomed_image = self.image.copy()
            if _type == 0:
               zoomed_image = self.image.resize((zoomed_image.width - zoomed_image.width // 10, zoomed_image.height - zoomed_image.height // 10))
               self.image = zoomed_image
            if _type == 1:
                if zoomed_image.width + zoomed_image.width // 10 < self.CVS_width_default and zoomed_image.height + zoomed_image.height // 10 < self.CVS_height_default:
                    zoomed_image = self.image.resize((zoomed_image.width + zoomed_image.width // 10, zoomed_image.height + zoomed_image.height // 10))
                    self.image = zoomed_image
            self.image_backup = zoomed_image.copy()  # Create a deep copy of the image
            self.draw = ImageDraw.Draw(self.image)
            self.tk_image = ImageTk.PhotoImage(zoomed_image)
            self.CVS.config(height=self.image.height, width=self.image.width)
            self.CVS.delete(ALL)
            self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
            self.CVS.image = self.tk_image
            self.CVS_width, self.CVS_height = self.image.width, self.image.height
            self.image_states.append(("image", None, None, None, None, None, None, None))

    def extend_canvas(self):
        if self.CVS_height < self.CVS_height_default and self.CVS_width < self.CVS_width_default:
            self.CVS_height = self.CVS_height_default
            self.CVS_width = self.CVS_width_default
            self.CVS.config(height=self.CVS_height, width=self.CVS_width)

            extended_image = Image.new('RGB', (self.CVS_width, self.CVS_height), (255, 255, 255))
            extended_image.paste(self.image, (0, 0))
            
            self.image = extended_image.copy()
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.CVS.delete(ALL)
            self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
            self.CVS.image = self.tk_image
            self.draw = ImageDraw.Draw(self.image)
            self.image_backup = self.image.copy()
        elif self.CVS_height >= self.CVS_height_default or self.CVS_width >= self.CVS_width_default:
            self.CVS_height = self.CVS_height_extended
            self.CVS_width = self.CVS_width_extended
            self.CVS.config(height=self.CVS_height, width=self.CVS_width)
            self.CVS.place(x=self.width-1280, y=0)

            extended_image = Image.new('RGB', (self.CVS_width, self.CVS_height), (255, 255, 255))
            extended_image.paste(self.image, (0, 0))
            
            self.image = extended_image.copy()
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.CVS.delete(ALL)
            self.CVS.create_image(0, 0, anchor=NW, image=self.tk_image)
            self.CVS.image = self.tk_image
            self.draw = ImageDraw.Draw(self.image)
            self.image_backup = self.image.copy()
            self.x_deviation = 250

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
        if self.achievements['ach_8'] == 0:
            self.achievements['ach_8'] = 1
            self.handle_achievements(1)
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

        achievements_status = [self.ach_1_complete, self.ach_2_complete,self.ach_3_complete, self.ach_4_complete, self.ach_5_complete, self.ach_6_complete, self.ach_7_complete, self.ach_8_complete]

        achievements_images_inc = [self.photo_achievement_1_inc, self.photo_achievement_2_inc, self.photo_achievement_3_inc, self.photo_achievement_4_inc, self.photo_achievement_5_inc, self.photo_achievement_6_inc, self.photo_achievement_7_inc, self.photo_achievement_8_inc]

        achievements_images_com = [self.photo_achievement_1_com, self.photo_achievement_2_com, self.photo_achievement_3_com, self.photo_achievement_4_com, self.photo_achievement_5_com, self.photo_achievement_6_com, self.photo_achievement_7_com, self.photo_achievement_8_com]

        for i in range(0, 8):
            image = achievements_images_com[i] if achievements_status[i] else achievements_images_inc[i]
            button = Button(frame, command=lambda: self.handle_achievements(0), image=image)
            button.config(width=470, height=80)
            button.grid(row=i if i < 2 else i + 1, column=0, pady=5)

        frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        except:
            pass

    def open_new_file_window(self):
        if not self.first_click_2:
            self.NFW = Toplevel()
            self.NFW.attributes('-topmost', True)
            self.NFW.resizable(False, False)
            self.NFW.title("New")
            self.NFW.protocol('WM_DELETE_WINDOW', self.cancel_create_new)
            x = self.WIN.winfo_x()
            y = self.WIN.winfo_y()
            self.NFW.geometry(f"+{x + 640}+{y + 210}")

            label_pxl_size = Label(self.NFW, text="Pixel size:")
            label_pxl_size.grid(column=0, row=0, pady=5)

            label_width = Label(self.NFW, text="Width: ")
            label_width.grid(column=0, row=1, pady=5)
            
            label_height = Label(self.NFW, text="Height: ")
            label_height.grid(column=0, row=2, pady=5)

            spinbox_width = Spinbox(self.NFW, from_=1, to=1000)
            spinbox_width.grid(column=1, row=1)

            spinbox_height = Spinbox(self.NFW, from_=1, to=720)
            spinbox_height.grid(column=1, row=2)

            label_pxl_0 = Label(self.NFW, text="pixels")
            label_pxl_0.grid(column=2, row=1)

            label_pxl_1 = Label(self.NFW, text="pixels")
            label_pxl_1.grid(column=2, row=2)

            button_confirm = Button(self.NFW, text="OK", command=lambda: self.new_file(int(spinbox_width.get()), int(spinbox_height.get())))
            button_confirm.grid(column=1, row=3)
            button_confirm.config(width=10)

            button_cancel = Button(self.NFW, text="Cancel", command=self.cancel_create_new)
            button_cancel.grid(column=2, row=3)
            button_cancel.config(width=7)

            spinbox_width.bind("<FocusOut>", lambda event: self.validate_spinbox_value(spinbox_width, 1270))
            spinbox_height.bind("<FocusOut>", lambda event: self.validate_spinbox_value(spinbox_height, 720))

            self.first_click_2 = True

    def new_file(self, width, height): #Acelasi lucru dar da fill cu alb (si face un canvas nou in Pillow)
            if width > 1260:
                width = 1260
            if height > 720:
                height = 720
            self.CVS.config(height=height, width=width)
            self.CVS.create_rectangle(2, 2, width, height, fill = "#ffffff", outline="#000000")
            self.image = Image.new("RGB", (width, height), "#ffffff")
            self.draw = ImageDraw.Draw(self.image)
            self.CVS_width = width
            self.CVS_height = height
            self.image_states = []
            self.NFW.destroy()
            self.first_click_2 = False
            if width <= 1000:
                self.x_deviation = 0
            else:
                self.x_deviation = width - 1000
                self.CVS.place(x=self.width-1300 + self.x_deviation//7, y=0)
            self.y_deviation = 0

    def validate_spinbox_value(self, spinbox, max_value):
        value = spinbox.get()
        if value.isdigit() and int(value) > max_value:
            spinbox.delete(0, 'end')
            spinbox.insert(0, max_value)

    def cancel_create_new(self):
        self.NFW.destroy()
        self.first_click_2 = False

    def handle_notes(self, action):
        appdata_dir = os.getenv('APPDATA')
        shelf_dir = os.path.join(appdata_dir, "ArtX")
        os.makedirs(shelf_dir, exist_ok=True)
        shelf_path = os.path.join(shelf_dir, "notes")
        if action == 0: # load
            with shelve.open(shelf_path) as shelf:
                notes = shelf.get('notes', '')
                self.notes_text.delete(1.0, "end")
                self.notes_text.insert("end", notes)
        elif action == 1:  # save
            with shelve.open(shelf_path) as shelf:
                notes = self.notes_text.get(1.0, "end").strip()
                shelf['notes'] = notes
            if self.achievements['ach_7'] == 0:
                self.achievements['ach_7'] = 1
                self.handle_achievements(1)

    def draw_label(self):   # Text + Notes
        label_notes = Label(self.WIN, text="📋Notes", font=("Arial", 16, "bold"), fg="black", bg="white")
        label_notes.place(x=95, y=370)
        self.notes_text = Text(self.WIN, width=30, height=17, bg="grey94")
        self.notes_text.place(x=10, y=400)
        self.handle_notes(0)
        load_button = Button(self.WIN, image=self.photo_load_text, command=lambda: self.handle_notes(0))
        load_button.place(x=10, y=680)
        load_button.config(width=110)
        save_button = Button(self.WIN, image=self.photo_save_text, command=lambda: self.handle_notes(1))
        save_button.place(x=135, y=680)
        save_button.config(width=110)

    def handle_achievements(self, action):
        appdata_dir = os.getenv('APPDATA')
        
        shelf_dir = os.path.join(appdata_dir, "ArtX")
        os.makedirs(shelf_dir, exist_ok=True)
        shelf_path = os.path.join(shelf_dir, "achievement_progress")

        if action == 0:
            with shelve.open(shelf_path) as db:
                self.achievements = db.get('achievements', {'ach_1': 0, 'ach_2': 0, 'ach_3': 0, 'ach_4': 0, 'ach_6': 0, 'ach_7': 0, 'ach_8': 0})

            if self.achievements['ach_1'] == 1:
                self.ach_1_complete_shown = True
            if self.achievements['ach_2'] >= 100:
                self.ach_2_complete_shown = True
            if self.achievements['ach_3'] >= 3600:
                self.ach_3_complete_shown = True
            if self.achievements['ach_4'] >= 20:
                self.ach_4_complete_shown = True
            if self.achievements['ach_2'] >= 500:
                self.ach_5_complete_shown = True
            if self.achievements['ach_6'] == 1:
                self.ach_6_complete_shown = True
            if self.achievements['ach_7'] == 1:
                self.ach_7_complete_shown = True        
            if self.achievements['ach_8'] == 1:
                self.ach_8_complete_shown = True
            print(self.achievements)
        
        if action == 1:
            self.end_time = time.time()
            self.achievements['ach_3'] = int(self.end_time - self.start_time)
            self.start_time = time.time()
            with shelve.open(shelf_path) as db:
                db['achievements'] = self.achievements
            self.handle_achievements(2)

        if action == 2:
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
            if self.achievements['ach_7'] == 1:
                self.ach_7_complete = True
                self.achievement_notification(7)
                self.ach_7_complete_shown = True            
            if self.achievements['ach_8'] == 1:
                self.ach_8_complete = True
                self.achievement_notification(8)
                self.ach_8_complete_shown = True
            
    def achievement_notification(self, action):
        achievements_complete_shown = [self.ach_1_complete_shown, self.ach_2_complete_shown, self.ach_3_complete_shown, self.ach_4_complete_shown, self.ach_5_complete_shown, self.ach_6_complete_shown, self.ach_7_complete_shown, self.ach_8_complete_shown]
        if action in range(1, 10) and not achievements_complete_shown[action - 1]:
            ACH_N = Toplevel(self.WIN)
            ACH_N.title("Achievement Got!")
            ACH_N.geometry("500x100")
            ACH_N.attributes('-topmost', True)
            ACH_N.resizable(False, False)
            ACH_N.iconphoto(False, self.photo_trophy)
            achievements_complete_shown = [self.ach_1_complete_shown, self.ach_2_complete_shown, self.ach_3_complete_shown, self.ach_4_complete_shown, self.ach_5_complete_shown, self.ach_6_complete_shown, self.ach_7_complete_shown, self.ach_8_complete_shown]
            achievements_images_com = [self.photo_achievement_1_com, self.photo_achievement_2_com, self.photo_achievement_3_com, self.photo_achievement_4_com, self.photo_achievement_5_com, self.photo_achievement_6_com, self.photo_achievement_7_com, self.photo_achievement_8_com]
            image = None
            if action in range(1, 10) and not achievements_complete_shown[action - 1]:
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
        spinbox_brush_size.place(x=2, y = 5, height=27)
        #confirma marimea 
        button_check = Button(self.WIN, image=self.photo_check)
        button_check.place(x=50, y=5)                                                                   #Foloseste lambda ca sa dea call la functie doar cand apesi pe buton
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
        button_suggestion = Button(self.WIN, image=self.photo_draw)
        button_suggestion.place(x=10, y=300)
        button_suggestion.config(width=73, height=35, cursor="hand2", command = self.get_idea)
        #dreptunghi
        button_rectangle = Button(self.WIN, image = self.photo_rectangle, compound = LEFT)
        button_rectangle.place(x=5, y=35)
        button_rectangle.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("rectangle"))
        #elipsa
        button_ellipse = Button(self.WIN, image = self.photo_ellipse, compound = LEFT)
        button_ellipse.place(x=90, y=35)
        button_ellipse.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("ellipse"))
        #triangle
        button_triangle = Button(self.WIN, image = self.photo_triangle, compound = LEFT)
        button_triangle.place(x=175, y=35)
        button_triangle.config(width=73, height=36, cursor="hand2", command = lambda: self.set_type("triangle"))
        #linie
        button_line = Button(self.WIN, image = self.photo_line, compound = LEFT)
        button_line.place(x=175, y=85)
        button_line.config(width=73, height=14, cursor="hand2", command = lambda: self.set_type("line"))
        #darken
        button_darken = Button(self.WIN, image = self.photo_darken, compound = LEFT)
        button_darken.place(x=5, y=85)
        button_darken.config(width=73, height=36, cursor="hand2", command = lambda: self.brightness(0))
        #lighten
        button_lighten = Button(self.WIN, image = self.photo_lighten, compound = LEFT)
        button_lighten.place(x=90, y=85)
        button_lighten.config(width=73, height=36, cursor="hand2", command = lambda: self.brightness(1))
        #pick
        button_picker = Button(self.WIN, image = self.photo_picker, compound = LEFT)
        button_picker.place(x=175, y=107)
        button_picker.config(width=73, height=14, cursor="hand2", command = lambda: self.set_type("picker"))
        #zoom out
        button_zoom_out = Button(self.WIN, image = self.photo_zoom_out, compound = LEFT)
        button_zoom_out .place(x=5, y=135)
        button_zoom_out .config(width=73, height=36, cursor="hand2", command = lambda: self.handle_zoom(0))
        #zoom in
        button_zoom_in = Button(self.WIN, image = self.photo_zoom_in, compound = LEFT)
        button_zoom_in.place(x=90, y=135)
        button_zoom_in.config(width=73, height=36, cursor="hand2", command = lambda: self.handle_zoom(1))
        
    def draw_buttons_right(self):
        if self.buttons_right_open == False:
            self.buttons_right_open = True
            self.WIN_BTR = Toplevel()
            self.WIN_BTR.attributes('-topmost', True)
            self.WIN_BTR.title("Color")
            self.WIN_BTR.resizable(False, False)
            self.WIN_BTR.geometry("255x230")
            self.update_window_position()
            self.WIN.bind("<Configure>", lambda event: self.update_window_position())
            self.WIN_BTR.protocol('WM_DELETE_WINDOW', self.br_close)
            #butoane dreapta
            #clr/bgr
            button_pick = Button(self.WIN_BTR, image=self.photo_pick_clr)
            button_pick.place(x=5, y=185)
            button_pick.config(width=120, height=36, cursor="hand2", command = self.pick_color)
            color_button = Button(self.WIN_BTR, image=self.photo_bucket)
            color_button.place(x=134, y=185)
            color_button.config(width=110, height=36, cursor="hand2", command = self.paint_background)
            #rgb
            button_r = Button(self.WIN_BTR,bg="#ff0000")
            button_r.place(x=5, y=5)
            button_r.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ff0000"))
            button_g = Button(self.WIN_BTR, bg="#228b22")
            button_g.place(x=87, y=5)
            button_g.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#228b22"))
            button_b = Button(self.WIN_BTR, bg="#00008b")
            button_b.place(x=169, y=5)
            button_b.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#00008b"))
            #yop
            button_y = Button(self.WIN_BTR, bg="#e6cc00")
            button_y.place(x=5, y=50)
            button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#e6cc00"))
            button_o = Button(self.WIN_BTR, bg="#fca510")
            button_o.place(x=87, y=50)
            button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#fca510"))
            button_p = Button(self.WIN_BTR, bg="#8a00c2")
            button_p.place(x=169, y=50)
            button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#8a00c2"))
            #bpb
            button_y = Button(self.WIN_BTR, bg="#724a24")
            button_y.place(x=5, y=95)
            button_y.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#724a24"))
            button_o = Button(self.WIN_BTR, bg="#f98cb9")
            button_o.place(x=87, y=95)
            button_o.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#f98cb9"))
            button_p = Button(self.WIN_BTR, bg="#d2b48c")
            button_p.place(x=169, y=95)
            button_p.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#d2b48c"))
            #wbg
            button_w = Button(self.WIN_BTR, bg="#ffffff")
            button_w.place(x=5, y=140)
            button_w.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#ffffff"))
            button_blk = Button(self.WIN_BTR, bg="#000000000")
            button_blk.place(x=87, y=140)
            button_blk.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#000000000"))
            button_gry = Button(self.WIN_BTR, bg="#808080")
            button_gry.place(x=169, y=140)
            button_gry.config(width=10, height=2, cursor="hand2", command = lambda: self.assign_colour("#808080"))

    def draw_menu(self):    #Creaza butoanele din meniu
        file_menu: Menu = Menu(self.menu)
        tool_menu: Menu = Menu(self.menu)
        filter_menu: Menu = Menu(self.menu)
        self.menu.add_cascade(label='📄 File', menu=file_menu)
        file_menu.add_command(label='🗒 New          Ctrl+N', command=self.open_new_file_window)
        file_menu.add_command(label='📂 Open...      Ctrl+O', command=self.open_image)
        file_menu.add_command(label='💾 Save As...   Ctrl+S', command = lambda: self.save_image_as(0))
        file_menu.add_separator()
        file_menu.add_command(label='❌ Exit', command=self.WIN.quit)

        self.menu.add_cascade(label='🛠️ Tools', menu=tool_menu)
        tool_menu.add_cascade(label='Brush Shape', menu=self.bs_sub_menu)
        self.bs_sub_menu.add_command(label='Ellipse', command= lambda: self.pick_shape("ellipse"))
        self.bs_sub_menu.add_command(label='Rectangle', command= lambda: self.pick_shape("rectangle"))
        self.bs_sub_menu.add_command(label='Pen', command= lambda: self.pick_shape("pen"))

        
        tool_menu.add_cascade(label="Shapes", menu=self.sp_sub_menu)
        self.sp_sub_menu.add_command(label='Rectangle', command = lambda: self.set_type("rectangle"))
        self.sp_sub_menu.add_command(label='Ellipse', command = lambda: self.set_type("ellipse"))
        self.sp_sub_menu.add_command(label='Triangle', command = lambda: self.set_type("triangle"))
        self.sp_sub_menu.add_command(label='Line', command = lambda: self.set_type("line"))


        tool_menu.add_cascade(label='Canvas Tools', menu=self.ct_sub_menu)
        self.ct_sub_menu.add_command(label='Colors', command= self.draw_buttons_right)
        self.ct_sub_menu.add_command(label='Compare Colors', command= self.compare_colors)
        self.ct_sub_menu.add_command(label='Extend Canvas', command= self.extend_canvas)

        self.menu.add_cascade(label='🌪️ Filters', menu=filter_menu)
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

        self.menu.add_cascade(label='🏆 Achievements', command= lambda: self.open_achievement_window())
        self.menu.add_cascade(label='🤼 Competition', command= lambda: self.competition())

    def compare_colors(self):
        if self.compare_colors_open == False:
            self.compare_colors_open = True
            self.WIN_CLR = Toplevel(self.WIN)
            self.WIN_CLR.attributes('-topmost', True)
            self.WIN_CLR.title("Compare Colors")
            self.WIN_CLR.resizable(False, False)
            self.CLR = Canvas(self.WIN_CLR, width=250, height=280)
            self.CLR.grid(row=1, column=0)
            self.update_window_position()
            self.WIN.bind("<Configure>", lambda event: self.update_window_position())         
            self.CLR.bind( "<Button-1>", app.clr_test )
            self.WIN_CLR.protocol('WM_DELETE_WINDOW', self.cc_close)
    
    def cc_close(self):
        self.compare_colors_open = False
        self.WIN_CLR.destroy()
    
    def br_close(self):
        self.buttons_right_open = False
        self.WIN_BTR.destroy()

    def update_window_position(self):
        x = self.WIN.winfo_x()
        y = self.WIN.winfo_y()
        try:
            self.WIN_CLR.geometry(f"+{x + 1280 + self.x_deviation}+{y + 448 + self.y_deviation}")
            if self.WIN_BTR != None:
                self.WIN_BTR.geometry(f"+{x + 1280 + self.x_deviation}+{y + 50 + self.y_deviation}")
            if self.CLS != None:
                self.CLS.geometry(f"+{x + 640 }+{y + 220}")
            if self.NFW != None:
                self.NFW.geometry(f"+{x + 640 }+{y + 220}")
        except TclError as e:
            pass


    def competition(self):
        if self.achievements['ach_6'] == 0:
            self.achievements['ach_6'] = 1
            self.handle_achievements(1)
        CON = Tk()
        CON.resizable(False, False)
        competition = Competition(CON)
        CON.mainloop()

    def on_closing(self):
        if self.closing == False:
            self.CLS = Toplevel(self.WIN)
            self.CLS.attributes('-topmost', True)
            self.CLS.resizable(False, False)
            self.CLS.title("Quit? ")
            x = self.WIN.winfo_x()
            y = self.WIN.winfo_y()
            self.CLS.geometry(f"+{x + 640}+{y + 210}")
            label = Label(self.CLS, text="Do you want to quit?")
            label.grid(row=0, column= 1)
            cancel = Button(self.CLS, text="Cancel", command= lambda: self.cancel_closing())
            cancel.grid(row=1, column=0)
            save = Button(self.CLS, text="Save & Quit", command= lambda: self.save_image_as(1))
            save.grid(row=1, column=1)
            quit = Button(self.CLS, text="Quit", command= lambda: self.quit_app())
            quit.grid(row=1, column=2)
            self.handle_achievements(1)
            self.closing = True
            self.handle_notes(1)
            self.CLS.protocol('WM_DELETE_WINDOW', self.cancel_closing)
        else:
            pass

    def cancel_closing(self):
        self.CLS.destroy()
        self.closing = False
        
    def quit_app(self):
            try:
                self.WIN.destroy()
                self.CLS.destroy() 
                self.NFW.destroy()     
            except TclError:
                pass

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


app.compare_colors()

app.WIN.bind( "<KeyPress>", app.on_key_press )

app.draw_label()
app.draw_menu()
app.draw_buttons()
app.draw_buttons_right()
app.handle_achievements(0)
app.handle_achievements(2)
app.WIN.protocol('WM_DELETE_WINDOW', app.on_closing)
mainloop()