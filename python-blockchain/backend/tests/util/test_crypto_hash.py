from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
  # It should create the same hash with arguments of different data types in any order
  assert crypto_hash(1,[2], 'three') == crypto_hash('three', 1, [2])
  assert crypto_hash('food') == '90960c7a6145a97cbb09d6478535c2b31f76050310286dabe9ae2463ee003850'