
import sqlite3
import os

# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database storage folder
DATABASE_FOLDER = os.path.join(BASE_DIR, "db_storage")

# Database file
DATABASE_PATH = os.path.join(
    DATABASE_FOLDER,
    "analog_forestry.db"
)


def create_connection():

    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def create_tables():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS af_site_species (
        species_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_excel_row INTEGER UNIQUE,
        sr_no INTEGER,
        zone TEXT,
        family TEXT,
        botanical_name TEXT,
        common_name_sinhala TEXT,
        common_name_english TEXT,
        species_origin TEXT,
        af_notation TEXT,
        growth_rate TEXT,
        uses TEXT,
        ecological_function TEXT,
        propagation TEXT,
        canopy_type TEXT,
        flower_color TEXT,
        flowering_time TEXT,
        fruiting_time TEXT,
        fruit_type TEXT,
        root_type TEXT,
        preferred_soil TEXT,
        impact_on_soil TEXT,
        salinity_tolerance TEXT,
        drought_tolerance TEXT,
        temperature_range TEXT,
        light_preference TEXT,
        water_preference TEXT,
        conservation_status TEXT,
        distribution TEXT,
        pb_cycle TEXT,
        weight_photosynthetic_biomass TEXT,
        leaf_length TEXT,
        leaf_breadth TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS natural_forest_species (
        species_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_excel_row INTEGER UNIQUE,
        serial_no INTEGER,
        family TEXT,
        botanical_name TEXT,
        sinhala_common_name TEXT,
        english_common_name TEXT,
        growth_form TEXT,
        af_notation TEXT,
        forest_layer_ecological_role TEXT,
        ecological_function TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS source_notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_sheet TEXT,
        source_excel_row INTEGER,
        row_data_json TEXT,
        UNIQUE(source_sheet, source_excel_row)
    )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_tables()
