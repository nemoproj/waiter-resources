#!/usr/bin/env python3
import os, json, shutil
from PIL import Image, ImageOps
import zipfile
from datetime import datetime

# Define base directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UI_JSON = os.path.join(BASE_DIR, "ui", "_global_variables.json")
TEXTURES_DIR = os.path.join(BASE_DIR, "textures", "font")
OUTPUT_FONT_DIR = os.path.join(BASE_DIR, "font")

CELL_SIZE = 128      # Each glyph cell size (128x128)
GRID_SIZE = 16       # 16x16 grid of cells
SHEET_SIZE = CELL_SIZE * GRID_SIZE  # 2048x2048

def create_sprite_sheet():
    """Create a new transparent sprite sheet of size 2048x2048 (16x16 grid of 128x128 cells)."""
    # Create a new transparent image with the desired dimensions
    image = Image.new('RGBA', (SHEET_SIZE, SHEET_SIZE), (0, 0, 0, 0))
    return image

def add_sprite_to_sheet(sheet, sprite_path, position):
    """Add a sprite to the sheet at the specified position (row, col) using a 128x128 cell."""
    try:
        with Image.open(sprite_path) as sprite:
            # Force the sprite to fill exactly a 128x128 cell (cropping if necessary)
            fitted_sprite = ImageOps.fit(sprite, (CELL_SIZE, CELL_SIZE), method=Image.LANCZOS)
            # Calculate the cell's top-left coordinates
            cell_x = position[1] * CELL_SIZE
            cell_y = position[0] * CELL_SIZE
            # Paste the fitted sprite onto the sheet
            sheet.paste(fitted_sprite, (cell_x, cell_y), fitted_sprite.convert('RGBA'))
    except Exception as e:
        print(f"Error processing sprite {sprite_path}: {e}")

def create_mcpack():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mcpack_name = f"waiter_resources_{timestamp}.mcpack"
    mcpack_path = os.path.join(BASE_DIR, "..", mcpack_name)

    with zipfile.ZipFile(mcpack_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        required_files = [
            "manifest.json",
            "font",  # Directory containing glyph files
            "ui"     # Directory containing UI definitions
        ]

        for item in required_files:
            item_path = os.path.join(BASE_DIR, item)
            if os.path.isfile(item_path):
                zipf.write(item_path, item)
            elif os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, BASE_DIR)
                        print(f"Adding to mcpack: {rel_path}")
                        zipf.write(file_path, rel_path)

    print(f"\nCreated {mcpack_name}")
    return mcpack_path

def update_manifest():
    manifest_path = os.path.join(BASE_DIR, "manifest.json")
    manifest = {
        "format_version": 2,
        "header": {
            "description": "Custom Sprites Resource Pack",
            "name": "Waiter Resources",
            "uuid": "4c966fa9-9883-487a-a0cf-9851d3216089",
            "version": [0, 0, 3],
            "min_engine_version": [1, 16, 0]
        },
        "modules": [
            {
                "description": "Custom Sprites",
                "type": "resources",
                "uuid": "e6f07494-df6b-41e8-a3ed-e9057c70adb7",
                "version": [0, 0, 3]
            }
        ]
    }

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def main():
    # Create output directory for the font if it doesn't exist
    os.makedirs(OUTPUT_FONT_DIR, exist_ok=True)

    # Create a new sprite sheet of size 2048x2048
    sheet_e0 = create_sprite_sheet()

    # Define sprite positions in the 16x16 grid. Each position = (row, col)
    sprite_positions = {
        "debug": (0, 0),        # \uE000
        "debug_white": (0, 1),    # \uE001
        "startup": (0, 2),        # \uE002
        "startup_white": (0, 3)   # \uE003
    }

    # For each custom glyph, add it to the sprite sheet
    for key, pos in sprite_positions.items():
        src_path = os.path.join(BASE_DIR, "textures", "font", key + ".png")
        if not os.path.isfile(src_path):
            print(f"Source file not found: {src_path}")
            continue
        add_sprite_to_sheet(sheet_e0, src_path, pos)

    # Save the sprite sheet as glyph_E0.png in the OUTPUT_FONT_DIR
    output_sheet_path = os.path.join(OUTPUT_FONT_DIR, "glyph_E0.png")
    sheet_e0.save(output_sheet_path)
    print(f"Sprite sheet created and saved to {output_sheet_path}!")

    # Update the manifest
    update_manifest()

    # Create the mcpack
    mcpack_path = create_mcpack()
    print("\nResource pack is ready to use!")
    print("To install:")
    print(f"1. Copy {os.path.basename(mcpack_path)} to your device")
    print("2. Open the file on your device to import it into Minecraft")
    print("3. Enable the pack in Global Resources")
    print("\nTo use in custom UI:")
    print("Debug Sprite: \uE000")
    print("Debug White: \uE001")
    print("Startup: \uE002")
    print("Startup White: \uE003")

if __name__ == "__main__":
    main()