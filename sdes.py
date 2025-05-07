def permutation(s: str, indices: list[int]) -> str:
    return ''.join(s[i] for i in indices)

#Initial Permutation Function
IP = lambda s: permutation(s, [1, 5, 2, 0, 3, 7, 4, 6])

#Inverse Function of Initial Permutation
IP_INV = lambda s: permutation(s, [3, 0, 2, 4, 6, 1, 7, 5])

#f_k Function
# f_k(L, R) = (L xor F(R, SK), R)

#Permutation Function that switches the two halves of the data
SW = lambda s: permutation(s, [4, 5, 6, 7, 0, 1, 2, 3])

#Key Permutation Function 
P10 = lambda s: permutation(s, [2, 4, 1, 6, 3, 9, 0, 8, 7, 5])

#Permutation Function that produces subkeys (K1 and K2)
P8  = lambda s: permutation(s, [5, 2, 6, 3, 7, 4, 9, 8])

def Shift(key: str, n: int):
    fst_half = key[0:5]
    snd_half = key[5:10]

    return (fst_half[n:] + fst_half[:n] + snd_half[n:] + snd_half[:n])

#K1 = P8 (Shift_1 (P10 (key)))
#K2 = P8 (Shift_2 (Shift_1 (P10 (key))))
#S-DES function that produces (K1, K2)

def key_gen(key: str):
    if not (set(key).issubset({'0', '1'}) and len(key) == 10):
        raise ValueError("Input must be a 10-bit integer")
    
    intermediate_key = Shift((P10(key)), 1)

    K1 = P8(intermediate_key)
    K2 = P8(Shift(intermediate_key, 2))

    return (K1, K2)


#S-DES Encryption Definition
# ciphertext = IP_inv (f_k2 (SW (f_k1 (IP(plaintext)))))


#S-DES Decryption Definition
# plaintext = IP_inv (f_k1 (SW (f_k2 (IP (ciphertext)))))
