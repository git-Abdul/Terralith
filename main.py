import customtkinter as ctk
import os
from PIL import Image

# Window

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("theme.json")

app = ctk.CTk()
app.title("Terralith • Terrain Analysis")
app.state("zoomed")
app.geometry("1100x600")
app.iconbitmap("icon.ico")
app.update()

# Assets

base_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(base_path, "assets")

logo_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "icon.png")),
    size=(70, 70)
)

background_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "background.png")), 
    size=(app.winfo_width()-100, app.winfo_height()-100)
)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

main = ctk.CTkFrame(app, fg_color="transparent")
main.grid(row=0, column=0, sticky="nsew")

bg_image_label = ctk.CTkLabel(main, text="", image=background_img, fg_color="transparent")
bg_image_label.place(relx=0.5, rely=0.5, anchor="center")

main.grid_rowconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=2)
main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(0, weight=1)

analytics = ctk.CTkFrame(app, fg_color="transparent")
analytics.grid(row=0, column=0, sticky="nsew")

analytics.grid_rowconfigure(0, weight=1)
analytics.grid_rowconfigure(1, weight=2)
analytics.grid_rowconfigure(2, weight=1)
analytics.grid_columnconfigure(0, weight=1)

#Functions

def select_frame(name):
    if name == "main":
        main.grid(row=0, column=0, sticky="nsew")
    else:
        main.grid_forget()
    if name == "analytics":
        analytics.grid(row=0, column=0, sticky="nsew")
    else:
        analytics.grid_forget()

def analytics_frame():
    select_frame("analytics")

def main_frame():
    select_frame("main")

# Fonts

heading_font = ctk.CTkFont(
    family="Benzin-bold",
    size=100,
)

text_font = ctk.CTkFont(
    family="Benzin-Regular",
    size=18,
)


# Elements

select_frame("main")

logo = ctk.CTkLabel(
    main,
    text="",
    image=logo_img
)

logo.grid(row=0, column=0, pady=(40, 10), sticky="n")

title = ctk.CTkLabel(
    main,
    text="TERRALITH",
    font=heading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=1, column=0, sticky="n")

btn = ctk.CTkButton(
    main,
    text="Open Analytics",
    font=text_font,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=20,
    border_width=3,
    hover_color="#e0dbd0",
    command=analytics_frame
)
btn.grid(row=2, column=0, sticky="n",ipady=10, ipadx=15)

btn = ctk.CTkButton(
    analytics,
    text="⫷",
    font=text_font,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=20,
    border_width=3,
    hover_color="#e0dbd0",
    command=main_frame
)
btn.grid(row=0, column=0, sticky="w",ipady=10, ipadx=15)

app.mainloop()
