# -*- coding: utf-8 -*-

# Vutils for Crypto

import base64, hashlib

# ---

def b64_encode(text): return base64.b64encode(text)

def b64_decode(text): return base64.b64decode(text)

def hash(algo, string, upper = True):
    cipher = ""
    try:
        HL = getattr(hashlib, algo)()
        HL.update(string.encode("utf-8"))
        cipher = HL.hexdigest()
    except Exception as e:
        print(e, "- Hashes :", hashlib.algorithms_guaranteed)
    return cipher if not upper else cipher.upper()