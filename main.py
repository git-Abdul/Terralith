import customtkinter as ctk
from dotenv import load_dotenv
import os
import time
import geocoder
from google import genai
from PIL import Image

# Globals

file_name = ""
biome_text = ""
energy_text = ""
infra_text = ""
caution_text = ""

load_dotenv()
API_KEY = os.environ.get("API_KEY")

# Window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("theme.json")
client = genai.Client(api_key=API_KEY)

app = ctk.CTk()
app.title("Terralith • Terrain Analysis")
app.state("zoomed")
app.geometry("1100x600")
app.iconbitmap("icon.ico")
app.minsize(width=900, height=400)
app.update()

# Assets

base_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(base_path, "assets")

logo_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "icon.png")),
    size=(70, 70)
)

land_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "land.png")),
    size=(200, 200)
)

water_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "water.png")),
    size=(160, 160)
)

nature_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "nature.png")),
    size=(175, 175)
)

background_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "background.png")),
    size=(app.winfo_width()-100, app.winfo_height()-100)
)

backarrow_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "backarrow.png")),
    size=(30, 30)
)

location_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "location.png")),
    size=(160, 160)
)

map_img = ctk.CTkImage(
    Image.open(os.path.join(assets_path, "map.png")),
    size=(200, 200)
)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

main = ctk.CTkFrame(app, fg_color="transparent")
main.grid(row=0, column=0, sticky="nsew")

bg_image_label = ctk.CTkLabel(
    main, text="", image=background_img, fg_color="transparent")
bg_image_label.place(relx=0.5, rely=0.5, anchor="center")

main.grid_rowconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=2)
main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(0, weight=1)

loader = ctk.CTkFrame(app, fg_color="transparent")
loader.grid(row=0, column=0, sticky="nsew")

loader.grid_rowconfigure(0, weight=1)
loader.grid_rowconfigure(1, weight=0)
loader.grid_rowconfigure(2, weight=1)
loader.grid_columnconfigure(0, weight=1)

analytics = ctk.CTkScrollableFrame(app, fg_color="transparent")
analytics.grid(row=0, column=0, sticky="nsew")

analytics.grid_rowconfigure(0, weight=0)
analytics.grid_rowconfigure(1, weight=1, minsize=800)
analytics.grid_rowconfigure(2, weight=0)
analytics.grid_columnconfigure(0, weight=1)
analytics.grid_columnconfigure(1, weight=1)
analytics.grid_columnconfigure(2, weight=1)

parametrics = ctk.CTkScrollableFrame(app, fg_color="transparent")
parametrics.grid(row=0, column=0, sticky="nsew")

parametrics.grid_rowconfigure(0, weight=1)
parametrics.grid_rowconfigure(1, weight=1)
parametrics.grid_rowconfigure(2, weight=1)
parametrics.grid_columnconfigure(0, weight=0)
parametrics.grid_columnconfigure(1, weight=1)

report = ctk.CTkFrame(app, fg_color="transparent")
report.grid(row=0, column=0, sticky="nsew")

report.grid_rowconfigure(0, weight=1)
report.grid_columnconfigure(0, weight=1)


# Functions


def select_frame(name):
    if name == "main":
        main.grid(row=0, column=0, sticky="nsew")
    else:
        main.grid_forget()
    if name == "loader":
        loader.grid(row=0, column=0, sticky="nsew")
    else:
        loader.grid_forget()
    if name == "analytics":
        analytics.grid(row=0, column=0, sticky="nsew")
    else:
        analytics.grid_forget()
    if name == "parametrics":
        parametrics.grid(row=0, column=0, sticky="nsew")
    else:
        parametrics.grid_forget()
    if name == "report":
        report.grid(row=0, column=0, sticky="nsew")
    else:
        report.grid_forget()


def main_frame():
    select_frame("main")


def loader_frame():
    select_frame("loader")


def analytics_frame():
    select_frame("analytics")


def parametrics_frame():
    select_frame("parametrics")


