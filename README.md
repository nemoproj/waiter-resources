# waiter-resources

> [!NOTE]
> this tool was developed for use in `ac`.
> 
> credit: kestrel@alphacorp

minecraft resource pack creation utility for custom sprites, supporting both java and bedrock editions.

## overview

this resource pack provides custom font-based sprites for minecraft servers. it supports both java (post 1.16) and bedrock editions.

## features

- dual platform support (java + bedrock)
- custom sprite integration via font system
- automated build process for both platforms

## directory structure

```
.
├── assets/            # resource pack assets
│   ├── bedrock/      # bedrock-specific assets
│   └── java/         # java-specific assets
├── images/           # source sprite images
├── src/              # build scripts
│   ├── bedrock/      # bedrock build system
│   └── java/         # java build system
└── build/            # compiled resource packs
```

## building

### requirements
- python 3.x
- pillow (python imaging library)

### commands
- java edition: `python src/java/build.py`
- bedrock edition: `python src/bedrock/build.py`

builds will be generated in the `build/` directory with timestamps.

## installation

### java edition
1. locate the generated zip file in `build/java/`
2. copy to `.minecraft/resourcepacks/`
3. activate in minecraft's resource packs menu

### bedrock edition
1. locate the generated mcpack file in `build/bedrock/`
2. open the file on your device
3. import into minecraft
4. enable in global resources

## usage

use in minecraft titles with this command:

```
/title @a title {"text":"\u+defined_unicode_character"}
```

## technical details

### sprite loading

#### java edition
sprites are loaded through the font system using bitmap providers in `assets/java/minecraft/font/default.json`:
- each sprite is defined as a separate bitmap provider
- sprites use 128x128 pixel dimensions
- configuration includes:
  - type: "bitmap"
  - file: path to the sprite
  - ascent: 64 (vertical positioning)
  - height: 128 (sprite height)
  - chars: unicode character mapping

example configuration:
```json
{
  "type": "bitmap",
  "file": "minecraft:font/debug.png",
  "ascent": 64,
  "height": 128,
  "chars": [""]
}
```

#### bedrock edition
sprites are combined into a single sprite sheet:
- sheet dimensions: 2048x2048 pixels
- grid layout: 16x16 cells
- cell size: 128x128 pixels
- file name: `glyph_A0.png`

sprite positions in sheet:
- debug: (0, 0)
- debug_white: (0, 1)
- startup: (0, 2)
- startup_white: (0, 3)

### adding new sprites

#### java edition
1. add sprite png to `images/font/`
2. add bitmap provider entry in `assets/java/minecraft/font/default.json`
3. run java build script

#### bedrock edition
1. add sprite png to `images/font/`
2. add position mapping in `src/bedrock/build.py`
3. run bedrock build script to generate new sprite sheet
