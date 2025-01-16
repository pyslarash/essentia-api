# Essentia API

Essentia API is a Python/Flask-based API designed for seamless interaction with Essentia models, providing advanced audio analysis and music information retrieval. The API supports both GPU and CPU environments for efficient performance.

---

## 🚀 Quick Start with Docker

The easiest way to run this project is by pulling the pre-built Docker image from Docker Hub.

### **1. Pull the Docker Image**
```bash
docker pull pyslarash/essentia-api
```

### **2. Run the Container**
- **With GPU support** (for accelerated processing):
  ```bash
  docker run --gpus all -p 9878:9878 pyslarash/essentia-api
  ```

- **Without GPU support** (defaults to CPU):
  ```bash
  docker run -p 9878:9878 pyslarash/essentia-api
  ```

### **3. Access the API**
Open your browser and navigate to:
```
http://localhost:9878
```
Explore the API endpoints and start analyzing audio right away!

---

## Features
- Pre-configured API for Essentia models.
- Supports GPU acceleration for faster audio processing.
- Easily accessible API endpoints on port `9878`.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality.

---

## Acknowledgments
This project utilizes the [Essentia library](https://essentia.upf.edu/) for audio analysis and music information retrieval.

---

<div>
	<code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/></code>
	<code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/flask.png" alt="Flask" title="Flask"/></code>
	<code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/tensorflow.png" alt="TensorFlow" title="TensorFlow"/></code>
</div>
