from PIL import Image 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.image as img 
 
def load_and_display_image(img_path): 
    image=Image.open(img_path) 
    image.show() 
 
def convert_to_grayscale(img_path): 
    image=Image.open(img_path).convert("L") 
    plt.imshow(image, cmap='gray') 
    plt.axis('off') 
    plt.show() 
 
def resize_image(img_path): 
    image=Image.open(img_path) 
    image=image.resize((10,10)) 
    image.show() 
 
def display_histogram(img_path): 
    image=Image.open(img_path) 
    image_array=np.array(image) 
    color_channels=('Red','Green','Blue') 
    for i,color in enumerate(color_channels): 
        histogram,bin_edges=np.histogram( 
            image_array[:,:,i],bins=256,range=(0,255) 
        ) 
        plt.plot(bin_edges[0:-1],histogram,color=color.lower()) 
    plt.show() 
 
load_and_display_image("C:\\sem5\\Adv_Python_Lab\\Hanike.jpg") 
convert_to_grayscale("C:\\sem5\\Adv_Python_Lab\\Hanike.jpg") 
resize_image("C:\\sem5\\Adv_Python_Lab\\Hanike.jpg") 
display_histogram("C:\\sem5\\Adv_Python_Lab\\Hanike.jpg") 