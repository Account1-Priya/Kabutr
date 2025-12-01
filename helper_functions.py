import cv2 
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

# Magic header to identify valid steganography images
MAGIC_HEADER = b"STG1"

def derive_key(password, salt):
    """
    Derives a key from a password using PBKDF2
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_message(message, password):
    """
    Encrypts a message using AES (Fernet) and a password.
    Returns: salt (16 bytes) + encrypted_token
    """
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(message.encode('utf-8'))
    return salt + token

def decrypt_message(data, password):
    """
    Decrypts a message using AES (Fernet) and a password.
    Expects data to be: salt (16 bytes) + encrypted_token
    """
    try:
        if len(data) < 16:
            return "Error: Incorrect password or corrupted data."
        
        salt = data[:16]
        token = data[16:]
        
        key = derive_key(password, salt)
        f = Fernet(key)
        return f.decrypt(token).decode('utf-8')
    except Exception:
        # Generic error message to avoid leaking internals
        return "Error: Incorrect password or corrupted data."

def ensure_rgb_uint8(image):
    """
    Ensures the image is in RGB format and uint8 dtype.
    Converts Grayscale and BGRA to BGR.
    Strictly enforces 3 channels.
    """
    if image.dtype != np.uint8:
        raise ValueError("Image must be uint8 type")
    
    # Handle Grayscale (2D array)
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Handle BGRA (3D array with 4 channels)
    elif image.ndim == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    
    # Strict check for 3 channels
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"Image must have 3 channels (RGB/BGR). Found shape: {image.shape}")
        
    return image

def encode(image, message, password):
    """
    Hides an encrypted message in the image using LSB steganography.
    Format: [4 bytes length][4 bytes magic][16 bytes salt][encrypted_data]
    """
    image = ensure_rgb_uint8(image)

    # Early capacity check: Ensure image can at least hold the header (4 bytes len + 4 bytes magic = 64 bits)
    if image.size < 64:
        raise ValueError("Image resolution is too small to safely encode data.")

    # 1. Encrypt the message
    encrypted_payload = encrypt_message(message, password)
    
    # 2. Prepare the full payload with length header and magic signature
    # Payload = Magic + Salt + Encrypted Data
    payload_content = MAGIC_HEADER + encrypted_payload
    payload_length = len(payload_content)
    
    length_header = payload_length.to_bytes(4, 'big')
    full_payload = length_header + payload_content
    
    # 3. Convert to bits (Optimized using numpy)
    payload_bytes_arr = np.frombuffer(full_payload, dtype=np.uint8)
    payload_bits = np.unpackbits(payload_bytes_arr)
    
    needed_bits = len(payload_bits)
    total_bits_available = image.size # H * W * 3
    
    # 4. Check capacity
    if needed_bits > total_bits_available:
        raise ValueError(f"Message too large. Needed bits: {needed_bits}, but only {total_bits_available} bits available.")
    
    # 5. Flatten image to 1D array
    flat_image = image.flatten()
    
    # 6. Embed bits (Safe Slicing)
    # Use explicit view slicing to prevent overflow and ensure safe writing
    flat_image_view = flat_image[:needed_bits]
    flat_image_view &= 0xFE
    flat_image_view |= payload_bits
        
    # 7. Reshape back to original image
    encoded_image = flat_image.reshape(image.shape)
    
    return encoded_image

def decode_image(image, password):
    """
    Extracts and decrypts a message from an image.
    """
    image = ensure_rgb_uint8(image)
    flat_image = image.flatten()
    
    # 1. Extract length header (first 32 bits = 4 bytes)
    header_bits = flat_image[:32] & 1
    header_bytes = np.packbits(header_bits)
    payload_length = int.from_bytes(header_bytes.tobytes(), 'big')
    
    # Validate length
    if payload_length <= 0:
         return "Error: No valid steganography data found."
    
    # Enhanced Decode Robustness: Check if payload fits in remaining image
    max_payload_bytes = (len(flat_image) - 32) // 8
    if payload_length > max_payload_bytes:
        return "Error: Encoded data incomplete or corrupted."
    
    total_payload_bits = payload_length * 8
    end_index = 32 + total_payload_bits
    
    # Check for truncation (Redundant but safe double-check)
    if end_index > len(flat_image):
        return "Error: Encoded data incomplete or corrupted."

    # 2. Extract payload bits
    payload_bits = flat_image[32:end_index] & 1
    payload_bytes = np.packbits(payload_bits).tobytes()
    
    # 3. Verify Magic Header
    if len(payload_bytes) < 4 or payload_bytes[:4] != MAGIC_HEADER:
        return "Error: No valid steganography data found."
        
    # 4. Decrypt (skip magic header)
    encrypted_data = payload_bytes[4:]
    return decrypt_message(encrypted_data, password)