def ai_process(input: str):
    global file_name
    global biome_text
    global infra_text
    global energy_text
    global caution_text
    response = client.models.generate_content(
        model="gemma-3-4b-it",
        contents=f'DO NOT USE BOLD TEXT ANYWHERE IN THE INPUT DO NOT USE ASTERIX TO DENOTE ANYTHING. You are an expert in biomes and sustainable architecture/renewable energy. USER INPUT IS: {input}, respond in the following structured format with clear section labels and bullet points. First, output ONLY the single closest matching biome name from this exact list ["brine","canyon","desert","inland_coastal","marsh","mediterranean","montane_plateau","mountainous_alpine","plains","polar","rainforest","riverine","savannah","steppe","temperate_forest","temperate_oceanic","tundra","volcanic","windy_coastal"]. Then include these sections in order: Biome Characteristics (4–6 concise bullet points covering climate, terrain, vegetation, geology, and visual appearance), Sustainable Energy Resources (bullet points listing viable renewables such as solar, wind, hydro, geothermal, biomass with brief reasons tied to local geography and climate), Commercial & Residential Opportunities (bullet points describing realistic developments like eco-tourism, energy farms, off-grid housing, eco-villages aligned with renewables), and Cautions (bullet points highlighting key environmental, ecological, cultural, and practical constraints such as habitat protection, water scarcity, erosion, flooding risks, protected areas, or indigenous heritage). Do not add extra commentary outside these sections.',
    )
    file_name = f"{response.text.split()[0].lower()}.png"
    biome_text = response.text.partition("Biome Characteristics")[
        2].split("Sustainable Energy Resources")[0]
    energy_text = response.text.partition("Sustainable Energy Resources")[
        2].split("Commercial & Residential Opportunities")[0]
    infra_text = response.text.partition("Commercial & Residential Opportunities")[
        2].split("Cautions")[0]
    caution_text = response.text.partition("Cautions")[2]


def custom_location_input():
    select_frame("loader")
    dialog = ctk.CTkInputDialog(
        text="Type in a location and surrounding visuals:", title="Terralith")
    dialog.wm_iconbitmap("icon.ico")
    value = dialog.get_input()
    if value is not None:
        select_frame("loader")
        ai_process(value)
        l2.configure(text=biome_text)
        l4.configure(text=energy_text)
        l6.configure(text=infra_text)
        l8.configure(text=caution_text)
        lbl.configure(text=f"{file_name[0:len(file_name)-4].title()}".replace("_", " "))
        biome_img = ctk.CTkImage(
            Image.open(os.path.join(biome_path, file_name)),
            size=(200, 200)
        )
        land1.configure(image=biome_img)
        select_frame("report")
    else:
        select_frame("analytics")


def your_location_input():
    select_frame("loader")
    g = geocoder.ip('me')
    value = g.address
    select_frame("loader")
    print(value)
    ai_process(value)
    l2.configure(text=biome_text)
    l4.configure(text=energy_text)
    l6.configure(text=infra_text)
    l8.configure(text=caution_text)
    lbl.configure(text=f"{file_name[0:len(file_name)-4].title()}".replace("_", " "))
    biome_img = ctk.CTkImage(
        Image.open(os.path.join(biome_path, file_name)),
        size=(200, 200)
    )
    land1.configure(image=biome_img)
    select_frame("report")


