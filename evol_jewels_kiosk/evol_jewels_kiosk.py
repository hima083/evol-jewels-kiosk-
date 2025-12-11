import tkinter as tk
from tkinter import Frame, Label, Button, Canvas
from PIL import Image, ImageTk
import os

# Root window setup
root = tk.Tk()
root.title("Evol Jewels - AI Jewelry Kiosk")
root.attributes("-fullscreen", True)

# Global variables
answers = {}
images = {}

# Fonts
font_header = ("Segoe UI", 36, "bold")
font_sub = ("Segoe UI", 24)
font_button = ("Segoe UI", 18, "bold")
font_small = ("Segoe UI", 14)

# Main canvas for background
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)

def load_image(filename, size=None):
    """Load image only when needed"""
    path = os.path.join("assets", filename)
    if os.path.exists(path):
        try:
            img = Image.open(path)
            if size:
                img = img.resize(size)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    else:
        print(f"Missing: {filename}")
    return None

def clear_screen():
    """Clear all widgets from screen"""
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()

def show_background():
    """Display background image - load only when needed"""
    canvas.delete("all")
    if "bg_mirror.jpg" not in images:
        images["bg_mirror.jpg"] = load_image("bg_mirror.jpg", (root.winfo_screenwidth(), root.winfo_screenheight()))
    
    if "bg_mirror.jpg" in images and images["bg_mirror.jpg"]:
        canvas.create_image(0, 0, image=images["bg_mirror.jpg"], anchor="nw")

def create_button(text, command, x, y, width=20, height=2, bg="#FFD700", fg="#111111"):
    """Helper function to create consistent buttons"""
    btn = Button(root, text=text, font=font_button, bg=bg, fg=fg, 
                width=width, height=height, relief="flat", command=command)
    btn.place(x=x, y=y, anchor="center")
    return btn

def create_label(text, font, fg, x, y):
    """Helper function to create consistent labels"""
    lbl = Label(root, text=text, font=font, fg=fg, bg="#000000")
    lbl.place(x=x, y=y, anchor="center")
    return lbl

