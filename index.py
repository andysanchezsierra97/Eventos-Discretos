import random
import math

def u_var(a, b):
    u = random.random()
    while not u:
        u = random.random()
    return a + (b - a) * u

def exp_var(l):
    return -(1 / l) * math.log(u_var(0,1))

def normal_s_var():
    while 1:
        e = exp_var(1)
        u = u_var(0,1)
        if u < math.e ** (-((e - 1) **2) / 2):
            x = e

            r = u_var(0,1)
            if r <= .5:
                x *= -1

            return x

def normal_var(m, s):
    return normal_s_var()*s+m

def poisson_var(l):
    p = 1
    n = 0
    while 1:
        p*= u_var(0, 1)
        n+=1
        if p < math.e**(-l):
            break

    return n - 1

def random_var(X,P):
    u = u_var(0,1)
    f = 0
    for i in range(len(X)):
        f += P[i]
        if u < f:
            return X[i]


#Variables de tiempo
t = 0
ta = poisson_var(20)
T = 480 #Jornada de trabajo (8h)

#Vendedores
tDv1 = math.inf
tDv2 = math.inf

#Especializado
tDe = math.inf

#Tecnicos
tDt1 = math.inf
tDt2 = math.inf
tDt3 = math.inf

#Variables contadoras

G = 0 # ganacia
Gs = {}

Na = 0
A = {}

#Vendedores
nv = 0
NDv1 = 0
NDv2 = 0
Dv1 = {}
Dv2 = {}

#Especializado
ne = 0
NDe = 0
De = {}


#Tecnicos
nt = 0
NDt1 = 0
NDt2 = 0
NDt3 = 0
Dt1 = {}
Dt2 = {}
Dt3 = {}

#Variables de estado
P = [0, 350, 500, 750] # precios

ST = [0,0,0,0,[]] # [n, Ct1, Ct2, Ct3 Qt]
SV = [0,0,0,[]] # [n, Cv1, Cv2, Qv]
SE = [0,0,[]] # [n, Ce, Qe]


