import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def generate_and_store_keys(env_file_path=".env"):
    # Generate the Ed25519 private key
    private_key = ed25519.Ed25519PrivateKey.generate()
    
    # Serialize private key to PEM format
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Generate the corresponding public key
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write to .env file securely
    with open(env_file_path, "w") as f:
        f.write(f"PVSAD_PRIVATE_KEY='{private_bytes.decode('utf-8')}'\n")
        f.write(f"PVSAD_PUBLIC_KEY='{public_bytes.decode('utf-8')}'\n")
        
    # Restrict file permissions so only the owner can read/write
    os.chmod(env_file_path, 0o600)
    print("[+] Ed25519 keys successfully generated and securely stored in .env")

if __name__ == "__main__":
    generate_and_store_keys()
