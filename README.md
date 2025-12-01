# Kabutr | Secure Image Steganography

**Kabutr** is a powerful web application that allows you to hide secret text messages inside images using advanced steganography techniques combined with AES encryption. It ensures that your secrets remain invisible and secure.

![Kabutr Hero](https://via.placeholder.com/800x400?text=Kabutr+Steganography)

## 🚀 Features

-   **Invisible Storage:** Hides text messages within the pixels of an image without any visible loss of quality.
-   **Double Security:** Uses **AES Encryption (Fernet)** to encrypt your message before hiding it. Even if the data is extracted, it cannot be read without the password.
-   **Client-Side Feel:** Powered by AJAX for seamless, no-refresh interactions.
-   **Fast Processing:** Optimized algorithms using NumPy and OpenCV for millisecond-level encoding and decoding.
-   **Responsive Design:** Fully responsive UI that works perfectly on Desktops, Tablets, and Mobile devices.
-   **Modern UI:** Built with Bootstrap 5 and custom CSS for a premium look and feel.

## 🛠️ Tech Stack

-   **Backend:** Python, Flask
-   **Image Processing:** OpenCV (`cv2`), NumPy, Pillow (`PIL`)
-   **Encryption:** Cryptography (`Fernet`, `PBKDF2HMAC`)
-   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Animate.css

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pradeepx-dev/Kabutr.git
    cd Kabutr
    ```

2.  **Create a virtual environment (Optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

## 📖 How It Works

1.  **Encryption:** The secret message is first encrypted using a key derived from your password (PBKDF2HMAC-SHA256) and a random salt.
2.  **Formatting:** The payload is structured as: `[Length (4 bytes)] + [Magic Header (STG1)] + [Salt (16 bytes)] + [Encrypted Data]`.
3.  **Embedding:** The binary bits of this payload are embedded into the Least Significant Bits (LSB) of the image pixels.
4.  **Result:** A new PNG image is generated that looks identical to the original but contains your hidden secret.

## 📝 Usage

### Encoding (Hiding)
1.  Upload a PNG or JPG image.
2.  Enter your secret message.
3.  Set a strong password.
4.  Click **Encrypt & Hide Message**.
5.  Download the resulting "Stego Image".

### Decoding (Revealing)
1.  Upload the encoded "Stego Image".
2.  Enter the password used during encryption.
3.  Click **Decrypt & Reveal Message**.
4.  Your secret message will appear on the screen.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---
Created with ❤️ by [pradeepx-dev](https://github.com/pradeepx-dev)
