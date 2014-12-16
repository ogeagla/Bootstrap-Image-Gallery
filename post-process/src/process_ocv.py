import cv2
import numpy as np
import glob
from matplotlib import pyplot as plt
import random
from math import floor

def get_image_files_from_dir(dir):
    files = glob.glob(dir+'/*')
    return files

def get_cv_image(image_file):
    cv_image = cv2.imread(image_file,cv2.IMREAD_COLOR)
    return cv_image

def get_cv_edges_image(cv_image, lower_thresh=10, upper_thresh=60):
    cv_edges_image = cv2.Canny(cv_image,lower_thresh,upper_thresh)
    return cv_edges_image

def get_cv_thresholded_image(cv_image, block_size=11, subtraction_constant=2):
    cv_thresholded_image = cv2.adaptiveThreshold(cv_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,block_size,subtraction_constant)
    return cv_thresholded_image
    
def get_cv_grayscale_image(cv_image):
    cv_grayscale_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    return cv_grayscale_image

def get_cv_bilateral_filtered_image(cv_image, nhood_size=9, sigma_color=80, sigma_space=80):
    cv_filtered_image = cv2.bilateralFilter(cv_image,nhood_size,sigma_color,sigma_space)
    return cv_filtered_image

def get_cv_scaled_image(cv_image, scalar):
    cv_scaled_image = cv2.resize(cv_image, (0,0), fx=scalar, fy=scalar, interpolation=cv2.INTER_LANCZOS4)
    return cv_scaled_image

def get_cv_scaled_image(cv_image, size_x, size_y):
    rows,cols,channels = cv_image.shape
    cv_scaled_image = cv2.resize(cv_image, (0,0), fx=float(size_x)/float(cols), fy=float(size_y)/float(rows), interpolation=cv2.INTER_LANCZOS4)
    return cv_scaled_image

def get_sum_of_images(img1, img2):
    sum_img = cv2.add(img1, img2)
    return sum_img

def transform_resize(cv_image, x, y, sx, sy):
    rows,cols = cv_image.shape
    M = np.float32([[1,0,x],[0,1,y]])
    ref_img = cv2.warpAffine(cv_image, M, (int(cols*sx), int(rows*sy)))
    return ref_img

def show_side_by_side(original_images, altered_images):
    assert len(original_images) == len(altered_images)
    number_of_subplots = len(original_images)

    max_per_plot = 1
    original_images_split = []
    altered_images_split = []
    if number_of_subplots > max_per_plot:
        original_images_copy = original_images
        altered_images_copy = altered_images
        while len(original_images_copy) >= max_per_plot:
            original_images_split.append(original_images_copy[:max_per_plot])
            altered_images_split.append(altered_images_copy[:max_per_plot])
            
            original_images_copy = original_images_copy[max_per_plot:]
            altered_images_copy = altered_images_copy[max_per_plot:]

        if len(original_images_copy) > 0:
            original_images_split.append(original_images_copy)
            altered_images_split.append(altered_images_copy)
            
    else:
        original_images_split = [original_images]
        altered_images_split = [altered_images]
    
    plt.subplots_adjust(hspace=0.000, wspace=0.0)#,left=0.0, right=0.0, bottom=0.0, top=0.0)
    #plt.tight_layout()
    
    for s in xrange(len(original_images_split)):
        originals = original_images_split[s]
        altereds = altered_images_split[s]
        subplots_count = len(originals)
        if s is not 0:
            plt.figure()
        for i,v in enumerate(xrange(subplots_count)):
            v = v + 1

            plt.subplot(subplots_count,2,2*v-1)
            plt.imshow(originals[i], cmap='gray')
            #plt.title('original')
            plt.xticks([])
            plt.yticks([])

            plt.subplot(subplots_count,2,2*v)
            plt.imshow(altereds[i], cmap='gray')
            #plt.title('original')
            plt.xticks([])
            plt.yticks([])
        plt.draw()
    plt.show()

