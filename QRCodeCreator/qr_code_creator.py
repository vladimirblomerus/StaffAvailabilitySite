import os
import pathlib
import qrcode

FILE_EXTENSION = ".jpg" # File extension for qr codes
QR_CODE_FOLDER = "QR-codes" # Folder to store qr codes

if not os.path.exists(QR_CODE_FOLDER):
    os.makedirs(QR_CODE_FOLDER)

def generate_qr_code(data, file_name):
    """Function to generate qr codes"""
    img = qrcode.make(data)
    type(img)
    img.save(f"{QR_CODE_FOLDER}/{file_name}{FILE_EXTENSION}")

created_qr_code_names = [] # List to store names of created qr codes for printing
def create_qr_codes():
    """Function to create qr codes"""
    print("Generate new QR code:")
    qr_data = input("Data (leave empty to exit): ")
    if qr_data == "":
        return
    qr_name = input("File name (without extension): ")
    if qr_name == "":
        qr_name = qr_data
    generate_qr_code(qr_data, qr_name)
    created_qr_code_names.append(qr_name)
    create_qr_codes()

create_qr_codes()
