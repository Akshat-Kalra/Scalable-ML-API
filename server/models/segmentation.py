from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

model = YOLO("yolov8n-seg.pt")

def process_image(image_path):
    print('starting processing image ')
    
    # running the model on the given image
    #  
    # sample output of the next line (just for self reference):
    # image 1/1 /content/Food.jpeg: 608x640 1 fork, 1 spoon, 2 broccolis, 1 pizza, 663.0ms
    # Speed: 25.7ms preprocess, 663.0ms inference, 91.2ms postprocess per image at shape (1, 3, 608, 640)
    # ultralytics.engine.results.Results object with attributes:
    # boxes: ultralytics.engine.results.Boxes object
    # keypoints: None
    # masks: ultralytics.engine.results.Masks object
    results = model(image_path)
    
    
    
    # just checking for the classes
    # it is a general segmenter model, but if time permits
    # I will try to fine tune it on a food dataset
    print(model.names)
    
    
    result = results[0]


    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image")
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Iterate over each detected instance
    if hasattr(result, "masks") and result.masks is not None:
        for idx in range(len(result.masks)):
            # Get the mask data
            mask = result.masks.data[idx].cpu().numpy()

            # Resize the mask to the image's shape
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

            # Convert mask to binary
            binary_mask = mask > 0.5
            
            # Calculate the area as the sum of pixels in the mask
            area = int(np.sum(binary_mask))
            print(f"Detected object with area: {area} pixels")
            
            
            colored_mask = np.zeros_like(image)
            
            # Resize binary mask before application
            resized_binary_mask = binary_mask.astype(np.uint8)
            resized_binary_mask = cv2.resize(resized_binary_mask, (colored_mask.shape[1], colored_mask.shape[0]))
            resized_binary_mask = resized_binary_mask.astype(bool)
            
            colored_mask[resized_binary_mask] = [255, 0, 0]
            image = cv2.addWeighted(image, 0.7, colored_mask, 0.3, 0)
                    
    # Show the final image with overlays
    plt.imshow(image)
    plt.title(f"Results for {image_path}")
    plt.axis("off")
    plt.savefig(f"output_{image_path.split('/')[-1]}")
    plt.show()

if __name__ == "__main__":
    process_image('Food.jpeg')
    