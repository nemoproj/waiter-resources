#!/usr/bin/env python3
import os
import zipfile
from datetime import datetime
import shutil

# Define base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images", "font")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build", "java")

# Define asset paths
JAVA_DIR = os.path.join(ASSETS_DIR, "java")

# Ensure build directory exists
os.makedirs(BUILD_DIR, exist_ok=True)

def create_java_pack():
    """Package the Java resource pack.
    The resulting pack will have:
    - pack.mcmeta at the root
    - assets/ac/font/default.json for font mapping
    - assets/ac/textures/font/*.png for the actual glyphs"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pack_name = f"waiter_resources_java_{timestamp}.zip"
    pack_path = os.path.join(BUILD_DIR, pack_name)

    with zipfile.ZipFile(pack_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add pack.mcmeta from project root
        mcmeta_path = os.path.join(PROJECT_ROOT, "pack.mcmeta")
        if os.path.exists(mcmeta_path):
            print("Adding pack.mcmeta")
            zipf.write(mcmeta_path, "pack.mcmeta")
        else:
            print("Warning: pack.mcmeta not found at project root!")

        # Add font mapping from assets/java/ac/font/default.json
        font_json = os.path.join(JAVA_DIR, "ac", "font", "default.json")
        if os.path.exists(font_json):
            target_path = os.path.join("assets", "ac", "font", "default.json")
            print(f"Adding {target_path}")
            zipf.write(font_json, target_path)

        # Add textures under assets/ac/textures/font
        if os.path.exists(IMAGES_DIR):
            for file in os.listdir(IMAGES_DIR):
                if file.endswith('.png'):
                    file_path = os.path.join(IMAGES_DIR, file)
                    # Create path like assets/ac/textures/font/debug.png
                    target_path = os.path.join("assets", "ac", "textures", "font", file)
                    print(f"Adding {target_path}")
                    zipf.write(file_path, target_path)

    print(f"\nCreated Java resource pack: {pack_name}")
    print("\nTo install:")
    print(f"1. Copy {pack_name} to your .minecraft/resourcepacks folder")
    print("2. Enable the pack in Minecraft's Resource Packs menu")
    print("\nTo use in titles:")
    print('Debug:        /title @a title {"text":"\\uE000"}')
    print('Debug White:  /title @a title {"text":"\\uE001"}')
    print('Startup:      /title @a title {"text":"\\uE002"}')
    print('Startup White:/title @a title {"text":"\\uE003"}')
    return pack_path

def main():
    create_java_pack()

if __name__ == "__main__":
    main()