def run_all_pics(number_pics=5):

    size_x = 800
    size_y = 600

    collage_scale_x = 1
    collage_scale_y = 1

    image_files = get_image_files_from_dir('/home/octavian/github/Bootstrap-Image-Gallery/post-process/imgs-input')
    print 'found ', len(image_files), ' image files on FS'

    cv_images = [get_cv_image(image_file) for image_file in image_files[:number_pics]]
    loaded_cv_images_count = len(cv_images)
    print 'loaded ', loaded_cv_images_count, ' images into CV'
    
    cv_scaled_images = [get_cv_scaled_image(cv_image, size_x, size_y) for cv_image in cv_images]
    print 'generated ', len(cv_scaled_images), ' CV scaled images'

    cv_grayscale_images = [get_cv_grayscale_image(cv_image) for cv_image in cv_scaled_images]
    print 'generated ', len(cv_grayscale_images), ' CV grayscale images'

    cv_bilateral_filtered_images = [get_cv_bilateral_filtered_image(cv_image) for cv_image in cv_grayscale_images]    
    print 'generated ', len(cv_bilateral_filtered_images), ' CV bilaterally filtered images'

    #cv_thresholded_images = [get_cv_thresholded_image(cv_image, 5,2) for cv_image in cv_grayscale_images]
    #print 'generated ', len(cv_thresholded_images), ' CV thresholded images'

    cv_edges_images = [get_cv_edges_image(cv_image) for cv_image in cv_bilateral_filtered_images]
    print 'generated ', len(cv_edges_images), ' CV edges images'

    random.seed(127)

    print 'processing imgs'
    cv_sampled_images = []
    for i in range(1):#len(cv_edges_images)):
        #print 'running for ',i+1, ' of ',len(cv_edges_images)
        pos_x = int(random.random()*float(collage_scale_x))*size_x
        pos_y = int(random.random()*float(collage_scale_y))*size_y
        ref_img = transform_resize(cv_edges_images[i], pos_x, pos_y, collage_scale_x, collage_scale_y)
        for j in range(4*collage_scale_x*collage_scale_y):#len(cv_edges_images)):
            rand_idx = int(floor(random.random()*float(len(cv_edges_images))))
            pos_x = int(random.random()*float(collage_scale_x))*size_x
            pos_y = int(random.random()*float(collage_scale_y))*size_y

            rand_img = transform_resize(cv_edges_images[rand_idx], pos_x, pos_y, collage_scale_x, collage_scale_y)
            print 'shapes: ', cv_edges_images[rand_idx].shape, rand_img.shape
            ref_img = get_sum_of_images(ref_img, rand_img)
        cv_sampled_images.append(ref_img)

    gauss_blurred = [cv2.GaussianBlur(cv_img, (25,25), 0) for cv_img in cv_sampled_images]
    rgbs = [cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB) for gray in gauss_blurred]
    new_rgbs = []
    for i in range(len(rgbs)):
        img = rgbs[i]
        print img.shape
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                px = img[x,y]
                var_B = int(15.0*(random.random()-0.5))
                var_G = int(25.0*(random.random()-0.5))
                var_R = int(5.0*(random.random()-0.5))

                # print var_B
                # exit(0)
                img.itemset((x,y,0),(px[0] + var_B) % 256)
                img.itemset((x,y,1),(px[1] + var_G) % 256)
                img.itemset((x,y,2),(px[2] + var_R) % 256)
        new_rgbs.append(img)


    print 'displaying'

    # show_side_by_side(cv_edges_images, cv_sampled_images)


    # tmp = [get_cv_bilateral_filtered_image(cv_img) for cv_img in cv_sampled_images]
    # show_side_by_side(cv_sampled_images, tmp)

    show_side_by_side(rgbs, new_rgbs)

    # show_side_by_side(cv_sampled_images, [get_sum_of_images(cv_sampled_images[i], tmp[i]) for i in range(len(cv_sampled_images))])



    return cv_edges_images

def run_one_pic(index=3):
    image_files = get_image_files_from_dir('/home/octavian/github/Bootstrap-Image-Gallery/post-process/imgs-input')
    print 'found ', len(image_files), ' image files on FS'

    image_files = [image_files[index], image_files[index], image_files[index]]

    cv_images = [get_cv_image(image_file) for image_file in image_files]
    loaded_cv_images_count = len(cv_images)
    print 'loaded ', loaded_cv_images_count, ' images into CV'
    
    cv_grayscale_images = [get_cv_grayscale_image(cv_image) for cv_image in cv_images]
    print 'generated ', len(cv_grayscale_images), ' CV grayscale images'

    #cv_bilateral_filtered_images = [get_cv_bilateral_filtered_image(cv_image) for cv_image in cv_grayscale_images]

    cv_bilateral_filtered_images = [get_cv_bilateral_filtered_image(cv_grayscale_images[0], 9,80,80),get_cv_bilateral_filtered_image(cv_grayscale_images[0],9,80,80),get_cv_bilateral_filtered_image(cv_grayscale_images[0],9,80,80)]
    print 'generated ', len(cv_bilateral_filtered_images), ' CV bilaterally filtered images'

    #cv_thresholded_images = [get_cv_thresholded_image(cv_grayscale_images[0], 5, 2), get_cv_thresholded_image(cv_grayscale_images[0], 7, 2), get_cv_thresholded_image(cv_grayscale_images[0], 15, 2)]
    #cv_thresholded_images = [get_cv_thresholded_image(cv_image) for cv_image in cv_grayscale_images]
    #print 'generated ', len(cv_thresholded_images), ' CV thresholded images'

    cv_edges_images = [get_cv_edges_image(cv_bilateral_filtered_images[0], 10, 60), get_cv_edges_image(cv_bilateral_filtered_images[1], 10, 60), get_cv_edges_image(cv_bilateral_filtered_images[2], 10, 60)]
#    cv_edges_images = [get_cv_edges_image(cv_image) for cv_image in cv_bilateral_filtered_images]
    print 'generated ', len(cv_edges_images), ' CV edges images'

    show_side_by_side(cv_bilateral_filtered_images, cv_edges_images)




def main():

    run_all_pics(10)

    
if __name__ == "__main__":
    main()
