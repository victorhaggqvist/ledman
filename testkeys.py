import hashlib
import time

__author__ = 'victor'

now = int(time.time())
text = str(now)+'testkeychangeme'
token = hashlib.sha256(text.encode('utf8')).hexdigest()
print(now)

print('?token=%s&timestamp=%s' % (token, now))
