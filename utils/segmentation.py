from skimage import io
import numpy

img = "images/1.jpg"
imagenCargada = io.imread(img)
img_width, img_height, depth = imagenCargada.shape

print(img_width, img_height, depth)