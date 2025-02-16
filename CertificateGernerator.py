
from jwcrypto import jwk, jwt
import json

from cryptography.hazmat.primitives import serialization

SAVE_TO = "./private.json"
SAVE_PRIVATE_KEY_TO = "./private.pem"
SAVE_PUBLIC_KEY_TO = "./public.pem"


ALGORITHM = "RSA256"
SIZE = 2048
USE = "sig"
KTY = "RSA"


class CertificateAuthority:
    def getCall():
        print('ello h')
        #CertificateGernerator.runWebServer()


class CertificateGernerator():

    def generateJWKS(no_of_jwks):
        list_of_jwks = []
        for kid in range(1, no_of_jwks+1):
            kid = str(kid)
            key = jwk.JWK.generate(kty = KTY, size = SIZE, alg=ALGORITHM,use = USE , kid = kid)
            list_of_jwks.append(key)
            print("key%s is %s" % (kid,key))
        return list_of_jwks
    
    def saveJWKSAsJsonFileInLocalStorage(list_of_JWKS):
        private_file = open(SAVE_TO,mode='w+')
        private_keys = []
        for jwk in list_of_JWKS:  
            private_keys.append(jwk.export(private_key = True, as_dict = True))

        json.dump({"keys":private_keys},private_file)
        private_file.close()


    def loadPublicJWKS():
        private_file = open(SAVE_TO, mode = 'r')
        jwks = jwk.JWKSet.from_json(private_file.read())
        private_file.close()
        return jwks.export(private_keys = False)  # export public key 
    
    def issueJWS(key,alg,claims):
                 
        # read private key
        with open(SAVE_PRIVATE_KEY_TO, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
            
        # Step 2: Convert private key to JWK format
        jwk_key = jwk.JWK.from_pem(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
 
        claims['exp'] = 1739709999
        header={}
        header['alg'] = 'RS256'
        header['typ'] = 'JWT'
        header['kid'] = jwk_key.export(private_key=False,as_dict=True).get('kid')   # export public key to add with jwt 
        token = jwt.JWT(header=header,claims=claims)
        token.make_signed_token(key=jwk_key)
        print('\n gernerated token is \n  %s' % token)
        return token.serialize()    
    

    def getKID(key):
        return key.export(private_key=False,as_dict=True).get('kid')
    
    def printPrivateKey(jwks):
         
        private_key_in_pem = jwks.export_to_pem(private_key = True, password = None)      
        print("\n[Private Key]\n%s" % (str(private_key_in_pem, 'utf-8')))
        try:
            with open(SAVE_PRIVATE_KEY_TO,"w") as flwriter:
                flwriter.write(str(private_key_in_pem, 'utf-8'))             
            print(f"\nPrivate key successfully saved to {SAVE_PRIVATE_KEY_TO}")
        except Exception as e:
            print(f"\nError saving private key: {e}")

    
    def printPublicKey(jwks):
         
        public_key_in_pem = jwks.export_to_pem() 
        try:
            with open(SAVE_PUBLIC_KEY_TO,"w") as flwriter:
                flwriter.write(str(public_key_in_pem, 'utf-8'))             
            print(f"\n Private key successfully saved to {SAVE_PRIVATE_KEY_TO}")
        except Exception as e:
            print(f"\n Error saving private key: {e}")  
        print("\n[Public Key]\n%s" % (str(public_key_in_pem, 'utf-8')))
  
 
