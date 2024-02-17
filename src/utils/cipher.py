def encrypt_str(str_: str) -> str:
    reverse_str = str_[::-1]
    reverse_str_array = [str(ord(c) * 3) for c in reverse_str]
    finalStr = "<5>".join(reverse_str_array)
    return finalStr

def decrypt_str(str_: str) -> str:
    str_array = str_.split("<5>")
    str_array = [int(int(s)/3) for s in str_array]
    str_array = [chr(s) for s in str_array]
    finalStr = "".join(str_array)[::-1]
    return finalStr
