import os

# Tạo một secret key ngẫu nhiên và duy nhất
secret_key = os.urandom(24)
print(secret_key)
