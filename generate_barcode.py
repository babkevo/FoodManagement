import barcode
from barcode.writer import ImageWriter

# Generate a barcode image using the EAN13 format
barcode_value = '1234567890123'  # Replace with your desired barcode value
ean = barcode.get('ean13', barcode_value, writer=ImageWriter())

# Save the barcode image as 'barcode_image.jpg'
filename = 'barcode_image.jpg'
ean.save(filename)
