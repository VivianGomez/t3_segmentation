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

def asignacionPC(centroides, imagenCargada):
	grupos = {}
	img_width, img_height, deph = imagenCargada.shape
	for x in range(0, img_width):
		for y in range(0, img_height):
			pixelActual = imagenCargada[x, y]
			distanciaMinima = 99999
			centroideMin = 0

			for i in range(0, len(centroides)):
				d = numpy.sqrt((int(centroides[i][0]) - int(pixelActual[0]))**2 + (int(centroides[i][1]) - int(pixelActual[1]))**2 + (int(centroides[i][2]) - int(pixelActual[2]))**2)
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

def cambianCentroides(centroides, centroidesItAnterior, umbral):
	if len(centroidesItAnterior) == 0:
		return False

	for i in range(0, len(centroides)):
		cent = centroides[i]
		centroideAnterior = centroidesItAnterior[i]
		if ((int(centroideAnterior[0]) - umbral) <= cent[0] <= (int(centroideAnterior[0]) + umbral)) and ((int(centroideAnterior[1]) - umbral) <= cent[1] <= (int(centroideAnterior[1]) + umbral)) and ((int(centroideAnterior[2]) - umbral) <= cent[2] <= (int(centroideAnterior[2]) + umbral)):
			continue
		else:
			return False
	return True

def kmeans(nGrupos, imagenCargada, limite, umbral, aleatorio, centroides):
	centroidesAct = []
	centroidesItAnterior = []
	iteracion = 1

	img_width, img_height, deph = imagenCargada.shape

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
	while not cambianCentroides(centroidesAct, centroidesItAnterior, umbral) and iteracion <= limite:
		print("Iteracion actual -> " + str(iteracion))
		iteracion += 1
		centroidesItAnterior = centroidesAct 								
		grupos = asignacionPC(centroidesAct, imagenCargada) 						
		centroidesAct = actualizarCentroides(centroidesItAnterior, grupos) 
		img = numpy.zeros((img_width, img_height, 3), numpy.uint8)

	for x in range(img_width):
		for y in range(img_height):
			distanciaMinima = 9999
			centroideMin = 0
			pixel = imagenCargada[x, y]

			for i in range(0, len(centroidesAct)):
				d = numpy.sqrt((int(centroidesAct[i][0]) - int(pixel[0]))**2 + (int(centroidesAct[i][1]) - int(pixel[1]))**2 + (int(centroidesAct[i][2]) - int(pixel[2]))**2)
				if d < distanciaMinima:
					distanciaMinima = d
					centroideMin = i
			img[x, y] = centroidesAct[centroideMin]

	plt.imshow(img)
	plt.show()

	return centroidesAct

#kmeans(3, io.imread("images/1.jpg"), 25, 5, True, [(31, 32, 27), (179, 176, 221), (87, 125, 128)])
