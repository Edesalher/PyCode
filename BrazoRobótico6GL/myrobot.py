"""
*** CLASS TO CREATE THE ROBOTIC ARM AND CONTROL IT ***
Author: Edwing Alvarez
Date: October 29, 2020.

Denavit-Hartenberg description for the robotic arm with 6 degrees of freedom.
    a   |  alpha  |   d    |   theta
--------|---------|--------|-----------
   0    |  pi/2   |  d1    |    q1
   a2   |  0      |  0     |    q2
   a3   |  0      |  0     |    q3
   0    |  -pi/2  |  0     |    q4
   0    |  pi/2   |  0     |    q5
   0    |  0      |  d6    |    q6
"""

import sympy as sp
import numpy as np


def print_matrix(matrix):
    for m in range(len(matrix[:, 0])):
        print('[ ', end='')
        for n in range(len(matrix[0, :])):
            print(f'{matrix[m, n]} ', end='')
            if n < len(matrix[0, :]) - 1:
                print(', ', end='')
        print(' ]')
    print('\n')


def get_t_from_dh(a, alpha, d, theta):
    """
    DESCRIPTION:
    This function takes the Denavit-Hartenberg parameters to produce the corresponding
    transformation matrix.

    :param a:     Distance along x(i+1) to join the origin of system i with system i+1.
    :param alpha: Angle around x(i+1) by which z(i) must be rotated to align with z(i+1).
    :param d:     Distance along z(i) to join the origin of system i with system i+1.
    :param theta: Angle around z(i) by which x(i) need to be rotated to align with x(i+1).

    :return matrix: Transformation matrix based on the given parameters.
    """
    matrix = sp.Matrix(
        [[sp.cos(theta), -sp.sin(theta) * sp.cos(alpha), sp.sin(theta) * sp.sin(alpha), a * sp.cos(theta)],
         [sp.sin(theta), sp.cos(theta) * sp.cos(alpha), -sp.cos(theta) * sp.sin(alpha), a * sp.sin(theta)],
         [0, sp.sin(alpha), sp.cos(alpha), d],
         [0, 0, 0, 1]])
    return matrix


def euler_angles_zyz(R):
    """
    DESCRIPTION:
    This function calculates the Euler angles in representation of RzRyRz.

    In general, there are 2 solutions for R = Rz(phi)*Ry(theta)*Rz(psi). This function returns the solutions in a 2x3
    matrix. The first row contains the phi, theta, psi values when sin (theta) is positive. The second row contains
    the values corresponding to the case where sin (theta) is negative.

    :param R: Rotation matrix, if it is homogeneous only the sub-matrix corresponding to the rotation
              is considered.
    :return solution_zyz: 2x3 matrix that contains, in separate rows, the 2 solutions for phi, theta y psi that
                          make R = Rz(phi)*Ry(theta)*Rz(psi)
    """
    stheta = sp.sqrt(1 - R[2, 2]**2)

    # Solution with sin(theta) > 0.
    theta1 = sp.atan2(stheta, R[2, 2])
    phi1 = sp.atan2(R[1, 2], R[0, 2])
    psi1 = sp.atan2(R[2, 1], -R[2, 0])

    # Solution with sin(theta) < 0.
    theta2 = sp.atan2(-stheta, R[2, 2])
    phi2 = sp.atan2(-R[1, 2], -R[0, 2])
    psi2 = sp.atan2(-R[2, 1], R[2, 0])

    solution_zyz = sp.Matrix([[phi1, theta1, psi1],
                              [phi2, theta2, psi2]])
    return solution_zyz


