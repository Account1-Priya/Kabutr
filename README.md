# Kabutr

> A secure, production-ready web application for image steganography with AES encryption

**Kabutr** is a sophisticated steganography application that enables users to securely embed encrypted text messages within digital images. By combining advanced LSB (Least Significant Bit) steganography techniques with industry-standard AES encryption, Kabutr ensures that hidden messages remain both invisible and protected against unauthorized access.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

**Live Demo:** [kabutr.onrender.com](https://kabutr.onrender.com/)

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Security Considerations](#security-considerations)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Features

### Core Capabilities

- **🔒 Advanced Encryption**: Messages are encrypted using AES-256 (Fernet) with PBKDF2 key derivation (100,000 iterations) before embedding
- **🖼️ Invisible Embedding**: LSB steganography ensures zero visible quality degradation in the host image
- **🔐 Password Protection**: Strong cryptographic key derivation from user passwords with random salt generation
- **⚡ High Performance**: Optimized NumPy and OpenCV operations for millisecond-level encoding/decoding
- **🌐 Modern Web Interface**: Responsive, AJAX-powered UI with Bootstrap 5 and custom animations
- **📱 Cross-Platform**: Fully responsive design supporting desktop, tablet, and mobile devices
- **✅ Data Integrity**: Magic header validation and comprehensive error handling for robust operation

### Technical Highlights

- **Format Support**: PNG and JPG input/output with automatic format conversion
- **Capacity Management**: Automatic validation of image capacity before encoding
- **Error Handling**: Comprehensive error messages for invalid inputs, corrupted data, and incorrect passwords
- **Client-Side Processing**: Seamless user experience with no page refreshes

---

## Technology Stack

### Backend
- **Framework**: Flask 2.0+
- **Language**: Python 3.9+

### Image Processing
- **OpenCV** (`cv2`): Advanced image manipulation and format conversion
- **NumPy**: High-performance array operations for bit manipulation
- **Pillow (PIL)**: Image I/O and format handling

### Cryptography
- **cryptography**: Fernet (AES-128 in CBC mode) for symmetric encryption
- **PBKDF2HMAC**: Password-based key derivation with SHA-256 hashing

### Frontend
- **HTML5/CSS3**: Modern semantic markup and styling
- **JavaScript**: AJAX for asynchronous operations
- **Bootstrap 5**: Responsive UI framework
- **Animate.css**: Smooth animations and transitions

---

## Architecture

### Encoding Pipeline

```
User Input (Image + Message + Password)
    ↓
Message Encryption (AES-256 Fernet)
    ↓
Payload Construction [Length | Magic Header | Salt | Encrypted Data]
    ↓
LSB Embedding (Least Significant Bit Steganography)
    ↓
Stego Image Output (PNG)
```

### Decoding Pipeline

```
Stego Image Input
    ↓
LSB Extraction
    ↓
Magic Header Validation
    ↓
Payload Extraction [Salt | Encrypted Data]
    ↓
Message Decryption (AES-256 Fernet)
    ↓
Decrypted Message Output
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/pradeepx-dev/Kabutr.git
   cd Kabutr
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000` (or the port specified in `app.py`)

### Production Deployment

For production deployment (e.g., on Render, Heroku, or similar platforms):

1. Ensure `Procfile` is configured correctly
2. Set appropriate environment variables
3. Use a production WSGI server (e.g., Gunicorn)
4. Configure proper security headers and HTTPS

---

## Usage

### Encoding a Message (Hiding)

1. Navigate to the application homepage
2. Click on the **"Encrypt & Hide Message"** tab
3. Upload a PNG or JPG image file
4. Enter the secret message you wish to hide
5. Set a strong password (used for encryption)
6. Click **"Encrypt & Hide Message"**
7. Download the generated stego image

**Note**: The stego image will appear visually identical to the original image.

### Decoding a Message (Revealing)

1. Navigate to the application homepage
2. Click on the **"Decrypt & Reveal Message"** tab
3. Upload the stego image that contains the hidden message
4. Enter the password used during encoding
5. Click **"Decrypt & Reveal Message"**
6. The decrypted message will be displayed

**Important**: You must use the exact same password that was used during encoding. Incorrect passwords will result in an error message.

---

## How It Works

### Encryption Process

1. **Key Derivation**: The user's password is processed through PBKDF2HMAC with:
   - Algorithm: SHA-256
   - Iterations: 100,000
   - Salt: 16-byte random salt (unique per message)
   - Key Length: 32 bytes (256 bits)

2. **Message Encryption**: The plaintext message is encrypted using Fernet (AES-128 in CBC mode) with the derived key.

3. **Payload Construction**: The encrypted data is packaged with:
   - **Length Header** (4 bytes): Total payload size
   - **Magic Header** (4 bytes): `STG1` identifier for validation
   - **Salt** (16 bytes): Random salt used for key derivation
   - **Encrypted Data**: The Fernet-encrypted message

### Steganography Process

1. **Image Preparation**: The input image is converted to RGB format (3 channels) with uint8 data type.

2. **Capacity Check**: The application verifies that the image has sufficient pixels to store the payload:
   - Required bits = (4 + 4 + 16 + encrypted_data_length) × 8
   - Available bits = image_height × image_width × 3

3. **LSB Embedding**: 
   - The payload is converted to a binary bit stream
   - Each bit is embedded into the least significant bit of image pixel values
   - The image is flattened to a 1D array for efficient processing
   - Bits are embedded sequentially across all color channels

4. **Image Reconstruction**: The modified pixel array is reshaped back to the original image dimensions.

### Decryption Process

1. **LSB Extraction**: The least significant bits are extracted from the stego image pixels.

2. **Length Validation**: The first 32 bits (4 bytes) are read to determine the payload length.

3. **Magic Header Verification**: The next 32 bits are checked for the `STG1` magic header to ensure valid steganography data.

4. **Salt Extraction**: The 16-byte salt is extracted from the payload.

5. **Key Derivation**: The same PBKDF2HMAC process is used with the extracted salt to derive the decryption key.

6. **Message Decryption**: The encrypted data is decrypted using Fernet and the derived key.

---

## Security Considerations

### Cryptographic Security

- **Strong Encryption**: AES-256 encryption provides industry-standard security
- **Key Derivation**: PBKDF2 with 100,000 iterations makes brute-force attacks computationally expensive
- **Random Salt**: Each message uses a unique salt, preventing rainbow table attacks
- **Secure Random Generation**: Uses `os.urandom()` for cryptographically secure random number generation

### Steganography Security

- **Invisibility**: LSB modification is imperceptible to human eyes
- **Format Preservation**: Output images maintain visual fidelity
- **Magic Header**: Prevents false positives and validates data integrity

### Best Practices

- **Password Strength**: Users should use strong, unique passwords
- **Image Selection**: Larger images provide more capacity and better security through obscurity
- **Secure Transmission**: Always use HTTPS in production environments
- **Data Disposal**: Securely delete original images and messages after use if handling sensitive data

### Limitations

- **Capacity Constraints**: Message size is limited by image dimensions
- **Format Requirements**: Input images must be in PNG or JPG format
- **Password Dependency**: Lost passwords result in permanent data loss (by design)
- **Not Quantum-Resistant**: Current encryption algorithms are not quantum-resistant

---

## Development

### Project Structure

```
Kabutr/
├── app.py                 # Flask application and route handlers
├── helper_functions.py    # Core steganography and encryption logic
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── LICENSE               # MIT License
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Frontend template
└── static/
    ├── css/              # Stylesheet directory
    ├── style.css         # Custom styles
    └── favicon.png       # Site favicon
```

### Running in Development Mode

```bash
python app.py
```

The application will run with debug mode enabled on `http://127.0.0.1:5000`.

### Code Quality

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Include docstrings for all functions
- Handle exceptions appropriately
- Validate all user inputs

---

## Contributing

Contributions are welcome and encouraged! To contribute:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with appropriate tests and documentation
4. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### Contribution Guidelines

- Ensure all code follows the existing style and conventions
- Add comments and docstrings for new functions
- Test your changes thoroughly
- Update documentation as needed
- Keep commits focused and atomic

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2025 Pradeep Kumar Maurya**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the conditions specified in the LICENSE file.

---

## Author

**Pradeep Kumar Maurya**

- GitHub: [@pradeepx-dev](https://github.com/pradeepx-dev)
- Project Link: [https://github.com/pradeepx-dev/Kabutr](https://github.com/pradeepx-dev/Kabutr)

**Anurag Kumar**

- GitHub: [@Account1-Anurag](https://github.com/Account1-Anurag)
- Project Link: [https://github.com/Account1-Anurag/Kabutr](https://github.com/Account1-Anurag/Kabutr)
---

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Image processing powered by [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/)
- Cryptography provided by [cryptography](https://cryptography.io/)
- UI framework: [Bootstrap](https://getbootstrap.com/)

---

**Note**: This tool is intended for legitimate purposes only. Users are responsible for complying with all applicable laws and regulations regarding the use of steganography and encryption technologies.
