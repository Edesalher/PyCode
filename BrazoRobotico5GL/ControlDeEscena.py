"""
ROBOTIC ARM
Autor: Edwing Estuardo Alvarez Hernández.
Fecha: Noviembre 6, 2020.

***CONTROL Y EJECUCIÓN DE LA ESCENA DEL BRAZO ROBÓTICO EN COPPELIASIM***

Instrucciones:
    Se debe abrir la escena LabRBTK_PROYECTOvFinal en CoppeliaSim y luego ejecutar este script.

Descripción de Denavit-Hartenber del brazo robot
    a   |  alpha  |   d    |   theta
--------|---------|--------|-----------
   0    |  pi/2   |  0.12  |    q1
   0.36 |  0      | -0.04  |    q2
   0.18 |  0      |  0     |    q3
   0    |  pi/2   | -0.04  |    q4 + pi/2
   0    |  0      |  0.344 |    q5
"""

import b0RemoteApi
import time
import sympy as sp
from myrobot import Robot, print_matrix
from pynput import keyboard as kb


def exit_scene(tecla):
    # Si la tecla pulsada fué esc entonces el False terminará el hilo.
    if tecla == kb.Key.esc:
        return False


with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:
    # ************************************* PREPARACIÓN DE LA ESCENA ************************************************ #

    # Se obtienen los controladores para cada una de las articulaciones del brazo robótico.
    joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
    joints = []
    for joint in joint_names:
        j = client.simxGetObjectHandle(joint, client.simxServiceCall())[1]
        joints.append(j)

    # Se obtienen los controladores a usar para determinar la Tm0 de interés.
    o = client.simxGetObjectHandle('joint1', client.simxServiceCall())[1]
    m = client.simxGetObjectHandle('mf', client.simxServiceCall())[1]
    # c = client.simxGetObjectHandle('Cuboid', client.simxServiceCall())[1]
    # red = client.simxGetObjectHandle('red', client.simxServiceCall())[1]
    # green = client.simxGetObjectHandle('green', client.simxServiceCall())[1]

    # Definición de la variable simbólica para cada ángulo de cada articulación del brazo robótico.
    sq = sp.symbols(['q1', 'q2', 'q3', 'q4', 'q5'])

    # Se define la matriz D-H que contiene la descripción de Denavit-Hartenber del brazo robótico.
    # dh = sp.Matrix([[0,    sp.pi/2,  0.12,  sq[0]],
    #                 [0.36, 0,       -0.04,  sq[1]],
    #                 [0.18, 0,        0,     sq[2]],
    #                 [0,    sp.pi/2, -0.04,  sq[3] + sp.pi/2],
    #                 [0,    0,        0.344, sq[4]]])
    dh = sp.Matrix([[0, sp.pi / 2, 0.12, sq[0]],
                    [0.36, 0, -0.04, sq[1]],
                    [0.18, 0, 0, sq[2]],
                    [0.12, 0, -0.04, sq[3]],
                    [0, sp.pi / 2, 0, sp.pi / 2],
                    [0, 0, 0.224, sq[4]]])

    # SE CREA EL BRAZO ROBÓTICO.
    robot = Robot(joints, dh, client)

    # Se determina la Tm0 correspondiente a la pose que se desea que tenga el manipulador final.
    Tm0 = robot.get_tm0(o, m)
    print('Tm0 DESEADA:')
    print_matrix(Tm0)

    # Se calcula la cinemática inversa para la pose Tm0.
    tm0_solutions = robot.do_inverse_kinematics(Tm0)
    print('SOLUCIONES PARA q1, q2, q3, q4, q5:')
    print_matrix(tm0_solutions)

    # ***************************************** EJECUCIÓN DE LA ESCENA ********************************************** #

    # SE INICIA LA SIMULACIÓN.
    client.simxStartSimulation(client.simxDefaultPublisher())

    # Se crea un hilo que permitirá estar al pendiente de la pulsación de una tecla.
    listener = kb.Listener(exit_scene)
    # Se inicia el hilo "listener".
    listener.start()

    while listener.is_alive():
        robot.set_joints(joints, tm0_solutions[2, :])
        # pass

    # time.sleep(2)
    # SE TERMINA LA SIMULACIÓN.
    client.simxStopSimulation(client.simxDefaultPublisher())
