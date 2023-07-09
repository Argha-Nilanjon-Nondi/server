import requests
import json
from lib.cryptographic import load_key,encrypt_file
import base64

input_filename="test_my.wav"
loaded_public_key =  load_key('public_key.pem')
print("Key is loaded")
input_file=open(input_filename,"rb")
input_content=input_file.read()
input_file.close()
print("File is readed")

encrypted_content=encrypt_file(input_content, loaded_public_key)
print("Content is encrypted")
encoded_data = base64.b64encode(encrypted_content).decode()
print("Content is encoded")


url = 'https://real-carrots-cheer.loca.lt/api/upload'  # Replace with the actual URL of the server endpoint
data = {
    'file_name': input_filename,
    'file_content': encoded_data
}

# Convert the data to JSON format
json_data = json.dumps(data)
print("Data is jsoned")
# Send the JSON data to the server
response = requests.post(url, json=json_data)
print("Data is send , wait......")
# Check the response
if response.status_code == 200:
    print('Data sent successfully')
else:
    print('Failed to send data')
