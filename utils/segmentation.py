import requests
from skimage import io
import matplotlib.pyplot as plt
import numpy

def download_image(url, filename="image.jpg"):
    """
    Function that downloads and opens the image
    :param url: the url of the image
    :param filename: the filename of the image
    :return: the image loaded in memory
    """
    # We get the image address
    r = requests.get(url)

    # We open the image in "write-mode"
    with open(filename, "wb") as f:
        # We write the content to the file
        f.write(r.content)

    # Read the image with the module imread
    img = io.imread(filename)

    # Print the image shape
    print(f"The shape of the image is: {img.shape}")
    return img

def asignacionPC(centroides):
	grupos = {}

	for x in range(0, img_width):
		for y in range(0, img_height):
			pixelActual = imagenCargada[x, y]
			distanciaMinima = 99999
			centroideMin = 0

			for i in range(0, len(centroides)):
				d = numpy.sqrt(int((centroides[i][0] - pixelActual[0]))**2 + int((centroides[i][1] - pixelActual[1]))**2 + int((centroides[i][2] - pixelActual[2]))**2)
				if d < distanciaMinima:
					distanciaMinima = d
					centroideMin = i
			try:
				grupos[centroideMin].append(pixelActual)
			except KeyError:
				grupos[centroideMin] = [pixelActual]

	return grupos

def actualizarCentroides(centroides, grupos):
	actualizados = []	
	for posCentroide in sorted(grupos.keys()):
		n = numpy.mean(grupos[posCentroide], axis=0)
		centroideNuevo = (int(n[0]), int(n[1]), int(n[2]))
		actualizados.append(centroideNuevo)

	return actualizados

def cambianCentroides(centroides, centroidesItAnterior, error):
	if len(centroidesItAnterior) == 0:
		return False

	for i in range(0, len(centroides)):
		cent = centroides[i]
		centroideAnterior = centroidesItAnterior[i]
		if ((int(centroideAnterior[0]) - error) <= cent[0] <= (int(centroideAnterior[0]) + error)) and ((int(centroideAnterior[1]) - error) <= cent[1] <= (int(centroideAnterior[1]) + error)) and ((int(centroideAnterior[2]) - error) <= cent[2] <= (int(centroideAnterior[2]) + error)):
			continue
		else:
			return False
	return True

def kmeans(nGrupos, limite, error, aleatorio, centroides):
	centroidesAct = []
	centroidesItAnterior = []
	iteracion = 1

	if not aleatorio:
		centroidesAct = centroides
	else:
		for k in range(0, nGrupos):
			a = numpy.random.randint(0, img_width)
			b = numpy.random.randint(0, img_height)
			print("Coordenadas aleatorias ", a, b)
			cent = imagenCargada[a, b]
			print("Pixel ", cent)
			centroidesAct.append(tuple(cent))

	print("C ", centroidesAct)
	while not cambianCentroides(centroidesAct, centroidesItAnterior, error) and iteracion <= limite:
		print("Iteracion actual -> " + str(iteracion))
		iteracion += 1
		centroidesItAnterior = centroidesAct 								
		grupos = asignacionPC(centroidesAct) 						
		centroidesAct = actualizarCentroides(centroidesItAnterior, grupos) 
		img = numpy.zeros((img_width, img_height, 3), numpy.uint8)

	for x in range(img_width):
		for y in range(img_height):
			distanciaMinima = 9999
			centroideMin = 0
			pixel = imagenCargada[x, y]

			for i in range(0, len(centroidesAct)):
				d = numpy.sqrt(int((centroidesAct[i][0] - pixel[0]))**2 + int((centroidesAct[i][1] - pixel[1]))**2 + int((centroidesAct[i][2] - pixel[2]))**2)
				if d < distanciaMinima:
					distanciaMinima = d
					centroideMin = i
			img[x, y] = centroidesAct[centroideMin]

	plt.imshow(img)
	plt.show()

	return centroidesAct

k = 3
limite = 25
error = 5
img = "images/1.jpg"
imagenCargada = io.imread(img)
img_width, img_height, deph = imagenCargada.shape

imagenSegmentada = kmeans(k, limite, error, True, [(31, 32, 27), (179, 176, 221), (87, 125, 128)])
