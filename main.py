import numpy

informacion=[]

abecedario=[]
for i in range(0,256):
    abecedario.append(chr(i))

mensaje1=[]
for i in input('mensaje1: '):
    mensaje1.append(abecedario.index(i))

clave=[]
for i in input('contraseña: '):
    clave.append(abecedario.index(i))


#vamos a calcular el número mínimo de carácteres que tiene que tener el mensaje final

indice_de_ampliacion=0
while (44**indice_de_ampliacion) <= 256 * len(mensaje1):
    indice_de_ampliacion+=1

informacion.append('Indice de ampliacion:')
informacion.append(indice_de_ampliacion)
indice2=0
while 44**indice2 <= len(mensaje1):
    indice2 += 1 #el indice2 nos dice lo que nos ocupara en el mensaje final dar un pista sobre el numero de caracteres que posee el mensaje inicial
informacion.append('Número de carácteres que usaremos para dar pistas sobre el número de carácteres que tenía el mensaje antes de encriptarse:')
informacion.append(indice2)

largominimo=len(mensaje1)*indice_de_ampliacion + 1 + indice2
informacion.append('largo minimo ')
informacion.append(largominimo)

largo=int(input('Número de carácteres del mensaje final (el mínimo de caráteres será {0}): '.format(largominimo)))

if largo < largominimo:
    largo=largominimo

clave1lista=False
clave2lista=False
clave3lista=False
clave1=[]
clave2=[]
clave3=[]
claveternaria=[]


