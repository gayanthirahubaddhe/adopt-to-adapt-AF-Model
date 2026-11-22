import tkinter as tk
from tkinter import ttk, messagebox
import os

from PIL import Image, ImageTk, ImageDraw, ImageFont

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import create_connection


# ==========================================================
# 1. APPLICATION SETTINGS
# ==========================================================

root = tk.Tk()

root.title("ADOPT TO ADAPT - Analog Forestry Model Information System")
root.geometry("1200x780")
root.minsize(950, 650)
root.configure(bg="#F4F5F0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "plant_images")

HERO_IMAGE_PATH = os.path.join(
    BASE_DIR,
    "images",
    'landscape.jpg'
)


# ==========================================================
# 2. COLOUR PALETTE
# ==========================================================

FOREST = "#183F32"
FOREST_LIGHT = "#285B46"
CREAM = "#F4F5F0"
WHITE = "#FFFFFF"
TEXT_DARK = "#26382F"
TEXT_MUTED = "#68786D"
GOLD = "#B69A60"
BORDER = "#D9E0D8"


# ==========================================================
# 3. APPLICATION CONTAINERS
# ==========================================================

home_frame = tk.Frame(root, bg=CREAM)
inventory_frame = tk.Frame(root, bg=CREAM)


# ==========================================================
# 4. DATABASE HELPER
# ==========================================================

def get_species_records(search_text=""):

    connection = create_connection()
    cursor = connection.cursor()

    if search_text:

        keyword = f"%{search_text}%"

        cursor.execute("""
            SELECT
                species_id,
                botanical_name,
                common_name_english,
                family
            FROM af_site_species
            WHERE
                botanical_name LIKE ?
                OR common_name_english LIKE ?
                OR family LIKE ?
                OR common_name_sinhala LIKE ?
            ORDER BY species_id ASC
        """, (keyword, keyword, keyword, keyword))

    else:

        cursor.execute("""
            SELECT
                species_id,
                botanical_name,
                common_name_english,
                family
            FROM af_site_species
            ORDER BY species_id ASC
        """)

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================================
# 5. PAGE NAVIGATION
# ==========================================================

def open_inventory():

    home_frame.pack_forget()

    inventory_frame.pack(
        fill="both",
        expand=True
    )

    load_species()
    update_dashboard_summary()


def show_home():

    inventory_frame.pack_forget()

    home_frame.pack(
        fill="both",
        expand=True
    )


# ==========================================================
# 6. HOMEPAGE
# ==========================================================

# ---------- Header ----------

home_header = tk.Frame(
    home_frame,
    bg=FOREST,
    height=100
)

home_header.pack(fill="x")
home_header.pack_propagate(False)

# ==========================================
# ADOPT TO ADAPT LOGO
# ==========================================

logo_path = os.path.join(BASE_DIR, "Logo.png")

try:

    logo_original = Image.open(logo_path)

    logo_original.thumbnail(
        (75, 75),
        Image.Resampling.LANCZOS
    )

    logo_image = ImageTk.PhotoImage(logo_original)

    logo_label = tk.Label(
        home_header,
        image=logo_image,
        bg=FOREST
    )

    logo_label.image = logo_image

    logo_label.pack(
        side="left",
        padx=(25, 12),
        pady=10
    )

except Exception as error:

    print("Logo loading error:", error)

brand_frame = tk.Frame(
    home_header,
    bg=FOREST
)

brand_frame.pack(
    side="left",
    padx=35,
    pady=18
)


tk.Label(
    brand_frame,
    text="ADOPT TO ADAPT",
    font=("Arial", 24, "bold"),
    fg=WHITE,
    bg=FOREST
).pack(anchor="w")


tk.Label(
    brand_frame,
    text="ANALOG FORESTRY  |  PROJECT INFORMATION SYSTEM",
    font=("Arial", 9, "bold"),
    fg="#C8D9CC",
    bg=FOREST
).pack(anchor="w", pady=(4, 0))


tk.Label(
    home_header,
    text="SRI LANKA",
    font=("Arial", 10, "bold"),
    fg="#D7C49B",
    bg=FOREST
).pack(side="right", padx=40)


# ==========================================================
# HERO SECTION - FULL WIDTH BLENDED LANDSCAPE
# ==========================================================

hero = tk.Frame(
    home_frame,
    bg=FOREST_LIGHT,
    height=280
)

hero.pack(
    fill="x",
    padx=25,
    pady=(20, 14)
)

hero.pack_propagate(False)


try:

    # Get display dimensions
    hero_width = root.winfo_screenwidth() - 70
    hero_height = 280

    # Load photograph
    hero_original = Image.open(
        HERO_IMAGE_PATH
    ).convert("RGB")

    # Crop photograph to fill the entire Hero area
    ratio = max(
        hero_width / hero_original.width,
        hero_height / hero_original.height
    )

    resized_width = int(hero_original.width * ratio)
    resized_height = int(hero_original.height * ratio)

    hero_original = hero_original.resize(
        (resized_width, resized_height),
        Image.Resampling.LANCZOS
    )

    left = (resized_width - hero_width) // 2
    top = (resized_height - hero_height) // 2

    hero_original = hero_original.crop((
        left,
        top,
        left + hero_width,
        top + hero_height
    ))

    # Create a dark green gradient overlay.
    # Stronger on the left for readable text.
    gradient = Image.new("L", (hero_width, 1))

    gradient.putdata([
        int(220 - 165 * (x / hero_width))
        for x in range(hero_width)
    ])

    gradient = gradient.resize(
        (hero_width, hero_height)
    )

    overlay = Image.new(
        "RGBA",
        (hero_width, hero_height),
        (24, 63, 50, 0)
    )

    overlay.putalpha(gradient)

    hero_background = Image.alpha_composite(
        hero_original.convert("RGBA"),
        overlay
    )

    # Draw text directly onto the photograph
    draw = ImageDraw.Draw(hero_background)

    try:
        heading_font = ImageFont.truetype(
            "arialbd.ttf", 34
        )

        paragraph_font = ImageFont.truetype(
            "arial.ttf", 20
        )

    except OSError:
        heading_font = ImageFont.load_default()
        paragraph_font = ImageFont.load_default()

    heading = (
        "RESTORING LANDSCAPES & "
        "RECONNECTING BIODIVERSITY"
    )

    description = (
        "An Analog Forestry initiative exploring ecological "
        "restoration, plant diversity and sustainable landscapes "
        "in the Upper Knuckles foothills. Restoration of "
        "Mid-Country Forest Ecosystems through Analog Forestry "
        "in Mariland Estate, Beddegama, Panwila, Kandy, "
        "Central Province, Sri Lanka."
    )

    # Wrap text to fit the left side
    def wrap_text(text, font, max_width):

        words = text.split()
        lines = []
        current_line = ""

        for word in words:

            test_line = (
                current_line + " " + word
            ).strip()

            if draw.textlength(
                test_line,
                font=font
            ) <= max_width:

                current_line = test_line

            else:

                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    heading_text = wrap_text(
        heading,
        heading_font,
        int(hero_width * 0.53)
    )

    description_text = wrap_text(
        description,
        paragraph_font,
        int(hero_width * 0.48)
    )

    # Heading
    draw.multiline_text(
        (45, 45),
        heading_text,
        font=heading_font,
        fill="#E3C99A",
        spacing=8
    )

    # Description
    draw.multiline_text(
        (47, 155),
        description_text,
        font=paragraph_font,
        fill="#FFFFFF",
        spacing=7
    )

    # Convert to Tkinter image
    hero_photo = ImageTk.PhotoImage(
        hero_background.convert("RGB")
    )

    hero_background_label = tk.Label(
        hero,
        image=hero_photo,
        bd=0,
        highlightthickness=0
    )

    hero_background_label.image = hero_photo

    hero_background_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

except Exception as error:

    print("Hero design error:", error)

# ---------- Project overview ----------

overview_frame = tk.Frame(
    home_frame,
    bg=CREAM
)

overview_frame.pack(
    fill="x",
    padx=35,
    pady=(3, 10)
)


tk.Label(
    overview_frame,
    text="EXPLORE THE PROJECT",
    font=("Arial", 15, "bold"),
    fg=FOREST,
    bg=CREAM
).pack(anchor="w")


tk.Label(
    overview_frame,
    text=(
        "Discover the ecological approach, restoration strategy "
        "and project landscape behind Adopt to Adapt."
    ),
    font=("Arial", 10),
    fg=TEXT_MUTED,
    bg=CREAM
).pack(anchor="w", pady=(4, 5))


# ---------- Project information window ----------

def show_project_section(title, description, content):

    section_window = tk.Toplevel(root)

    section_window.title(title)
    section_window.geometry("720x520")
    section_window.minsize(600, 400)
    section_window.configure(bg=CREAM)

    title_bar = tk.Frame(
        section_window,
        bg=FOREST,
        height=85
    )

    title_bar.pack(fill="x")
    title_bar.pack_propagate(False)

    tk.Label(
        title_bar,
        text=title,
        font=("Arial", 17, "bold"),
        fg=WHITE,
        bg=FOREST
    ).pack(anchor="w", padx=25, pady=25)

    content_area = tk.Frame(
        section_window,
        bg=WHITE,
        padx=30,
        pady=25
    )

    content_area.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    tk.Label(
        content_area,
        text=description,
        font=("Arial", 12, "bold"),
        fg=FOREST_LIGHT,
        bg=WHITE,
        wraplength=600,
        justify="left"
    ).pack(anchor="w", pady=(0, 15))

    tk.Label(
        content_area,
        text=content,
        font=("Arial", 11),
        fg=TEXT_DARK,
        bg=WHITE,
        wraplength=600,
        justify="left",
        anchor="nw"
    ).pack(anchor="w", fill="x")

    ttk.Button(
        section_window,
        text="Close",
        command=section_window.destroy
    ).pack(pady=(0, 15))


# ---------- Project cards ----------

cards_frame = tk.Frame(
    home_frame,
    bg=CREAM
)

cards_frame.pack(
    fill="x",
    padx=30,
    pady=5
)

cards_frame.columnconfigure(0, weight=1)
cards_frame.columnconfigure(1, weight=1)


project_sections = [

    (
        "01",
        "ANALOG FORESTRY",
        "Understanding forest-inspired ecological restoration.",
        "Analog Forestry is an ecological restoration and "
        "land-management approach that seeks to develop "
        "productive ecosystems resembling the structure "
        "and ecological functions of natural forests."
    ),

    (
        "02",
        "RESTORATION STRATEGY",
        "Biodiversity, species selection and ecological functions.",
        "The restoration strategy considers plant diversity, "
        "forest structure, ecological roles and the integration "
        "of useful species to support resilient landscapes."
    ),

    (
        "03",
        "PROJECT LOCATION",
        "Mariland Estate – Panwila, Sri Lanka.",
        "The Adopt to Adapt initiative focuses on a landscape "
        "in the Upper Knuckles foothills. The project explores "
        "the potential of Analog Forestry for restoring "
        "mid-country forest ecosystems."
    ),

    (
        "04",
        "SPECIES INVENTORY",
        "Explore the documented AF Site plant species.",
        "Access the plant inventory to explore botanical names, "
        "common names, plant families, ecological functions, "
        "growth characteristics and other recorded information."
    )
]


for index, section in enumerate(project_sections):

    number, title, description, content = section

    row = index // 2
    column = index % 2

    card = tk.Frame(
        cards_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=18,
        pady=12
    )

    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=7,
        pady=6
    )

    tk.Label(
        card,
        text=number,
        font=("Arial", 18, "bold"),
        fg=GOLD,
        bg=WHITE
    ).pack(anchor="w")

    tk.Label(
        card,
        text=title,
        font=("Arial", 11, "bold"),
        fg=FOREST,
        bg=WHITE
    ).pack(anchor="w", pady=(4, 4))

    tk.Label(
        card,
        text=description,
        font=("Arial", 9),
        fg=TEXT_MUTED,
        bg=WHITE,
        wraplength=400,
        justify="left"
    ).pack(anchor="w")

    if number == "04":

        card_button = ttk.Button(
            card,
            text="Open Inventory",
            command=open_inventory
        )

    else:

        card_button = ttk.Button(
            card,
            text="Explore Section",
            command=lambda t=title, d=description, c=content:
                show_project_section(t, d, c)
        )

    card_button.pack(anchor="w", pady=(9, 0))


