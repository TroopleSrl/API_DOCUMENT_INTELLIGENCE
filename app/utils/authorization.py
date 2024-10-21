from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from settings import get_settings

from database.functions import get_key_if_client

# This is defining specific headers that we'll use for our authentication /authorization
admin_token = APIKeyHeader(name="X-ADMIN-TOKEN", auto_error=True, scheme_name="X-ADMIN-TOKEN")
client_token = APIKeyHeader(name="X-CLIENT-TOKEN", auto_error=True, scheme_name="X-CLIENT-TOKEN")


# Instead of using the key's uuid as it, we'll give client a hash that is composed 
# of both the client's id and the key's id. Why ? Because it's more secure and it's fun
def encode_fernet(client_id: str, key_id: str) -> str:
    from cryptography.fernet import Fernet
    f = Fernet(get_settings().FERNET_KEY.get_secret_value())
    return f.encrypt(f"{client_id}:{key_id}".encode('utf-8')).decode('utf-8')

# We could add a try except block here to catch any errors that might occur but lazy me
def decode_fernet(client_token: str) -> tuple[str, str]:
    try:
        from cryptography.fernet import Fernet
        f = Fernet(get_settings().FERNET_KEY.get_secret_value())
        decoded = f.decrypt(client_token.encode('utf-8')).decode('utf-8')
        return tuple(decoded.split(':'))
    except: raise HTTPException(status_code=401, detail="Unauthorized")
    
# We'll "secure" the /admin routes with a token that is encoded in the .envs
def is_admin(key: str = Depends(admin_token)):
    if key == get_settings().ADMIN_TOKEN.get_secret_value(): return True
    else: raise HTTPException(status_code=401, detail="Unauthorized")

def is_client(client_token: str = Depends(client_token)):
    client_id, key_id = decode_fernet(client_token)
    print(client_id, key_id)
    key = get_key_if_client(client_id, key_id)
    if key: return key
    else: raise HTTPException(status_code=401, detail="Unauthorized")