#General function used to define specific permutation functions
def permutation(s: str, indices: list[int]) -> str:
    return ''.join(s[i] for i in indices)

#Initial Permutation Function
IP = lambda s: permutation(s, [1, 5, 2, 0, 3, 7, 4, 6])

#Inverse Function of Initial Permutation
IP_INV = lambda s: permutation(s, [3, 0, 2, 4, 6, 1, 7, 5])

#f_k Function
# f_k(L, R) = (L xor F(R, SK), R)
# F(R, SK) =
#   let s := (E/P(R) xor SK)
#       P4(S0[s[0] + s[3]][s[1] + s[2]] + S1[s[4] + s[7]][s[5] + s[6]]))

#S-Boxes used in F function
S0 = {'00': {'00': '01', '01': '00', '10': '11', '11': '10'},
      '01': {'00': '11', '01': '10', '10': '01', '11': '00'},
      '10': {'00': '00', '01': '10', '10': '01', '11': '11'},
      '11': {'00': '11', '01': '01', '10': '11', '11': '10'}
      }

S1 = {'00': {'00': '00', '01': '01', '10': '10', '11': '11'},
      '01': {'00': '10', '01': '00', '10': '01', '11': '11'},
      '10': {'00': '11', '01': '00', '10': '01', '11': '00'},
      '11': {'00': '10', '01': '01', '10': '00', '11': '11'}
      }

#Permutation that produces F function result
P4 = lambda s: permutation(s, [1, 3, 2, 0])

#Extension Permutation (E/P) used in the beginning of F function
EP = lambda s: permutation(s, [3, 0, 1, 2, 1, 2, 3, 0])

#XOR function to work with strings
def XOR(s1:str, s2:str):
    return ''.join('1' if c1 != c2 else '0' for c1, c2 in zip(s1, s2))

#F function used in f_k
def F(R: str, SK: str):
    s = XOR(EP(R), SK)
    return P4(S0[s[0] + s[3]][s[1] + s[2]] + S1[s[4] + s[7]][s[5] + s[6]])

#f_k function
def f_k(S:str, K:str):
    L = S[:4]
    R = S[4:]
    return (XOR(L, F(R, K))) + R

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
    intermediate_key = Shift((P10(key)), 1)

    K1 = P8(intermediate_key)
    K2 = P8(Shift(intermediate_key, 2))

    return (K1, K2)

#S-DES Encryption Definition
# ciphertext = IP_inv (f_k2 (SW (f_k1 (IP(plaintext)))))
def sdes_encryption(plaintext:str, key:str):
    if not(set(plaintext).issubset({'0', '1'}) and len(plaintext) == 8):
        raise ValueError("Plaintext input must be an 8-bit integer")
    if not (set(key).issubset({'0', '1'}) and len(key) == 10):
        raise ValueError("Input must be a 10-bit integer")

    (K1, K2) = key_gen(key)

    return IP_INV(f_k(SW(f_k(IP(plaintext), K1)), K2))

def print_sdes_encryption(plaintext:str, key:str):
    if not(set(plaintext).issubset({'0', '1'}) and len(plaintext) == 8):
        raise ValueError("Plaintext input must be an 8-bit integer")
    if not (set(key).issubset({'0', '1'}) and len(key) == 10):
        raise ValueError("Input must be a 10-bit integer")
    print(f"Chave: {key}")
    (K1, K2) = key_gen(key)
    print(f"Sub Chave 1: {K1}")
    print(f"Sub Chave 2: {K2}")

    tmp = IP(plaintext)
    print(f"Mensagem apos IP: {tmp}")
    tmp = f_k(tmp, K1)
    print(f"Messagem apos o primeiro f_k: {tmp}")
    tmp = SW(tmp)
    print(f"Mensagem apos o primeiro switch: {tmp}")
    tmp = f_k(tmp, K2)
    print(f"Mensagem apos o segundo f_k: {tmp}")
    print(f"Cipher text: {IP_INV(tmp)}")

#S-DES Decryption Definition
# plaintext = IP_inv (f_k1 (SW (f_k2 (IP (ciphertext)))))
def sdes_decryption(ciphertext:str, key:str):
    if not(set(ciphertext).issubset({'0', '1'}) and len(ciphertext) == 8):
        raise ValueError("Ciphertext input must be an 8-bit integer")
    if not (set(key).issubset({'0', '1'}) and len(key) == 10):
        raise ValueError("Input must be a 10-bit integer")

    (K1, K2) = key_gen(key)

    return IP_INV(f_k(SW(f_k(IP(ciphertext), K2)), K1))

######### Modos de Operacao ###########

#Eletronic codeblock (ECB)
# C_j = E(K, P_j)
# P_j = D(K, C_j)
# No need for padding because block length is the same as message length (*8 bits) 
def ecb_encrypt(message: str, key: str) -> list[str]:
    blocks = message.strip().split()
    return ' '.join([sdes_encryption(block, key) for block in blocks])

def ecb_decrypt(ciphertext: str, key: str) -> str:
    blocks = ciphertext.strip().split()
    return ' '.join([sdes_decryption(block, key) for block in blocks])


#Cipher Block Chaining (CBC)
# C_1 = E(K, [P_1 XOR IV])
# P_1 = D(K, C_1) XOR IV
# C_j = E(K, [P_j XOR C_j-1])
# P_j = D(K, C_j) XOR C_j-1
def cbc_encrypt(message: str, key: str, iv: str) -> list[str]:
    if not(set(iv).issubset({'0', '1'}) and len(iv) == 8):
        raise ValueError("IV must be an 8-bit binary string")

    blocks = message.strip().split()
    ciphertext_blocks = []
    prev = iv

    for block in blocks:
        xored = XOR(block, prev)
        cipher = sdes_encryption(xored, key)
        ciphertext_blocks.append(cipher)
        prev = cipher

    return ' '.join(ciphertext_blocks)

def cbc_decrypt(ciphertext: str, key: str, iv: str) -> str:
    if not(set(iv).issubset({'0', '1'}) and len(iv) == 8):
        raise ValueError("IV must be an 8-bit binary string")

    blocks = ciphertext.strip().split()
    plaintext_blocks = []
    prev = iv

    for block in blocks:
        decrypted = sdes_decryption(block, key)
        plaintext = XOR(decrypted, prev)
        plaintext_blocks.append(plaintext)
        prev = block

    return ' '.join(plaintext_blocks)

