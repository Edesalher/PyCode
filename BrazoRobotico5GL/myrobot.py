"""
ROBOTIC ARM.
Autor: Edwing Estuardo Alvarez Hernández.
Fecha: Octubre 28, 2020.

***CLASE PARA CREAR EL BRAZO ROBÓTICO Y PODER CONTROLARLO***

"""

import sympy as sp
import numpy as np


def print_matrix(matrix):
    for m in range(len(matrix[:, 0])):
        print('[ ', end='')
        for n in range(len(matrix[0, :])):
            print(f'{matrix[m, n]}', end='')
            if n < len(matrix[0, :]) - 1:
                print(', ', end='')
        print(' ]')
    print('')


def get_t_from_dh(a, alpha, d, theta):
    """
    DESCRIPCIÓN:
    Esta función toma los parámetros de Denavit y Hartenberg para producir la matriz
    de transformación correspondiente.

    :param a:     Distancia a lo largo de x(i+1) para unir los orígenes del sistema i con el sistema i+1.
    :param alpha: Ángulo alrededor de x(i+1) por el cual hay que rotar z(i) para alinearlo con z(i+1).
    :param d:     Distancia a lo largo de z(i) para unir los orígenes del sistema i con el sistema i+1.
    :param theta: Ángulo alrededor de z(i) por el cual hay que rotar x(i) para alinearlo con x(i+1).

    :return matrix: matriz de transformación en base a los parámetros dados.
    """
    matrix = sp.Matrix([
                    [sp.cos(theta), -sp.sin(theta) * sp.cos(alpha), sp.sin(theta) * sp.sin(alpha), a * sp.cos(theta)],
                    [sp.sin(theta), sp.cos(theta) * sp.cos(alpha), -sp.cos(theta) * sp.sin(alpha), a * sp.sin(theta)],
                    [0, sp.sin(alpha), sp.cos(alpha), d],
                    [0, 0, 0, 1]])
    return matrix


