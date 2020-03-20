from simplex import *

if __name__ == "__main__":
    err = 0.0001
    tensile_coef = 4
    compress_coef = 0.5
    res = Simplex(err, tensile_coef, compress_coef)
    print(res)