def createToplevel():
    root = ctk.CTkToplevel(app)
    select_frame("analytics")
    root.title(f"Terralith • {file_name[0:len(file_name)-4].title()}")
    root.state("zoomed")
    root.geometry("900x400")
    root.wm_iconbitmap("icon.ico")
    root.minsize(width=1100, height=400)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    base_path = os.path.dirname(os.path.realpath(__file__))
    assets_path = os.path.join(base_path, "assets")
    biome_path = os.path.join(assets_path, "biomes")

    biome_img = ctk.CTkImage(
        Image.open(os.path.join(biome_path, file_name)),
        size=(200, 200)
    )

    rootF = ctk.CTkScrollableFrame(root, fg_color="transparent")
    rootF.grid(row=0, column=0, sticky="nsew")

    rootF.grid_rowconfigure(0, weight=1)
    rootF.grid_rowconfigure(1, weight=1)
    rootF.grid_rowconfigure(2, weight=1)
    rootF.grid_columnconfigure(0, weight=0)
    rootF.grid_columnconfigure(1, weight=1)

    btn1 = ctk.CTkButton(
        rootF,
        text="",
        font=text_font,
        image=backarrow_img,
        text_color="#b96a4b",
        border_color="#b96a4b",
        fg_color="transparent",
        corner_radius=200,
        border_width=3,
        width=50,
        hover_color="#e0dbd0",
        command=root.destroy
    )
    btn1.grid(row=0, column=0, sticky="nw",
              ipady=10, ipadx=15, padx=10, pady=15)

    title1 = ctk.CTkLabel(
        rootF,
        text="TERRALITH",
        font=subheading_font,
        text_color="#2b2622",
        fg_color="transparent",
        bg_color="transparent"
    )
    title1.grid(row=0, column=0, sticky="n", pady=32, columnspan=2)

    a1 = ctk.CTkFrame(rootF, fg_color="transparent", border_width=0,
                      border_color="#b96a4b", corner_radius=5, height=600)
    a1.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)

    a1.grid_rowconfigure(0, weight=1)
    a1.grid_rowconfigure(1, weight=2)
    a1.grid_rowconfigure(2, weight=1)
    a1.grid_columnconfigure(0, weight=1)

    land1 = ctk.CTkLabel(
        a1,
        text="",
        image=biome_img
    )

    land1.grid(row=0, column=0)

    lbl = ctk.CTkLabel(a1, text=f"{file_name[0:len(file_name)-4].title()}".replace(
        "_", " "), font=text_font, fg_color="#b96a4b", text_color="#f0efef", corner_radius=5)
    lbl.grid(row=1, column=0, ipady=10, ipadx=15, pady=30)

    lbl = ctk.CTkButton(a1, text="", font=text_font, image=backarrow_img, corner_radius=5,
                        fg_color="transparent", border_width=2, border_color="#b96a4b", hover_color="#e0dbd0")
    lbl.grid(row=2, column=0, ipady=10, ipadx=33)

    b = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                     border_color="#b96a4b", corner_radius=5, height=400)
    b.grid(row=1, column=1, sticky="nsew", pady=20, padx=20)

    b.grid_rowconfigure(0, weight=1)
    b.grid_rowconfigure(1, weight=2)
    b.grid_rowconfigure(2, weight=1)
    b.grid_columnconfigure(0, weight=1)

    l1 = ctk.CTkButton(b, text="Biome Characteristics", font=subsubheading_font, border_width=2,
                       border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
    l1.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

    l2 = ctk.CTkLabel(b, text=biome_text, font=subtext_font, wraplength=800)
    l2.grid(row=1, column=0, padx=10, pady=10)

    c = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                     border_color="#b96a4b", corner_radius=5, height=400)
    c.grid(row=2, column=1, sticky="nsew", pady=20, padx=20)

    c.grid_rowconfigure(0, weight=1)
    c.grid_rowconfigure(1, weight=2)
    c.grid_rowconfigure(2, weight=1)
    c.grid_columnconfigure(0, weight=1)

    l3 = ctk.CTkButton(c, text="Sustainable Energy Resources", font=subsubheading_font, border_width=2,
                       border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
    l3.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

    l4 = ctk.CTkLabel(c, text=energy_text, font=subtext_font, wraplength=800)
    l4.grid(row=1, column=0, padx=10, pady=10)

    d = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                     border_color="#b96a4b", corner_radius=5, height=400)
    d.grid(row=3, column=1, sticky="nsew", pady=20, padx=20)

    d.grid_rowconfigure(0, weight=1)
    d.grid_rowconfigure(1, weight=2)
    d.grid_rowconfigure(2, weight=1)
    d.grid_columnconfigure(0, weight=1)

    l5 = ctk.CTkButton(d, text="Commercial & Residential Opportunities", font=subsubheading_font, border_width=2,
                       border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
    l5.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

    l6 = ctk.CTkLabel(d, text=infra_text, font=subtext_font, wraplength=800)
    l6.grid(row=1, column=0, padx=10, pady=10)

    e = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                     border_color="#b96a4b", corner_radius=5, height=400)
    e.grid(row=4, column=1, sticky="nsew", pady=20, padx=20)

    e.grid_rowconfigure(0, weight=1)
    e.grid_rowconfigure(1, weight=2)
    e.grid_rowconfigure(2, weight=1)
    e.grid_columnconfigure(0, weight=1)

    l7 = ctk.CTkButton(e, text="Cautions", font=subsubheading_font, border_width=2, border_color="#b96a4b",
                       state="disabled", fg_color="transparent", text_color_disabled="#000000", )
    l7.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

    l8 = ctk.CTkLabel(e, text=caution_text, font=subtext_font, wraplength=800)
    l8.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()
