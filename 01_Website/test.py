roles = {
    'Doctor':1,
    'Asistente': 2,
    'Manager': 3
}

usr = 'Manager'

for i in roles:
    if usr == i:
        id_puesto = roles[i]

print("este es el puesto {}" .format(id_puesto))