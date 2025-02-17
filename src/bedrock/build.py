#!/usr/bin/env python3
import os, json, shutil
from PIL import Image, ImageOps
import zipfile
from datetime import datetime

# Define base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images", "font")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build", "bedrock")

# Define asset paths
BEDROCK_DIR = os.path.join(ASSETS_DIR, "bedrock")
FONT_DIR = os.path.join(BEDROCK_DIR, "font")

# Ensure directories exist
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)

CELL_SIZE = 128      # Each glyph cell size (128x128)
GRID_SIZE = 16       # 16x16 grid of cells
SHEET_SIZE = CELL_SIZE * GRID_SIZE  # 2048x2048

def create_sprite_sheet():
    """Create a new transparent sprite sheet of size 2048x2048 (16x16 grid of 128x128 cells)."""
    image = Image.new('RGBA', (SHEET_SIZE, SHEET_SIZE), (0, 0, 0, 0))
    return image

def add_sprite_to_sheet(sheet, sprite_path, position):
    """Add a sprite to the sheet at the specified position (row, col) using a 128x128 cell."""
    try:
        with Image.open(sprite_path) as sprite:
            fitted_sprite = ImageOps.fit(sprite, (CELL_SIZE, CELL_SIZE), method=Image.LANCZOS)
            cell_x = position[1] * CELL_SIZE
            cell_y = position[0] * CELL_SIZE
            sheet.paste(fitted_sprite, (cell_x, cell_y), fitted_sprite.convert('RGBA'))
    except Exception as e:
        print(f"Error processing sprite {sprite_path}: {e}")

def create_mcpack():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Rename the generated glyph sheet to glyph_A0.png to reflect \uA codepoints
    mcpack_name = f"waiter_resources_bedrock_{timestamp}.mcpack"
    mcpack_path = os.path.join(BUILD_DIR, mcpack_name)

    with zipfile.ZipFile(mcpack_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add manifest.json
        manifest_path = os.path.join(BEDROCK_DIR, "manifest.json")
        if os.path.exists(manifest_path):
            zipf.write(manifest_path, "manifest.json")
            print(f"Adding to mcpack: manifest.json")

        # Add font directory
        if os.path.exists(FONT_DIR):
            for root, _, files in os.walk(FONT_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, BEDROCK_DIR)
                    print(f"Adding to mcpack: {rel_path}")
                    zipf.write(file_path, rel_path)

    print(f"\nCreated {mcpack_name}")
    return mcpack_path

def update_manifest():
    manifest_path = os.path.join(BEDROCK_DIR, "manifest.json")
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
    sheet = create_sprite_sheet()
    sprite_positions = {
        "debug": (0, 0),        # intended for \uA000
        "debug_white": (0, 1),    # intended for \uA001
        "startup": (0, 2),        # intended for \uA002
        "startup_white": (0, 3)   # intended for \uA003
    }

    for key, pos in sprite_positions.items():
        src_path = os.path.join(IMAGES_DIR, f"{key}.png")
        if not os.path.isfile(src_path):
            print(f"Source file not found: {src_path}")
            continue
        add_sprite_to_sheet(sheet, src_path, pos)

    output_sheet_path = os.path.join(FONT_DIR, "glyph_A0.png")
    sheet.save(output_sheet_path)
    print(f"Sprite sheet created and saved to {output_sheet_path}!")

    update_manifest()

    mcpack_path = create_mcpack()
    print("\nResource pack is ready to use!")
    print("To install:")
    print(f"1. Copy {os.path.basename(mcpack_path)} to your device")
    print("2. Open the file on your device to import it into Minecraft")
    print("3. Enable the pack in Global Resources")
    print("\nTo use in titles:")
    print('Debug:        /title @a title {"text":"\\uA000"}')
    print('Debug White:  /title @a title {"text":"\\uA001"}')
    print('Startup:      /title @a title {"text":"\\uA002"}')
    print('Startup White:/title @a title {"text":"\\uA003"}')

if __name__ == "__main__":
    main()