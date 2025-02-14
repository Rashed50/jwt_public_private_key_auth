### Authentication
Authentication is the process of verifying the identity of a client. It is an essential part of most applications and can help to protect our services from illegal client connections.

#### What is JWKS Endpoint?
No matter which signature algorithm we use, there is a risk of key leakage. So it is better to rotate or update the key regularly. But manually configuring new keys into the server is not a good choice, especially when multiple servers use the same set of keys. In a multi-tenant scenario, we may also need to provide different keys for different tenants.

We need a more efficient mechanism for managing and distributing keys, and there comes the JWKS Endpoint.

JWKS Endpoint is an HTTP Server that responds to GET requests and then returns JWKS (JSON Web Key Set). JWKS is a set of JWKs represented by a JSON object. The JSON object only contains a keys member, and the value of keys is determined by a JSON array of one or more JWKs.

JWK is a way to st
