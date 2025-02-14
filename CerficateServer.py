
from jwcrypto import jwk, jwt
import json

SAVE_TO = "./private.json"

class CertificateAuthority:
    def getCall():
        print('ello h')
        #CertificateGernerator.runWebServer()


class CertificateGernerator():

    def generateJWKS(no_of_jwks):
        list_of_jwks = []
        for kid in range(1, no_of_jwks+1):
            kid = str(kid)
            key = jwk.JWK.generate(kty = 'RSA', size = 2048, alg='RSA256',use = 'sig' , kid = kid)
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
        #key = list_of_jwks[0]
        header={}
        header['alg'] = alg
        header['typ'] = 'JWT'
        header['kid'] = key.export(private_key=False,as_dict=True).get('kid')   # export public key to add with jwt 
        token = jwt.JWT(header=header,claims=claims)
        token.make_signed_token(key=key)
        print('\n gernerated token is \n  %s' % token)
        return token.serialize()

    def getKID(key):
        return key.export(private_key=False,as_dict=True).get('kid')
    
    def printPrivateKey(jwks):
        # private_file = open(SAVE_TO, mode = 'r')
        # jwks = jwk.JWKSet.from_json(private_file.read())
        # private_file.close()
        private_key_in_pem = jwks.export_to_pem(private_key = True, password = None)

        print("\n[Private Key]\n%s" % (str(private_key_in_pem, 'utf-8')))
    
    def printPublicKey(jwks):
        # private_file = open(SAVE_TO, mode = 'r')
        # jwks = jwk.JWKSet.from_json(private_file.read())
        # private_file.close()
        public_key_in_pem = jwks.export_to_pem()
        print("\n[Public Key]\n%s" % (str(public_key_in_pem, 'utf-8')))
        
   

