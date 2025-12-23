import hashlib,hmac,random,string,base64,json


def compose_jwt(payload:dict, typ:str="JWT", header:dict|None = None, alg:str = "HS256", secret_key:bytes|None = None) -> str:
    header = {
        "alg": alg,
        "typ": typ
    }
    j_header = json.dumps(header)
    j_payload = json.dumps(payload)
    b_header = base64.urlsafe_b64encode(j_header.encode("utf-8"))
    b_payload = base64.urlsafe_b64encode(j_payload.encode("utf-8"))

    body = b'.'.join([b_header, b_payload])

    signature = get_signature(body, secret_key, alg)
    return b'.'.join([body, signature.encode("ascii")]).decode("ascii")

def get_signature(data:bytes, secret_key:bytes|None = None, alg:str = "HS256", form:str = "base64url") -> str:
    if secret_key is None:
        secret_key = "secret".encode()
    if alg == "HS256":
        mode = hashlib.sha256
    elif alg == "HS512":
        mode = hashlib.sha512
    elif alg == "HS384":
        mode = hashlib.sha384
    else:
        raise ValueError(f"get_signature error: Unsupported algorithm: {alg}")
    mac = hmac.new(secret_key, data, mode)
    if form == "base64url":
        return base64.urlsafe_b64encode(mac.digest()).decode('ascii')
    elif form == "base64std":
        return base64.standard_b64encode(mac.digest()).decode('ascii')
    elif form == "hex":
        return mac.digest().hex()
    else:
        raise ValueError(f"get_signature error: Unsupported form: {form}")
    
    

def generate_salt(length:int=16) -> str:
    symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(symbols) for _ in range(length))