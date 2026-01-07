
# 🌐 VisaFlow AI

<img width="1919" height="969" alt="image" src="https://github.com/user-attachments/assets/5fc88d1f-573a-4013-ac48-c38b8b55bc2a" />
<img width="1904" height="970" alt="image" src="https://github.com/user-attachments/assets/6a099b7c-fd6e-46f0-833e-44c077cd3932" />
<img width="1899" height="953" alt="image" src="https://github.com/user-attachments/assets/74ae65d1-378d-4b4a-a8ec-a65dcf7735ba" />
<img width="1880" height="841" alt="image" src="https://github.com/user-attachments/assets/75ad6d4a-af3b-4b78-b8b3-e4ef8fbf27db" />




## AI-Driven Document Intelligence & Visa Assistance System

VisaFlow AI is a **computer vision + OCR + LLM–assisted application** built using **Python and Streamlit**.
The system focuses on **document understanding** and **visa-related assistance** by combining:

* **YOLOv8** for document region detection
* **EasyOCR** for multi-language text extraction
* **Rule-based + regex logic** for structured field extraction
* **Large Language Models (Gemini)** for visa assistance and conversational support

The project demonstrates how **classical CV pipelines and modern LLMs** can be integrated into a single, modular AI system.

---

## 🎯 Core Objectives

* Detect and isolate documents from uploaded images
* Extract text from multilingual identity documents
* Classify document type using extracted text
* Extract structured fields (ID numbers, DOB, names, etc.)
* Provide AI-generated visa guidance through a chatbot interface

---

## 🧠 System Design Overview

```
Input Document / User Query
        │
        ├── Image / File Upload
        │       │
        │       ▼
        │  YOLOv8 Document Detection
        │       │
        │       ▼
        │  Image Preprocessing (CV)
        │       │
        │       ▼
        │  EasyOCR (Multi-language)
        │       │
        │       ▼
        │  Text Blocks + Confidence Scores
        │       │
        │       ▼
        │  Rule-Based Document Classification
        │       │
        │       ▼
        │  Field Extraction (Regex + Heuristics)
        │
        └── User Chat / Visa Query
                │
                ▼
          Gemini LLM (Visa Assistant)
```

---

## 📄 Document Intelligence Pipeline

### 1️⃣ Document Detection (YOLOv8)

* Uses **YOLOv8 (ultralytics)** with the `yolov8n.pt` model
* Detects document regions inside uploaded images
* Crops detected regions with padding
* Falls back to full-image processing if detection fails
* Detection confidence is captured and shown in UI

**Purpose:**
Improve OCR accuracy by reducing background noise.

---

### 2️⃣ Image Preprocessing (Computer Vision)

Before OCR, images undergo:

* Grayscale conversion
* CLAHE (Contrast Limited Adaptive Histogram Equalization)
* Bilateral filtering (noise reduction while preserving edges)
* Otsu thresholding

This preprocessing pipeline is implemented manually using **OpenCV**.

---

### 3️⃣ OCR (EasyOCR)

* Uses **EasyOCR** with selectable languages
* OCR is executed directly on NumPy arrays
* Multi-pass strategy:

  * Cropped region OCR
  * Full image OCR (preprocessed)
  * Original image OCR (fallback)
* Each text block includes a confidence score

---

## 🗂️ Document Type Detection

Document type is inferred using:

* Keyword matching across extracted text
* Language-specific keyword dictionaries
* Regex fallback for:

  * Aadhaar numbers (12 digits)
  * PAN numbers (ABCDE1234F)

Supported document types:

* Aadhaar Card
* Passport
* PAN Card

---

## 🧾 Structured Field Extraction

After classification, document-specific extraction is performed.

### Aadhaar

* Aadhaar number
* Name (heuristic-based)
* Date of Birth
* Gender

### Passport

* Passport number
* Date of Birth
* Surname (relative position heuristic)

### PAN

* PAN number
* Name
* Date of Birth

Extraction is implemented using **regex + positional heuristics**, not ML models.

---

## 🤖 LLM-Based Visa Assistant

VisaFlow AI integrates a **Large Language Model (Gemini)** for conversational and informational tasks.

### Implemented Capabilities

* Visa-related Q&A via chat interface
* Country-to-country visa requirement queries
* Purpose-based visa guidance (tourist, student, business, etc.)
* Free-text reasoning and explanation

### Important Notes

* Responses are **LLM-generated**
* No scraping or official government API is used
* Output is informational, not legally binding

The LLM logic is isolated in `llm_assistant.py`.

---

## 🖥️ Streamlit Application

* Multi-page Streamlit UI:

  * Document Scanner
  * Visa Requirements
  * AI Assistant
  * About
* Custom CSS for layout and styling
* Displays:

  * Detection confidence
  * OCR confidence
  * Extracted fields
  * Text blocks (expandable)
* Stateful chat history for chatbot interaction

---

## 🧠 LLM + CV Integration Focus

This project demonstrates:

* Practical integration of **deep learning (YOLO)** with **OCR pipelines**
* Use of **LLMs as reasoning and assistance layers**
* Separation of concerns:

  * CV/OCR → deterministic pipelines
  * LLM → reasoning & natural language tasks
* Modular AI system design

---

## 🛠️ Tech Stack

### 🧠 AI / ML

* YOLOv8 (Ultralytics)
* EasyOCR
* Google Gemini LLM
* PyTorch

### 🖼️ Computer Vision

* OpenCV
* CLAHE
* Bilateral Filtering
* Thresholding
* NumPy

### 🌐 Application

* Streamlit
* Python 3.12
* Regex
* PIL / Pillow
* PyMuPDF (PDF handling – partial)

---

## 📂 Project Structure

```
VisaFlow-AI/
├── app.py                         # Streamlit application
├── src/
│   ├── document_detector_advanced.py  # CV + OCR + detection logic
│   └── llm_assistant.py               # Gemini-based visa assistant
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Execution

```bash
git clone https://github.com/antra04/VisaFlow-AI.git
cd VisaFlow-AI
pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Run:

```bash
streamlit run app.py
```

---

## 🧪 Sample Output

```
Document Type: Aadhaar
YOLO Confidence: 0.91
Average OCR Confidence: 0.76

Extracted Fields:
Name: Antra Tiwari
DOB: 14/04/2004
Gender: Female
Aadhaar Number: 4078XXXXXXXX
```

---

## ⚠️ Limitations (As of Current Code)

* PDF and DOCX parsing is minimal
* Document classification is rule-based
* No fine-tuned OCR or detection models
* LLM output is non-deterministic

---

## 👩‍💻 Author

**Antra Tiwari**
B.Tech CSE
Focus: AI / ML • Computer Vision • LLM Systems

GitHub: [https://github.com/antra04](https://github.com/antra04)

---

