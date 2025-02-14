#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signature
import jwksserver
# from CerficateServer import CertificateAuthority, CertificateGernerator
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwt_sig_auth.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# abc = CertificateGernerator.generateJWKS(3)
# claims = {}
# claims['client'] = 'myclient'
# claims['username'] = 'myuser'
# jwt = CertificateGernerator.issueJWS(abc[0], 'RS256', claims)
#jwksserver.load_public_jwks()
 




