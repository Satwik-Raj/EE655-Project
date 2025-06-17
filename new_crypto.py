import cv2
import numpy as np
from cryptography.fernet import Fernet
import hashlib
def generate_key():
    return Fernet.generate_key()
def encrypt_data(data, key):
    return Fernet(key).encrypt(data)
def decrypt_data(data, key):
    return Fernet(key).decrypt(data)
def encode_image(cover_path, message_path, output_path, n, key):
    cover = cv2.imread(cover_path)
    message = cv2.imread(message_path)
    if cover is None or message is None:
        raise ValueError("Image loading failed.")

    message_flat = message.ravel()
    encrypted_bytes = encrypt_data(message_flat.tobytes(), key)
    binary_message = ''.join(f"{b:08b}" for b in encrypted_bytes)
    total_bits = len(binary_message)

    flat_cover = cover.ravel()
    if total_bits > flat_cover.size * n:
        raise ValueError("Cover image too small.")
   #  print(f"Encrypted length: {len(encrypted_bytes)} bytes") #debug
    # Generate consistent shuffle
    seed = int(hashlib.sha256(key).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    indices = np.random.permutation(flat_cover.size)[:(total_bits + n - 1) // n]

    # Vectorized bit chunk conversion
    bit_chunks = np.array([
        int(binary_message[i:i+n].ljust(n, '0'), 2)
        for i in range(0, total_bits, n)
    ], dtype=np.uint8)

    # Embed bits
    mask = 0xFF ^ ((1 << n) - 1)
    flat_cover[indices] = (flat_cover[indices] & mask) | bit_chunks

    stego = flat_cover.reshape(cover.shape)
    cv2.imwrite(output_path, stego)
    print(f"Stego-image saved as {output_path}")
    return total_bits

def decode_image(stego_path, message_width, message_height, output_path, n, key, total_bits):
    stego = cv2.imread(stego_path)
    if stego is None:
        raise ValueError("Failed to load stego image.")

    flat = stego.ravel()
    seed = int(hashlib.sha256(key).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    indices = np.random.permutation(flat.size)[:(total_bits + n - 1) // n]

    # Extract bits fast
    extracted = flat[indices] & ((1 << n) - 1)
    bit_str = ''.join(f"{val:0{n}b}" for val in extracted)
    bit_str = bit_str[:total_bits]

   #  print(f"Extracted bits: {len(bit_str)} / Expected: {total_bits}") #debug

    # Convert bits to bytes
    byte_data = bytes(int(bit_str[i:i+8], 2) for i in range(0, total_bits, 8))
    decrypted = decrypt_data(byte_data, key)

    # Reconstruct image
    flat_msg = np.frombuffer(decrypted, dtype=np.uint8)
    expected = message_width * message_height * 3
    if len(flat_msg) < expected:
        print("[ERROR] Decrypted message too short.")
        return

    img = flat_msg[:expected].reshape((message_height, message_width, 3))
    cv2.imwrite(output_path, img)
    print(f"Decoded message saved as {output_path}")


if __name__ == "__main__":
    
    choice = input("Give me the cover image path: ")
    cover_path = choice
   #  cover_path = "rcb.jpg" //default cover
    choice = input("Give me the message image path: ")
    message_path = choice
   #  message_path = "trophy.jpg"//default message
    output_stego = "stego.png"
    output_message = "decoded_message.png"
    n = 4  # bits per channel, can change at any point of time later

    message_img = cv2.imread(message_path)
    if message_img is None:
        raise ValueError("Can't read message image.")

    mh, mw = message_img.shape[:2]
    key = generate_key() # same key for both encoding and decoding
    while True:
      choice = input("Do you want to start encoding the message? (y/n/quit): ")
      if choice.lower() in ["y","yes"]:
          print("Encoding the message...")
          break
      elif choice.lower() in ["quit","exit"]:
          print("Exiting.")
          exit()
    try:
        total_bits = encode_image(cover_path, message_path, output_stego, n, key)
    except Exception as e:
        print(f"[ERROR] Encoding failed: {e}")
        exit()
    choice = input("Do you want to decode the message? (y/n): ")
    if not choice.lower() in ["y","yes"]:
        print("Exiting without decoding.")
        exit()
    # Decode the message
    print("Decoding the message...")
    try:
        decode_image(output_stego, mw, mh, output_message, n, key, total_bits)
    except Exception as e:
        print(f"[ERROR] Decoding failed: {e}")