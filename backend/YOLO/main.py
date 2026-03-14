from ultralytics import YOLO
import cv2
import numpy as np

import util
from sort.sort import Sort
from util import get_car, read_license_plate, write_csv

import torch

print('Using GPU:', torch.cuda.is_available())
print('GPU Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')

# Initialize video capture
cap = cv2.VideoCapture('./sample.mp4')

# Initialize MOT tracker
mot_tracker = Sort()

# Load models once
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('license_plate_detector.pt')

vehicles = [2, 3, 5, 7]  # Vehicle class IDs to detect (e.g., car, bus, truck, motorcycle)

results = {}

frame_nmr = -1
ret = True
max_frames = 500  # Set max frames to process (set None to process full video)

while ret and (max_frames is None or frame_nmr < max_frames):
    frame_nmr += 1
    ret, frame = cap.read()
    if not ret:
        break

    if frame_nmr % 10 == 0:
        print(f"Processing frame {frame_nmr}")

    results[frame_nmr] = {}

    # Detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])

    # Track vehicles
    track_ids = mot_tracker.update(np.asarray(detections_))

    # Detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # Assign license plate to car using your util function
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            # Crop license plate region
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

            # Process license plate for OCR
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

            # Read license plate text
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                results[frame_nmr][car_id] = {
                    'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                    'license_plate': {
                        'bbox': [x1, y1, x2, y2],
                        'text': license_plate_text,
                        'bbox_score': score,
                        'text_score': license_plate_text_score
                    }
                }

# Release video capture
cap.release()

# Write results to CSV
write_csv(results, './test.csv')

print("Processing complete. Results saved to test.csv")