class Robot:
    def __init__(self, joints, dh_matrix, client):
        # Variables del robot donde se almacena la información de sus joints y su tabla de D-H.
        self.joints = joints
        self.dh = dh_matrix
        # Variable del robot donde se almacena al cliente de CoppeliaSim para poder controlarlo.
        self.client = client
        # Variables del robot donde se guarda la configuración de los 5 ángulos (q1, ..., q5) para cada caso.
        self.config_a = []  # Zona A = zona donde se recogen los cubitos de la banda.
        self.config_r = []  # Caja R = caja a la que se llevan los cubitos rojos.
        self.config_g = []  # Caja G = caja a la que se llevan los cubitos verdes.
        self.config_y = []  # Caja Y = caja a la que se llevan los cubitos amarillos.
        # Variables donde se almacena al controlador de la garra del brazo robótico, su velocidad y fuerza.
        self.claw_handle = self.client.simxGetObjectHandle('RG2_openCloseJoint', self.client.simxServiceCall())[1]
        self.claw_motor_velocity = 0.05  # m/s
        self.claw_motor_force = 20       # N

    def move_joint(self, joint, angle):
        # Se envía el valor del ángulo en radianes.
        self.client.simxSetJointTargetPosition(joint, angle, self.client.simxServiceCall())

    def set_joints(self, list_of_joints, list_of_angles):
        # Se mueve un conjunto de joints en vez de uno por uno.
        for j in range(len(list_of_joints)):
            self.move_joint(list_of_joints[j], list_of_angles[j])

    def actuate_the_gripper(self, state=False):
        """
        DESCRIPCIÓN:
        Esta función permite controlar la garra RG2 que ya viene incluida entre los modelos que trae
        CoppeliaSim.

        La forma en que se abre y cierra la garra es simplemente cambiando la dirección de la velocidad
        del motor de la garra.

        :param state: Indica si se quiere que la pinza (gripper) se abra o se cierre.
                      state = True --> la pinza se cierra.
        """
        if state:
            v = -self.claw_motor_velocity
            # data = self.client.simxGetIntSignal('RG2_open', self.client.simxServiceCall())
            # if data and (not data) == 0:
            #     v = motor_velocity
            self.client.simxSetJointForce(self.claw_handle, self.claw_motor_force, self.client.simxServiceCall())
            self.client.simxSetJointTargetVelocity(self.claw_handle, v, self.client.simxServiceCall())
        else:
            v = self.claw_motor_velocity
            # data = self.client.simxGetIntSignal('RG2_open', self.client.simxServiceCall())
            # if data and (not data) == 0:
            #     v = motor_velocity
            self.client.simxSetJointForce(self.claw_handle, self.claw_motor_force, self.client.simxServiceCall())
            self.client.simxSetJointTargetVelocity(self.claw_handle, v, self.client.simxServiceCall())

    def do_direct_kinematics(self):
        """
        DESCRIPCIÓN:
        Esta función recibe la tabla de la descripción de Denavit-Hartenberg para producir la matriz
        de transformación Tm0 que representa al manipulador final respecto del sistema 0.

        :return T: matriz de transformación Tm0.
        """
        # se prepara una matriz identidad como valor inicial.
        To = sp.eye(4, 4)
        for m in range(len(self.dh[:, 0])):
            # Se calcula la matriz correspondiente a los parámetros a, alpha, d, theta seleccionados.
            A = get_t_from_dh(self.dh[m, 0], self.dh[m, 1], self.dh[m, 2], self.dh[m, 3])
            # print(f'A{m+1}:')
            # print_matrix(A)
            # Se posmultiplica la matriz de transformación encontrada al resultado anterior.
            To = To * A
        T = sp.simplify(To)

        return T

    def do_inverse_kinematics(self, tm0):
        """
        DESCRIPCIÓN:
        Esta función recibe la tabla de la descripción de Denavit-Hartenberg y la Tm0 que es la matriz
        que se conoce numéricamente y que represeta la pose que se desea para el manipulador final.

        :param tm0: pose deseada para el manipulador final. SE CONOCE NUMÉRICAMENTE.

        :return qs: matriz de 8x5 que contiene las 8 posibles soluciones para los 5 ángulos q1, ..., q5
        """
        # Se obtienen los valores de a y d que interesan.
        a2 = self.dh[1, 0]
        a3 = self.dh[2, 0]
        a4 = self.dh[3, 0]
        d1 = self.dh[0, 2]
        d2 = self.dh[1, 2]
        d4 = self.dh[3, 2]
        # d5 = self.dh[4, 2]
        d6 = self.dh[5, 2]
        # Se obtiene el origen del sistema 3 = coordenas x3, y3, z3 RESPECTO DEL SISTEMA 0.
        # o3 = tm0 * sp.Matrix([[0, abs(d2 + d4), -d5, 1]]).T
        # x3, y3, z3 = o3[:3, 0]
        t4m = sp.Matrix([[0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [1, 0, 0, -d6],
                         [0, 0, 0, 1]])

        t40 = tm0 * t4m
        d = sp.Matrix([[-a4, abs(d2 + d4), 0, 1]])
        o3 = t40 * d.T
        x3 = o3[0]
        y3 = o3[1]
        z3 = o3[2]
        # print(f'ORIGEN DEL SISTEMA 3: x3={x3}, y3={y3}, z3={z3}\n')

        # Se prepara la matriz "solutions" que contendrá las 8 posibles configuraciones de q1 a q5.
        solutions = np.zeros((8, 5))

        """ **** CASO "A" DE THETA 1 POSITIVO **** """

        # Se obtiene los valores de theta1 posibles.
        q1_1a = sp.atan2(y3, x3)

        cos_q3 = (x3**2 + y3**2 + (z3 - d1)**2 - a2**2 - a3**2) / (2 * a2 * a3)

        # Se obtienen los valores de theta3 posibles.
        q3_1a = sp.atan2(sp.sqrt(1 - cos_q3**2), cos_q3)
        q3_2a = sp.atan2(-sp.sqrt(1 - cos_q3**2), cos_q3)
        # Se obtienen los valores de theta2 posibles.
        q2_1a = sp.atan2(z3 - d1, sp.sqrt(x3 ** 2 + y3 ** 2)) - sp.atan2(a3 * sp.sin(q3_1a), a2 + a3 * sp.cos(q3_1a))
        q2_2a = sp.atan2(z3 - d1, sp.sqrt(x3 ** 2 + y3 ** 2)) - sp.atan2(a3 * sp.sin(q3_2a), a2 + a3 * sp.cos(q3_2a))

        # Se agregan los resultados de q1, q2 y q3 para el caso "A" a la matriz de soluciones.
        solutions[0:4, 0] = q1_1a
        solutions[0:2, 1] = q2_1a
        solutions[2:4, 1] = q2_2a
        solutions[0:2, 2] = q3_1a
        solutions[2:4, 2] = q3_2a

        """ **** CASO "B" DE THETA 1 NEGATIVO**** """

        # Se obtiene los valores de theta1 posibles.
        q1_2b = sp.atan2(-y3, -x3)
        # Se obtienen los valores de theta2 posibles.
        q2_1b = sp.pi - q2_1a
        q2_2b = sp.pi - q2_2a
        # Se obtienen los valores de theta3 posibles.
        # q3_1b = sp.atan2(z3 - d1 - a2 * sp.sin(q2_1b), sp.sqrt(x3**2 + y3**2) - a2 * sp.cos(q2_1b)) - q2_1b
        # q3_2b = sp.atan2(z3 - d1 - a2 * sp.sin(q2_2b), sp.sqrt(x3**2 + y3**2) - a2 * sp.cos(q2_2b)) - q2_2b
        q3_1b = -q3_1a
        q3_2b = -q3_2a

        # Se agregan los resultados de q1, q2 y q3 para el caso "B" a la matriz qs.
        solutions[4:8, 0] = q1_2b
        solutions[4:6, 1] = q2_1b
        solutions[6:8, 1] = q2_2b
        solutions[4:6, 2] = q3_1b
        solutions[6:8, 2] = q3_2b

        """
        **** DETERMINACIÓN DE q4 y q5 PARA TODOS LOS CASOS ****
        Se realiza un recorrido de la matriz "qs" que hasta este punto solo contiene la solución de q1, q2 y q3.
        Por medio de los for se recorre cada combinación posible de q1, q2, q3 y con ellas se obtiene
        el q4 y q5 que corresponde a esa combinación, y de esa forma se completa la configuración
        conformada por q1, ..., q5.
        """
        for j in range(1, 3):
            theta1 = solutions[(j - 1) * 4, 0]
            for k in range(1, 3):
                theta2 = solutions[(k - 1) * 2 + (j - 1) * 4, 1]
                theta3 = solutions[(k - 1) * 2 + (j - 1) * 4, 2]
                """
                Ahora, sabiendo que,
                    Tm0 = A1(q1)*A2(q2)*A3(q3)*A4(q4)*A5(q5)

                Se tiene,
                    inversa[ A1(q1)*A2(q2)*A3(q3) ] * Tm0 = A4(q4)*A5(q5)

                y como ya se conoce q1, q2 y q3 se calcula la matriz númerica R = inversa[ A1(q1)*A2(q2)*A3(q3) ] * Tm0
                Ahora R = A4(q4)*A5(q5)

                A partir de R se determinan los valores de theta4 y theta5 posibles sabiendo que de la cinemática
                directa del brazo robot y su descripción de D-H

                A4(q4)*A5(q5) = | -sin(q4)*cos(q5)   sin(q4)*sin(q5)  cos(q4)   0.344*cos(q4) |
                                |  cos(q4)*cos(q5)  -sin(q5)*cos(q4)  sin(q4)   0.344*sin(q4) |
                                |  sin(q5)           cos(q5)          0        -0.04          |
                                |  0                 0                0         1             |

                R13 = cos(q4), R23 = sin(q4) --> con atan2 se obtiene q4.
                R31 = sin(q5), R32 = cos(q5)  --> con atan2 se obtiene q5.
                """
                # Se calculan las matrices A1, A2 y A3 usando los parámetros DH correspondientes.
                A1 = get_t_from_dh(self.dh[0, 0], self.dh[0, 1], self.dh[0, 2], theta1)
                A2 = get_t_from_dh(self.dh[1, 0], self.dh[1, 1], self.dh[1, 2], theta2)
                A3 = get_t_from_dh(self.dh[2, 0], self.dh[2, 1], self.dh[2, 2], theta3)
                # Se calcula la matriz de transformación A31 = A1*A2*A3.
                A31 = A1*A2*A3
                # Se calcula R = inversa[ A1(q1)*A2(q2)*A3(q3) ] * Tm0.
                R = A31.inv() * tm0

                # Se obtienen los valores de theta4 posibles.
                q4_1 = sp.atan2(R[1, 2], R[0, 2])
                q4_2 = sp.atan2(-R[1, 2], -R[0, 2])
                # Se obtienen los valores de theta5 posibles.
                q5_1 = sp.atan2(R[2, 0], R[2, 1])
                q5_2 = sp.atan2(-R[2, 0], -R[2, 1])

                # Se agregan los resultados de q4 y q5 a la matriz de configuraciones qs.
                solutions[(k - 1) * 2 + (j - 1) * 4, 3] = q4_1
                solutions[(k - 1) * 2 + (j - 1) * 4, 4] = q5_1
                solutions[(k - 1) * 2 + (j - 1) * 4 + 1, 3] = q4_2
                solutions[(k - 1) * 2 + (j - 1) * 4 + 1, 4] = q5_2

        return solutions

    def get_tm0(self, system_0, system_m):
        """
        DESCRIPCIÓN:
        Se busca obtener la Tm0 que representa la pose que el manipulador final debe tener para poder
        ubicarse donde se desea recoger/soltar los cubitos que se identificarán en la banda transportadora.

            DATO: La pose que se desea para el manipulador final se indicará en coppeliaSim con un dummy
            llamado "mf". El cuál se moverá y orientara según la pose que se desea para el manipulador final.

        Para encontrar la Tm0 se recurirá a la ecuación aprendida en clase:
            Tm0 = Tw0 * Thw * (Thm)^(-1)
            Donde:
                Tm0 --> Pose del manipulador final respecto del sistema 0. SE OBTENDRÁ NUMÉRICAMENTE.
                Tw0 --> Matriz T que relaciona al sistema de trabajo w con el sistema 0.
                Thw --> Matriz T que relaciona al sistema de la herramienta (el cubo) con el sistema de trabajo w.
                Thm --> Matriz T que relaciona al sistema de la herramienta (el cubo) con el manipulador final.

        Para el caso de este brazo el sistema w coincidirá siempre con el sistema h del cubo por lo tanto la
        Thw será siempre la identidad, entonces, la ecuación anterior se reduce a:
            Cambiando nombre de sistema h por sistema c...

            Tm0 = Tc0 * (Tcm)^(-1)

        Las matrices Tc0 y Tcm se obtienen con simxGetObjectMatrix que da la posición x, y, z asi como la
        orientación respecto al sistema que se desee.

        :return Tmo: matriz que representa la pose del manipulador final.
        """
        # Se obtiene las matrices Tc0 y Tcm que se deben convertir con sp.Matrix a su forma de matriz.
        # tc0 = self.client.simxGetObjectMatrix(system_c, system_0, self.client.simxServiceCall())[1]
        # Tc0 = sp.Matrix([tc0[:4], tc0[4:8], tc0[8:12], [0, 0, 0, 1]])
        #
        # tcm = self.client.simxGetObjectMatrix(system_c, system_m, self.client.simxServiceCall())[1]
        # Tcm = sp.Matrix([tcm[:4], tcm[4:8], tcm[8:12], [0, 0, 0, 1]])

        tm0 = self.client.simxGetObjectMatrix(system_m, system_0, self.client.simxServiceCall())[1]
        Tm0 = sp.Matrix([tm0[:4], tm0[4:8], tm0[8:12], [0, 0, 0, 1]])

        # Se determina la Tm0 utilizando la ecuación planteada arriba.
        # Tm0 = Tc0 * Tcm.inv()

        return Tm0

