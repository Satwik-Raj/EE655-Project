# 🔐 Crypto-Based Image Steganography Tool

> A secure and flexible Python-based steganography system that embeds encrypted data into images using cryptographic randomness and LSB encoding.

## 🌟 Project Overview

This project presents a cryptographically-enhanced image steganography system that securely hides a **message image** inside a **cover image**, with minimal visual distortion. Unlike traditional LSB (Least Significant Bit) methods, this tool leverages **symmetric encryption** and **pseudo-randomized bit placement**, ensuring that only users with the correct key can retrieve the hidden message.

---

## ✨ Features

- 🔒 **Cryptographic Embedding**  
  Uses a user-provided key to:
  - Encrypt the message using Fernet symmetric encryption.
  - Seed a pseudo-random generator to securely select pixel locations for embedding.

- 🎚️ **Bit-Depth Flexibility**  
  Supports 1 to 8 bits per pixel channel for embedding — choose between stealth or higher capacity.

- 🖼️ **Multi-Format Image Support**  
  Supports common image formats like JPEG, PNG, and BMP via OpenCV, assuming the files are readable.

- 🧪 **Robust Against Attacks**  
  Without the correct key:
  - Pixel positions remain unpredictable.
  - Decrypted content is inaccessible.

- 💻 **User-Friendly CLI**  
  Simple prompts to encode and decode messages, with minimal user configuration.

---

## 🔧 Methodology

### 1. **Encoding Process**
- Load cover and message images.
- Encrypt message bytes using Fernet.
- Convert encrypted bytes to binary.
- Pseudo-randomly select pixel positions using a key-seeded NumPy RNG.
- Embed bits using LSB across chosen indices.

### 2. **Decoding Process**
- Load stego image.
- Pseudo-randomly retrieve embedding indices using the same key.
- Extract bits and decrypt them to reconstruct the original message image.

---

## 🛡️ Security Architecture

- **Encryption**: Fernet ensures both confidentiality and integrity.
- **Key-based Embedding**: The embedding process is tied to the key, making reverse-engineering infeasible.
- **Layered Defense**:
  - Obscured pixel positions
  - Encrypted message content
  - No key = no message

---

## 🖥️ Usage

### 🔐 Encode

```bash
$ python steg_tool.py
Give me the cover image path: cover.jpg
Give me the message image path: secret.png
Do you want to start encoding the message? (y/n): y
```

### 🔓 Decode

```bash
Do you want to decode the message? (y/n): y
```

The stego image will be saved as `stego.png`, and the recovered message as `decoded_message.png`.

---

## 🧪 Experimental Results

- **Visual Quality**: Stego images were nearly indistinguishable from original cover images even at 4-bit embedding.
- **Recovery**: Decoded messages matched the original with high fidelity.
- **Security**: Unauthorized decoding attempts without the key fail completely, validating cryptographic security.

---

## 📁 Sample Output

| Original Cover | Stego Image |
|----------------|-------------|
| ![](rcb.jpg) | ![](stego.png) |

| Original Message | Decoded Message |
|------------------|-----------------|
| ![](trophy.jpg) | ![](decoded_message.png) |

---

## 🧠 Tech Stack

- Python 3
- OpenCV (`cv2`)
- NumPy
- Cryptography (`Fernet`)

---

## 👨‍💻 Developers

- Satwik Raj Wadhwa (230937)
- Gaurav Kumar (230792)
- Vinay Chavan (231155)
- Pritam Priyadarshi (230793)  
*EE655, IIT Kanpur — Guided by Prof. Koteswar Jerripothula*

---

## 📜 License

This project is part of a university course and is intended for academic use only. Contact the developers for further usage permissions.
