from lib.cryptographic import generate_key_pair,save_key_to_file

private_key, public_key = generate_key_pair()
save_key_to_file(private_key, 'private_key.pem')
save_key_to_file(public_key, 'public_key.pem')
