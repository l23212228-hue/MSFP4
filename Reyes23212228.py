"""
Práctica 4: Modelado y control del sistema endocrino
Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Mariant Reyes Zamudio
Número de control: 23212228
Correo institucional: l23212228@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 10, 5
N = round(tend / dt) + 1
t = np.linspace(t0, tend, N)
u = np.ones(N)

# Función del sistema basada en la función de transferencia
def sis(C, R2, nombre):
    R1, L = 1E3, 100E-3
    num = [L, R2]
    den = [C * L * R1, C * R1 * R2 + L, R1 + R2]
    sys = ctrl.tf(num, den)
    print(f"Función de transferencia {nombre}: {sys}\n")
    return sys

sysControl = sis(1E-6, 100E3, "Control")
sysCaso = sis(1000E-6, 1E3, "Caso")

# Componentes del controlador PID
kP, kI, kD = 2048.14768883037, 776909.685302916, 0.181141069703887
Cr = 1E-6
Re = 1 / (Cr * kI)
Rr = kP * Re
Ce = kD / Rr

numPID = [Re * Rr * Ce * Cr, Re * Ce + Rr * Cr, 1]
denPID = [Re * Cr, 0]
PID = ctrl.tf(numPID, denPID)

print(f"El valor de la capacitancia Cr es de {Cr} Faradios.")
print(f"El valor de la resistencia Re es de {Re:.4f} Ohms.")
print(f"El valor de la resistencia Rr es de {Rr:.4f} Ohms.")
print(f"El valor de la capacitancia Ce es de {Ce:.6e} Faradios.\n")
print(f"Función de transferencia del controlador PID: {PID}\n")

# Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID, sysCaso), 1, sign=-1)
print(f"Función de transferencia en lazo cerrado: {sysPID}\n")

# Colores de tu gráfica
clr1 = np.array([66, 133, 244]) / 255   # Azul
clr2 = np.array([234, 67, 53]) / 255    # Rojo
clr3 = np.array([251, 188, 5]) / 255    # Amarillo
clr4 = np.array([52, 168, 83]) / 255    # Verde

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t, sys, u):
    _, Vs = ctrl.forced_response(sys, t, u, x0)
    return Vs

def closedloop(t, sys, u):
    _, tratamientoPID = ctrl.forced_response(sys, t, u, x0)
    return tratamientoPID

# Respuestas: Simulaciones numéricas
Control = openloop(t, sysControl, u)
Caso = openloop(t, sysCaso, u)
Tratamiento = closedloop(t, sysPID, Control)

# Configuración y graficación
fg = plt.figure()
fg.set_size_inches(w, h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

plt.plot(t, u, '-', linewidth=1.5, color=clr1, label='$V_e(t)$')
plt.plot(t, Control, ':', linewidth=1.5, color=clr2, label='$F_S(t)$: Control')
plt.plot(t, Caso, '--', linewidth=1.5, color=clr3, label='$F_S(t)$: Caso')
plt.plot(t, Tratamiento, '-.', linewidth=1.5, color=clr4, label='$PID(t)$: Tratamiento')

plt.xlim(-0.1, 10); plt.xticks(np.arange(0, 11, 1))
plt.ylim(0, 1.2); plt.yticks(np.arange(0, 1.3, 0.1))

plt.xlabel('$t [s]$')
plt.ylabel('$F_S(t)$ [V]')

plt.legend(bbox_to_anchor=(0.5, 1.08), loc='center', ncol=4, frameon=False)

fg.savefig('Control_caso_python3.pdf', bbox_inches='tight')
plt.show()
