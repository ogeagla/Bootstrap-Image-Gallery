import cv2
import numpy as np
import glob
from matplotlib import pyplot as plt


def get_image_files_from_dir(dir):
    files = glob.glob(dir+'/*')
    return files

def get_cv_image(image_file):
    cv_image = cv2.imread(image_file,0)#cv2.IMREAD_COLOR)
    return cv_image

def get_cv_edges_image(cv_image):
    cv_edges_image = cv2.Canny(cv_image,100,200)
    return cv_edges_image
    
def show_side_by_side(original_images, altered_images):
    assert len(original_images) is len(altered_images)
    number_of_subplots = len(original_images)

    max_per_plot = 5
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

def main():

    image_files = get_image_files_from_dir('/home/octavian/github/Bootstrap-Image-Gallery/post-process/imgs-input')
    print 'found ', len(image_files), ' image files on FS'

    cv_images = [get_cv_image(image_file) for image_file in image_files[:15]]
    loaded_cv_images_count = len(cv_images)
    print 'loaded ', loaded_cv_images_count, ' images into CV'
    
    cv_edges_images = [get_cv_edges_image(cv_image) for cv_image in cv_images]
    print 'generated ', len(cv_edges_images), ' CV edges images'
    
    show_side_by_side(cv_images, cv_edges_images)

if __name__ == "__main__":
    main()
