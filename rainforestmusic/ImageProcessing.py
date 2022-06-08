"""
Image Processing
"""
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import colorsys
from sklearn.cluster import KMeans

class ImageProcessing():
    def __init__(self, img_name):
        # open the image
        plt.style.use('seaborn-white')
        self.img = Image.open("images/{}.jpg".format(img_name))
    
    ''' function to resize the image to find average colours or make it faster to process '''
    def resize_image(self, new_width, new_height):
        self.img = self.img.resize((new_width, new_height), Image.ANTIALIAS)
      
    ''' function to display the chosen image '''
    def show_image(self):
        self.img.show()
    
    ''' function to plot the different colours within an image'''
    def plot_colourspace(self):
        pixels = self.img.load()
        plt.figure(figsize=(25,25))
        axes = plt.axes(projection = '3d')
        
        x = []
        y = []
        z = []
        c = []
                    
        for row in range(0,self.img.height):
            for col in range(0, self.img.width):
                pix = pixels[col,row]
                binary_colour = (pix[0] / 255, pix[1] / 255, pix[2] / 255)
        
                if(not binary_colour in c):
                    x.append(pix[0])
                    y.append(pix[1])
                    z.append(pix[2])
                    c.append(binary_colour)
                    
        axes.scatter(x,y,z, c = c)
        axes.set_xlabel('r')
        axes.set_ylabel('g')
        axes.set_zlabel('b')
        plt.show()
        
    ''' function to plot the hue and value of pixels in an image'''
    def plot_hv(self):
        pixels = self.img.load()
        hsv_pixels = self.hsv_img.load()
        plt.figure(figsize=(25,25))
        
        self.h = []
        self.v = []
        c = []
                    
        for row in range(0,self.img.height):
            for col in range(0, self.img.width):
                pix = pixels[col,row]
                hsv_pix = hsv_pixels[col,row]
                binary_colour = (pix[0] / 255, pix[1] / 255, pix[2] / 255)
        
                self.h.append(hsv_pix[0])
                self.v.append(hsv_pix[2])
                c.append(binary_colour)
         
        plt.xlabel('Hue')
        plt.ylabel('Value')
        plt.scatter(self.h,self.v, c = c)
        plt.show()
        
    def convert_to_hsv(self):
        r,g,b = self.img.split()
        hue = []
        saturation = []
        value = [] 
        
        for red,green,blue in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(red/255.,green/255.,blue/255.)
            hue.append(int(h*360.))
            saturation.append(int(s*100.))
            value.append(int(v*100.))
        r.putdata(hue)
        g.putdata(saturation)
        b.putdata(value)
        self.hsv_img = Image.merge('RGB',(r,g,b))
        
        
    # need to do 1-7 instead of 0-8
    def choose_note(self, hsv_pixel):
        # mapping hsv colour values to notes (30 degrees each)
        notes = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
        # 0 - 30 C
        # 31 - 60 c (C sharp)
        # 61 - 90 D
        # 91 - 120 d
        # 121 - 150 E
        # 151 - 180 F
        # 181 - 210 f
        # 211 - 240 G
        # 241 - 270 g
        # 271 - 300 A
        # 301 - 330 a
        # 331 - 360 B
        # first choose the note based on the hue
        hue = hsv_pixel[0]
        hue_idx = hue // 30
        note = notes[hue_idx]
        # choose the octave based on the value
        value = hsv_pixel[2]
        value_no = int(value // (100/6))
        # choose the loudness based on the value
        return note + str(value_no+1)
    
    # can we figure out a way to path spiraling outwards from an image
    def read_spiral(self):
        pattern = np.array([[1,0], [0,-1], [-1, 0], [0, 1]])
        # find the centre point of the photo
        centre = np.array([self.img.width//2, self.img.height//2])
        current_pixel = centre.copy()
        print('centre: ', centre)
        path = [centre]
        # overall spiral
        for n in range(0,self.img.width//2):
            # left
            for i in range(2*n):
                current_pixel += pattern[0]
                print(current_pixel)
                path.append(current_pixel.copy())
            # down
            for i in range(2*n):
                current_pixel += pattern[1]
                print(current_pixel)
                path.append(current_pixel.copy())
            # right
            for i in range(2*n+1):
                current_pixel += pattern[2]
                print(current_pixel)
                path.append(current_pixel.copy())
            # up
            for i in range(2*n+1):
                current_pixel += pattern[3]
                print(current_pixel)
                path.append(current_pixel.copy())
                
        path = np.array(path)
        return path
        
    def hsv_kmeans_cluster(self):
        # create the array for the kmeans to work on
        hv = np.vstack((self.h, self.v)).T
        # instantiate and fit the kmeans clusters
        kmeans = KMeans(n_clusters=4).fit(hv)
        centroids = kmeans.cluster_centers_
        
        #Getting unique labels
        u_labels = np.unique(kmeans.labels_)
        plt.figure(figsize=(25,25))
         
        #plotting the results:
        for i in u_labels:
            plt.scatter(hv[kmeans.labels_ == i , 0] , hv[kmeans.labels_ == i , 1] , label=i)
        plt.scatter(centroids[:,0] , centroids[:,1] , s = 500, color = 'k')
        plt.show()
        
        self.cluster_centres = centroids
        
    def pitch_cluster_centres(self):
        for centre in self.cluster_centres:
            print(centre)
            print(self.choose_note([int(centre[0]), 0, int(centre[1])]))
        
# 1,2,5,6,7,8,9
image = ImageProcessing('9')

# make square for easiness
# if img height is 80, call on range 0-79
# access a pixel by calling img[width(x), height(y)]
image.resize_image(image.img.width//50, image.img.width//50)
image.plot_colourspace()
image.convert_to_hsv()
hsv_pix = image.hsv_img.load()

image.plot_hv()
image.hsv_kmeans_cluster()
image.pitch_cluster_centres()


# pixels = image.img.load()
# path = image.read_spiral()

# x = path[:,0]
# y = path[:,1]
# plt.plot(x, y)