import secrets
from Crypto.PublicKey import ECC,RSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

#TODO: open(private_key_location,'rt').read()

def _saving_handler(address, data):
    if (address == ''):
        print(f"your key is :\n {data}")
        return
    f = open(address,'wt')
    f.write(data)
    f.close()
    print(f'successfully generated key. key can be found at: ./{address}')

def get_private_key(address='privatekey.pem'):
    key = ECC.generate(curve="p256")
    exported_key = key.export_key(format='PEM')
    _saving_handler(address, exported_key)
    return exported_key


def get_public_key(private_key, address='publickey.pem'):
    key = ECC.import_key(private_key)
    exported_key = key.public_key().export_key(format='PEM')
    _saving_handler(address, exported_key)
    return exported_key

def sign_message(private_key, message):
    key = ECC.import_key(private_key)
    h = SHA256.new(message)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    return signature

def verify_message(public_key, message, signature):
    key = ECC.import_key(public_key)
    h = SHA256.new(message)
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print('this message is verified.')
        return True
    except:
        print(f'signature "{signature}" was not authentic.')
        return False

"""
Just a simple code to demonstrate the functionality of code.

x = get_private_key(address='')
a = get_public_key(x,address='')
message = 'someMessage'
z = sign_message(x,message.encode())
verify_message (a, message.encode(), z)
verify_message (a, message.encode(), 'notRealSignature')

Output:
your key is :
 -----BEGIN PRIVATE KEY-----
XXX
-----END PRIVATE KEY-----
your key is :
 -----BEGIN PUBLIC KEY-----
XXX
-----END PUBLIC KEY-----
this message is verified.
signature "notRealSignature" was not authentic.
"""
