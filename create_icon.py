from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Create an image with transparent background
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a rounded rectangle (or circle) background
    bg_color = (0, 122, 204, 255) # VS Code Blue / Modern Blue
    # draw.ellipse((20, 20, 236, 236), fill=bg_color)
    draw.rounded_rectangle((20, 20, 236, 236), radius=40, fill=bg_color)

    # Draw text "K/L"
    try:
        # Try to load a font, fallback to default
        font = ImageFont.truetype("arial.ttf", 100)
    except IOError:
        font = ImageFont.load_default()

    text = "K/L"
    
    # Calculate text size using font.getbbox or textbbox (newer pillow)
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width, text_height = draw.textsize(text, font=font)

    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2 - 10 # slightly adjust up for visual center

    draw.text((x, y), text, font=font, fill="white")

    # Save as .ico
    image.save("icon.ico", format='ICO', sizes=[(256, 256)])
    print("icon.ico created successfully.")

if __name__ == "__main__":
    create_icon()
