# Icon Placeholders

The browser extension needs icons in the following sizes:
- icon16.png (16x16 pixels)
- icon48.png (48x48 pixels)  
- icon128.png (128x128 pixels)

## Creating Icons

You can create icons using:
1. **Online tools**: favicon.io, canva.com
2. **Graphics software**: GIMP, Photoshop, Figma
3. **AI generators**: Generate shield/security themed icons

## Suggested Design

- Theme: Shield or scan symbol
- Colors: Blue/green for security
- Simple, recognizable at small sizes
- Transparent background

## Quick Solution

For now, you can use simple colored squares or generate icons at:
https://favicon.io/favicon-generator/

Or use this Python script to generate basic placeholders:

```python
from PIL import Image, ImageDraw

sizes = [16, 48, 128]
for size in sizes:
    img = Image.new('RGB', (size, size), color='#0066cc')
    draw = ImageDraw.Draw(img)
    # Add a simple shield shape
    img.save(f'icon{size}.png')
```

Temporary workaround: Create blank PNG files or copy any existing icon and rename them.
