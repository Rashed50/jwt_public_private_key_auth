### Authentication
Authentication is the process of verifying the identity of a client. It is an essential part of most applications and can help to protect our services from illegal client connections.

#### What is JWKS Endpoint?
No matter which signature algorithm we use, there is a risk of key leakage. So it is better to rotate or update the key regularly. But manually configuring new keys into the server is not a good choice, especially when multiple servers use the same set of keys. In a multi-tenant scenario, we may also need to provide different keys for different tenants.

We need a more efficient mechanism for managing and distributing keys, and there comes the JWKS Endpoint.

JWKS Endpoint is an HTTP Server that responds to GET requests and then returns JWKS (JSON Web Key Set). JWKS is a set of JWKs represented by a JSON object. The JSON object only contains a keys member, and the value of keys is determined by a JSON array of one or more JWKs.

JWK is a way to store keys in JSON format. A public key in PEM format:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0CVTPVrufUOfjPvdfzRe
JY9lEknYc0rARYIO2kCDrFvTrQHLwmh11nVmHodxDWJqkzkqRWWoyp5Uy7EG9e/x
y5P4cYtvr+myg1V3RUrYnwvcso0q1LjQSeFVnDH0t1uoCf38aP/jE9xPwNpliqEx
G8gbdoX5xQbk6hox9QOWaNYF0iMJt+As/3BhmgDD0grIzPy/md14KFjxEW8pj5/A
NoGEhsKozHni+yJkxWwgWXb0DLt8XjinpKDbI/e5pcGr6QqCvsH3bstNz8Ke7sft
6tHeKVR2PfcBHYn2fcSeCwN6aOUFhJ30A6T4RIUwbOgX+JGR85d8YUt+28p5leo2
1wIDAQAB
-----END PUBLIC KEY-----
```

If represented as a JWK, it would be of the form:
```
{
  "alg":"RSA256",
  "e":"AQAB",
  "kid":"1",
  "kty":"RSA",
  "n":"0CVTPVrufUOfjPvdfzReJY9lEknYc0rARYIO2kCDrFvTrQHLwmh11nVmHodxDWJqkzkqRWWoyp5Uy7EG9e_xy5P4cYtvr-myg1V3RUrYnwvcso0q1LjQSeFVnDH0t1uoCf38aP_jE9xPwNpliqExG8gbdoX5xQbk6hox9QOWaNYF0iMJt-As_3BhmgDD0grIzPy_md14KFjxEW8pj5_ANoGEhsKozHni-yJkxWwgWXb0DLt8XjinpKDbI_e5pcGr6QqCvsH3bstNz8Ke7sft6tHeKVR2PfcBHYn2fcSeCwN6aOUFhJ30A6T4RIUwbOgX-JGR85d8YUt-28p5leo21w",
  "use":"sig"
}
```

#### How to build a JWKS Endpoint?
First create a fastapi or django python project then install below library 

```
pip3 install jwcrypto
and
from jwcrypto import jwk
```

Building a JWKS Endpoint is a straightforward process once you understand its principle.
First, we use the http.server module to build a simple HTTP Server, which only supports GET requests.

```
from http.server import HTTPServer, BaseHTTPRequestHandler

HOSTNAME = "127.0.0.1"
PORT = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"keys": []}', 'utf-8'))

if __name__ == "__main__":
    web_server = HTTPServer((HOSTNAME, PORT), MyServer)
    print("Server started http://%s:%s" % (HOSTNAME, PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")
```


Next, we only need to implement the code to generate JWKS, and then return it in the callback function do_GET of the GET request.

We can use the following code to generate a pair of RSA public and private keys:
```
from jwcrypto import jwk

key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = 1)

```

Then export the public or private key in JWK format:
```
# Export Public Key in JWK
key.export(private_key = False)

# Export Private Key in JWK
key.export(private_key = True)
```

In this Project, we first use the RSA algorithm to sign three sets of key pairs and then use the private key in the first set of key pairs to sign a JWT.

Details process you will get here 
https://www.emqx.com/en/blog/jwt-authentication-and-jwks-endpoint-in-mqtt



