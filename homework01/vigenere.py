#import typing as tp


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    count = 0
    while len(plaintext) > len(keyword):
        keyword += keyword[count]
        count += 1
    for i, _ in enumerate(keyword):
        if keyword[i].isupper():
            key = ord(keyword[i]) - ord('A')
        elif keyword[i].islower():
            key = ord(keyword[i]) - ord('a')
        if plaintext[i].isalpha():
            chiselko = ord(plaintext[i])
            if plaintext[i].isupper() and chiselko >= ord('Z') + 1 - key:
                ciphertext += chr(chiselko - 26 + key)
            elif plaintext[i].islower() and chiselko >= ord('z') + 1 - key:
                ciphertext += chr(chiselko - 26 + key)
            else:
                ciphertext += chr(chiselko + key)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    count = 0
    while len(ciphertext) > len(keyword):
        keyword += keyword[count]
        count += 1
    for i, _ in enumerate(keyword):
        if keyword[i].isupper():
            key = ord(keyword[i]) - ord('A')
        elif keyword[i].islower():
            key = ord(keyword[i]) - ord('a')
        if ciphertext[i].isalpha():
            chiselko = ord(ciphertext[i])
            if ciphertext[i].isupper() and chiselko <= 64 + key:
                plaintext += chr(chiselko + 26 - key)
            elif ciphertext[i].islower() and chiselko <= 96 + key:
                plaintext += chr(chiselko + 26 - key)
            else:
                plaintext += chr(chiselko - key)
        else:
            plaintext += ciphertext[i]
    return plaintext

