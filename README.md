# Quncertainty
This code usies IBM's QISKit and other packages to validate Heisenberg uncertainty and measurement uncertainty in IBM's "ibmqx2." The scripts are designed to gather data and export it csv files. From there, I import the data files to an excel spreadsheet to do the final analysis.

## Heisenberg Uncertainty
In 1927 Heisenberg published his paper on what we call Heisenberg uncertainty. The idea was developed further by Robertson to a more general equation. This script gathers data and exports to a file. As stated above, the final analysis is done in an excel spreadsheet.


## Measurement Uncertainty
Ozawa has promoted the idea of uncertainty in measuring quantum systems. This code will build two quantum circuits: one to measure error(Z), the other to measure disturbance(Y). See https://arxiv.org/pdf/1511.03462.pdf for details on equations, methods, and theory.
