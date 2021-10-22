import numpy

def identity_stance(arr):
    try:
        print('IDENTITY STANCE') #Kiai 
        print(arr.shape)
        return arr
    except:
        print('IDENTITY STANCE FAILED...')
        print(' one must use an array')