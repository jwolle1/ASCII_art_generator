One form of [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) involves taking a raster image and representing its pixels with plain text.

This script generates ASCII art and gives users control over input parameters such as font, character density (resolution), and color. Since the script generates a pixel-to-ASCII conversion dictionary every time it runs, you can even select which characters are included in the "palette."

One obstacle in ASCII art is that text tends to be taller than it is wide, which leads to a stretched image if you replace pixels directly with text. This script solves the problem by measuring each character in the palette and stretching the input image to compensate.

Another issue is that ASCII art is usually only possible with fixed-width "monospace" fonts. This script lets users generate images with any font, fixed- or variable-width.

Although the script's primary function is to produce ASCII art as an image file, users also have the option to save as a text file.

---

Below are examples of high-, medium-, and low-resolution art the script can produce.

##### _Memorial Stadium (Lincoln, NE), 720x336 characters:_
![Memorial Stadium 720x336](img/memorial_stadium_output_720x336_resized.jpg)

---

##### _Cheetah, 360x171 characters:_
![Cheetah 360x171](img/cheetah_output_360x171.jpg)
_Original image credit: Shutterstock._

---

##### _Abe Lincoln, 144x117 characters. This was generated using the variable-width font Public Sans, designed in 2019 for federal government use:_
![Abe Lincoln 120x86](img/abe_output_144x117.jpg)

---

**To use:**

1. Required dependencies are `OpenCV`, `Pillow`, and `Numpy`. If you don't have them installed or you're using old versions, run `pip3 install -r requirements.txt`.
2. Set image path and desired options at the top of `main.py` and run.

Three fonts are included but the script should work with any Truetype (_.ttf_) font.