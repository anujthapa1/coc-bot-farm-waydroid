"""
Vision module using Ultralytics YOLOv8 for object detection and EasyOCR for text/resource extraction.
Operates strictly on relative image coordinates (0,0 origin).
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
import config

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

try:
    import easyocr
except ImportError:
    easyocr = None


class Vision:
    """Vision processing class for Clash of Clans game state detection and OCR."""

    def __init__(self, yolo_model_path: str = config.YOLO_MODEL_PATH):
        self.yolo_model = None
        if YOLO is not None:
            try:
                self.yolo_model = YOLO(yolo_model_path)
            except Exception:
                self.yolo_model = None

        self.ocr_reader = None
        if easyocr is not None:
            try:
                self.ocr_reader = easyocr.Reader(config.EASYOCR_LANGUAGES, gpu=config.EASYOCR_GPU)
            except Exception:
                self.ocr_reader = None

    def detect_objects(self, image: np.ndarray, conf_threshold: float = config.CONFIDENCE_THRESHOLD) -> List[Dict[str, Any]]:
        """
        Runs YOLOv8 object detection on relative image coordinates.
        Returns list of detections with bounding boxes (x1, y1, x2, y2, center_x, center_y), confidence, and label.
        """
        if self.yolo_model is None or image is None:
            return []

        results = self.yolo_model(image, conf=conf_threshold, verbose=False)
        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                label = result.names[cls_id]

                x1, y1, x2, y2 = map(int, xyxy)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bbox": (x1, y1, x2, y2),
                    "center": (center_x, center_y)
                })

        return detections

    def extract_text(self, image: np.ndarray, bbox: Tuple[int, int, int, int] = None) -> str:
        """
        Runs EasyOCR on full image or cropped ROI using relative coordinates.
        """
        if self.ocr_reader is None or image is None:
            return ""

        if bbox is not None:
            x1, y1, x2, y2 = bbox
            roi = image[y1:y2, x1:x2]
        else:
            roi = image

        if roi.size == 0:
            return ""

        results = self.ocr_reader.readtext(roi, detail=0)
        return " ".join(results).strip()