# ---------- Homepage footer ----------

home_footer = tk.Frame(
    home_frame,
    bg=FOREST,
    height=35
)

home_footer.pack(
    side="bottom",
    fill="x"
)

home_footer.pack_propagate(False)


tk.Label(
    home_footer,
    text="ADOPT TO ADAPT  |  ANALOG FORESTRY PROJECT",
    font=("Arial", 8, "bold"),
    fg="#DCEBDD",
    bg=FOREST
).pack(pady=9)


# ==========================================================
# 7. INVENTORY PAGE HEADER
# ==========================================================

inventory_header = tk.Frame(
    inventory_frame,
    bg=FOREST,
    height=75
)

inventory_header.pack(fill="x")
inventory_header.pack_propagate(False)


header_left = tk.Frame(
    inventory_header,
    bg=FOREST
)

header_left.pack(
    side="left",
    padx=25,
    pady=12
)


tk.Label(
    header_left,
    text="AF SITE SPECIES INVENTORY",
    font=("Arial", 18, "bold"),
    fg=WHITE,
    bg=FOREST
).pack(anchor="w")


tk.Label(
    header_left,
    text="ADOPT TO ADAPT  |  ANALOG FORESTRY",
    font=("Arial", 8, "bold"),
    fg="#C8D9CC",
    bg=FOREST
).pack(anchor="w")


