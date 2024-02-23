import tkinter as tk
from tkinter import ttk,colorchooser
from PIL import ImageGrab, ImageTk,Image,ImageDraw
from math import cos, sin, pi
from tkinter import messagebox,filedialog
import io




class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 850
        self.canvas_height = 550
        self.drawing_mode = "draw"
        self.selected_color = "black"
        self.selected_width = 2
        self.eraser_colors = ["white"]
        self.prev_x = None  
        self.prev_y = None  
        self.select_rect = None
        self.canvas = None  
        self.saved_canvas = None  
        self.move_start_x = 0
        self.move_start_y = 0
        self.select_start_x=0
        self.select_start_y=0
        self.draw_mode = False
        self.fill_mode = False
        self.curve_points = []  

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP)

        self.draw_button = tk.Button(self.root, text="Draw", command=self.set_draw_mode)
        self.draw_button.pack(side=tk.TOP)

        self.erase_button = tk.Button(self.root, text="Erase", command=self.set_erase_mode)
        self.erase_button.pack(side=tk.LEFT)

        self.color_frame = tk.Frame(self.root)
        self.color_frame.pack(side=tk.TOP)

        colors = ["black", "red", "blue", "green", "yellow", "orange", "purple", "pink", "white", "brown", "gray", "magenta"]

        for color in colors:
            color_button = tk.Button(self.color_frame, bg=color, width=2, command=lambda c=color: self.set_color(c))
            color_button.pack(side=tk.LEFT)

        button_color = tk.Button(self.root, text="Choose Color", command=self.pick_color)
        button_color.pack()

        self.eraser_frame = tk.Frame(self.root)
        self.eraser_frame.pack(side=tk.LEFT)

        self.eraser_label = tk.Label(self.eraser_frame, text="Eraser Colors:")
        self.eraser_label.pack(side=tk.LEFT)

        self.eraser_buttons = []
        for color in colors:
            eraser_button = tk.Button(self.eraser_frame, bg=color, width=2, command=lambda c=color: self.toggle_eraser_color(c))
            eraser_button.pack(side=tk.LEFT)
            self.eraser_buttons.append(eraser_button)

        self.color_picker_button = tk.Button(self.root, text="Color Picker", command=self.set_color_picker_mode)
        self.color_picker_button.pack(side=tk.LEFT)

        self.fill_button = tk.Button(self.root, text="Fill", command=self.set_fill_mode)
        self.fill_button.pack(side=tk.LEFT)

        self.width_frame = tk.Frame(self.root)
        self.width_frame.pack(side=tk.LEFT)

        self.width_label = tk.Label(self.width_frame, text="Width:")
        self.width_label.pack(side=tk.LEFT)

        self.width_scale = tk.Scale(self.width_frame, from_=1, to=5, orient=tk.HORIZONTAL, length=100, command=self.set_width)
        self.width_scale.set(self.selected_width)
        self.width_scale.pack(side=tk.LEFT)

        self.select_button = tk.Button(self.root, text="Select", command=self.set_select_mode)
        self.select_button.pack(side=tk.LEFT)

        self.magnifier_button = tk.Button(self.root, text="Magnifier", command=self.set_magnifier_mode)
        self.magnifier_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.root, text="Save Canvas", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.root, text="Load Canvas", command=self.load_canvas)
        self.load_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.circle_button = tk.Button(self.root, text="Circle", command=self.set_circle_mode)
        self.circle_button.pack(side=tk.LEFT)

        self.oval_button = tk.Button(self.root, text="Oval", command=self.set_oval_mode)
        self.oval_button.pack(side=tk.LEFT)

        self.square_button = tk.Button(self.root, text="Square", command=self.set_square_mode)
        self.square_button.pack(side=tk.LEFT)

        self.rectangle_button = tk.Button(self.root, text="Rectangle", command=self.set_rectangle_mode)
        self.rectangle_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(self.root, text="Line", command=self.set_line_mode)
        self.line_button.pack(side=tk.LEFT)

        self.triangle_button = tk.Button(self.root, text="Triangle", command=self.set_triangle_mode)
        self.triangle_button.pack(side=tk.LEFT)

        self.star_button = tk.Button(self.button_frame, text="Star", command=self.set_star_mode)
        self.star_button.pack(side=tk.LEFT)

        self.pentagon_button = tk.Button(self.button_frame, text="Pentagon", command=self.set_pentagon_mode)
        self.pentagon_button.pack(side=tk.LEFT)

        self.hexagon_button = tk.Button(self.button_frame, text="Hexagon", command=self.set_hexagon_mode)
        self.hexagon_button.pack(side=tk.LEFT)

        self.polygon_button = tk.Button(self.button_frame, text="Polygon", command=self.set_polygon_mode)
        self.polygon_button.pack(side=tk.LEFT)

        self.curve_button = tk.Button(self.button_frame, text="Curve", command=self.set_curve_mode)
        self.curve_button.pack(side=tk.LEFT)


        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_motion)


    def set_draw_mode(self):
        self.drawing_mode = "draw"
        self.fill_mode = False


    def set_erase_mode(self):
        self.drawing_mode = "erase"

    def set_color(self, color):
        self.selected_color = color

    def set_width(self, width):
        self.selected_width = int(width)

    def toggle_eraser_color(self, color):
        if color in self.eraser_colors:
            self.eraser_colors.remove(color)
        else:
            self.eraser_colors.append(color)

    def set_color_picker_mode(self):
        self.drawing_mode = "color_picker"

    def set_fill_mode(self):
        self.drawing_mode = "fill"

    def set_select_mode(self):
        self.drawing_mode = "select"

    def set_magnifier_mode(self):
        self.drawing_mode = "magnifier"
        

    def set_clear_mode(self):
        self.drawing_mode = "clear"

    def get_pixel_color(self, x, y):
        item = self.canvas.find_closest(x, y)[0]  # Get the closest canvas item
        return self.canvas.itemcget(item, "fill")  # Get the fill color of the item

    def set_pixel_color(self, x, y, color):
        item = self.canvas.find_closest(x, y)[0]  # Get the closest canvas item
        self.canvas.itemconfigure(item, fill=color)

    def pick_color(self):
        color = colorchooser.askcolor(title="Choose color")
        self.selected_color = color[1]

   

    def handle_click(self, event):
        if self.drawing_mode == "color_picker":
            x = event.x
            y = event.y
            image = ImageGrab.grab()
            rgb = image.load()[x, y]
            color = "#%02x%02x%02x" % rgb
            self.selected_color = color
            messagebox.showinfo("Color Picker", "Selected color: {}".format(color))
       
        elif self.drawing_mode == "fill":
            x, y = event.x, event.y
            target_color = self.get_pixel_color(x, y)
            self.fill(x, y, target_color, self.selected_color)   
           
        elif self.drawing_mode == "select":
            self.select_start_x = event.x
            self.select_start_y = event.y
            self.select_rect=None
        elif self.drawing_mode == "circle":
            self.circle_center_x = event.x
            self.circle_center_y = event.y
            self.circle = None
        elif self.drawing_mode == "oval":
            self.oval_start_x = event.x
            self.oval_start_y = event.y
            self.oval = None
        elif self.drawing_mode == "square":
            self.square_start_x = event.x
            self.square_start_y = event.y
            self.square = None
        elif self.drawing_mode == "rectangle":
            self.rectangle_start_x = event.x
            self.rectangle_start_y = event.y
            self.rectangle = None
        elif self.drawing_mode == "triangle":
            self.triangle_start_x = event.x
            self.triangle_start_y = event.y
            self.triangle = None
        elif self.drawing_mode == "line":
            self.line_start_x = event.x
            self.line_start_y = event.y
            self.line = None
        elif self.drawing_mode == "pentagon":
            self.pentagon_start_x = event.x
            self.pentagon_start_y = event.y
            self.pentagon = None
        elif self.drawing_mode == "hexagon":
            self.hexagon_start_x = event.x
            self.hexagon_start_y = event.y
            self.hexagon = None
        elif self.drawing_mode == "star":
            self.star_start_x = event.x
            self.star_start_y = event.y
            self.star = None
        elif self.drawing_mode == "polygon":
            self.polygon_start_x = event.x
            self.polygon_start_y = event.y
            self.polygon = None

        elif self.drawing_mode == "curve":
            self.curve_start_x = event.x
            self.curve_start_y = event.y
            self.curve = None

        
        else:
            self.prev_x = event.x
            self.prev_y = event.y

    def handle_motion(self, event):
        if self.drawing_mode == "draw":
            self.draw(event)
        elif self.drawing_mode == "erase":
            self.erase(event)
        elif self.drawing_mode == "select":
            self.draw_select_rect(event)
        elif self.drawing_mode == "magnifier":
            self.show_magnifier(event)
        elif self.drawing_mode == "clear":
            self.clear_canvas(event)
        elif self.drawing_mode == "circle":
            self.draw_circle(event)
        elif self.drawing_mode == "oval":
            self.draw_oval(event)
        elif self.drawing_mode == "square":
            self.draw_square(event)
        elif self.drawing_mode == "rectangle":
            self.draw_rectangle(event)
        elif self.drawing_mode == "triangle":
            self.draw_triangle(event)
        elif self.drawing_mode == "line":
            self.draw_line(event)
        elif self.drawing_mode == "star":
            self.draw_star(event)
        elif self.drawing_mode == "hexagon":
            self.draw_hexagon(event)
        elif self.drawing_mode == "pentagon":
            self.draw_pentagon(event)
        elif self.drawing_mode == "polygon":
            self.draw_polygon(event)
        elif self.drawing_mode == "curve":
            self.draw_curve(event)
        elif self.drawing_mode == "move":
            self.move_object(event)


    def draw_circle(self, event):
        if self.circle:
            self.canvas.delete(self.circle)
        x1, y1 = self.circle_center_x, self.circle_center_y
        x2, y2 = event.x, event.y
        radius = max(abs(x2 - x1), abs(y2 - y1))
        self.circle = self.canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius, outline=self.selected_color, width=self.selected_width)

    def draw_oval(self, event):
        if self.oval:
            self.canvas.delete(self.oval)
        x1, y1 = self.oval_start_x, self.oval_start_y
        x2, y2 = event.x, event.y
        self.oval = self.canvas.create_oval(x1, y1, x2, y2, outline=self.selected_color, width=self.selected_width)

    def draw_square(self, event):
        if self.square:
            self.canvas.delete(self.square)
        x1, y1 = self.square_start_x, self.square_start_y
        x2, y2 = event.x, event.y
        size = max(abs(x2 - x1), abs(y2 - y1))
        self.square = self.canvas.create_rectangle(x1, y1, x1 + size, y1 + size, outline=self.selected_color, width=self.selected_width)

 
    def draw_rectangle(self, event):

        if self.rectangle:
            self.canvas.delete(self.rectangle)
        x1, y1 = self.rectangle_start_x, self.rectangle_start_y
        x2, y2 = event.x, event.y

        
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        size = max(width, height)

        
        if width < height:
            if x2 < x1:
                x1 = x1 - size
            else:
                x2 = x1 + size
        else:
            if y2 < y1:
                y1 = y1 - size
            else:
                y2 = y1 + size

        
        self.rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.selected_color, width=self.selected_width)


    

    def draw_line(self, event):  
         if self.line:
            self.canvas.delete(self.line)

         x1, y1 = self.line_start_x, self.line_start_y
         x2, y2 = event.x, event.y
            

         self.line=self.canvas.create_line(x1, y1, x2, y2, fill=self.selected_color, width=self.selected_width)

       


    def draw_triangle(self, event):
        if self.triangle:
            self.canvas.delete(self.triangle)

        x1, y1 = self.triangle_start_x, self.triangle_start_y
        x2, y2 = event.x, event.y
        x3, y3 = x2, y1

        self.triangle = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.selected_color,fill="", width=self.selected_width)

    def draw_star(self, event):
        if self.star:
            self.canvas.delete(self.star)

        cx, cy = event.x, event.y
        radius_outer = min(cx, cy) - 10
        radius_inner = radius_outer / 2

        points = []
        angle = 2 * pi / 5

        for i in range(5):
            x_outer = cx + radius_outer * cos(i * angle)
            y_outer = cy + radius_outer * sin(i * angle)
            points.append(x_outer)
            points.append(y_outer)

            x_inner = cx + radius_inner * cos((i + 0.5) * angle)
            y_inner = cy + radius_inner * sin((i + 0.5) * angle)
            points.append(x_inner)
            points.append(y_inner)

        self.star = self.canvas.create_polygon(points, outline=self.selected_color, fill="", width=self.selected_width)
        




    def draw_pentagon(self, event):
        if self.pentagon:
            self.canvas.delete(self.pentagon)

        cx, cy = event.x, event.y
        radius = min(cx, cy) - 10

        points = []
        angle = 2 * pi / 5

        for i in range(5):
            x = cx + radius * cos(i * angle)
            y = cy + radius * sin(i * angle)
            points.append((x, y))

        self.pentagon=self.canvas.create_polygon(points, outline=self.selected_color, fill="", width=self.selected_width)

    def draw_hexagon(self, event):
        if self.hexagon:
            self.canvas.delete(self.hexagon)
        cx, cy = event.x, event.y
        radius = min(cx, cy) - 10

        points = []
        angle = 2 * pi / 6

        for i in range(6):
            x = cx + radius * cos(i * angle)
            y = cy + radius * sin(i * angle)
            points.append((x, y))

        self.hexagon=self.canvas.create_polygon(points, outline=self.selected_color, fill="", width=self.selected_width)


    def draw_polygon(self,event):
        if self.polygon:
            self.canvas.delete(self.polygon)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        max_radius = min(canvas_width, canvas_height) // 2 - 12

        cx, cy = event.x, event.y
        radius = min(max_radius, max(cx, cy) - 15)

        num_sides_label = ttk.Label(text="Number of Sides:")
        num_sides_label.pack()
        num_sides_var = tk.StringVar()
        num_sides_dropdown = ttk.Combobox(values=[3, 4, 5, 6, 7, 8], textvariable=num_sides_var)
        num_sides_dropdown.pack()
        num_sides_dropdown.current(0)

        def create_polygon():
            sides = int(num_sides_var.get())

            points = []
            angle = 2 * pi / sides

            for i in range(sides):
                x = cx + radius * cos(i * angle)
                y = cy + radius * sin(i * angle)
                points.append((x, y))

            self.polygon = self.canvas.create_polygon(points, outline=self.selected_color, fill="", width=3)

        create_button = ttk.Button(text="Create", command=create_polygon)
        create_button.pack()

    def draw_curve(self, event):

        if self.curve:
            self.canvas.delete(self.curve)

        x1, y1 = self.curve_start_x, self.curve_start_y
        x2, y2 = event.x, event.y

        # Draw the curve using the create_arc method
        self.curve=self.canvas.create_arc(x1, y1, x2, y2, start=0, extent=180, style="arc", outline=self.selected_color, width=self.selected_width)

    

    def set_circle_mode(self):
        self.drawing_mode = "circle"

    def set_oval_mode(self):
        self.drawing_mode = "oval"

    def set_square_mode(self):
        self.drawing_mode = "square"

    def set_rectangle_mode(self):
        self.drawing_mode = "rectangle"

    def set_triangle_mode(self):
        self.drawing_mode = "triangle"

    def set_line_mode(self):
        self.drawing_mode = "line"

    def set_star_mode(self):
        self.drawing_mode = "star"

    def set_pentagon_mode(self):
        self.drawing_mode = "pentagon"

    def set_hexagon_mode(self):
        self.drawing_mode = "hexagon"

    def set_polygon_mode(self):
        self.drawing_mode = "polygon"

    def set_curve_mode(self):
        self.drawing_mode = "curve"

    def move_object(self, event):
        if self.select_rect:
            x = event.x - self.select_rect_start_x
            y = event.y - self.select_rect_start_y
            self.canvas.move(self.select_rect, x, y)
            self.select_rect_start_x = event.x
            self.select_rect_start_y = event.y

    def draw(self, event):
        x1, y1 = self.prev_x, self.prev_y
        x2, y2 = event.x, event.y
        self.canvas.create_line(x1, y1, x2, y2, fill=self.selected_color, width=self.selected_width)
        self.prev_x = event.x
        self.prev_y = event.y

    def erase(self, event):
        for color in self.eraser_colors:
            x1, y1 = event.x - 5, event.y - 5
            x2, y2 = event.x + 5, event.y + 5
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def clear_canvas(self):
        self.canvas.delete("selected")  # Delete selected region
        self.canvas.delete("all")  # Clear the entire canvas

    def draw_select_rect(self, event):
        if self.select_rect:
            self.canvas.delete(self.select_rect)
        x1, y1 = self.select_start_x, self.select_start_y
        x2, y2 = event.x, event.y
        self.select_rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', dash=(4, 4), tags="select_rect")
        self.canvas.tag_bind(self.select_rect, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.select_rect, "<B1-Motion>", self.move_rect)
        self.canvas.tag_bind(self.select_rect, "<ButtonRelease-1>", self.stop_move)

    def start_move(self, event):
        self.move_start_x = event.x
        self.move_start_y = event.y

    def move_rect(self, event):
        dx = event.x - self.move_start_x
        dy = event.y - self.move_start_y
        self.canvas.move(self.select_rect, dx, dy)
        self.move_start_x = event.x
        self.move_start_y = event.y

    def stop_move(self, event):
            
            x1, y1, x2, y2 = self.canvas.coords(self.select_rect)

            # Calculate the width and height of the moved select rectangle
            width = x2 - x1
            height = y2 - y1

            # Create a new rectangle to represent the selected area
            selected_area = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', dash=(4, 4))

            # Deselect the original select rectangle
            self.canvas.delete(self.select_rect)
            self.select_rect = None

            

            # Set the selected area as the current selection
            self.selection = selected_area

            # Reset move start coordinates
            self.move_start_x = None
            self.move_start_y = None



    def show_magnifier(self, event):
        magnifier_size = 200
        x, y = event.x, event.y
        x1, y1 = x - magnifier_size, y - magnifier_size
        x2, y2 = x + magnifier_size, y + magnifier_size

        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image = image.resize((400, 400), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        if hasattr(self, "magnifier_window"):
            self.magnifier_window.destroy()

        self.magnifier_window = tk.Toplevel(self.root)
        self.magnifier_window.wm_title("Magnifier")
        self.magnifier_canvas = tk.Canvas(self.magnifier_window, width=400, height=400)
        self.magnifier_canvas.pack()
        self.magnifier_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.magnifier_canvas.image = photo

    def save_canvas(self):

         file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPG Files", ".jpg"), ("All Files", ".*")])
         if file_path:
                try:
                    image = ImageGrab.grab(self.canvas)
                    image.save(file_path)
                    messagebox.showinfo("Save", "Canvas saved successfully.")
                except Exception as e:
                    messagebox.showerror("Error", "Failed to save canvas: " )

    

    def load_canvas(self):
       file_path = filedialog.askopenfilename(filetypes=[("PNG Files", ".png"), ("All Files", ".*")])
       if file_path:
            try:
                image = Image.open(file_path)
                photo_image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor="nw", image=photo_image)
               
                self.canvas.image = photo_image
            except Exception as e:
                print("Error opening image:", e)

           
   
    def fill(self, x, y, target_color, replacement_color):
        target_color = self.get_pixel_color(x, y)
        if target_color == replacement_color:
            return

        boundaries = self.get_shape_boundaries(x, y)
        for i in range(boundaries['min_x'], boundaries['max_x'] + 1):
            for j in range(boundaries['min_y'], boundaries['max_y'] + 1):
                self.set_pixel_color(i, j, replacement_color)

    def canvas_click(self, event):
        if self.draw_mode:
            self.draw_shape(event.x, event.y)
        elif self.fill_mode:
            self.fill_shape(event.x, event.y)
        else:
            self.change_canvas_color()

    def change_canvas_color(self):
        self.canvas.configure(background=self.selected_color)

    def get_shape_boundaries(self, x, y):
        item = self.canvas.find_closest(x, y)[0]
        coordinates = self.canvas.coords(item)

        min_x = min(coordinates[0::2])
        max_x = max(coordinates[0::2])
        min_y = min(coordinates[1::2])
        max_y = max(coordinates[1::2])

        return {
            'min_x': int(min_x),
            'max_x': int(max_x),
            'min_y': int(min_y),
            'max_y': int(max_y)
        }


    def fill_recursive(self, x, y, target_color, replacement_color):
        current_color = self.get_pixel_color(x, y)
        if current_color == target_color:
            self.canvas.create_line(x, y, x + 1, y, fill=replacement_color)
            self.fill_recursive(x + 1, y, target_color, replacement_color)
            self.fill_recursive(x - 1, y, target_color, replacement_color)
            self.fill_recursive(x, y + 1, target_color, replacement_color)
            self.fill_recursive(x, y - 1, target_color, replacement_color)

    


root = tk.Tk()
root.title("Paint App")
app = PaintApp(root)


root.mainloop()
