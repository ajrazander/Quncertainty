import sys
sys.path.append('../../')
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
from scipy import linalg as la
from tools.visualization import plot_histogram, plot_state
import csv
import time

# Build the quantum cirucit. We are going to build two circuits: one for
# error in Z the other for distrubane in Y
qp1 = QuantumProgram()
n = 3 #number of qubits and bits
q = qp1.create_quantum_register('q',n)
c = qp1.create_classical_register('c',n)
# quantum circuit for error in Z
ErrorZ = qp1.create_circuit('ErrorZ',[q],[c])
ErrorZ.x(q[2])
ErrorZ.measure(q[2],c[2])
ErrorZ.h(q[1])
ErrorZ.measure(q[1],c[1])
ErrorZ.h(q[0])
ErrorZ.z(q[0])
ErrorZ.measure(q[0],c[0])
# quantum circuit for distrubance in Y
DistY = qp1.create_circuit('DistY',[q],[c])
DistY.h(q[2])
DistY.sdg(q[2])
DistY.sdg(q[2])
DistY.h(q[2])
DistY.measure(q[2],c[2])
DistY.h(q[1])
DistY.sdg(q[1])
DistY.h(q[1])
DistY.measure(q[1],c[1])
DistY.h(q[0])
DistY.z(q[0])
DistY.sdg(q[0])
DistY.h(q[0])
DistY.measure(q[0],c[0])

# Execute the quantum circuits
circuits = ['ErrorZ','DistY']
filename = 'OzawaMeasurment.csv' #file where data will be exported
total_shots = 1024
Max_Iterations = 30 #max number of loops, or the loop will end if units/credits are below 3
count = 0
while count <= Max_Iterations::
    count += 1
    backend = 'ibmqx2'
    if Q_program.get_backend_status(backend)['available']:
        qp1.set_api(Qconfig.APItoken,Qconfig.config['url']) # set YOUR OWN APItoken and API url
        result = qp1.execute(circuits, backend, shots=total_shots, max_credits=3, wait=10, timeout=60)
        #print(result)
        #plot_histogram(result.get_counts('X'))
        #plot_histogram(result.get_counts('Y'))
        #plot_histogram(result.get_counts('Z'))
        
        errorZ = result.get_counts('ErrorZ')
        distY = result.get_counts('DistY')

        temp_EpX = 0
        temp_EmX = 0
        temp_DpX = 0
        temp_DmX = 0
        temp_Y = 0
        temp_Z = 0
        expect_Zz = 0
        expect_Zmx = 0
        expect_Zpx = 0
        expect_Yy = 0
        expect_Ypx = 0
        expect_Ymx = 0
        #turn probablities into expectation values
        for i,q in sorted(errorZ.items()):
            if i[-1] == '0':
                temp_EpX = temp_EpX - q
            elif i[-1] == '1':
                temp_EpX = temp_EpX + q
            if i[-2] == '0':
                temp_EmX = temp_EmX - q
            elif i[-2] == '1':
                temp_EmX = temp_EmX + q
            if i[-3] == '0':
                temp_Z = temp_Z - q
            elif i[-3] == '1':
                temp_Z = temp_Z + q
        expect_Zz = temp_Z/total_shots
        expect_Zmx = temp_EmX/total_shots
        expect_Zpx = temp_EpX/total_shots
        print(total_shots,expect_Zz,expect_Zmx,expect_Zpx)
        
        #turn probablities into expectation values
        for i,q in sorted(distY.items()):
            if i[-1] == '0':
                temp_DpX = temp_DpX - q
            elif i[-1] == '1':
                temp_DpX = temp_DpX + q
            if i[-2] == '0':
                temp_DmX = temp_DmX - q
            elif i[-2] == '1':
                temp_DmX = temp_DmX + q
            if i[-3] == '0':
                temp_Y = temp_Y - q
            elif i[-3] == '1':
                temp_Y = temp_Y + q
        expect_Yy = temp_Y/total_shots
        expect_Ymx = temp_DmX/total_shots
        expect_Ypx = temp_DpX/total_shots
        print(total_shots,expect_Yy,expect_Ymx,expect_Ypx)

        # Send data to csv file "filename"
        with open(filename, 'a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([total_shots,expect_Zz,expect_Zmx,expect_Zpx,expect_Yy,expect_Ymx,expect_Ypx])
            
        time.sleep(1) #wait one second(s). I think this is needed to reload credits
    else:
        print("ibmqx2 is not available")
print('DONE')