home_button = ttk.Button(
    inventory_header,
    text="← Home",
    command=show_home
)

home_button.pack(
    side="right",
    padx=25,
    pady=20
)


# ==========================================================
# 8. DASHBOARD SUMMARY CARDS
# ==========================================================

summary_frame = tk.Frame(
    inventory_frame,
    bg=CREAM
)

summary_frame.pack(
    fill="x",
    padx=20,
    pady=(12, 5)
)

for column in range(4):
    summary_frame.columnconfigure(column, weight=1)


def create_summary_card(parent, title, value, column):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=15,
        pady=10
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=6,
        pady=4
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 9, "bold"),
        fg=TEXT_MUTED,
        bg=WHITE
    ).pack(anchor="w")

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 23, "bold"),
        fg=FOREST,
        bg=WHITE
    )

    value_label.pack(anchor="w", pady=(3, 0))

    return value_label


total_species_label = create_summary_card(
    summary_frame,
    "TOTAL SPECIES",
    "0",
    0
)

family_count_label = create_summary_card(
    summary_frame,
    "PLANT FAMILIES",
    "0",
    1
)

english_count_label = create_summary_card(
    summary_frame,
    "ENGLISH NAMES RECORDED",
    "0",
    2
)

ecology_count_label = create_summary_card(
    summary_frame,
    "ECOLOGICAL RECORDS",
    "0",
    3
)


