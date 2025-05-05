#Initial Permutation Function
#def IP():

#Inverse Function of Initial Permutation
#def IP_inv():

#f_k Function
#def f_k():

#Permutation Function that switches the two halves of the data
#def SW():

#Key Permutation Function 
#def P10():

#Permutation Function that produces subkeys (K1 and K2)
#def P8():

#S-DES Encryption Definition
# ciphertext = IP_inv (f_k2 (SW (f_k1 (IP(plaintext)))))

# K1 = P8 (Shift (P10 (key)))
# K2 = P8 (Shift (Shift (P10 (key))))

#S-DES Decryption Definition
# plaintext = IP_inv (f_k1 (SW (f_k2 (IP (ciphertext)))))
