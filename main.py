def suma(a, b):
    c = a + b
    d = a*b
    return c,d

def resta(c, d):
    return (c - d)

if __name__ == '__main__':
    v1, v2 = suma(3, 4)
    v3 = resta(v1, v2)
    print(v3)