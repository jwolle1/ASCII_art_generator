import cv2
from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np


input_file = "img/cheetah.jpg"
output_file = "output.jpg"
scale_pct = 30
font_path = "fonts/DejaVuSansMono-Bold.ttf"
text_size = 16
text_color = (0, 0, 0)
bg_color = (241, 253, 254)
save_resized_image = False
output_to_txt_file = False
verbose = True

ascii_palette = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                 "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "!", "@",
                 "#", "$", "%", "&", "(", "-", "+", "=", "?", "/", ">"]


# ################ # ################ # ################ # ################ # ################


def pixel_to_char(px):
    smallest_diff = 1e6
    closest = None
    for ch in weight_dict:
        diff = abs(px - weight_dict[ch])
        if diff < smallest_diff:
            smallest_diff = diff
            closest = ch
    return closest


def get_char_dimensions(arr):
    top = 0
    for idx, cell in np.ndenumerate(arr):
        if cell != 255:
            top = idx[0]
            break
    bottom = 0
    for idx, cell in np.ndenumerate(np.flip(arr)):
        if cell != 255:
            bottom = idx[0]
            break
    right = 0
    for idx, cell in np.ndenumerate(np.rot90(arr, 1)):
        if cell != 255:
            right = idx[0]
            break
    left = 0
    for idx, cell in np.ndenumerate(np.rot90(arr, 3)):
        if cell != 255:
            left = idx[0]
            break
    return np.shape(arr)[1] - left - right, np.shape(arr)[0] - top - bottom


def prepare_font(palette, sz, fnt):
    weight_dict_raw = {}
    width_max = 0
    height_max = 0
    blank = np.zeros((sz * 2, sz, 3), np.uint8)
    blank[:,:] = (255, 255, 255)
    for char in palette:
        image = Image.fromarray(blank)
        image = ImageOps.grayscale(image)
        draw = ImageDraw.Draw(image)
        draw.text((3, 3), char, 0, font=fnt)
        char_img = np.array(image)
        tot = 0
        for row in char_img:
            for cell in row:
                tot += cell
        w, h = get_char_dimensions(char_img)
        if w > width_max:
            width_max = w
        if h > height_max:
            height_max = h
        weight_dict_raw.update({char: tot})
    weight_min = min(weight_dict_raw.values())
    weight_max = max(weight_dict_raw.values()) - weight_min
    wt_dict = {}
    for char in weight_dict_raw:
        gray_8bit = (weight_dict_raw[char] - weight_min) / weight_max * 255
        wt_dict.update({char: gray_8bit})
    return wt_dict, width_max, height_max


def resize_image(path, scale, width_max, height_max, save, verb):
    original_img = cv2.imread(path)
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    new_width = gray_img.shape[1] * scale / 100
    new_height = gray_img.shape[0] * scale / 100
    new_height *= width_max / height_max
    new_dimensions = (int(round(new_width)), int(round(new_height)))
    if verb:
        print(f"new dimensions (H, W): {new_dimensions}")
    new_img = cv2.resize(gray_img, new_dimensions, interpolation=cv2.INTER_AREA)
    if save:
        cv2.imwrite("resized.jpg", new_img)
    return new_img


def generate_art(pixels, save, verb):
    if verb:
        print("\nConverting pixels to ASCII...")
    art_string = ""
    for i, row in enumerate(pixels):
        if verb:
            if i % 20 == 0 and i > 0:
                print("  {:.0f}%".format((i + 1) / len(pixels) * 100))
        for pixel in row:
            art_string += pixel_to_char(pixel)
        art_string += "\n"
    if verb:
        print("  Done!")
    if save:
        with open("output_text.txt", "w+") as f:
            f.write(art_string)
    return art_string


def draw_output_image(text, width_max, height_max, fnt, txt_clr, bg_clr, output_fn, verb):
    art_lines = text.strip().split("\n")
    canvas_width = int(len(art_lines[0]) * width_max) + 40
    canvas_height = int(len(art_lines) * height_max) + 40
    blank = np.zeros((canvas_height, canvas_width, 3), np.uint8)
    blank[:,:] = bg_clr
    if verb:
        print("\nDrawing image...")
    image = Image.fromarray(blank)
    draw = ImageDraw.Draw(image)
    for i, line in enumerate(art_lines):
        if verb:
            if i % 20 == 0 and i > 0:
                print("  {:.0f}%".format((i + 1) / len(art_lines) * 100))
        for c, char in enumerate(line):
            draw.text((int(round(c * width_max)) + 20 + int(round(width_max / 2)),
                       int(round(i * height_max)) + 20 + int(round(height_max / 2))),
                      char, txt_clr, font=fnt, anchor="mm")
    result = np.array(image)
    cv2.imwrite(output_fn, result)
    if verb:
        print("  Done!")
    return


font = ImageFont.truetype(font_path, text_size)

weight_dict, char_width_max, char_height_max = prepare_font(ascii_palette, text_size, font)

img = resize_image(input_file, scale_pct, char_width_max, char_height_max, save_resized_image, verbose)

art = generate_art(img, output_to_txt_file, verbose)

draw_output_image(art, char_width_max, char_height_max, font, text_color, bg_color, output_file, verbose)
