import hashlib
dencrypt = "T0s0l!nh123"
encrypt = str(hashlib.md5(dencrypt.strip().encode("utf-8")).hexdigest())
encrypt = str(hashlib.sha1(encrypt.strip().encode("utf-8")).hexdigest())
encrypt = str(hashlib.sha1(encrypt.strip().encode("utf-8")).hexdigest())
encrypt = str(hashlib.md5(encrypt.strip().encode("utf-8")).hexdigest())

print(encrypt)