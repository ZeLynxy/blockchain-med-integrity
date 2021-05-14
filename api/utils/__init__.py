import hashlib
import json

def hashData(data):
  hashGenerator = hashlib.sha512()
  hashGenerator.update(json.dumps(data,sort_keys=True).encode("utf-8"))
  return hashGenerator.hexdigest()