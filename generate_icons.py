"""
Generate placeholder icons for the browser extension
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with shield symbol"""
    # Create image with blue background
    img = Image.new('RGBA', (size, size), color=(0, 102, 204, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple shield shape
    shield_color = (255, 255, 255, 255)
    margin = size // 8
    
    # Shield outline (simplified)
    points = [
        (size//2, margin),  # Top center
        (size - margin, margin + size//4),  # Top right
        (size - margin, size - margin*2),  # Bottom right
        (size//2, size - margin),  # Bottom center
        (margin, size - margin*2),  # Bottom left
        (margin, margin + size//4),  # Top left
    ]
    
    draw.polygon(points, fill=shield_color)
    
    # Save
    img.save(filename, 'PNG')
    print(f"Created {filename}")

def main():
    # Get the icons directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(script_dir, 'browser-extension', 'icons')
    
    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate icons in required sizes
    sizes = [16, 48, 128]
    
    for size in sizes:
        filename = os.path.join(icons_dir, f'icon{size}.png')
        create_icon(size, filename)
    
    print("\n✅ All icons created successfully!")
    print(f"Location: {icons_dir}")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("Error: Pillow not installed")
        print("Install with: pip install Pillow")
        print("\nAlternatively, create your own PNG icons manually")
