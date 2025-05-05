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
    bin_str = f"{key:010b}"

    p10_idx = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]

    permutation = ''.join(bin_str[i] for i in p10_idx)

    return int(permutation, 2)

#Permutation Function that produces subkeys (K1 and K2)
def P8(key: int):
    bin_str = f"{key:010b}"

    p8_idx = [5, 2, 6, 3, 7, 4, 9, 8]

    permutation = ''.join(bin_str[i] for i in p8_idx)

    return int(permutation, 2)

def Shift(key: int, n: int):
    bin_str = f"{key:010b}"
    fst_half = bin_str[0:5]
    snd_half = bin_str[5:10]

    return int((fst_half[n:] + fst_half[:n] + snd_half[n:] + snd_half[:n]), 2)

#K1 = P8 (Shift_1 (P10 (key)))
#K2 = P8 (Shift_2 (Shift_1 (P10 (key))))
#S-DES function that produces (K1, K2)

def key_gen(key: int):
    if not (0 <= key < 1024):
        raise ValueError("Input must br a 10-bit integer")
    
    intermediate_key = Shift((P10(key)), 1)

    K1 = P8(intermediate_key)
    K2 = P8(Shift(intermediate_key, 2))

    return (K1, K2)


#S-DES Encryption Definition
# ciphertext = IP_inv (f_k2 (SW (f_k1 (IP(plaintext)))))


#S-DES Decryption Definition
# plaintext = IP_inv (f_k1 (SW (f_k2 (IP (ciphertext)))))