class Robot:
    def __init__(self, joints, dh_matrix, client):
        # Variables of the robotic arm where the information of his joints and his D-H description is stored.
        self.joints = joints
        self.dh = dh_matrix
        # Variable of the robotic arm where the coppeliaSim client is stored to control it.
        self.client = client

    def move_joint(self, joint, angle):
        # The value of the angle is sent in radians.
        self.client.simxSetJointTargetPosition(joint, angle, self.client.simxServiceCall())

    def set_joints(self, list_of_joints, list_of_angles):
        # This function allows to move multiple joints and not do it one by one.
        for j in range(len(list_of_joints)):
            self.move_joint(list_of_joints[j], list_of_angles[j])

    def do_direct_kinematics(self):
        """
        DESCRIPTION:
        This function uses the table from the Denavit-Hartenberg description to produce the transformation
        matrix Tm0 that represents the final manipulator with respects to system 0.

        :return T: Transformation matrix Tm0.
        """
        # An identity matrix is prepared as the initial valor.
        To = sp.eye(4, 4)
        for m in range(len(self.dh[:, 0])):
            # The matrix corresponding to the chosen parameters a, alpha, d theta is calculated.
            A = get_t_from_dh(self.dh[m, 0], self.dh[m, 1], self.dh[m, 2], self.dh[m, 3])
            # The transformation matrix found is post-multiplied to the previous result.
            To = To * A
        T = sp.simplify(To)

        return T

    def do_inverse_kinematics(self, tm0):
        """
        DESCRIPTION:
        This function receives the table from the Denavit-Hartenberg description and the Tm0 which is the matrix
        that is known numerically and represents the pose that is desired for the final manipulator.

        :param tm0: Desired pose for the final manipulator. IT IS KNOWN NUMERICALLY.

        :return qs: 8x5 matrix containing the 8 possible solutions for the 5 angles q1, ..., q5.
        """
        # The values of a and d of interest are obtained.
        a2 = self.dh[1, 0]
        a3 = self.dh[2, 0]
        d1 = self.dh[0, 2]
        d6 = self.dh[5, 2]

        # The center of the spherical wrist is obtained with respect of the system 0.
        spherical_wrist_center = tm0 * sp.Matrix([[0, 0, -d6, 1]]).T
        xc = spherical_wrist_center[0]
        yc = spherical_wrist_center[1]
        zc = spherical_wrist_center[2]

        # The matrix "solutions" is prepared that will contain the 8 possible configurations of q1, ..., q5.
        solutions = np.zeros((8, 6))

        """ **** CASE "A" WITH theta1 POSITIVE **** """

        # The possible theta1 value is obtained.
        q1_1a = sp.atan2(yc, xc)
        # The possible theta3 values are obtained.
        cos_q3 = (xc**2 + yc**2 + (zc - d1)**2 - a2**2 - a3**2) / (2 * a2 * a3)
        q3_1a = sp.atan2(sp.sqrt(1 - cos_q3**2), cos_q3)
        q3_2a = sp.atan2(-sp.sqrt(1 - cos_q3**2), cos_q3)
        # The possible theta2 values are obtained.
        q2_1a = sp.atan2(zc - d1, sp.sqrt(xc**2 + yc**2)) - sp.atan2(a3 * sp.sin(q3_1a), a2 + a3 * sp.cos(q3_1a))
        q2_2a = sp.atan2(zc - d1, sp.sqrt(xc**2 + yc**2)) - sp.atan2(a3 * sp.sin(q3_2a), a2 + a3 * sp.cos(q3_2a))

        # The result of q1, q2 and q3 for case "A" are added to the solution matrix.
        solutions[0:4, 0] = q1_1a
        solutions[0:2, 1] = q2_1a
        solutions[2:4, 1] = q2_2a
        solutions[0:2, 2] = q3_1a
        solutions[2:4, 2] = q3_2a

        """ **** CASE "B" WITH theta1 NEGATIVE **** """

        # The possible theta1 value is obtained.
        q1_2b = sp.atan2(-yc, -xc)
        # The possible theta2 values are obtained.
        q2_1b = sp.pi - q2_1a
        q2_2b = sp.pi - q2_2a
        # The possible theta3 values are obtained.
        # q3_1b = sp.atan2(zc - d1 - a2 * sp.sin(q2_1b), sp.sqrt(xc**2 + yc**2) - a2 * sp.cos(q2_1b)) - q2_1b
        # q3_2b = sp.atan2(zc - d1 - a2 * sp.sin(q2_2b), sp.sqrt(xc**2 + yc**2) - a2 * sp.cos(q2_2b)) - q2_2b
        q3_1b = -q3_1a
        q3_2b = -q3_2a

        # The result of q1, q2 and q3 for case "B" are added to the solution matrix.
        solutions[4:8, 0] = q1_2b
        solutions[4:6, 1] = q2_1b
        solutions[6:8, 1] = q2_2b
        solutions[4:6, 2] = q3_1b
        solutions[6:8, 2] = q3_2b

        """ 
        **** DETERMINATION OF q4, q5 and q6 FOR THE ALL CASES ****
        A displacement is made on the "solution" matrix that up to this point only contains the solution for 
        q1, q2 and q3.
        Through the for loops, each possible combination (or row) of q1, q2 and q3 is traversed and with them the 
        solution for q4, q5 and q6 that corresponds to that combination (or row) is obtained, and in that way the
        configuration formed by q1, ..., q5 is completed.
        """
        for j in range(1, 3):
            theta1 = solutions[(j - 1) * 4, 0]
            for k in range(1, 3):
                theta2 = solutions[(k - 1) * 2 + (j - 1) * 4, 1]
                theta3 = solutions[(k - 1) * 2 + (j - 1) * 4, 2]
                """
                Now, knowing that,
                    Tm0 = A1(q1)*A2(q2)*A3(q3)*A4(q4)*A5(q5)*A6(q6)

                we can have,
                    [ A1(q1)*A2(q2)*A3(q3) ]^(-1) * Tm0 = A4(q4)*A5(q4)*A6(q6)

                And since the value of q1, q2 and q3 is known up to this point, the numerical matrix 
                R = [ A1(q1)*A2(q2)*A3(q3) ]^(-1) * Tm0 is calculated.
                
                Now, R = A4(q4)*A5(q5)*A6(q6)

                From R, the possible values of q4, q5 and q6 are determined using the solution for Euler angles ZYZ.
                
                fi+ = q4+ = Atan2(R13, R23)
                fi- = q4- = Atan2(-R13, -R23)
                
                theta+ = q5+ = Atan2(R33, sqrt(1-R33²))
                theta- = q5- = Atan2(R33, -sqrt(1-R33²))
                
                psi+ = q6+ = Atan2(-R31, R32)
                psi- = q6- = Atan2(R31, -R32)
                """
                # The A1, A2 and A3 matrix are calculated using the corresponding parameters from the DH description.
                A1 = get_t_from_dh(0, sp.pi/2, d1, theta1)
                A2 = get_t_from_dh(a2, 0, 0, theta2)
                A3 = get_t_from_dh(a3, 0, 0, theta3)
                # The A31 = A1*A2*A3 matrix is calculated.
                A31 = A1*A2*A3
                # R = [ A1(q1)*A2(q2)*A3(q3) ]^(-1) * Tm0 is calculated.
                R = A31.inv() * tm0

                # The possible theta4, theta5 and theta6 values are obtained using the solution for Euler angles ZYZ.
                Azyz = euler_angles_zyz(R)

                # The result of q4, q5 and q6 are added to the solution matrix.
                solutions[(k - 1) * 2 + (j - 1) * 4, 3] = Azyz[0, 0]
                solutions[(k - 1) * 2 + (j - 1) * 4, 4] = Azyz[0, 1]
                solutions[(k - 1) * 2 + (j - 1) * 4, 5] = Azyz[0, 2]

                solutions[(k - 1) * 2 + (j - 1) * 4 + 1, 3] = Azyz[1, 0]
                solutions[(k - 1) * 2 + (j - 1) * 4 + 1, 4] = Azyz[1, 1]
                solutions[(k - 1) * 2 + (j - 1) * 4 + 1, 5] = Azyz[1, 2]

        return solutions

    def get_tm0(self, system_0, system_w, system_m, system_h):
        """
        DESCRIPTION:
        This function allows to obtain the Tm0 that represents the pose that the final manipulator must have
        to be located where we want.

            FACT: The desired pose for the final manipulator will be indicated in coppeliaSim with a dummy
                  called "mf". This dummy will move and orient according to the pose that is desired for the
                  final manipulator.

        To find the Tm0 we will use the equation learned in class.
            Tm0 = Tw0 * Thw * (Thm)^(-1)

                Tm0 --> Pose of the final manipulator with respect to system 0. IT IS KNOWN NUMERICALLY.
                Tw0 --> Matrix T that relates the work system w with the system 0.
                Thw --> Matrix T that relates the system of the tool h with the work system w.
                Thm --> Matrix T that relates the system of the tool h with the final manipulator.

        The matrices Tw0, Thw and Thm are obtained with simxGetObjectMatrix that return the x, y, z position and
        the orientation with respect the desired systey.

        :return Tmo: Matrix that represents the pose of the final manipulator.
        """
        # The matrices Tw0, Thw and Thm are obtained and they must be converted with sp.Matrix to their matrix form.
        tw0 = self.client.simxGetObjectMatrix(system_w, system_0, self.client.simxServiceCall())[1]
        Tw0 = sp.Matrix([tw0[:4], tw0[4:8], tw0[8:12], [0, 0, 0, 1]])

        thw = self.client.simxGetObjectMatrix(system_h, system_w, self.client.simxServiceCall())[1]
        Thw = sp.Matrix([thw[:4], thw[4:8], thw[8:12], [0, 0, 0, 1]])

        thm = self.client.simxGetObjectMatrix(system_h, system_m, self.client.simxServiceCall())[1]
        Thm = sp.Matrix([thm[:4], thm[4:8], thm[8:12], [0, 0, 0, 1]])

        # The Tm0 is determined using the equation shown above.
        Tm0 = Tw0 * Thw * Thm.inv()

        return Tm0

