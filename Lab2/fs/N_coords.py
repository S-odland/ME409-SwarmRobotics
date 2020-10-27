from PIL import Image

filename = 'N.jpg'

## size = 186 x 258

img = Image.open(filename)
newsize = (30,36)
img = img.resize(newsize)

coordinate1 = 1,1
img = img.convert('1')
img.show()

coordinates = []

for i in range(0,30):
    for j in range(0,36):

        coordinate = i,j
        if img.getpixel(coordinate) == 0:
            coordinates.append(coordinate)

list_of_lists = [list(elem) for elem in coordinates]
print(coordinates)
print('\n')
print(list_of_lists)