import hashlib
import string

MAX_VALUE = 0x7FFFFFFF

CPU_COST = 1 << 15
BLOCK_SIZE = 8
PARALLELIZATION_COST = 1

ALPHABET = string.ascii_lowercase + string.ascii_uppercase
VALID_SYMBOLS = "@#$%&*._!"
ALLOWED_CHARACTERS = (
    VALID_SYMBOLS + string.digits + string.ascii_uppercase + string.ascii_lowercase
)


def sanitize(pashword: str, symbols: bool = True, numbers: bool = True) -> str:
    pashword_list = list(pashword)
    prng_obj = hashlib.shake_256()

    def generate_index(hash_text: str) -> int:
        hash_text = hash_text.encode(encoding="utf8")
        prng_obj.update(hash_text)
        prng = prng_obj.digest(255)
        result = int.from_bytes(prng, "big")
        return result % len(ALPHABET)

    if not symbols:
        for i, char in enumerate(pashword_list[:]):
            if char in VALID_SYMBOLS:
                pashword_list[i] = ALPHABET[generate_index(f"{i}{char}")]

    if not numbers:
        for i, char in enumerate(pashword_list[:]):
            if char.isdigit():
                pashword_list[i] = ALPHABET[generate_index(f"{i}{char}")]

    return "".join(pashword_list)


def generate_pashword(website: str, username: str, secret: str, length: int = 32) -> str:
    sha3_obj = hashlib.sha3_512()
    prng_obj = hashlib.shake_256()

    sha3_obj.update(secret.encode(encoding="utf8"))
    secret = sha3_obj.hexdigest()
    hash_text = hashlib.scrypt(
        secret.encode(encoding="utf8"),
        salt=f"{username}{website}".encode(encoding="utf8"),
        n=CPU_COST,
        r=BLOCK_SIZE,
        p=PARALLELIZATION_COST,
        dklen=32,
        maxmem=64 * 1024 * 1024,
    )

    def generate_index(modulo: int) -> int:
        prng_obj.update(hash_text)
        prng = prng_obj.digest(255)
        result = int.from_bytes(prng, "big")
        return result % modulo

    def pick_character(chars: str) -> str:
        return chars[generate_index(len(chars))]

    pick_index = list(range(length))
    idx = [-1, -1, -1, -1]

    for i in range(4):
        remove_index = generate_index(len(pick_index))
        idx[i] = pick_index.pop(remove_index)

    pashword = ""

    for i in range(length):
        if i == idx[0]:
            pashword += pick_character(string.ascii_lowercase)
        elif i == idx[1]:
            pashword += pick_character(string.ascii_uppercase)
        elif i == idx[2]:
            pashword += pick_character(VALID_SYMBOLS)
        elif i == idx[3]:
            pashword += pick_character(string.digits)
        else:
            pashword += pick_character(ALLOWED_CHARACTERS)

    return pashword