# Fonts


heading_font = ctk.CTkFont(
    family="Benzin-bold",
    size=100,
)

subheading_font = ctk.CTkFont(
    family="Benzin-bold",
    size=18,
)

subsubheading_font = ctk.CTkFont(
    family="Benzin-medium",
    size=18,
)

text_font = ctk.CTkFont(
    family="Benzin-Regular",
    size=20,
)

subtext_font = ctk.CTkFont(
    family="Benzin-Regular",
    size=16,
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
    text="Analyse Terrain",
    font=text_font,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=20,
    border_width=3,
    hover_color="#e0dbd0",
    command=analytics_frame
)
btn.grid(row=2, column=0, sticky="n", ipady=10, ipadx=15)

# Loader Page

progressbar = ctk.CTkProgressBar(
    loader, orientation="horizontal", width=600, height=10)
progressbar.grid(row=1, column=0, sticky="ns")
progressbar.configure(mode="indeterminate")
progressbar.start()

# Analytics Page

btn = ctk.CTkButton(
    analytics,
    text="",
    font=text_font,
    image=backarrow_img,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=200,
    border_width=3,
    width=50,
    hover_color="#e0dbd0",
    command=main_frame
)
btn.grid(row=0, column=0, sticky="nw", ipady=10, ipadx=15, padx=10, pady=15)

title = ctk.CTkLabel(
    analytics,
    text="TERRALITH",
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=0, column=0, sticky="n", pady=32, columnspan=3)

frame1 = ctk.CTkFrame(analytics, fg_color="transparent",
                      border_width=2, border_color="#b96a4b", corner_radius=15)
frame1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_columnconfigure(0, weight=1)

title = ctk.CTkLabel(
    frame1,
    text="",
    image=land_img,
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=0, column=0, pady=10)

btn = ctk.CTkButton(
    frame1,
    text="Parametric",
    font=text_font,
    command=parametrics_frame,
)
btn.grid(row=1, column=0, pady=10, ipady=10, ipadx=15)

frame2 = ctk.CTkFrame(analytics, fg_color="transparent",
                      border_width=2, border_color="#b96a4b", corner_radius=15)
frame2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

frame2.grid_rowconfigure(0, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_columnconfigure(0, weight=1)

title = ctk.CTkLabel(
    frame2,
    text="",
    image=map_img,
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=0, column=0, pady=10)

btn = ctk.CTkButton(
    frame2,
    text="Custom Location",
    font=text_font,
    command=custom_location_input,
)
btn.grid(row=1, column=0, pady=10, ipady=10, ipadx=15)

frame3 = ctk.CTkFrame(analytics, fg_color="transparent",
                      border_width=2, border_color="#b96a4b", corner_radius=15)
frame3.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

frame3.grid_rowconfigure(0, weight=1)
frame3.grid_rowconfigure(1, weight=1)
frame3.grid_columnconfigure(0, weight=1)

title = ctk.CTkLabel(
    frame3,
    text="",
    image=location_img,
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=0, column=0, pady=10)

btn = ctk.CTkButton(
    frame3,
    text="Your Location",
    font=text_font,
    command=your_location_input,
)
btn.grid(row=1, column=0, pady=10, ipady=10, ipadx=15)

# Parametrics Page

btn = ctk.CTkButton(
    parametrics,
    text="",
    font=text_font,
    image=backarrow_img,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=200,
    border_width=3,
    width=50,
    hover_color="#e0dbd0",
    command=analytics_frame
)
btn.grid(row=0, column=0, sticky="nw", ipady=10, ipadx=15, padx=10, pady=15)

title = ctk.CTkLabel(
    parametrics,
    text="TERRALITH",
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title.grid(row=0, column=0, sticky="n", pady=32, columnspan=2)

a = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=0, border_color="#b96a4b", corner_radius=15)
a.grid(row=1, column=0, sticky="nwse", pady=20, padx=20)

a.grid_rowconfigure(0, weight=1)
a.grid_rowconfigure(1, weight=2)
a.grid_rowconfigure(2, weight=1)
a.grid_columnconfigure(0, weight=1)

land = ctk.CTkLabel(
    a,
    text="",
    image=land_img
)

land.grid(row=0, column=0)

b = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=2, border_color="#b96a4b", corner_radius=15)
b.grid(row=1, column=1, sticky="nesw", pady=20, padx=20)