# ==========================================================
# 9. DASHBOARD SUMMARY UPDATE
# ==========================================================

def update_dashboard_summary():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM af_site_species
    """)

    total_species = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT family)
        FROM af_site_species
        WHERE family IS NOT NULL
        AND TRIM(family) != ''
    """)

    family_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM af_site_species
        WHERE common_name_english IS NOT NULL
        AND TRIM(common_name_english) != ''
    """)

    english_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM af_site_species
        WHERE ecological_function IS NOT NULL
        AND TRIM(ecological_function) != ''
    """)

    ecology_count = cursor.fetchone()[0]

    connection.close()

    total_species_label.config(text=str(total_species))
    family_count_label.config(text=str(family_count))
    english_count_label.config(text=str(english_count))
    ecology_count_label.config(text=str(ecology_count))


# ==========================================================
# 10. PLANT FAMILY DISTRIBUTION CHART
# ==========================================================

chart_frame = tk.LabelFrame(
    inventory_frame,
    text="Plant Family Distribution",
    font=("Arial", 10, "bold"),
    fg=FOREST,
    bg=WHITE,
    padx=8,
    pady=5
)

chart_frame.pack(
    fill="x",
    expand=False,
    padx=20,
    pady=5
)


def create_family_chart(parent):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT family, COUNT(*)
        FROM af_site_species
        WHERE family IS NOT NULL
        AND TRIM(family) != ''
        GROUP BY family
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)

    results = cursor.fetchall()

    connection.close()

    figure = Figure(
        figsize=(10, 2.1),
        dpi=100
    )

    ax = figure.add_subplot(111)

    if results:

        families = [row[0] for row in results]
        counts = [row[1] for row in results]

        ax.barh(
            families[::-1],
            counts[::-1],
            color=FOREST_LIGHT
        )

        ax.set_xlabel(
            "Number of species",
            fontsize=8
        )

        ax.tick_params(
            axis="both",
            labelsize=8
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        figure.tight_layout()

    else:

        ax.text(
            0.5,
            0.5,
            "No family records available",
            ha="center",
            va="center"
        )

        ax.axis("off")

    chart_canvas = FigureCanvasTkAgg(
        figure,
        master=parent
    )

    chart_canvas.draw()

    chart_canvas.get_tk_widget().pack(
        fill="x",
        expand=False,
        padx=5,
        pady=3
    )


create_family_chart(chart_frame)


# ==========================================================
# 11. SEARCH SECTION
# ==========================================================

search_frame = tk.Frame(
    inventory_frame,
    bg=CREAM
)

search_frame.pack(
    fill="x",
    padx=25,
    pady=(8, 5)
)


tk.Label(
    search_frame,
    text="Search species:",
    font=("Arial", 10, "bold"),
    fg=TEXT_DARK,
    bg=CREAM
).pack(side="left", padx=(0, 8))


search_entry = ttk.Entry(
    search_frame,
    width=40,
    font=("Arial", 10)
)

search_entry.pack(
    side="left",
    padx=5
)


record_count_label = tk.Label(
    search_frame,
    text="",
    font=("Arial", 9),
    fg=TEXT_MUTED,
    bg=CREAM
)

record_count_label.pack(
    side="right",
    padx=10
)


# ==========================================================
# 12. SPECIES TABLE
# ==========================================================

table_frame = tk.Frame(
    inventory_frame,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(3, 12)
)


style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT_DARK,
    rowheight=27,
    fieldbackground=WHITE,
    font=("Arial", 9)
)

