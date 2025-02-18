from http.server import HTTPServer, BaseHTTPRequestHandler
from jwcrypto import jwk, jwt
import json

from CertificateGernerator import CertificateGernerator

HOSTNAME = "127.0.0.1"
PORT = 8090

SAVE_TO = "./private.json"

def issue_jws(key, alg, claims):
    print(f"Before create jwt {key}")
    header = {}
    header['alg'] = alg
    header['typ'] = 'JWT'
    header['kid'] = get_kid(key)
    token = jwt.JWT(header = header, claims = claims)
    token.make_signed_token(key)
    return token.serialize()

def generate_jwks(number):
    jwks = []
    for kid0 in range(1, number + 1):
        kid = str(kid0)
        key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg = 'RSA256', use = 'sig', kid = kid)
        jwks.append(key)
        print(f'\n jwks{kid}-{key}')

    return jwks

def get_kid(key):
    return key.export(private_key = False, as_dict = True).get("kid")

# store jwks to local memory
def save_jwks(jwks):
    private_file = open(SAVE_TO, mode = 'w+')
    private_keys = []
    for jwk in jwks:
        private_keys.append(jwk.export(private_key = True, as_dict = True))

    json.dump({"keys": private_keys}, private_file)
    private_file.close()

def load_public_jwks():
    private_file = open(SAVE_TO, mode = 'r')
    jwks = jwk.JWKSet.from_json(private_file.read())
    private_file.close()
    return jwks.export(private_keys = False)  


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        old = load_public_jwks() # CertificateGernerator.loadPublicJWKS()
        self.wfile.write(bytes(old, 'utf-8'))




# jwks = CertificateGernerator.generateJWKS(3)
# CertificateGernerator.saveJWKSAsJsonFileInLocalStorage(jwks)
# claims = {}
# claims['client'] = 'admin'
# claims['username'] = 'admin'
# jwt = CertificateGernerator.issueJWS(jwks[0], 'RSA256', claims)

# CertificateGernerator.printPrivateKey(jwks=jwks[0])
# CertificateGernerator.printPublicKey(jwks=jwks[0])



jwks = generate_jwks(3)
save_jwks(jwks)
# Export public key and private key in PEM
public_key_in_pem = jwks[0].export_to_pem()
private_key_in_pem = jwks[0].export_to_pem(private_key = True, password = None)

print("[Public Key]\n%s" % (str(public_key_in_pem, 'utf-8')))
print("[Private Key]\n%s" % (str(private_key_in_pem, 'utf-8')))

# Sign the JWT using the first JWK
claims = {}
claims['client_id'] = 'abc_admin'
claims['username'] = 'abc_admin'
jwt = issue_jws(jwks[0], 'RS256', claims)

print("JWT Value: \n [JWT]\n%s\n" % (jwt))

save_jwks(jwks)



print('calling server')
web_server = HTTPServer((HOSTNAME, PORT), MyServer)
print("Server started http://%s:%s" % (HOSTNAME, PORT))

try:
    web_server.serve_forever()
except KeyboardInterrupt:
    pass

web_server.server_close()
print("Server stopped.")