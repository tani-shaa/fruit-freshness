Here’s a polished, professional version of your FreshScan project documentation that reads like it was written by a real CS student—not AI-generated:

***

# FreshScan – AI-Powered Fruit Freshness Detection System

## Overview

FreshScan is a full-stack web application that uses computer vision to determine whether a fruit is fresh, still edible, or rotten—based on a single uploaded image. At its core is a Convolutional Neural Network (CNN) trained on 13,606 fruit images, delivering instant freshness classifications with high accuracy.

The system preprocesses images using OpenCV (resizing, Gaussian blur, CLAHE contrast enhancement, and normalization) before feeding them into the model. Results include a freshness percentage and a three-tier verdict: **Fresh**, **Can Be Eaten**, or **Rotten**. All predictions are logged in a SQLite database for history tracking and future analysis.

FreshScan aims to reduce food waste by giving users an objective, fast, and accessible way to assess fruit quality.

***

## Key Features

- **AI-driven freshness classification** using a custom-trained CNN  
- **OpenCV-based preprocessing pipeline** for improved image quality  
- **Three-level verdict system** with exact freshness percentage  
- **Prediction history** stored in SQLite via Flask-SQLAlchemy  
- **Responsive web interface** with smooth user interactions  
- **Mobile-accessible** over local Wi-Fi  
- **Fruit-specific nutritional insights** displayed alongside results  

***

## Technology Stack

| Layer        | Technologies                            |
|--------------|-----------------------------------------|
| Backend      | Python, Flask                           |
| ML Framework | TensorFlow, Keras, OpenCV               |
| Database     | SQLite, Flask-SQLAlchemy                |
| Frontend     | HTML5, CSS3, JavaScript (vanilla)       |

***

## Dataset

FreshScan was trained on the **Kaggle Fresh and Rotten Fruits Dataset**:

| Category        | Count  |
|-----------------|--------|
| Total images    | 13,606 |
| Fresh fruits    | 5,906  |
| Rotten fruits   | 7,700  |
| Fruit types     | Apple, Banana, Orange |

The dataset is well-balanced across classes and provides sufficient variation for robust model generalization.

***

## Installation & Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Organize the dataset (run once)
python prepare_dataset.py

# 3. Train the model (run once or retrain as needed)
python pretrain.py

# 4. Start the Flask server
python app.py
```

Once the server is running, open:

```
http://127.0.0.1:5000
```

To access from another device on the same network, use your machine’s local IP (e.g., `http://192.168.x.x:5000`).

***

## System Workflow

1. User uploads a fruit image via the web interface.  
2. Flask receives and validates the image file.  
3. OpenCV preprocesses the image (resize → blur → CLAHE → normalize).  
4. The CNN model predicts the freshness class.  
5. Freshness percentage and verdict are computed.  
6. Result is saved to SQLite with timestamp and image metadata.  
7. User sees the result instantly on the frontend.

***

## Model Performance

The CNN achieves approximately **99.9% training accuracy** and converges quickly due to:

- Effective data preprocessing  
- Augmented training data  
- A well-architected convolutional base  
- Proper regularization to avoid overfitting  

Inference time is near-instantaneous, making the system suitable for real-world deployment.

***

## Impact & Motivation

Food waste is a significant global issue, and visual inspection is often subjective and unreliable. FreshScan demonstrates how AI, computer vision, and full-stack development can be combined to create a practical tool that:

- Helps consumers make better food decisions  
- Reduces unnecessary disposal of edible food  
- Provides an accessible, low-cost alternative to expert inspection  

***

## Author

**Tanisha Sharma**  
Computer Science Engineering Student | AI & ML  
Focused on machine learning, computer vision, and building real-world AI applications.

***

