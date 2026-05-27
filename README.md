# 🍎 FreshScan – AI Fruit Freshness Detection System

## Project Overview

FreshScan is an AI-powered web application that determines the freshness of fruits from a single uploaded image. The system uses a Convolutional Neural Network (CNN) trained on over 13,000 fruit images to classify fruits as **Fresh**, **Can be Eaten**, or **Rotten**. Images are preprocessed using OpenCV techniques such as resizing, Gaussian blurring, CLAHE contrast enhancement, and normalization to improve prediction accuracy.

The application is built using **Python, Flask, TensorFlow/Keras, OpenCV, SQLite, HTML, CSS, and JavaScript**. Users can upload a fruit image through an intuitive web interface and instantly receive a freshness score along with a verdict. All predictions are stored in a SQLite database, enabling history tracking and analysis.

By providing quick and objective freshness assessment, FreshScan helps reduce food waste and supports smarter food consumption decisions.

---

## 🚀 Features

- AI-powered fruit freshness detection using CNN
- OpenCV image preprocessing pipeline
- Freshness score with three-level verdict system
- Prediction history tracking with SQLite database
- Responsive and interactive web interface
- Mobile accessibility over local Wi-Fi network
- Nutritional information and fruit insights

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Machine Learning
- TensorFlow
- Keras
- OpenCV

### Database
- SQLite
- Flask-SQLAlchemy

### Frontend
- HTML
- CSS
- JavaScript

---

## 📊 Dataset

- Source: Kaggle Fresh and Rotten Fruits Dataset
- Total Images: 13,606
- Fresh Images: 5,906
- Rotten Images: 7,700
- Fruits Covered: Apple, Banana, Orange

---

## ⚙️ Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Organise dataset (first time only)
python prepare_dataset.py

# Train model (first time only)
python pretrain.py

# Run application
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🏗️ System Workflow

1. User uploads a fruit image.
2. Flask receives the image.
3. OpenCV preprocesses the image.
4. CNN predicts freshness.
5. Freshness percentage and verdict are generated.
6. Result is stored in SQLite.
7. Prediction is displayed instantly to the user.

---

## 🎯 Outcome

The trained CNN model achieved approximately **99.9% training accuracy** and provides near-instant predictions. FreshScan demonstrates the practical application of Artificial Intelligence, Computer Vision, and Full-Stack Web Development in solving real-world food waste problems.

---

## 👩‍💻 Author

**Tanisha Sharma**

Computer Science Engineering Student | Data Science Enthusiast