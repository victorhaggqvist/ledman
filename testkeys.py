import hashlib
import time
__author__ = 'victor'


now = int(time.time())

print hashlib.sha256(str(now)+'testkeychangeme').hexdigest()
print now
