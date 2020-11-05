from PIL import Image

filename = 'N.jpg'

## size = 186 x 258

img = Image.open(filename)
newsize = (31,31)
img = img.resize(newsize)

coordinate1 = 1,1
img = img.convert('1')
coordinates = []

for i in range(0,31):
    for j in range(0,31):

        coordinate = i,j
        if img.getpixel(coordinate) == 0:
            coordinates.append(coordinate)

list_of_lists = [list(elem) for elem in coordinates]
print(list_of_lists)