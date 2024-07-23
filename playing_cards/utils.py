import cv2
import matplotlib.pyplot as plt
import glob
import os
import random
import shutil


# Plot and visualize images in a 2x2 grid.
def visualize(result_dir):
    
    """
    Function accepts a list of images and plots
    them in either a 1x1 grid or 2x2 grid.
    """
    plt.figure(figsize=(15, 12))
    image_names = glob.glob(os.path.join(result_dir, '*.jpg'))
    if len(image_names) < 4:
        for i, image_name in enumerate(image_names):
            image = plt.imread(image_name)
            plt.subplot(1, 1, i+1)
            plt.imshow(image)
            plt.axis('off')
            break
    if len(image_names) >= 4:
        for i, image_name in enumerate(image_names):
            image = plt.imread(image_name)
            plt.subplot(2, 2, i+1)
            plt.imshow(image)
            plt.axis('off')
            if i == 3:
                break
    plt.tight_layout()
    plt.show()

# Function to convert bounding boxes in YOLO format to xmin, ymin, xmax, ymax.
def yolo2bbox(bboxes):
    xmin, ymin = bboxes[0]-bboxes[2]/2, bboxes[1]-bboxes[3]/2
    xmax, ymax = bboxes[0]+bboxes[2]/2, bboxes[1]+bboxes[3]/2
    return xmin, ymin, xmax, ymax

def plot_box(image, bboxes, labels, colors, classes):
    # Need the image height and width to denormalize
    # the bounding box coordinates
    h, w, _ = image.shape
    for box_num, box in enumerate(bboxes):
        x1, y1, x2, y2 = yolo2bbox(box)
        # Denormalize the coordinates.
        xmin = int(x1*w)
        ymin = int(y1*h)
        xmax = int(x2*w)
        ymax = int(y2*h)

        thickness = max(2, int(w/275))
        #print(labels[box_num])

    

        cv2.rectangle(
            image, 
            (xmin, ymin), (xmax, ymax),
            color=colors[int(labels[box_num])-1],
            thickness=thickness
        )
        cv2.putText(
            image,
            text=classes[int(labels[box_num])-1],
            org=(xmin, ymin-5),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=colors[int(labels[box_num])-1],
            thickness=1,
            lineType=cv2.LINE_AA
            )
    return image

# Function to plot images with the bounding boxes.
def plot(image_paths, label_paths, num_samples, colors, classes):
    all_images = []
    #os.chdir(image_paths)
    all_images.extend(glob.glob(image_paths+'/*.jpg'))
    
    all_images.sort()

    num_images = len(all_images)
    
    plt.figure(figsize=(15, 12))
    for i in range(num_samples):
        j = random.randint(0,num_images-1)
        image_name = all_images[j]
        image_name = '.'.join(image_name.split(os.path.sep)[-1].split('.')[:-1])
        image = cv2.imread(all_images[j])
        with open(os.path.join(label_paths, image_name+'.txt'), 'r') as f:
            bboxes = []
            labels = []
            label_lines = f.readlines()
            for label_line in label_lines:
                values = label_line.split(' ')
                label = int(values[0]) + 1
                bbox_string = ' '.join(values[1:])
                x_c, y_c, w, h = bbox_string.split(' ')
                x_c = float(x_c)
                y_c = float(y_c)
                w = float(w)
                h = float(h)
                bboxes.append([x_c, y_c, w, h])
                labels.append(label)
        result_image = plot_box(image, bboxes, labels, colors, classes)
        plt.subplot(2, 2, i+1)
        plt.imshow(result_image[:, :, ::-1])
        plt.axis('off')
    plt.subplots_adjust(wspace=1)
    plt.tight_layout()
    plt.show()
    #os.chdir('cd ~')

def random_color():
    '''
    Give a random color between 0 and 255
    '''
    color = random.randint(0,255)
    return color