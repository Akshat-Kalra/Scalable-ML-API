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
    #
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
    # print(model.names)
    
    
    result = results[0]


    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image")
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detected_items = []

    # Process segmentation masks if available
    if hasattr(result, "masks") and result.masks is not None:
        for idx in range(len(result.masks)):
            
            # for finding the food item / class name corresponding to the result
            class_id = int(result.boxes.cls[idx])
            class_name = model.names[class_id]
            
            
            
            mask = result.masks.data[idx].cpu().numpy()
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
            
            
            binary_mask = mask > 0.5
            
            # calculating the area
            area = int(np.sum(binary_mask))
            print(f"Detected {class_name} with area: {area} pixels")

            detected_items.append({"name": class_name, "area": area})
    
    return {"detected_items": detected_items}

if __name__ == "__main__":
    result = process_image('Food.jpeg')
    print(result)