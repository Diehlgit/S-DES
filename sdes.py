#Initial Permutation Function
#def IP():

#Inverse Function of Initial Permutation
#def IP_inv():

#f_k Function
#def f_k():

#Permutation Function that switches the two halves of the data
#def SW():

#Key Permutation Function 
def P10(key: int):
    if not (0 <= key < 1024):
        raise ValueError("Input must br a 10-bit integer")

    bin_str = f"{key:010b}"

    p10_idx = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]

    permutation = ''.join(bin_str[i] for i in p10_idx)

    return int(permutation, 2)

#Permutation Function that produces subkeys (K1 and K2)
#def P8():

#S-DES Encryption Definition
# ciphertext = IP_inv (f_k2 (SW (f_k1 (IP(plaintext)))))

# K1 = P8 (Shift (P10 (key)))
# K2 = P8 (Shift (Shift (P10 (key))))

#S-DES Decryption Definition
# plaintext = IP_inv (f_k1 (SW (f_k2 (IP (ciphertext)))))
