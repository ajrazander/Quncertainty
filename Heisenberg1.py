# Import QISKit packages, matlab plotting options, a file exporter, and time

import sys
sys.path.append('../../')
from qiskit import QuantumCircuit, QuantumProgram
import Qconfig

# useful additional packages 
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
from scipy import linalg as la

# import state tomography functions
from tools.visualization import plot_histogram, plot_state

# import file exporter
import csv

import time


# Building the quantum cirucit.
qp = QuantumProgram()
n = 3 #number of qubits and bits
q = qp.create_quantum_register('q', n)
c = qp.create_classical_register('c', n)
circuit = qp.create_circuit('Heisenberg', [q], [c])

#Implement gates to circuit
circuit.h(q[0])
circuit.sdg(q[1])
circuit.h(q[1])
#do nothing to qubit 2
circuit.measure(q[0], c[0])
circuit.measure(q[1], c[1])
circuit.measure(q[2], c[2])

# Execute circuit

filename = 'heisenbergTest.csv' #file where data will be exported to
total_shots = 1024
Max_Iterations = 40 #max number of loops, or the loop will end if my units/credits is below 3
count = 0
while count <= Max_Iterations:
    count += 1
    # you may need to check that ibmqx2 is available (the line below will tell you what is available)
    # qp.available_backends()
    backend = 'ibmqx2'
    if qp.get_backend_status(backend)['available']:
        qp.set_api(Qconfig.APItoken,Qconfig.config['url']) # set APItoken and API url, you will need to put in YOUR OWN token and url
        circuits = ['Heisenberg']  # Group of circuits to execute
        out = qp.execute(circuits, backend, shots=total_shots, max_credits=3, wait=5, timeout=60)
        #print(out)
        #plot_histogram(out.get_counts('Heisenberg')) #optional historgram plot of results
        
        # process results from bits (i.e. 0,1) to expectation values.
        res = out.get_counts('Heisenberg')
        temp_X = 0
        temp_Y = 0
        temp_Z = 0
        #turn probablities of qubits into expectation values
        for i,q in sorted(res.items()):
            # print(i,q)
            # 0 has an eigenvalue of -1 and 1 has an eigenvalue of 1 in pauli matrix representation
            if i[-1] == '0':
                temp_X = temp_X - q
            elif i[-1] == '1':
                temp_X = temp_X + q
            if i[-2] == '0':
                temp_Y = temp_Y - q
            elif i[-2] == '1':
                temp_Y = temp_Y + q
            if i[-3] == '0':
                temp_Z = temp_Z - q
            elif i[-3] == '1':
                temp_Z = temp_Z + q
        expect_X = temp_X/total_shots
        expect_Y = temp_Y/total_shots
        expect_Z = temp_Z/total_shots
        print(total_shots,expect_X,expect_Y,expect_Z)

        #appends data to file "filename"
        with open(filename, 'a',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([expect_X,expect_Y,expect_Z,total_shots])
                
            time.sleep(1) #wait one second(s) needed to reload credits (I think)
    else:
        print('ibmqx2 is not available')
print('DONE')
