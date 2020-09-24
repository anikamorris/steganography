from PIL import Image, ImageDraw, ImageChops


def decode_image(path_to_png):
    """
    Input: String
    Output: None
    Takes an image, isolates the red channel and creates a new image
    in black and white based on the least significant bit of each
    pixel in the original image (if LSB is 0, new image's 
    corresponding pixel will be black, otherwise it will be white).
    Saves resulting image to filesystem.
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
    decoded_image.save("decoded_image.png")


def encode_image(path_to_png, text_to_write):
    """
    Input: path_to_png: String, text_to_write: String
    Output: None
    Encodes a secret message in the red channel of a copy of the inputted 
    image and saves to filesystem.
    """
    # Open the image using PIL:
    base_image = Image.open(path_to_png)
    # Create a new image to write to
    new_image = Image.new("RGB", base_image.size)

    # Separate the red channel from the rest of the image:
    base_red_channel = base_image.getchannel(0)
    green_channel = base_image.getchannel(1)
    blue_channel = base_image.getchannel(2)

    # create image from text with same size as base image
    x_size, y_size = base_image.size
    secret_img = write_text(text_to_write, (x_size, y_size))

    # loop through x_size, y_size
    for x in range(x_size):
        for y in range(y_size):
            # get all channel values for pixel at (x, y)
            red_pixel = base_red_channel.getpixel((x,y))
            green_pixel = green_channel.getpixel((x,y))
            blue_pixel = blue_channel.getpixel((x,y))
            # set new image's pixel value at (x, y) to be the same as base
            new_image.putpixel((x,y), (red_pixel, green_pixel, blue_pixel))
            # if red channel pixel is odd
            if red_pixel % 2 == 1:
                # make it even
                red_pixel -= 1
                # reset new images's x,y pixel to new value
                new_image.putpixel((x,y), (red_pixel, green_pixel, blue_pixel))
    
     # add our new image and secret image together
    encoded_image = ImageChops.add(new_image, secret_img)
            
    encoded_image.save("encoded_house_image.png")
            


def write_text(text_to_write, image_size):
    """
    Input: text_to_write: String, image_size: Tuple
    Output: Image
    Takes a string and creates an image with that string included in the red channel
    """
    # create an image
    out = Image.new("RGB", image_size, (1,0,0))

    # get a drawing context
    d = ImageDraw.Draw(out)

    # draw multiline text
    d.multiline_text((10,10), text_to_write, fill=(0, 0, 0))

    return out
    


if __name__ == "__main__":
    encode_image("house.png", "known some call is air am")
    decode_image("encoded_house_image.png")