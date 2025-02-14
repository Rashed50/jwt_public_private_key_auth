import base64
import hmac

from hashlib import sha256

# Replace it with your secret
secret = "emqx".encode('utf-8')
print(secret)
# Replace it with the header given by jwt.io
base64_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
# Replace it with the payload given by jwt.io
base64_payload = "eyJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9"
# Replace it with the signature given by jwt.io
base64_signature = "4AE9JkW8rrIDI5WC5gyo3wZU5vG34as566LtNfBFoVo"


msg = (base64_header + "." + base64_payload).encode('utf-8')
signature = str(base64.urlsafe_b64encode(hmac.new(secret, msg, sha256).digest()), 'utf-8')
# Remove the padding and compare
if signature.replace('=', '') == base64_signature:
  print("Matched")
else:
  print("UnMatched")
