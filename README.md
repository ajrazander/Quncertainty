# Quncertainty
This code uses IBM's QISKit and other packages to validate Heisenberg uncertainty and measurement uncertainty in IBM's "ibmqx2" using pauli matrices. The scripts are designed to gather data and export it csv files. From there, I import the data files to an excel spreadsheet to do the final analysis.

## Heisenberg Uncertainty
In 1927, Heisenberg published his paper on what we now call Heisenberg uncertainty principle. The principle was developed further by Robertson to a more general level As stated above, this script gathers data, exports data to a file, and the final analysis is done in an excel spreadsheet.

### The approach
We need to find the expectation value of X, Y, and Z. There are two approaches: We can either find each expectation value on the same qubit (but on different runs), or on different bits in the same run. Fundamentaly, we would like to measure the qubit, then operator on it, and measure it again. IBM does not offer a multiple measurment, same run scheme. Between the two approaches previously stated the latter is less robust because different qubits have different gate and readout errors. At least operatoring on the same qubit will give consistent errors between calibrations.

### The script
There are actually two scripts--each testing the two different approaches. The first executes the least robust approach, and the second executes the more robust method.
The script is acts in two parts: first, build quantum circuits, and second execute the circuit and find the desired expectation values. 

## Measurement Uncertainty
Ozawa has promoted the idea of uncertainty in measuring quantum systems. This scipt was made to test an inequality describing this measurement uncertainty derived by Branciard (and later updated by Oawa). The scipt will build two quantum circuits: one to measure error(Z), the other to measure disturbance(Y). See https://arxiv.org/pdf/1511.03462.pdf for details on methods and theory behind measurement uncertainty.

### The approach
We need to find the expectation value of Y and Z with six differently prepared states. There are two approaches: they are the same ones listed under "Heisenberg Uncertainty" under "the approach." Equations, methods, and thoery on measurement uncertainty relations by doing a literary search on "measurement uncertainty relations." Ozawa has published the most, but also look into Branciard and Busch's work to get more information and greater context to the idea of measurement uncertainty.

### The script
There is only one script for Measurement Uncertainty (opposed to the two for Heisenberg Uncertainty). I only used the more robust method.
The script is acts in two parts: first, build quantum circuits, and second execute the circuit and find the desired expectation values.
