import requests
import json

response_API = requests.get("https://www.google.com/recaptcha/api2/reload?k=6LdWmKEcAAAAAF7-W57A_y9xilJdApbSYelKBDTQ")


data = response_API.text

print(data)
