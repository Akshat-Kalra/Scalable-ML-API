# basic_model_test.py

from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

# Load YOLOv8n-seg model (this will download the model if necessary)
model = YOLO("yolov8n-seg.pt")

# Define food classes to filter (adjust this list based on your needs)
food_classes = ["banana", "apple", "sandwich", "orange", "broccoli", 
                "carrot", "hot dog", "pizza", "donut", "cake"]

def process_image(image_path):
    # Run inference on the image
    results = model(image_path)
    result = results[0]

    # Read the image using OpenCV and convert to RGB for visualization
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading {image_path}")
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Iterate over each detected instance
    if hasattr(result, "boxes") and result.boxes is not None:
        for idx, cls_id in enumerate(result.boxes.cls.tolist()):
            class_name = model.names[int(cls_id)]
            # Only process if the class is in our list of food classes
            if class_name in food_classes:
                # Get bounding box coordinates
                box = result.boxes.xyxy[idx].tolist()
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
                # If segmentation masks are available
                if result.masks is not None:
                    mask = result.masks.data[idx].cpu().numpy()
                    # Convert mask to binary (threshold can be adjusted)
                    binary_mask = mask > 0.5
                    # Calculate the area as the sum of pixels in the mask
                    area = int(np.sum(binary_mask))
                    print(f"Detected {class_name} with area: {area} pixels")
                    
                    # Create a colored mask overlay
                    colored_mask = np.zeros_like(image)
                    colored_mask[binary_mask] = [255, 0, 0]  # Red overlay
                    image = cv2.addWeighted(image, 0.7, colored_mask, 0.3, 0)
                    
    # Show the final image with overlays
    plt.imshow(image)
    plt.title(f"Results for {image_path}")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    # Use glob to get a list of sample images (adjust the path and extension as needed)
    image_paths = glob.glob("client/test_images/*.jpg")[:5]  # Test on first 5 images
    for img_path in image_paths:
        process_image(img_path)
