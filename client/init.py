import os
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)


with open(os.path.join('',".env"), "w") as file1:
    toFile = 'PRIVATE_KEY={}\nPUBLIC_KEY={}\nREST_API_URL=http://localhost:8008'.format(private_key.as_hex(), signer.get_public_key().as_hex())
    file1.write(toFile)


print('\nGenerated .env file with public/private keys\n')
print('PRIVATE_KEY={}\nPUBLIC_KEY={}\nREST_API_URL=http://localhost:8008'.format(private_key.as_hex(), signer.get_public_key().as_hex()))
