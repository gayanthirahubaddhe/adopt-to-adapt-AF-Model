# ADOPT TO ADAPT
## Analog Forestry Model Information System

**Restoration of Mid-Country Forest Ecosystems through Analog Forestry in Mariland Estate, Sri Lanka**

---

## 1. Project Overview

ADOPT TO ADAPT is an Analog Forestry initiative focused on exploring ecological restoration, plant diversity and sustainable landscape management in the Upper Knuckles foothills of Sri Lanka.

This project explores the potential of Analog Forestry as an ecological restoration approach for mid-country forest ecosystems. It focuses on understanding plant diversity, ecological functions, forest structure and the integration of useful plant species within restoration landscapes.

To support project documentation and biodiversity information management, a dedicated desktop-based **Analog Forestry Model Information System** has been developed using Python.

The system provides a structured platform for recording, organizing, searching and exploring plant species information associated with the Analog Forestry project.

## 2. Project Location

**Study Area:** Mariland Estate, Beddegama, Panwila, Kandy, Central Province, Sri Lanka.

The project is situated in the Upper Knuckles foothills, a landscape of ecological importance within Sri Lanka's central highlands.

The initiative explores opportunities for restoring mid-country forest ecosystems through forest-inspired land management and biodiversity conservation.

## 3. Project Objectives

The main objectives are:

- Explore Analog Forestry as an ecological restoration approach.
- Document plant species diversity within the Analog Forestry project site.
- Organize botanical and ecological information into a structured database.
- Develop a digital information system for plant inventory management.
- Support the understanding of plant ecological functions and restoration strategies.
- Establish a foundation for future biodiversity monitoring and research.

## 4. Analog Forestry Information System

The ADOPT TO ADAPT desktop application was developed to support the organization and exploration of plant inventory information.

### Main Features

**Interactive Dashboard**
- Dedicated homepage introducing the Analog Forestry initiative.
- Project overview and information sections.
- Summary statistics and plant family visualization.
- Navigation to the plant inventory.

**AF Site Plant Inventory**
- Structured species inventory containing 117 recorded plant species.
- Searchable species records.
- Botanical names, English names and plant families.
- Species identification through a four-column inventory table.

**Species Details Window**

A dedicated species information window provides access to additional recorded information, including:

- Basic botanical information.
- Growth characteristics.
- Ecological functions.
- Environmental requirements.
- Conservation and additional information.
- Optional species photographs.
- Previous and next species navigation.

**Database Management**

The application uses an SQLite database to organize and retrieve plant inventory records.

## 5. Technology Stack

| Technology | Application |
|---|---|
| Python | Application development |
| Tkinter | Graphical user interface |
| SQLite | Database management |
| Matplotlib | Data visualization |
| Pillow (PIL) | Image processing and display |
| PyCharm | Development environment |

## 6. Project Structure

```text
ADOPT-TO-ADAPT/
│
├── af_inventory.py
├── database.py
├── Logo.png
│
├── images/
│   └── landscape.jpg
│
├── plant_images/
│   └── Species photographs
│
├── db_storage/
│   └── analog_forestry.db
│
├── README.md
└── requirements.txt
```

*The database and supporting files may be maintained separately from the public source-code repository.*

## 7. Installation and Setup

### Requirements

- Python 3.10 or later recommended.
- Pillow
- Matplotlib

Tkinter and SQLite are included with most standard Python installations.

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project directory

```bash
cd ADOPT-TO-ADAPT
```

### Step 3: Install required packages

```bash
pip install -r requirements.txt
```

### Step 4: Prepare the project files

Ensure that the required SQLite database is available in the expected location and that the image folders and logo are present.

### Step 5: Run the application

```bash
python af_inventory.py
```

## 8. Future Development

The current application establishes the foundation for a broader Analog Forestry information-management platform.

Potential future developments include:

- Natural Forest Species Inventory.
- Expanded plant species photographic documentation.
- Advanced biodiversity data visualization.
- Geographical visualization of plant distribution.
- Ecological and functional plant classification.
- Integration with GIS and remote-sensing datasets.
- Improved biodiversity monitoring and reporting capabilities.
- Web-based access to project information.

## 9. Project Significance

The ADOPT TO ADAPT initiative brings together ecological restoration, biodiversity documentation and digital information management.

By developing a dedicated plant inventory system, the project aims to improve the accessibility and organization of botanical and ecological information while supporting future research and restoration planning.

The information system is intended to evolve alongside the Analog Forestry initiative, providing a foundation for documenting and understanding plant diversity within restoration landscapes.

## 10. Acknowledgements

This project forms part of the ADOPT TO ADAPT Analog Forestry initiative in Mariland Estate, Sri Lanka.

The initiative acknowledges the importance of collaborative learning, ecological knowledge, biodiversity conservation and community engagement in developing sustainable restoration landscapes.

---

**Project:** ADOPT TO ADAPT – Analog Forestry Initiative  
**Location:** Mariland Estate, Beddegama, Panwila, Kandy, Sri Lanka  
**Information System:** Analog Forestry Model Information System  
**Developer:** Gayanthi Rahubaddhe

*An initiative towards restoring landscapes, reconnecting biodiversity and supporting sustainable forest ecosystems.* 🌿
