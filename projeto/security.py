from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def criptografar_senha(senha: str) -> str:
    return password_hash.hash(senha)

def verificar_senha(senha: str , hash: str) -> bool:
    return password_hash.verify(senha, hash)