b.grid_rowconfigure(0, weight=1)
b.grid_rowconfigure(1, weight=2)
b.grid_rowconfigure(2, weight=1)
b.grid_columnconfigure(0, weight=1)

c = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=0, border_color="#b96a4b", corner_radius=15)
c.grid(row=2, column=0, sticky="nsew", pady=20, padx=20)

c.grid_rowconfigure(0, weight=1)
c.grid_rowconfigure(1, weight=2)
c.grid_rowconfigure(2, weight=1)
c.grid_columnconfigure(0, weight=1)

water = ctk.CTkLabel(
    c,
    text="",
    image=water_img
)

water.grid(row=0, column=0)

d = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=2, border_color="#b96a4b", corner_radius=15)
d.grid(row=2, column=1, sticky="nsew", pady=20, padx=20)

d.grid_rowconfigure(0, weight=1)
d.grid_rowconfigure(1, weight=2)
d.grid_rowconfigure(2, weight=1)
d.grid_columnconfigure(0, weight=1)

e = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=0, border_color="#b96a4b", corner_radius=15)
e.grid(row=3, column=0, sticky="nsew", pady=20, padx=20)

e.grid_rowconfigure(0, weight=1)
e.grid_rowconfigure(1, weight=2)
e.grid_rowconfigure(2, weight=1)
e.grid_columnconfigure(0, weight=1)

nature = ctk.CTkLabel(
    e,
    text="",
    image=nature_img
)

nature.grid(row=0, column=0)

f = ctk.CTkFrame(parametrics, fg_color="transparent",
                 border_width=2, border_color="#b96a4b", corner_radius=15)
f.grid(row=3, column=1, sticky="nsew", pady=20, padx=20)

f.grid_rowconfigure(0, weight=1)
f.grid_rowconfigure(1, weight=2)
f.grid_rowconfigure(2, weight=1)
f.grid_columnconfigure(0, weight=1)

# Report Page:

base_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(base_path, "assets")
biome_path = os.path.join(assets_path, "biomes")

try:
    biome_img = ctk.CTkImage(
        Image.open(os.path.join(biome_path, file_name)),
        size=(200, 200)
    )
except FileNotFoundError:
    biome_img=""

rootF = ctk.CTkScrollableFrame(report, fg_color="transparent")
rootF.grid(row=0, column=0, sticky="nsew")

rootF.grid_rowconfigure(0, weight=1)
rootF.grid_rowconfigure(1, weight=1)
rootF.grid_rowconfigure(2, weight=1)
rootF.grid_columnconfigure(0, weight=0)
rootF.grid_columnconfigure(1, weight=1)

btn1 = ctk.CTkButton(
    rootF,
    text="",
    font=text_font,
    image=backarrow_img,
    text_color="#b96a4b",
    border_color="#b96a4b",
    fg_color="transparent",
    corner_radius=200,
    border_width=3,
    width=50,
    hover_color="#e0dbd0",
    command=analytics_frame
)
btn1.grid(row=0, column=0, sticky="nw",
            ipady=10, ipadx=15, padx=10, pady=15)

title1 = ctk.CTkLabel(
    rootF,
    text="TERRALITH",
    font=subheading_font,
    text_color="#2b2622",
    fg_color="transparent",
    bg_color="transparent"
)
title1.grid(row=0, column=0, sticky="n", pady=32, columnspan=2)

