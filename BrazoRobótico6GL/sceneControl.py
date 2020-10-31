"""
*** CONTROL Y EJECUCIÓN DE LA ESCENA DEL BRAZO ROBÓTICO EN COPPELIASIM ***
Author: Edwing Alvarez
Fecha: Octubre 29, 2020.

Instrucciones:
    Se debe abrir la escena LabRBTK_PROYECTOvFinal en CoppeliaSim y luego ejecutar este script.

Denavit-Hartenberg description for the robotic arm with 6 degrees of freedom.
    a   |  alpha  |   d    |   theta
--------|---------|--------|-----------
   0    |  pi/2   |  0.1   |    q1
   0.2  |  0      |  0     |    q2
   0.2  |  0      |  0     |    q3
   0    | -pi/2   |  0     |    q4
   0    |  pi/2   |  0     |    q5
   0    |  0      |  0.05  |    q6
"""

import b0RemoteApi
import time
import sympy as sp
from myrobot import Robot, print_matrix
from pynput import keyboard as kb


def exit_scene(keyboard_key):
    # If the key pressed was ESC, then the False will end the thread.
    if keyboard_key == kb.Key.esc:
        return False


with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:

    # ***************************************** PREPARATION OF THE SCENE ******************************************** #

    # Getting each handle of each joint for the robotic arm.
    joint_names = ['sys0', 'sys1', 'sys2', 'sys3', 'sys4', 'sys5']
    joints = []
    for joint in joint_names:
        j = client.simxGetObjectHandle(joint, client.simxServiceCall())[1]
        joints.append(j)

    # Getting each handle to use to determine the Tm0 of interest.
    o = client.simxGetObjectHandle('sys0', client.simxServiceCall())[1]
    w = client.simxGetObjectHandle('work_system', client.simxServiceCall())[1]
    m = client.simxGetObjectHandle('mf', client.simxServiceCall())[1]
    h = client.simxGetObjectHandle('Cuboid', client.simxServiceCall())[1]

    # Definition of the variable for each angle of each joint of the robotic arm.
    q1 = sp.symbols('q1')
    q2 = sp.symbols('q2')
    q3 = sp.symbols('q3')
    q4 = sp.symbols('q4')
    q5 = sp.symbols('q5')
    q6 = sp.symbols('q6')

    # Creating the D-H matrix containing the Denavit-Hartenberg description of the robotic arm.
    dh = sp.Matrix([[0,   sp.pi/2,  0.1,  q1],
                    [0.2, 0,        0,    q2],
                    [0.2, 0,        0,    q3],
                    [0,   -sp.pi/2, 0,    q4],
                    [0,   sp.pi/2,  0,    q5],
                    [0,   0,        0.05, q6]])

    # THE ROBOTIC ARM IS CREATED.
    robot = Robot(joints, dh, client)

    # Determining the matrix Tm0 corresponding to the desired pose for the final manipulator.
    Tm0 = robot.get_tm0(o, w, m, h)
    print_matrix(Tm0)

    # Calculating the inverse kinematics for the pose Tm0.
    tm0_solutions = robot.do_inverse_kinematics(Tm0)

    print_matrix(tm0_solutions)

    # ******************************************* EJECUCIÓN DE LA ESCENA ******************************************** #

    # STARTING THE SIMULATION.
    client.simxStartSimulation(client.simxDefaultPublisher())

    # A thread is created that will allow to be aware of the pressing of a key.
    listener = kb.Listener(exit_scene)
    # Starting the thread "listener".
    listener.start()

    while listener.is_alive():
        robot.set_joints(joints, tm0_solutions[0, :])

    # time.sleep(2)
    # FINISHING THE SIMULATION
    client.simxStopSimulation(client.simxDefaultPublisher())
