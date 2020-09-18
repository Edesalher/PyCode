import b0RemoteApi
import time

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi') as client:
    client.doNextStep = True

    def simulation_step_started(msg):
        sim_time = msg[1][b'simulationTime']
        print('Simulation step started. Simulation time: ', sim_time)

    def simulation_step_done(msg):
        sim_time = msg[1][b'simulationTime']
        print('Simulation step done. Simulation time: ', sim_time)
        client.doNextStep = True

    client.simxSynchronous(True)
    client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulation_step_started))
    client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulation_step_done))

    joint = client.simxGetObjectHandle('Revolute_joint', client.simxServiceCall())

    client.simxStartSimulation(client.simxDefaultPublisher())

    startTime = time.time()
    while time.time() < startTime + 5:
        if client.doNextStep:
            client.doNextStep = False
            client.simxSetJointTargetVelocity(joint[1], 0.8, client.simxDefaultPublisher())
            client.simxSynchronousTrigger()
        else:
            client.simxSpinOnce()

    client.simxStopSimulation(client.simxDefaultPublisher())
