# PU-QKD

Code to run Machine Learning (ML) modeling attacks on PUFs integrated in a PU-QKD system.

Two algorithms using Multi-Layer Perceptron (MLP) to attack integrated XOR PUFs in PU-QKD have been implemented:
 - Random guessing of data bits to decode PUF responses
 - Random guessing of PUF responses based on its bias

## Hot to cite

M. Ferens, "PU-QKD: Authentication in Quantum Key Distribution with Classical Physical Unclonable Functions," 2024, *unpublished*.

## Dependencies

The code was tested using the following:
 - Python 3.8
 - pypuf 3.3.1
 - numpy 1.23.1
 - tensorflow 2.4.4
 - pandas 1.5.1

## How to use

To run single experiments use on of the following (use `--help` for a list of arguments):
```
python3 PUQKD_random_XOR_test.py
python3 PUQKD_bias_XOR_test.py
```
Both algorithms have shown to only achive accuracies bound by the bias of the PUF.

## References

1. N. Wisiol, C. Gräbnitz, C. Mühl, B. Zengin, T. Soroceanu, N. Pirnay, K. T. Mursi, and A. Baliuka, "pypuf: Cryptanalysis of Physically Unclonable Functions," 2021, version v2. [Online]. Available: https://doi.org/10.5281/zenodo.3901410