a1 = ctk.CTkFrame(rootF, fg_color="transparent", border_width=0,
                    border_color="#b96a4b", corner_radius=5, height=600)
a1.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)

a1.grid_rowconfigure(0, weight=1)
a1.grid_rowconfigure(1, weight=2)
a1.grid_rowconfigure(2, weight=1)
a1.grid_columnconfigure(0, weight=1)

land1 = ctk.CTkLabel(
    a1,
    text="",
    image=biome_img
)

land1.grid(row=0, column=0)

lbl = ctk.CTkLabel(a1, text=f"{file_name[0:len(file_name)-4].title()}".replace(
    "_", " "), font=text_font, fg_color="#b96a4b", text_color="#f0efef", corner_radius=5)
lbl.grid(row=1, column=0, ipady=10, ipadx=15, pady=30)

lb1 = ctk.CTkButton(a1, text="", font=text_font, image=backarrow_img, corner_radius=5,
                    fg_color="transparent", border_width=2, border_color="#b96a4b", hover_color="#e0dbd0")
lb1.grid(row=2, column=0, ipady=10, ipadx=33)

b = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                    border_color="#b96a4b", corner_radius=5, height=400)
b.grid(row=1, column=1, sticky="nsew", pady=20, padx=20)

b.grid_rowconfigure(0, weight=1)
b.grid_rowconfigure(1, weight=2)
b.grid_rowconfigure(2, weight=1)
b.grid_columnconfigure(0, weight=1)

l1 = ctk.CTkButton(b, text="Biome Characteristics", font=subsubheading_font, border_width=2,
                    border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
l1.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

l2 = ctk.CTkLabel(b, text=biome_text, font=subtext_font, wraplength=800)
l2.grid(row=1, column=0, padx=10, pady=10)

c = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                    border_color="#b96a4b", corner_radius=5, height=400)
c.grid(row=2, column=1, sticky="nsew", pady=20, padx=20)

c.grid_rowconfigure(0, weight=1)
c.grid_rowconfigure(1, weight=2)
c.grid_rowconfigure(2, weight=1)
c.grid_columnconfigure(0, weight=1)

l3 = ctk.CTkButton(c, text="Sustainable Energy Resources", font=subsubheading_font, border_width=2,
                    border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
l3.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

l4 = ctk.CTkLabel(c, text=energy_text, font=subtext_font, wraplength=800)
l4.grid(row=1, column=0, padx=10, pady=10)

d = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                    border_color="#b96a4b", corner_radius=5, height=400)
d.grid(row=3, column=1, sticky="nsew", pady=20, padx=20)

d.grid_rowconfigure(0, weight=1)
d.grid_rowconfigure(1, weight=2)
d.grid_rowconfigure(2, weight=1)
d.grid_columnconfigure(0, weight=1)

l5 = ctk.CTkButton(d, text="Commercial & Residential Opportunities", font=subsubheading_font, border_width=2,
                    border_color="#b96a4b", state="disabled", fg_color="transparent", text_color_disabled="#000000", )
l5.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

l6 = ctk.CTkLabel(d, text=infra_text, font=subtext_font, wraplength=800)
l6.grid(row=1, column=0, padx=10, pady=10)

e = ctk.CTkFrame(rootF, fg_color="transparent", border_width=2,
                    border_color="#b96a4b", corner_radius=5, height=400)
e.grid(row=4, column=1, sticky="nsew", pady=20, padx=20)

e.grid_rowconfigure(0, weight=1)
e.grid_rowconfigure(1, weight=2)
e.grid_rowconfigure(2, weight=1)
e.grid_columnconfigure(0, weight=1)

l7 = ctk.CTkButton(e, text="Cautions", font=subsubheading_font, border_width=2, border_color="#b96a4b",
                    state="disabled", fg_color="transparent", text_color_disabled="#000000", )
l7.grid(row=0, column=0, padx=10, pady=(20, 10), ipadx=20, ipady=20)

l8 = ctk.CTkLabel(e, text=caution_text, font=subtext_font, wraplength=800)
l8.grid(row=1, column=0, padx=10, pady=10)

app.mainloop()