style.configure(
    "Treeview.Heading",
    background=FOREST,
    foreground=WHITE,
    font=("Arial", 9, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", FOREST_LIGHT)],
    foreground=[("selected", WHITE)]
)


columns = (
    "ID",
    "Botanical Name",
    "English Name",
    "Family"
)


species_tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)


species_tree.heading(
    "ID",
    text="ID"
)

species_tree.heading(
    "Botanical Name",
    text="Botanical Name"
)

species_tree.heading(
    "English Name",
    text="English Name"
)

species_tree.heading(
    "Family",
    text="Family"
)


species_tree.column(
    "ID",
    width=65,
    anchor="center"
)

species_tree.column(
    "Botanical Name",
    width=300
)

species_tree.column(
    "English Name",
    width=260
)

species_tree.column(
    "Family",
    width=220
)


vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=species_tree.yview
)

horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=species_tree.xview
)

species_tree.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


species_tree.grid(
    row=0,
    column=0,
    sticky="nsew"
)

vertical_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

horizontal_scrollbar.grid(
    row=1,
    column=0,
    sticky="ew"
)

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)


# ==========================================================
# 13. LOAD SPECIES
# ==========================================================

current_species_records = []


def load_species(search_text=""):

    global current_species_records

    for item in species_tree.get_children():
        species_tree.delete(item)

    current_species_records = get_species_records(search_text)

    for record in current_species_records:

        species_tree.insert(
            "",
            "end",
            values=record
        )

    record_count_label.config(
        text=f"{len(current_species_records)} species found"
    )


# ==========================================================
# 14. SEARCH FUNCTION
# ==========================================================

def search_species(event=None):

    search_text = search_entry.get().strip()

    load_species(search_text)


search_entry.bind(
    "<KeyRelease>",
    search_species
)


# ==========================================================
# 15. SPECIES DETAIL GROUPS
# ==========================================================

detail_groups = {

    "Basic Information": [
        ("Species ID", "species_id"),
        ("Serial Number", "sr_no"),
        ("Zone", "zone"),
        ("Family", "family"),
        ("Botanical Name", "botanical_name"),
        ("Sinhala Common Name", "common_name_sinhala"),
        ("English Common Name", "common_name_english"),
        ("Species Origin", "species_origin"),
        ("Analog Forestry Notation", "af_notation")
    ],

    "Growth and Ecological Characteristics": [
        ("Growth Rate", "growth_rate"),
        ("Uses", "uses"),
        ("Ecological Function", "ecological_function"),
        ("Propagation", "propagation"),
        ("Canopy Type", "canopy_type"),
        ("Flower Colour", "flower_color"),
        ("Flowering Time", "flowering_time"),
        ("Fruiting Time", "fruiting_time"),
        ("Fruit Type", "fruit_type"),
        ("Root Type", "root_type")
    ],

    "Environmental Requirements": [
        ("Preferred Soil", "preferred_soil"),
        ("Impact on Soil", "impact_on_soil"),
        ("Salinity Tolerance", "salinity_tolerance"),
        ("Drought Tolerance", "drought_tolerance"),
        ("Temperature Range", "temperature_range"),
        ("Light Preference", "light_preference"),
        ("Water Preference", "water_preference")
    ],

    "Conservation and Additional Data": [
        ("Conservation Status", "conservation_status"),
        ("Distribution", "distribution"),
        ("PB Cycle", "pb_cycle"),
        ("Weight of Photosynthetic Biomass", "weight_photosynthetic_biomass"),
        ("Leaf Length", "leaf_length"),
        ("Leaf Breadth", "leaf_breadth")
    ]
}


