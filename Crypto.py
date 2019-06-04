# -*- coding: utf-8 -*-

# Vutils for Crypto

import base64, hashlib

# ---

def Base64Encode(text): return base64.b64encode(text)

def Base64Decode(text): return base64.b64decode(text)

def Hash(algo, string, upper = True):
    cipher = ""
    try:
        HL = getattr(hashlib, algo)()
        HL.update(string.encode("utf-8"))
        cipher = HL.hexdigest()
    except Exception as e:
        print(e, "- Hashes :", hashlib.algorithms_guaranteed)
    return cipher if not upper else cipher.upper()