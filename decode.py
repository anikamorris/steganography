from PIL import Image, ImageDraw, ImageChops


def decode_image(path_to_png):
    """
    Input: String
    Output: None
    Takes an image, isolates the red channel and creates a new image
    in black and white based on the least significant bit of each
    pixel in the original image (if LSB is 0, new image's 
    corresponding pixel will be black, otherwise it will be white).
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    # loop through x_size, y_size
    for x in range(x_size):
        for y in range(y_size):
            # convert each red channel pixel value to binary string
            binary = bin(red_channel.getpixel((x,y)))
            # check if string ends in 0 or 1
            count = len(binary)
            lsb = binary[count-1]
            # ends in 0, pixel at x_size, y_size = black
            if lsb == "0":
                decoded_image.putpixel((x,y), (0,0,0))
            # ends in 1, pixels at x_size, y_size = white
            else:
                decoded_image.putpixel((x,y), (255,255,255))
    
    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_hills_image.png")


def encode_image(path_to_png):
    """
    TODO: Add docstring and complete implementation.
    """
    # Open the image using PIL:
    base_image = Image.open(path_to_png)
    # Create a new image to write to
    encoded_image = Image.new("RGB", base_image.size)

    # Separate the red channel from the rest of the image:
    base_red_channel = base_image.split()[0]
    green_channel = base_image.split()[1]
    blue_channel = base_image.split()[2]

    # Create a new PIL image with the same size as the encoded image:
    pixels = base_image.load()
    x_size, y_size = base_image.size

    secret_img = write_text("hello", (x_size, y_size))
    text_red_channel = Image.open("text_image.png").split()[0]

    # loop through x_size, y_size
    for x in range(x_size):
        for y in range(y_size):
            red_pixel = base_red_channel.getpixel((x,y))
            green_pixel = green_channel.getpixel((x,y))
            blue_pixel = blue_channel.getpixel((x,y))
            encoded_image.putpixel((x,y), (red_pixel, green_pixel, blue_pixel))
            if red_pixel % 2 == 1:
                red_pixel -= 1
                encoded_image.putpixel((x,y), (red_pixel, green_pixel, blue_pixel))
            new_image = ImageChops.add(encoded_image, secret_img)
            
    new_image.save("encoded_image.png")
            


def write_text(text_to_write, image_size):
    """
    TODO: Add docstring and complete implementation.
    """
    # create an image
    out = Image.new("RGB", image_size, (1,0,0))

    # get a drawing context
    d = ImageDraw.Draw(out)

    # draw multiline text
    d.multiline_text((10,10), text_to_write, fill=(0, 0, 0))

    return out
    


if __name__ == "__main__":
    encode_image("hills.png")
    decode_image("encoded_image.png")