import cv2
import matplotlib.pyplot as plt
import numpy as np

#Gaussian Pyramid
def gaussian_pyramid (image, levels,scale_percent):
    reduced_images = [image]
    for i in range(levels):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dimension = (width, height)
        blurred_image = cv2.GaussianBlur(image,(19,19),0)
        blurred_image[::2 , ::2]
        downsampled_image = cv2.resize(blurred_image, dimension)
        reduced_images.append(downsampled_image)
        image = downsampled_image
    return reduced_images

#Laplacian Pyramid 
def laplacian_pyramid (image, levels, scale_percent):
    level = 0
    reduced_images = [image]
    residual_images = []
    while level <levels:
        if level < levels-1:
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dimension = (width, height)
            blurred_image = cv2.GaussianBlur(image,(19,19),0)
            blurred_image[::2 , ::2]
            residual = image - blurred_image
            residual_images.append(residual)
            downsampled_image = cv2.resize(blurred_image, dimension)    
            reduced_images.append(downsampled_image)
            image = downsampled_image
        else:
            residual_images.append(reduced_images[-1])
        level +=1
    return residual_images

#Reconstructing the image from Laplacian Pyramid
def reconstruction (pyramid):
    reconstructed_image = pyramid[-1]
    i = len(pyramid)-1
    while i > 0:
        image_upsampled = cv2.resize(reconstructed_image, (pyramid[i-1].shape[1], pyramid[i-1].shape[0]))
        residual_image = pyramid[i-1]
        reconstructed_image = image_upsampled + residual_image
        i-=1
    return reconstructed_image

#Multiresolution blending
def multiresolution(app, ora):
    r_img1,c_img1, ch_img1  = app.shape
    maskapp = np.zeros((r_img1,c_img1,ch_img1))
    maskapp[:, :int(c_img1/2)] = 1
    gauss_pyramidapple = gaussian_pyramid(maskapp,levels = 5, scale_percent = 50)
    lap_pyramidapple = laplacian_pyramid(app, levels = 5, scale_percent = 50)
    maskora= 1- maskapp
    gauss_pyramidorange = gaussian_pyramid(maskora,levels = 5, scale_percent = 50)
    lap_pyramidorange = laplacian_pyramid(ora, levels = 5, scale_percent = 50)
    
    arrapple=[]
    arrorange=[]
    for i in range(5):
        appblend= gauss_pyramidapple[i]*lap_pyramidapple[i]
        orablend= gauss_pyramidorange[i]*lap_pyramidorange[i]
        arrapple.append(appblend)
        arrorange.append(orablend)
    
    multiblend=[]
    for i in range(5):
        a3= arrapple[i]+arrorange[i]
        multiblend.append(a3)
    
    multi_blendeding= reconstruction(multiblend)
    return(multi_blendeding)

#Loading the image
image_main = cv2.imread("elephant.jpeg")
image_main = cv2.cvtColor(image_main, cv2.COLOR_BGR2RGB)

gauss_pyramid = gaussian_pyramid(image_main,levels = 5, scale_percent = 50)

#https://learning.oreilly.com/library/view/hands-on-image-processing/9781789343731/2138f4a7-df74-4826-9e1d-b7431a310b72.xhtml
i, n = 1, len(gauss_pyramid)
for p in gauss_pyramid:
    p = cv2.cvtColor(p, cv2.COLOR_BGR2RGB)
    cv2.imshow(" Gaussian Pyramid Image number {}".format(i),p)
    i+=1
cv2.waitKey(0)    
cv2.destroyAllWindows()

#Calling the laplacian_pyramid function and visualizing it
lap_pyramid = laplacian_pyramid(image_main, levels = 5, scale_percent = 50)

#https://learning.oreilly.com/library/view/hands-on-image-processing/9781789343731/2138f4a7-df74-4826-9e1d-b7431a310b72.xhtml
m, n = 1, len(lap_pyramid)
for l in lap_pyramid:
    l = cv2.cvtColor(l, cv2.COLOR_BGR2RGB)
    cv2.imshow(" Laplacian Pyramid Image number {}".format(i),l)
    i+=1
cv2.waitKey(0)    
cv2.destroyAllWindows()

#Reconstructing the original image
final_image = reconstruction(lap_pyramid)
plt.figure()
plt.imshow(final_image)
plt.title("Image reconstruction from Laplacian pyramid")
plt.show()

import skimage
apple= cv2.imread('apple.jpeg')
cv2.imshow('apple',apple)
apple= cv2.cvtColor(apple, cv2.COLOR_BGR2RGB)
orange= cv2.imread('orange.jpeg')
cv2.imshow('orange',orange)
orange= cv2.cvtColor(orange, cv2.COLOR_BGR2RGB)
apple_db = skimage.img_as_float64(apple, force_copy=False)
orange_db = skimage.img_as_float64(orange, force_copy=False) #https://scikit-image.org/docs/dev/api/skimage.html#module-skimage
cv2.waitKey(0)    
cv2.destroyAllWindows()

row_apple,col_apple, channel_apple  = apple_db.shape
row_orange, col_orange, channel_orange = orange_db.shape

mask = np.zeros((row_apple,col_apple,channel_apple))
mask[:, :int(col_apple/2)] = 1
cv2.imshow('Mask',mask)
cv2.waitKey(0)    
cv2.destroyAllWindows()

########################################################## Direct blending ######################
direct_blend =  mask*apple_db + (1 - mask)*orange_db 
plt.figure()
plt.imshow(direct_blend)
plt.title("Direct Blending")
plt.show()

########################################################## Alpha blending ######################
mask_blur = cv2.GaussianBlur((mask) , (15,15), 15, cv2.BORDER_WRAP)
alpha_blend = mask_blur*apple_db + (1 - mask_blur)*orange_db 
plt.figure()
plt.imshow(alpha_blend)
plt.title("Alpha Blending")
plt.show()

########################################################## Multiresolution blending ######################
reconstructed_image= multiresolution(apple_db,orange_db)
plt.figure()
plt.imshow(reconstructed_image)
plt.title("Multiresolution Blending")
plt.show()
