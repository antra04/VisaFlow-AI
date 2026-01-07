"""Advanced Document Detection with YOLOv8 + OCR"""
import cv2
import numpy as np
from pathlib import Path
import easyocr
from PIL import Image
import re
import fitz
import docx
import io
from ultralytics import YOLO
import torch

class AdvancedDocumentDetector:
    def __init__(self, languages=['en', 'hi']):
        print(f"[INFO] Loading models...")
        
        try:
            self.yolo_model = YOLO('yolov8n.pt')
        except Exception as e:
            print(f"[WARNING] YOLO model failed to load: {e}")
            self.yolo_model = None
        
        try:
            self.reader = easyocr.Reader(languages, gpu=torch.cuda.is_available())
        except Exception as e:
            print(f"[ERROR] EasyOCR failed to initialize: {e}")
            raise
        
        self.doc_patterns = {
            'aadhaar': {
                'en': ['government', 'india', 'aadhaar', 'uid', 'unique', 'identification', 'dob', 'male', 'female'],
                'hi': ['भारत सरकार', 'आधार', 'जन्म', 'पुरुष', 'महिला']
            },
            'passport': {
                'en': ['passport', 'surname', 'given', 'nationality', 'date of birth'],
                'hi': ['पासपोर्ट']
            },
            'pan': {
                'en': ['income tax', 'permanent account', 'pan', 'father'],
                'hi': ['आयकर', 'स्थायी']
            }
        }
        print("[SUCCESS] Models loaded!")
    
    def detect_document_region(self, image_path):
        """Detect document region using YOLO"""
        if not self.yolo_model:
            return None, None
        
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                print(f"[ERROR] Failed to read image: {image_path}")
                return None, None
                
            results = self.yolo_model(img, conf=0.3, verbose=False)
            
            if len(results[0].boxes) > 0:
                box = results[0].boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                
                # Add padding
                p = 20
                cropped = img[max(0, y1-p):min(img.shape[0], y2+p), 
                             max(0, x1-p):min(img.shape[1], x2+p)]
                print(f"[SUCCESS] YOLO detected document region (confidence: {conf:.2%})")
                return cropped, conf
            
            # Return full image if no detection
            return img, 1.0
            
        except Exception as e:
            print(f"[ERROR] YOLO detection failed: {e}")
            return None, None
    
    def preprocess_for_ocr(self, img):
        """Preprocess image for better OCR results"""
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # Apply CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply bilateral filter to denoise while preserving edges
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Apply thresholding
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def process_image(self, image_path):
        """Process image with OCR - Pass numpy arrays directly to EasyOCR"""
        try:
            # Read original image
            original_img = cv2.imread(str(image_path))
            if original_img is None:
                print(f"[ERROR] Could not read image: {image_path}")
                return [], None
            
            # Get cropped region from YOLO
            cropped, yolo_conf = self.detect_document_region(image_path)
            
            text_blocks = []
            
            # Try cropped region first if available
            if cropped is not None and cropped.size > 0:
                print(f"[INFO] Processing cropped region: {cropped.shape}")
                
                # Preprocess cropped image
                preprocessed = self.preprocess_for_ocr(cropped)
                
                # Convert back to BGR for EasyOCR (it expects BGR format)
                preprocessed_bgr = cv2.cvtColor(preprocessed, cv2.COLOR_GRAY2BGR)
                
                # Run OCR directly on numpy array
                print("[INFO] Running OCR on cropped region...")
                try:
                    results = self.reader.readtext(preprocessed_bgr, detail=1)
                    print(f"[DEBUG] OCR found {len(results)} raw results in cropped region")
                    
                    for item in results:
                        if len(item) >= 2:
                            text = item[1].strip()
                            conf = item[2] if len(item) > 2 else 0.9
                            print(f"[DEBUG] Text: '{text}' | Conf: {conf:.2f}")
                            if len(text) > 0 and conf > 0.1:
                                text_blocks.append({
                                    'text': text, 
                                    'confidence': float(conf)
                                })
                except Exception as e:
                    print(f"[WARNING] Cropped region OCR failed: {e}")
            
            # If no results, try full original image
            if len(text_blocks) == 0:
                print("[WARNING] No text in cropped region, trying full image...")
                
                # Preprocess full image
                preprocessed = self.preprocess_for_ocr(original_img)
                
                # Convert back to BGR for EasyOCR
                preprocessed_bgr = cv2.cvtColor(preprocessed, cv2.COLOR_GRAY2BGR)
                
                # Run OCR directly on numpy array
                print("[INFO] Running OCR on full image...")
                try:
                    results = self.reader.readtext(preprocessed_bgr, detail=1)
                    print(f"[DEBUG] OCR found {len(results)} results in full image")
                    
                    for item in results:
                        if len(item) >= 2:
                            text = item[1].strip()
                            conf = item[2] if len(item) > 2 else 0.9
                            print(f"[DEBUG] Text: '{text}' | Conf: {conf:.2f}")
                            if len(text) > 0 and conf > 0.1:
                                text_blocks.append({
                                    'text': text, 
                                    'confidence': float(conf)
                                })
                except Exception as e:
                    print(f"[ERROR] Full image OCR failed: {e}")
                    import traceback
                    traceback.print_exc()
            
            # If still no results, try original image without preprocessing
            if len(text_blocks) == 0:
                print("[WARNING] Trying original image without preprocessing...")
                try:
                    results = self.reader.readtext(original_img, detail=1)
                    print(f"[DEBUG] OCR found {len(results)} results in original")
                    
                    for item in results:
                        if len(item) >= 2:
                            text = item[1].strip()
                            conf = item[2] if len(item) > 2 else 0.9
                            print(f"[DEBUG] Text: '{text}' | Conf: {conf:.2f}")
                            if len(text) > 0 and conf > 0.05:  # Even lower threshold
                                text_blocks.append({
                                    'text': text, 
                                    'confidence': float(conf)
                                })
                except Exception as e:
                    print(f"[ERROR] Original image OCR failed: {e}")
            
            print(f"[SUCCESS] Extracted {len(text_blocks)} text blocks")
            return text_blocks, yolo_conf
            
        except Exception as e:
            print(f"[ERROR] Image processing failed: {e}")
            import traceback
            traceback.print_exc()
            return [], None
    
    def detect_file_type(self, file_path):
        """Detect file type from extension"""
        suffix = Path(file_path).suffix.lower()
        if suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
            return 'image'
        elif suffix == '.pdf':
            return 'pdf'
        elif suffix in ['.docx', '.doc']:
            return 'docx'
        return 'unknown'
    
    def detect_document_type(self, text_blocks):
        """Detect document type from text content"""
        all_text = ' '.join([b['text'].lower() for b in text_blocks])
        
        # Score each document type
        scores = {}
        for doc_type, patterns in self.doc_patterns.items():
            score = 0
            for lang, keywords in patterns.items():
                for kw in keywords:
                    if kw.lower() in all_text:
                        # Weight by keyword length and add bonus
                        score += len(kw.split()) + 2
            scores[doc_type] = score
        
        # If no keywords matched, try pattern matching
        if max(scores.values()) == 0:
            # Check for Aadhaar number pattern
            if re.search(r'\d{12}', all_text):
                return 'aadhaar', 0.6
            # Check for PAN pattern
            if re.search(r'[A-Z]{5}\d{4}[A-Z]', all_text):
                return 'pan', 0.7
            return 'unknown', 0.0
        
        # Return best match
        doc_type = max(scores, key=scores.get)
        confidence = min(scores[doc_type] / 20.0, 1.0)
        return doc_type, max(confidence, 0.5)
    
    def detect_document(self, file_path):
        """Main detection method"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        print(f"\n{'='*50}")
        print(f"[INFO] Processing: {file_path.name}")
        
        file_type = self.detect_file_type(file_path)
        
        if file_type == 'image':
            text_blocks, yolo_conf = self.process_image(file_path)
        elif file_type == 'pdf':
            return {'error': 'PDF processing not implemented in this version'}
        elif file_type == 'docx':
            return {'error': 'DOCX processing not implemented in this version'}
        else:
            return {'error': f'Unsupported file type: {file_type}'}
        
        if not text_blocks:
            return {'error': 'No text extracted from document'}
        
        # Calculate average OCR confidence
        avg_conf = sum(b['confidence'] for b in text_blocks) / len(text_blocks)
        
        # Detect document type
        doc_type, type_conf = self.detect_document_type(text_blocks)
        
        print(f"[SUCCESS] Document Type: {doc_type.upper()} (confidence: {type_conf:.1%})")
        print(f"{'='*50}\n")
        
        return {
            'document_type': doc_type,
            'type_confidence': float(type_conf),
            'text_blocks': text_blocks,
            'avg_ocr_confidence': float(avg_conf),
            'num_blocks': len(text_blocks),
            'file_type': file_type,
            'yolo_confidence': float(yolo_conf) if yolo_conf is not None else None
        }
    
    def extract_fields(self, detection_result):
        """Extract specific fields based on document type"""
        if 'error' in detection_result:
            return {}
            
        doc_type = detection_result.get('document_type')
        text_blocks = detection_result.get('text_blocks', [])
        
        if doc_type == 'aadhaar':
            return self._extract_aadhaar_fields(text_blocks)
        elif doc_type == 'passport':
            return self._extract_passport_fields(text_blocks)
        elif doc_type == 'pan':
            return self._extract_pan_fields(text_blocks)
        return {}
    
    def _extract_aadhaar_fields(self, text_blocks):
        """Extract Aadhaar-specific fields"""
        fields = {}
        all_text = ' '.join([b['text'] for b in text_blocks])
        
        # Aadhaar number (12 digits)
        match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', all_text)
        if match:
            fields['aadhaar_number'] = match.group().replace(' ', '')
        
        # Date of Birth
        match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', all_text)
        if match:
            fields['dob'] = match.group()
        
        # Gender
        match = re.search(r'\b(MALE|FEMALE|पुरुष|महिला)\b', all_text, re.IGNORECASE)
        if match:
            fields['gender'] = match.group().title()
        
        # Name (heuristic: text block with 2-4 words, no digits)
        for block in text_blocks:
            text = block['text'].strip()
            if block['confidence'] > 0.6 and 10 < len(text) < 50:
                if not any(c.isdigit() for c in text):
                    words = text.split()
                    if 2 <= len(words) <= 4:
                        fields['name'] = text
                        break
        
        return fields
    
    def _extract_passport_fields(self, text_blocks):
        """Extract Passport-specific fields"""
        fields = {}
        all_text = ' '.join([b['text'] for b in text_blocks])
        
        # Passport number
        match = re.search(r'\b[A-Z]\d{7,8}\b', all_text)
        if match:
            fields['passport_number'] = match.group()
        
        # Date of Birth
        match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', all_text)
        if match:
            fields['dob'] = match.group()
        
        # Surname
        for i, block in enumerate(text_blocks):
            if 'surname' in block['text'].lower():
                if i + 1 < len(text_blocks):
                    fields['surname'] = text_blocks[i + 1]['text']
                    break
        
        return fields
    
    def _extract_pan_fields(self, text_blocks):
        """Extract PAN-specific fields"""
        fields = {}
        all_text = ' '.join([b['text'] for b in text_blocks])
        
        # PAN number (format: ABCDE1234F)
        match = re.search(r'\b[A-Z]{5}\d{4}[A-Z]\b', all_text)
        if match:
            fields['pan_number'] = match.group()
        
        # Name
        for i, block in enumerate(text_blocks):
            text = block['text'].lower()
            if 'name' in text and i + 1 < len(text_blocks):
                fields['name'] = text_blocks[i + 1]['text']
                break
        
        # Date of Birth
        match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', all_text)
        if match:
            fields['dob'] = match.group()
        
        return fields


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = AdvancedDocumentDetector(languages=['en', 'hi'])
    
    # Process a document
    result = detector.detect_document("path/to/document.jpg")
    
    if 'error' not in result:
        print(f"Document Type: {result['document_type']}")
        print(f"Confidence: {result['type_confidence']:.2%}")
        print(f"Text blocks found: {result['num_blocks']}")
        
        # Extract specific fields
        fields = detector.extract_fields(result)
        print("\nExtracted Fields:")
        for key, value in fields.items():
            print(f"  {key}: {value}")
    else:
        print(f"Error: {result['error']}")