import hashlib
import json

def crypto_hash(*args):
  '''
  Return a sha-256 hash of the given arguments.
  '''
  stringified_args = sorted(map(lambda data: json.dumps(data), args))
  # print(f'stringified args: {stringified_args}')
  joined_data = ''.join(stringified_args) # Stringify and join needed as we'll be passing timestamp, last_hash and data
  # print(f'joined_data: {joined_data}')
  return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
  print(f"crypto_hash('args*'): {crypto_hash(2, 1, 'three', 'and', 2, 'tha', 5)}")
  print(f"crypto_hash('foo'): {hashlib.sha256('foo'.encode('utf-8')).hexdigest()}") # same as in other C++ implementation!!
  

if __name__ == '__main__':
  print(crypto_hash.__doc__)
  main()

  print("\nJust for fun, let's see how a string in binary is rendered in utf-16 and utf-8 respectively:" )
  print(b'\xcf\x84o\xcf\x81\xce\xbdo\xcf\x82'.decode('utf-16'))
  print(b'\xcf\x84o\xcf\x81\xce\xbdo\xcf\x82'.decode('utf-8'))