# ==========================================================
# 16. SPECIES DETAIL WINDOW
# ==========================================================

def view_species_details(event=None):

    selected_item = species_tree.selection()

    if not selected_item:

        messagebox.showinfo(
            "Select Species",
            "Please select a species from the table first."
        )

        return

    selected_values = species_tree.item(
        selected_item[0],
        "values"
    )

    species_id = selected_values[0]

    open_species_details(species_id)


def open_species_details(species_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM af_site_species
        WHERE species_id = ?
    """, (species_id,))

    record = cursor.fetchone()

    if record is None:

        connection.close()

        messagebox.showerror(
            "Species Not Found",
            "The selected species could not be found."
        )

        return

    column_names = [
        description[0]
        for description in cursor.description
    ]

    connection.close()

    species_data = dict(
        zip(column_names, record)
    )

    # Detail window

    detail_window = tk.Toplevel(root)

    detail_window.title(
        "Species Profile - " +
        str(species_data.get("botanical_name") or "")
    )

    detail_window.geometry("1050x720")
    detail_window.minsize(850, 550)
    detail_window.configure(bg=CREAM)

    # Header

    detail_header = tk.Frame(
        detail_window,
        bg=FOREST,
        height=85
    )

    detail_header.pack(fill="x")
    detail_header.pack_propagate(False)

    tk.Label(
        detail_header,
        text=species_data.get("botanical_name") or "Species Profile",
        font=("Arial", 19, "bold"),
        fg=WHITE,
        bg=FOREST
    ).pack(anchor="w", padx=25, pady=(13, 0))

    tk.Label(
        detail_header,
        text=species_data.get("common_name_english") or "",
        font=("Arial", 10),
        fg="#D7C49B",
        bg=FOREST
    ).pack(anchor="w", padx=27)

    # Main content

    main_content = tk.Frame(
        detail_window,
        bg=CREAM
    )

    main_content.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=12
    )

    # Left photograph panel

    photo_panel = tk.Frame(
        main_content,
        bg=WHITE,
        width=260,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    photo_panel.pack(
        side="left",
        fill="y",
        padx=(0, 12)
    )

    photo_panel.pack_propagate(False)

    tk.Label(
        photo_panel,
        text="SPECIES PHOTOGRAPH",
        font=("Arial", 10, "bold"),
        fg=FOREST,
        bg=WHITE
    ).pack(pady=(18, 10))

    photo_label = tk.Label(
        photo_panel,
        text="Photograph not available",
        font=("Arial", 10),
        fg=TEXT_MUTED,
        bg="#EDF1EC",
        width=25,
        height=12
    )

    photo_label.pack(
        padx=15,
        pady=10
    )

    photo_path = os.path.join(
        IMAGE_FOLDER,
        f"{species_id}.jpg"
    )

    if os.path.exists(photo_path):

        try:

            photo = Image.open(photo_path)

            photo.thumbnail(
                (220, 260),
                Image.Resampling.LANCZOS
            )

            photo_image = ImageTk.PhotoImage(photo)

            photo_label.config(
                image=photo_image,
                text="",
                width=photo_image.width(),
                height=photo_image.height()
            )

            photo_label.image = photo_image

        except Exception as error:

            print("Photo loading error:", error)

    tk.Label(
        photo_panel,
        text="BOTANICAL NAME",
        font=("Arial", 8, "bold"),
        fg=TEXT_MUTED,
        bg=WHITE
    ).pack(pady=(15, 3))

    tk.Label(
        photo_panel,
        text=species_data.get("botanical_name") or "Not recorded",
        font=("Arial", 11, "italic", "bold"),
        fg=FOREST,
        bg=WHITE,
        wraplength=220,
        justify="center"
    ).pack(padx=10)

    tk.Label(
        photo_panel,
        text="FAMILY",
        font=("Arial", 8, "bold"),
        fg=TEXT_MUTED,
        bg=WHITE
    ).pack(pady=(15, 3))

    tk.Label(
        photo_panel,
        text=species_data.get("family") or "Not recorded",
        font=("Arial", 11, "bold"),
        fg=FOREST_LIGHT,
        bg=WHITE
    ).pack()

    # Right details panel

    details_panel = tk.Frame(
        main_content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    details_panel.pack(
        side="right",
        fill="both",
        expand=True
    )

    details_canvas = tk.Canvas(
        details_panel,
        bg=WHITE,
        highlightthickness=0
    )

    details_scrollbar = ttk.Scrollbar(
        details_panel,
        orient="vertical",
        command=details_canvas.yview
    )

    details_canvas.configure(
        yscrollcommand=details_scrollbar.set
    )

    details_scrollbar.pack(
        side="right",
        fill="y"
    )

    details_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    details_content = tk.Frame(
        details_canvas,
        bg=WHITE
    )

    canvas_window = details_canvas.create_window(
        (0, 0),
        window=details_content,
        anchor="nw"
    )

    def update_scroll_region(event=None):

        details_canvas.configure(
            scrollregion=details_canvas.bbox("all")
        )

    def resize_details_content(event):

        details_canvas.itemconfigure(
            canvas_window,
            width=event.width
        )

    details_content.bind(
        "<Configure>",
        update_scroll_region
    )

    details_canvas.bind(
        "<Configure>",
        resize_details_content
    )

    # Display grouped information

    for group_title, fields in detail_groups.items():

        group_frame = tk.Frame(
            details_content,
            bg=WHITE,
            padx=18,
            pady=10
        )

        group_frame.pack(
            fill="x",
            padx=5,
            pady=4
        )

        tk.Label(
            group_frame,
            text=group_title.upper(),
            font=("Arial", 11, "bold"),
            fg=FOREST,
            bg=WHITE
        ).pack(anchor="w", pady=(3, 8))

        tk.Frame(
            group_frame,
            bg=GOLD,
            height=2
        ).pack(fill="x", pady=(0, 8))

        for label_text, field_name in fields:

            value = species_data.get(field_name)

            if value is None or str(value).strip() == "":
                value = "Not recorded"

            field_row = tk.Frame(
                group_frame,
                bg=WHITE
            )

            field_row.pack(
                fill="x",
                pady=4
            )

            field_row.columnconfigure(1, weight=1)

            tk.Label(
                field_row,
                text=label_text,
                font=("Arial", 9, "bold"),
                fg=TEXT_MUTED,
                bg=WHITE,
                width=30,
                anchor="nw"
            ).grid(
                row=0,
                column=0,
                sticky="nw",
                padx=(0, 8)
            )

            tk.Label(
                field_row,
                text=str(value),
                font=("Arial", 9),
                fg=TEXT_DARK,
                bg=WHITE,
                wraplength=450,
                justify="left",
                anchor="nw"
            ).grid(
                row=0,
                column=1,
                sticky="nw"
            )

    # Previous and Next navigation

    navigation_frame = tk.Frame(
        detail_window,
        bg=CREAM
    )

    navigation_frame.pack(
        fill="x",
        padx=15,
        pady=(0, 12)
    )

    def navigate_species(direction):

        current_ids = [
            str(record[0])
            for record in current_species_records
        ]

        current_id = str(species_id)

        if current_id not in current_ids:
            return

        current_index = current_ids.index(current_id)

        new_index = current_index + direction

        if 0 <= new_index < len(current_ids):

            new_id = current_ids[new_index]

            detail_window.destroy()

            open_species_details(new_id)

    ttk.Button(
        navigation_frame,
        text="← Previous Species",
        command=lambda: navigate_species(-1)
    ).pack(side="left", padx=5)

    ttk.Button(
        navigation_frame,
        text="Next Species →",
        command=lambda: navigate_species(1)
    ).pack(side="left", padx=5)

    ttk.Button(
        navigation_frame,
        text="Close",
        command=detail_window.destroy
    ).pack(side="right", padx=5)


# ==========================================================
# 17. OPEN SPECIES DETAILS
# ==========================================================

species_tree.bind(
    "<Double-1>",
    view_species_details
)


details_button = ttk.Button(
    search_frame,
    text="View Species Details",
    command=view_species_details
)

details_button.pack(
    side="left",
    padx=10
)


# ==========================================================
# 18. START APPLICATION
# ==========================================================

load_species()

update_dashboard_summary()

home_frame.pack(
    fill="both",
    expand=True
)

root.mainloop()