from PIL import Image


def convert_image_to_ascii(file):
    try:
        im = Image.open(file)
        print("Successfully loaded image")
    except FileNotFoundError:
        print("Unable to load image")
        return

    print(im.size)
    im.resize((round(im.size[0] * 0.25), round(im.size[1] * 0.25)))
    print("Resized: ", im.size)
    img = im.convert('RGB')

    pixels = [[0]*im.size[1] for i in range(im.size[0])]
    rgb = [[0]*im.size[1] for i in range(im.size[0])]

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixels[x][y] = im.getpixel((x, y))
            rgb[x][y] = im.getpixel((x, y))

    convert_to_lum(im=im, pixels=pixels)

    chars = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    return generate_ascii(chars=chars, im=im, pixels=pixels, rgb=rgb)


def print_pixels(im, pixels):
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            print(pixels[i][j], end='')
        print('')


def max_value(rgb):
    if (rgb[0] >= rgb[1]) and (rgb[0] >= rgb[2]):
        largest = rgb[0]
    elif (rgb[1] >= rgb[0]) and (rgb[1] >= rgb[2]):
        largest = rgb[1]
    else:
        largest = rgb[2]

    return largest


def min_value(rgb):
    if (rgb[0] <= rgb[1]) and (rgb[0] <= rgb[2]):
        smallest = rgb[0]
    elif (rgb[1] <= rgb[0]) and (rgb[1] <= rgb[2]):
        smallest = rgb[1]
    else:
        smallest = rgb[2]

    return smallest


def form(x):
    return round((x / 255) * 65)


def convert_to_average(im, pixels):
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i][j] = (pixels[i][j][0] + pixels[i][j][1] + pixels[i][j][2]) / 3


def convert_to_lightness(im, pixels):
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i][j] = (max_value(pixels[i][j]) + min_value(pixels[i][j]) / 2)


def convert_to_lum(im, pixels):
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i][j] = pixels[i][j][0] * 0.21 + pixels[i][j][1] * 0.72 + pixels[i][j][2] * 0.07


def generate_ascii(im, pixels, chars, rgb):
    f = open('file.txt', 'w')
    ascii_text = ""

    for j in range(im.size[1]):
        for i in range(im.size[0]):
            try:
                # color = '#{:02x}{:02x}{:02x}'.format(*rgb[i][j])
                # pixels[i][j] = f'<span style={{color: {color}}}>{chars[form(pixels[i][j])]}</span>'
                f.write(chars[form(pixels[i][j])])
                ascii_text += chars[form(pixels[i][j])]
            except IndexError:
                print("ERROR: ", i, j)
                print(form(pixels[i][j]))
                # print(ascii_text)
        f.write('\n')
        ascii_text += '\n'

    f.close()
    return ascii_text
