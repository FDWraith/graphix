import math

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]
    
    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

def calc_mag(vector):
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])

def scalar_mult(vector, scalar):
    return [ scalar * i for i in vector ]

def vector_subtraction(a, b):
    return [(a[0] - b[0]), (a[1] - b[1]), (a[2] - b[2])]

def toUnitVector(vector):
    v = [0, 0, 0]
    mag = calc_mag(vector)
    
    v[0] = (vector[0])/mag
    v[1] = (vector[1])/mag
    v[2] = (vector[2])/mag
    return v

def dot_product(a, b):
    a = toUnitVector(a)
    b = toUnitVector(b)

    p = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return p if p >= 0 else 0

def iAmbient(Lc, Ka):
    return Lc * Ka

def iDiffuse(Lc, Kd, N, L):
    p = dot_product(N, L)
    return Lc * Kd * p

def iSpecular(Lc, Ks, N, L):
    N_L = dot_product(N, L)
    p = scalar_mult(scalar_mult(N, 2), N_L)
    d = vector_subtraction(p, L)
    p = dot_product(d, [0, 0, 1])
    
    return Lc * Ks * (p ** 120)

def intensity(iAmbient, iDiffuse, iSpecular):
    s = iAmbient + iDiffuse + iSpecular
    return int(round(s)) if s <= 255 else 255

def calculateLight(N, constants, light_source):
    L = light_source['location']
    
    KaR = constants["red"][0]
    KdR = constants["red"][1]
    KsR = constants["red"][2]
    
    KaG = constants["green"][0]
    KdG = constants["green"][1]
    KsG = constants["green"][2]
    
    KaB = constants["blue"][0]
    KdB = constants["blue"][1]
    KsB = constants["blue"][2]
    
    LR = light_source['color'][0]
    LG = light_source['color'][1]
    LB = light_source['color'][2]
    
    red = intensity(iAmbient(LR, KaR), iDiffuse(LR, KdR, N, L), iSpecular(LR, KsR, N, L))
    green = intensity(iAmbient(LG, KaG), iDiffuse(LG, KdG, N, L), iSpecular(LG, KsG, N, L))
    blue = intensity(iAmbient(LB, KaB), iDiffuse(LB, KdB, N, L), iSpecular(LB, KsB, N, L))

    return [red, green, blue]

def getTotalColor(N, constants, sources):
    I = [0, 0, 0]
    
    for source in sources:
        light = calculateLight(N, constants, source)
        I[0] += light[0]
        I[1] += light[1]
        I[2] += light[2]
        
    I[0] = I[0] if I[0] <= 255 else 255
    I[1] = I[1] if I[1] <= 255 else 255
    I[2] = I[2] if I[2] <= 255 else 255
    return I