for i in range(len(clave)):
    claveternaria.append('')
    for j in range(5,-1,-1):
        claveternaria[i]+= str(clave[i] // (3**j))
        clave[i] %= 3**j

informacion.append('clave ternaria:')
informacion.append(claveternaria)

while clave1lista==False or clave2lista==False or clave3lista==False:
    clavesecuencia=''
    for i in claveternaria:
        añadido=False
        for j in range(5, -1, -1):
            if i[j] != '0' and añadido==False:
                clavesecuencia += '1' + i[:j] + str(int(i[j])-1) + ('2'*(5-j))
                añadido=True
        if añadido==False:
            clavesecuencia+= '022222'
    del claveternaria
    claveternaria=[]
    while len(clavesecuencia) % 6 != 0:
        clavesecuencia+='0'
    for i in range(len(clavesecuencia)//6):
        claveternaria.append(clavesecuencia[i*6:i*6+6])
    informacion.append('clave secuencia:')
    informacion.append(clavesecuencia)
    if len(clavesecuencia)//5 >= len(mensaje1)*2 and clave1lista==False: #clave1
        for i in range(len(mensaje1)):
            clave1.append([1,1])
            for j in range(5):
                clave1[i][0]+=int(clavesecuencia[(i*5)+j]) * (3**(4-j))
                clave1[i][1]+=int(clavesecuencia[(len(mensaje1)*5)+((i*5)+j)]) * (3**(4-j))
            clave1.insert(i, (clave1[i][0]*clave1[i][1])%257)
            clave1.remove(clave1[i+1])
        clave1lista=True
        informacion.append('Clave 1:')
        informacion.append(clave1)
    if len(clavesecuencia) > len(mensaje1)**2 and clave2lista==False: #clave2
        for i in range(len(mensaje1)):
            clave2.append([])
            for j in range(len(mensaje1)):
                if clavesecuencia[j+(i*len(mensaje1))] == '2':
                    clave2[-1].append(-1)
                else:
                    clave2[-1].append(int(clavesecuencia[j+(i*len(mensaje1))]))
        try: #puede ocurrir que se obtenga una matriz sin solucion, en este paso vamos a comprobar que nuestra matriz tiene solucion
            prueba_matriz=[]
            for i in range(len(mensaje1)):
                prueba_matriz.append(0)
                for j in range(len(mensaje1)):
                    prueba_matriz[i]+= range(1,len(mensaje1)+1)[j]*clave2[i][j]
            prueba_matriz_numeros=numpy.array(clave2)
            prueba_matriz_soluciones=numpy.array(prueba_matriz)
            prueba_incognitas=numpy.linalg.solve(prueba_matriz_numeros,prueba_matriz_soluciones)
            clave2lista=True
            informacion.append('Clave 2:')
            informacion.append(clave2)
        except:
            informacion.append('Matriz erronea:')
            informacion.append(prueba_matriz)
            clave2=[]
    if len(clavesecuencia)//4 >= largo*2 and clave3lista==False: #clave3
        for i in range(largo):
            clave3.append([1,1])
            for j in range(4):
                clave3[i][0]+=int(clavesecuencia[(i*4)+j]) * (3**(3-j))
                clave3[i][1]+=int(clavesecuencia[(largo*4)+((i*4)+j)]) * (3**(3-j))
            clave3.insert(i, (clave3[i][0]*clave3[i][1])%97)
            clave3.remove(clave3[i+1])
        clave3lista=True
        informacion.append('Clave 3:')
        informacion.append(clave3)
    
informacion.append('Clave 1:')
informacion.append(clave1)
informacion.append('Clave 2:')
informacion.append(clave2)
informacion.append('Clave 3:')
informacion.append(clave3)


#obtencion del mensaje 2 encriptando el mensaje 1 con la clave 1

mensaje2=[]
for i in range(len(mensaje1)):
    mensaje2.append((mensaje1[i]*clave1[i])%257)

informacion.append('Mensaje 2:')
informacion.append(mensaje2)

#obtencion del mensaje 3 encriptando el mensaje 2 con la clave 2

mensaje3=[]

for i in range(len(mensaje2)):
    mensaje3.append(0)
    for j in range(len(mensaje2)):
        mensaje3[i]+= mensaje2[j]*clave2[i][j]

informacion.append('Mensaje 3:')
informacion.append(mensaje3)

#calculamos los caracteres que debera ocupar en el mensaje final cada uno de los caracteres, para obtener un mensaje final con el numero de caracteres que desee el usuario

numero_de_caracteres_restantes=largo-1-indice2
cifras=[]

for i in range(len(mensaje1),0,-1):
    cifras.append(numero_de_caracteres_restantes//i)
    numero_de_caracteres_restantes -= cifras[-1]

informacion.append('Cuantos carácteres ocupará cada letra del mensaje inicial:')
informacion.append(cifras)


#obtencion del mensaje 4 haciendo mas grandes los numeros

mensaje4=[]
for i in range(len(mensaje3)):
    mensaje4.append(mensaje3[i]* ((44**(cifras[i])-1)//(256*len(mensaje3))) )

informacion.append('Mensaje 4:')
informacion.append(mensaje4)

negativos=[]

for i in range(len(mensaje4)):
    if mensaje4[i]<0:
        negativos.append(i)
        mensaje4.insert(i,0-mensaje4[i])
        mensaje4.remove(mensaje4[i+1])

informacion.append('Posición en la que se encontraban los números negativos en el mensaje 4:')
informacion.append(negativos)


#obtencion del mensaje 5
mensaje5=[]

for i in range(len(mensaje4)):
    for j in range(cifras[i]-1,-1,-1):
        mensaje5.append( 1 + ( mensaje4[i] // (44**j) ) )
        mensaje4[i] %= 44**j
        if i in negativos:
            mensaje5[-1]+=44
mensaje5.append(89)
numero_de_caracteres_del_mensaje_incial=len(mensaje3)

longitud_palabra=len(mensaje3)
while indice2 != 0:
    mensaje5.append(longitud_palabra//(44**(indice2-1)))
    longitud_palabra -= (longitud_palabra//(44**(indice2-1)))* (44**(indice2-1))
    indice2-=1

informacion.append('Mensaje 5:')
informacion.append(mensaje5)

#obtencion del mensaje 6 encriptando el mensaje 5 con la clave 3

mensaje6=[]

for i in range(len(mensaje5)):
    mensaje6.append((mensaje5[i]*(clave3[i]))%97)

informacion.append('Mensaje 6:')
informacion.append(mensaje6)

#obtencion del mensaje 7

mensaje7=''
mensaje7numeros=[]

for i in mensaje6:
    if i>92:
        mensaje7+=chr(i+69)
        mensaje7numeros.append(i+69)
    else:
        mensaje7+=chr(i+34)
        mensaje7numeros.append(i+34)

informacion.append('mensaje 7')
informacion.append(mensaje7numeros)
print('')
print('Mensaje cifrado:')
print(mensaje7)
print('')

if input('¿Quieres ver toda la informacion de la encriptación? [S/n]  ')=='S':
    print('')
    print('')
    for i in range(len(informacion)):
        print(informacion[i])
        if i%2==1:
            print('')