while 1:
    _min = min(ta, tDv1, tDv2, tDt1, tDt2, tDt3, tDe)

    #Arribo
    if _min == ta and ta <= T :

        t = ta
        Na +=1

        tAt = poisson_var(20)
        ta = t + tAt
        if ta > T:
            ta = math.inf

        A[Na] = t


        s = random_var([1,2,4,3], [.45, .25, .2, .1])
        G += P[s - 1]
        Gs[Na] = P[s - 1]

        #Arribo Cambio
        if s == 3:
            ne += 1
            if SE[1] == 0:
                SE = [ne, Na, SE[2]]
                tDet = exp_var(1/15)
                tDe = t + tDet
            else:
                SE = [ne, SE[1], SE[2] + [Na]]

        #Arribo Compra
        elif s == 4:
            nv += 1

            if SV[1] == 0:
                SV = [nv, Na, SV[2], SV[3]]
                tDv1t = normal_var(5,2)
                tDv1 = t + tDv1t

            elif SV[2] == 0:
                SV = [nv, SV[1], Na, SV[3]]
                tDv2t = normal_var(5,2)
                tDv2 = t + tDv2t
            
            else:
                SV = [nv, SV[1], SV[2], SV[3] + [Na]]

        #Arrivo Reparacion
        else:
            nt += 1

            if ST[1] == 0:
                ST = [nt, Na, ST[2], ST[3], ST[4]]
                tDt1t = exp_var(1/20)
                tDt1 = t + tDt1t

            elif ST[2] == 0:
                ST = [nt, ST[1], Na, ST[3], ST[4]]
                tDt2t = exp_var(1/20)
                tDt2 = t + tDt2t

            elif ST[3] == 0:
                ST = [nt, ST[1], ST[2], Na, ST[4]]
                tDt3t = exp_var(1/20)
                tDt3 = t + tDt3t
            
            elif SE[2] == 0 and len(SE[3]) == 0:
                ne+=1
                nt-=1
                SE = [ne, Na, []]
                tDet = exp_var(1/20)
                tDe = t + tDet

            else:
                ST = [nt, ST[1], ST[2], ST[3], ST[4] + [Na]]

    #Partida_v1
    elif _min == tDv1 and tDv1 <= T :
        t = tDv1
        NDv1 +=1
        Dv1[SV[1]] = t
        
        if nv == 1:
            nv -=1
            SV = [0,0,0,[]]
            tDv1 = math.inf

        elif nv == 2:
            nv -=1
            SV = [1,0,SV[2],[]]
            tDv1 = math.inf

        elif nv > 2:
            f = SV[3][0]
            SV[3].remove(f)
            nv -=1
            SV = [nv, f, SV[2], SV[3]]
            tDv1t = normal_var(5,2)
            tDv1 = t + tDv1t

    #Partida_v2
    elif _min == tDv2 and tDv2 <= T :
        t = tDv2
        NDv2 +=1
        Dv2[SV[2]] = t
        
        if nv == 1:
            nv -=1
            SV = [0,0,0,[]]
            tDv2 = math.inf

        elif nv == 2:
            nv -=1
            SV = [1,SV[1],0,[]]
            tDv2 = math.inf

        elif nv > 2:
            nv -=1
            f = SV[3][0]
            SV[3].remove(f)
            SV = [nv, SV[1], f, SV[3]]
            tDv2t = normal_var(5,2)
            tDv2 = t + tDv2t

    #Partida_e
    elif _min == tDe and tDe <= T :
        t = tDe
        NDe +=1
        De[SE[1]] = t
        
        if len(SE[2]) == 0:

            if len(ST[4]) == 0:
                ne-=1
                tDe = math.inf
                SE = [nv, 0, []]

            else:
                nt -=1
                tDet = exp_var(1/20)
                tDe = t + tDet
                f = ST[2][0]
                ST[2].remove(f)
                SE = [ne, f, []]
                ST[0] = nt

        else:
            ne-=1
            tDet = exp_var(1/15)
            tDe = t + tDet
            f = SE[2][0]
            SE[2].remove(f)
            SE = [ne, f, SE[2]]

    #Partida_t1
    elif _min == tDt1 and tDt1 <= T :
        t = tDt1
        NDt1 +=1
        Dt1[ST[1]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt1 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, 0, ST[2], ST[3], []]
            tDt1 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, f, ST[2], ST[3], ST[4]]
            tDt1t = exp_var(1/20)
            tDt1 = t + tDt1t

    #Partida_t2
    elif _min == tDt2 and tDt2 <= T :
        t = tDt2
        NDt2 +=1
        Dt2[ST[2]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt2 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, ST[1], 0, ST[3], []]
            tDt2 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, ST[1], f, ST[3], ST[4]]
            tDt2t = exp_var(1/20)
            tDt2 = t + tDt2t

    #Partida_t3
    elif _min == tDt3 and tDt3 <= T :
        t = tDt3
        NDt3 +=1
        Dt3[ST[3]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt3 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, ST[1], ST[2], 0, []]
            tDt3 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, ST[1], ST[2], f, ST[4]]
            tDt3t = exp_var(1/20)
            tDt3 = t + tDt3t
    
    #Cierres
    #V1
    elif _min == tDv1 and _min > T and nv > 0:
        t = tDv1
        NDv1 +=1
        Dv1[SV[1]] = t
        
        if nv == 1:
            nv -=1
            SV = [0,0,0,[]]
            tDv1 = math.inf

        elif nv == 2:
            nv -=1
            SV = [1,0,SV[2],[]]
            tDv1 = math.inf

        elif nv > 2:
            f = SV[3][0]
            SV[3].remove(f)
            nv -=1
            SV = [nv, f, SV[2], SV[3]]
            tDv1t = normal_var(5,2)
            tDv1 = t + tDv1t
    #V2
    elif _min == tDv2 and _min > T and nv > 0:
        t = tDv2
        NDv2 +=1
        Dv2[SV[2]] = t
        
        if nv == 1:
            nv -=1
            SV = [0,0,0,[]]
            tDv2 = math.inf

        elif nv == 2:
            nv -=1
            SV = [1,SV[1],0,[]]
            tDv2 = math.inf

        elif nv > 2:
            nv -=1
            f = SV[3][0]
            SV[3].remove(f)
            SV = [nv, SV[1], f, SV[3]]
            tDv2t = normal_var(5,2)
            tDv2 = t + tDv2t

    #E
    elif _min == tDe and _min > T and ne > 0:
        t = tDe
        NDe +=1
        De[SE[1]] = t
        
        if len(SE[2]) == 0:

            if len(ST[4]) == 0:
                ne-=1
                tDe = math.inf
                SE = [nv, 0, []]

            else:
                nt -=1
                tDet = exp_var(1/20)
                tDe = t + tDet
                f = ST[2][0]
                ST[2].remove(f)
                SE = [ne, f, []]
                ST[0] = nt

    #T1
    elif _min == tDt1 and _min > T and nt > 0:
        t = tDt1
        NDt1 +=1
        Dt1[ST[1]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt1 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, 0, ST[2], ST[3], []]
            tDt1 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, f, ST[2], ST[3], ST[4]]
            tDt1t = exp_var(1/20)
            tDt1 = t + tDt1t
    #T2
    elif _min == tDt2 and _min > T and nt > 0:
        t = tDt2
        NDt2 +=1
        Dt2[ST[2]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt2 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, ST[1], 0, ST[3], []]
            tDt2 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, ST[1], f, ST[3], ST[4]]
            tDt2t = exp_var(1/20)
            tDt2 = t + tDt2t
    #T3       
    elif _min == tDt3 and _min > T and nt > 0:
        t = tDt3
        NDt3 +=1
        Dt3[ST[3]] = t
        
        if nt == 1:
            nt -=1
            ST = [0,0,0,0,[]]
            tDt3 = math.inf

        elif nt == 2 or nt == 3:
            nt -=1
            ST = [1, ST[1], ST[2], 0, []]
            tDt3 = math.inf

        elif nt > 3:
            nt -=1
            f = ST[4][0]
            ST[4].remove(f)
            ST = [nt, ST[1], ST[2], f, ST[4]]
            tDt3t = exp_var(1/20)
            tDt3 = t + tDt3t

    else:
        break

print(f'Total de Clientes {len(A.keys())}')

for item in A:
    if item in Dv1.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {Dv1[item]}. Ganacia: {Gs[item]}')
    if item in Dv2.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {Dv2[item]}. Ganacia: {Gs[item]}')
    if item in Dt1.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {Dt1[item]}. Ganacia: {Gs[item]}')
    if item in Dt2.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {Dt2[item]}. Ganacia: {Gs[item]}')
    if item in Dt3.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {Dt3[item]}. Ganacia: {Gs[item]}')
    if item in De.keys():
        print(f'Cliente {item}: Arribo {A[item]} - Salida {De[item]}. Ganacia: {Gs[item]}')

print(f'Ganacia total: {G}')
