# PU-QKD

The Physically Unclonable Quantum Key Distribution (PU-QKD) attempts to leverage hardware-bound unique identifiers via PUFs to provide authentication to QKD protocols.
Additionally, performance is enhanced through the replacement of post-processing steps with encoding of the data bits string.

This repository includes two scripts for theoretically and experimentally (simulation) evaluating the performance in terms of "usable bits", i.e., bits that can be used as key material, of traditional QKD and PU-QKD.

Additionally, code to run Machine Learning (ML) modeling attacks on PUFs integrated in a PU-QKD system are included.
Two algorithms using Multi-Layer Perceptron (MLP) to attack integrated XOR PUFs in PU-QKD have been implemented:
 - Random guessing of data bits to decode PUF responses
 - Random guessing of PUF responses based on its bias

## Dependencies

The code was tested using the following:
 - Python 3.8
 - pypuf 3.3.1
 - numpy 1.23.1
 - tensorflow 2.4.4
 - pandas 1.5.1

## How to use

### Performance evaluation

To test the performance of QKD or PU-QKD use one of the following (use `--help` for a list of arguments):
```
python3 QKD_sim.py
Python3 QKD_theoretical.py
```
You should use the input arguments to configure the system towards QKD or PU-QKD. Specifically, in `QKD_sim.py` you should set `--drop-check=0` and `--hashed-key=0` for PU-QKD, and viceversa for QKD. On the other hand, in `QKD_theoretical` you simply set the post-processing parameters to the desired values.

### Security evaluation

To run single experiments for modeling attempts on PU-QKD use one of the following (use `--help` for a list of arguments):
```
python3 PUQKD_random_XOR_test.py
python3 PUQKD_bias_XOR_test.py
```
Both algorithms have shown to only achive accuracies bound by the bias of the PUF.

Additionally, you may run the the evaluation script which can be used to run further operations on the bit strings generated in the system and evaluate their bias:
```
python3 PUQKD_evaluation_test.py
```

## How to cite

M. Ferens, "PU-QKD: Authentication in Quantum Key Distribution with Classical Physical Unclonable Functions," *IEEE Global Communications Conference (GLOBECOM) 2025*.

## References

1. N. Wisiol, C. Gräbnitz, C. Mühl, B. Zengin, T. Soroceanu, N. Pirnay, K. T. Mursi, and A. Baliuka, "pypuf: Cryptanalysis of Physically Unclonable Functions," 2021, version v2. [Online]. Available: https://doi.org/10.5281/zenodo.3901410
