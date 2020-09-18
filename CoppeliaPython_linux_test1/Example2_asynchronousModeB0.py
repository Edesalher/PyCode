import b0RemoteApi
import time

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:
    joint = client.simxGetObjectHandle('Revolute_joint', client.simxServiceCall())

    client.simxStartSimulation(client.simxDefaultPublisher())
    start_time = time.time()
    while time.time() < start_time + 5:
        client.simxSetJointTargetVelocity(joint[1], 0.8, client.simxServiceCall())
    client.simxStopSimulation(client.simxDefaultPublisher())
