"""import type"""
import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    chiphertext = ""
    for j, _ in enumerate(plaintext):
        if plaintext[j].isalpha():
            chiselko = ord(plaintext[j])
            if plaintext[j].isupper() and chiselko >= ord("Z") + 1 - shift:
                chiphertext += chr(chiselko - 26 + shift)
            elif plaintext[j].islower() and chiselko >= ord("z") + 1 - shift:
                chiphertext += chr(chiselko - 26 + shift)
            else:
                chiphertext += chr(chiselko + shift)
        else:
            chiphertext += plaintext[j]
    return chiphertext


def decrypt_caesar(chiphertext: str, shift: int = 3) -> str:
    """
    Decrypts a chiphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for j, _ in enumerate(chiphertext):
        if chiphertext[j].isalpha():
            chiselko = ord(chiphertext[j])
            if chiphertext[j].isupper() and chiselko <= ord("A") - 1 + shift:
                plaintext += chr(chiselko + 26 - shift)
            elif chiphertext[j].islower() and chiselko <= ord("a") - 1 + shift:
                plaintext += chr(chiselko + 26 - shift)
            else:
                plaintext += chr(chiselko - shift)
        elif chiphertext.isspace():
            continue
        else:
            plaintext += chiphertext[j]
    return plaintext


def caesar_breaker_brute_force(chiphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