# SCREEN 1: WELCOME SCREEN
def show_welcome():
    clear_screen()
    show_background()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Title section - top 15%
    create_label("✨ Evol Jewels ✨", font_header, "#FFD700", screen_width//2, screen_height * 0.15)
    create_label("Your Personalized Jewelry Stylist", font_sub, "white", screen_width//2, screen_height * 0.22)
    
    # Buttons - middle 40%
    create_button("Tap to Start", ask_style, screen_width//2, screen_height * 0.4)
    create_button("Exit", root.destroy, screen_width//2, screen_height * 0.5, width=12, bg="#333333", fg="white")

# SCREEN 2: STYLE QUESTION - FIXED LAYOUT
def ask_style():
    clear_screen()
    show_background()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Title - top 10%
    create_label("How would you describe your style?", font_sub, "#FFD700", screen_width//2, screen_height * 0.1)
    
    styles = [
        ("Traditional & Graceful", "deepika.jpg"),
        ("Modern & Trendy", "alia.jpg"), 
        ("Bold & Festive", "priyanka.jpg"),
        ("Simple & Elegant", "kiara.jpg")
    ]
    
    # Style buttons - middle 50-70%
    start_y = screen_height * 0.3
    for i, (style_text, style_image) in enumerate(styles):
        # Load image only when needed for this button
        if style_image not in images:
            images[style_image] = load_image(style_image, (150, 150))  # Smaller images
        
        if style_image in images and images[style_image]:
            y_position = start_y + (i * 120)
            img_btn = Button(root, image=images[style_image], compound="top",
                           text=style_text, font=font_small, bg="white", fg="#111111",
                           relief="flat", command=lambda s=style_text: save_answer("style", s, ask_occasion))
            img_btn.place(x=screen_width//2, y=y_position, anchor="center")
    
    # Back button - bottom 15%
    create_button("← Back", show_welcome, screen_width//2, screen_height * 0.85, width=12)

# SCREEN 3: OCCASION QUESTION - FIXED LAYOUT
def ask_occasion():
    clear_screen()
    show_background()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Title - top 15%
    create_label("What's your favorite occasion to wear jewelry?", font_sub, "#FFD700", screen_width//2, screen_height * 0.15)
    
    occasions = ["Weddings", "Festivals", "Parties", "Everyday Wear"]
    
    # Occasion buttons - middle 40-70%
    start_y = screen_height * 0.3
    for i, occasion in enumerate(occasions):
        y_position = start_y + (i * 80)
        create_button(occasion, lambda o=occasion: save_answer("occasion", o, ask_budget), 
                     screen_width//2, y_position, width=25)
    
    # Back button - bottom 15%
    create_button("← Back", ask_style, screen_width//2, screen_height * 0.85, width=12)

# SCREEN 4: BUDGET QUESTION - FIXED LAYOUT
def ask_budget():
    clear_screen()
    show_background()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Title - top 15%
    create_label("What's your preferred budget range?", font_sub, "#FFD700", screen_width//2, screen_height * 0.15)
    
    budgets = ["₹5,000 – ₹10,000", "₹10,000 – ₹25,000", "₹25,000 – ₹50,000", "₹50,000+"]
    
    # Budget buttons - middle 40-70%
    start_y = screen_height * 0.3
    for i, budget in enumerate(budgets):
        y_position = start_y + (i * 80)
        create_button(budget, lambda b=budget: save_answer("budget", b, show_result), 
                     screen_width//2, y_position, width=25)
    
    # Back button - bottom 15%
    create_button("← Back", ask_occasion, screen_width//2, screen_height * 0.85, width=12)

def save_answer(key, value, next_screen):
    answers[key] = value
    next_screen()

# SCREEN 5: RESULTS SCREEN - FIXED LAYOUT
def show_result():
    clear_screen()
    show_background()
    
    style = answers.get("style", "")
    occasion = answers.get("occasion", "")
    
    # Determine celebrity match and products
    if "Traditional" in style and "Weddings" in occasion:
        celeb = "Deepika Padukone"
        celeb_img = "deepika.jpg"
        vibe = "Royal · Traditional · Bold"
        products = [
            ("Temple Gold Jhumka", "jhumka.jpg", "₹27,999"),
            ("Kundan Choker Set", "choker.jpg", "₹45,500"), 
            ("Gold Pearl Earrings", "earrings.jpg", "₹19,800")
        ]
    elif "Modern" in style:
        celeb = "Alia Bhatt"
        celeb_img = "alia.jpg"
        vibe = "Chic · Modern · Minimal"
        products = [
            ("Silver Pendant", "earrings.jpg", "₹9,999"),
            ("Diamond Ring", "ring.jpg", "₹24,500")
        ]
    elif "Bold" in style:
        celeb = "Priyanka Chopra" 
        celeb_img = "priyanka.jpg"
        vibe = "Glam · Statement · Vibrant"
        products = [
            ("Statement Earrings", "earrings.jpg", "₹18,999"),
            ("Gold Jhumka", "jhumka.jpg", "₹32,500")
        ]
    else:
        celeb = "Kiara Advani"
        celeb_img = "kiara.jpg"
        vibe = "Elegant · Subtle · Graceful"
        products = [
            ("Pearl Earrings", "earrings.jpg", "₹12,999"),
            ("Gold Ring", "ring.jpg", "₹22,500")
        ]
    
    # FIXED LAYOUT WITH PROPER SPACING
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Title section - top 10%
    create_label(f"✨ Your Style Matches: {celeb} ✨", font_header, "#FFD700", screen_width//2, screen_height * 0.1)
    create_label(f"Vibe: {vibe}", font_sub, "white", screen_width//2, screen_height * 0.16)
    
    # Load and display celebrity image - middle 30%
    if celeb_img not in images:
        images[celeb_img] = load_image(celeb_img, (220, 280))  # Smaller celeb image
    
    if celeb_img in images and images[celeb_img]:
        celeb_label = Label(root, image=images[celeb_img], bg="#000000")
        celeb_label.place(x=screen_width//2, y=screen_height * 0.3, anchor="center")
    
    # Products title - middle 45%
    create_label("Recommended Jewelry For You", font_sub, "#FFD700", screen_width//2, screen_height * 0.45)
    
    # Display products - middle 55-65%
    product_frame = Frame(root, bg="#000000")
    product_frame.place(x=screen_width//2, y=screen_height * 0.6, anchor="center")
    
    for i, (name, img_file, price) in enumerate(products):
        # Load jewelry image only when needed
        if img_file not in images:
            images[img_file] = load_image(img_file, (150, 150))  # Smaller product images
        
        if img_file in images and images[img_file]:
            product_subframe = Frame(product_frame, bg="#000000")
            product_subframe.grid(row=0, column=i, padx=20)
            
            Label(product_subframe, image=images[img_file], bg="#000000").pack()
            Label(product_subframe, text=name, fg="white", bg="#000000", font=font_small).pack()
            Label(product_subframe, text=price, fg="#FFD700", bg="#000000", font=font_small).pack()
    
    # Navigation buttons - bottom 15%
    button_frame = Frame(root, bg="#000000")
    button_frame.place(x=screen_width//2, y=screen_height * 0.85, anchor="center")
    
    Button(button_frame, text="← Back", font=font_button, bg="#FFD700", fg="#111111",
           width=12, relief="flat", command=ask_budget).pack(side="left", padx=10)
    
    Button(button_frame, text="Restart", font=font_button, bg="#FFD700", fg="#111111",
           width=12, relief="flat", command=show_welcome).pack(side="left", padx=10)

# Start the application
show_welcome()
root.mainloop()