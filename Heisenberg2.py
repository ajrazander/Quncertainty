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

# Build the quantum cirucit. We are going to build three circuits: one for the X expectation value, one
# for the Y expectation value, and one for the Z exepctation value
Q_program = QuantumProgram()
n = 1 #number of qubits and bits
q = Q_program.create_quantum_register('q',n)
c = Q_program.create_classical_register('c',n)

# quantum circuit for X expectation value
X = Q_program.create_circuit('X',[q],[c])
X.h(q[0])
X.measure(q[0],c[0])

# quantum circuit for Y expectation value
Y = Q_program.create_circuit('Y',[q],[c])
Y.sdg(q[0])
Y.h(q[0])
Y.measure(q[0],c[0])

# quantum circuit for Z expectation value
Z = Q_program.create_circuit('Z',[q],[c])
Z.measure(q[0],c[0])


# Execute the quantum circuit 
filename = 'heisenbergTestSameQubit.csv' #file where your data will be saved to
circuits = ['X','Y','Z']
total_shots = 1024
Max_Iterations = 30 #max number of loops, or the loop will error if units/credits are below 3
count = 0
while count <= Max_Iterations:
    count += 1
    #check that ibmqx2 is available
    backend = 'ibmqx2'
    if Q_program.get_backend_status(backend)['available']:
        Q_program.set_api(Qconfig.APItoken,Qconfig.config['url']) # set APItoken and API url to YOUR OWN token and url
        result = Q_program.execute(circuits, backend, shots=total_shots, max_credits=3, wait=10, timeout=60)
        #print(result)
        #plot_histogram(result.get_counts('X'))
        #plot_histogram(result.get_counts('Y'))
        #plot_histogram(result.get_counts('Z'))
    
        resX = result.get_counts('X')
        resY = result.get_counts('Y')
        resZ = result.get_counts('Z')
    
        expect_X = (resX['00001']-resX['00000'])/total_shots
        expect_Y = (resY['00001']-resY['00000'])/total_shots
        try:
            expect_Z = (resZ['00001']-resZ['00000'])/total_shots
        except KeyError: #resZ['0001'] may not exist sometimes
            expect_Z = -resZ['00000']/total_shots
       
        print(total_shots,expect_X,expect_Y,expect_Z)

        # Send data to csv file "filename"
        with open(filename, 'a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([expect_X,expect_Y,expect_Z,total_shots])
        
        time.sleep(1) #wait one second(s)
    else:
        print('ibmqx2 is not available')
print('DONE')
