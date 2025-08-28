# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:04:59 2024

@author: Mieszko Ferens

Script with classes and functions to simulate a QKD key exchange using BB84.
"""

import argparse
import pandas as pd
from pathlib import Path

import numpy as np

class Logger():
    def __init__(self):
        self.log = ''
    def log_tx(self, n_bits):
        self.log += "Transmitting " + str(n_bits) + " bits on quantum channel...OK\n"
    def log_rx(self, n_bits):
        self.log += "Receiving " + str(n_bits) + " bits from quantum channel...OK\n"
    def log_eavesdropper_detection(self, error_rate, detected):
        self.log += ("Performing eavesdropper check...\n" + 
                     " - Measured error rate is " + str(error_rate) + "%...")
        if(detected):
            self.log += "\n -- Eavesdropper detected! Abort.\n"
        else:
            self.log += "OK\n"
    def log_drop_detection_bits(self):
        self.log += "Dropping error measurement bits...OK\n"
    def log_ECC(self, n_bits):
        self.log += ("Performing error correction...\n" +
                     " - Sharing polarization bases...OK\n" +
                     " - Discarding erroneous bits...OK\n" +
                     " - Executing ECC...\n" +
                     " -- No errors found...OK\n" +
                     str(n_bits) + " shared secret bits available...OK\n")
    def log_key_generation(self, n_keys, n_efficient_bits, key_len, hashed):
        if(hashed):
            self.log += "Generating privacy amplified keys (hashing)...\n"
        else:
            self.log += "Generating direct keys (no hashing)...\n"
        self.log += " - " + str(n_efficient_bits) + " efficient bits available...OK\n"
        self.log += " - " + str(n_keys) + " keys of " + str(key_len) + " bits were generated...OK\n"

class Q_bit():
    def __init__(self, bit, base, seed=0):
        # Define the RNG
        self.rng = np.random.default_rng(seed=seed)
        # Define diagonal base transformation matrix
        self.H = (1/np.sqrt(2))*np.matrix([[1,1],[1,-1]])
        # Initialize quantum state
        if(bit):
            self.state = np.matrix([[0],[1]])
        else:
            self.state = np.matrix([[1],[0]])
        if(base):
            self.state = self.H*self.state
    def measure(self, base):
        # Measure the value of the quantum state
        if(base):
            self.state = self.H*self.state
        # If the base is correct the first term will be 1 or 0 (x10**6),
        # 0.5 otherwise leading to a random measurement
        if(np.power(np.matrix([1,0])*self.state, 2)*10**6 >
           self.rng.integers(10**6)):
            return 0
        else:
            return 1

def quantum_tx(tx_bits, bases):
    Q_bits = []
    for i in range(len(tx_bits)):
        Q_bits.append(Q_bit(tx_bits[i], bases[i]))
    return Q_bits

def quantum_rx(Q_bits, bases):
    bits=[]
    for i in range(len(Q_bits)):
        bits.append(Q_bits[i].measure(bases[i]))
    return bits

def main():
    
    # Parse arguments (bools are converted to int = {0,1} to prevent issues)
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=str, default="./Results/")
    parser.add_argument("--seed", type=int, default=0, help="Random seed.")
    parser.add_argument("--verbose", type=int, default=1)
    parser.add_argument("--n-tx-bits", type=int, default=100000,
                        help="Number of data bits to transmit.")
    parser.add_argument("--eavesdropper", type=int, default=0,
                        help="Whether an eavesdropper is present.")
    parser.add_argument("--eavesdropper-check", type=int, default=1,
                        help="Whether to perform eavesdropper detection.")
    parser.add_argument("--n-check-bits", type=int, default=20000,
                        help="The number of bits used to detect the " +
                        "eavesdropper.")
    parser.add_argument("--expected-error", type=float, default=0.28,
                        help="The acceptable max error rate for the " +
                        "communication on the quantum channel. This should " +
                        "include polarization base mismatch.")
    parser.add_argument("--drop-check", type=int, default=1,
                        help="Whether to drop the eavesdropper check bits.")
    parser.add_argument("--key-len", type=int, default=4096,
                        help="Length of generated key.")
    parser.add_argument("--hashed-key", type=int, default=1,
                        help="Whether to hash secret bits to generate the " +
                        "final keys.")
    parser.add_argument("--hash-ratio", type=int, default=3,
                        help="The input-output ratio of bits to the hash " +
                        "function.")
    args = parser.parse_args()
    
    # Set up the RNG
    rng = np.random.default_rng(seed=args.seed)
    
    # Generate the number of transmission bits randomly
    tx_bits = rng.integers(2, size=(args.n_tx_bits,))
    
    # Check that QKD session is possible with current parameters
    if(args.eavesdropper_check == True and args.hashed_key == True):
        assert len(tx_bits) >= args.n_check_bits + args.key_len*args.hash_ratio, (
            "Not enough tx bits to check for Eavesdropper and generate one " +
            "key. Ensure that (int(tx_bits) OR len(tx_bits)) >= n_check_bits " +
            "+ key_len*hash_ratio, or remove eavesdropper detection " +
            "(Eve_check = False) or privacy amplification (hashed_key = " +
            "False).")
    elif(args.eavesdropper_check == True and args.hashed_key == False):
        assert len(tx_bits) >= args.n_check_bits + args.key_len, (
            "Not enough tx bits to check for Eavesdropper and generate one " +
            "key. Ensure that (int(tx_bits) OR len(tx_bits)) >= n_check_bits " +
            "+ key_len, or remove eavesdropper detection (Eve_check = False).")
    elif(args.eavesdropper_check == False and args.hashed_key == True):
        assert len(tx_bits) >= args.key_len*args.hash_ratio, (
            "Not enough tx bits to generate one key. Ensure that " +
            "(int(tx_bits) OR len(tx_bits)) >= key_len*hash_ratio, or " +
            "remove privacy amplification (hashed_key = False).")
    else:
        assert len(tx_bits) >= args.key_len, (
            "Not enough tx bits to generate one key. Ensure that " +
            "len(tx_bits) >= key_len.")
    
    # Set up the logger
    logger = Logger()
    
    # Generate random TX and RX polarization bases
    b_Alice = rng.integers(2, size=(len(tx_bits),))
    b_Bob = rng.integers(2, size=(len(tx_bits),))
    if(args.eavesdropper):
        b_Eve = rng.integers(2, size=(len(tx_bits),))
    
    # Transmit qubits through quantum channel
    Q_bits = quantum_tx(tx_bits, b_Alice)
    logger.log_tx(len(tx_bits))
    
    # Eavesdrop (intersept) qubits in quantum channel
    if(args.eavesdropper):
        bits = quantum_rx(Q_bits, b_Eve)
        Q_bits = quantum_tx(bits, b_Eve)
    
    # Receive qubits through quantum channel
    bits = np.array(quantum_rx(Q_bits, b_Bob))
    logger.log_rx(len(bits))
    
    # Check error rate (eavesdropper detection)
    if(args.eavesdropper_check):
        error_rate = np.count_nonzero(
            tx_bits[:args.n_check_bits] - bits[:args.n_check_bits])/args.n_check_bits
        detected = error_rate > args.expected_error
        logger.log_eavesdropper_detection(round(error_rate*100, 2), detected)
        if(detected):
            if(args.verbose):
                print(logger.log, end='')
            return
        if(args.drop_check):
            final_bits = bits[args.n_check_bits:]
            final_b_Alice = b_Alice[args.n_check_bits:]
            final_b_Bob = b_Bob[args.n_check_bits:]
            logger.log_drop_detection_bits()
        else:
            final_bits = bits
            final_b_Alice = b_Alice
            final_b_Bob = b_Bob
    
    # Error correction
    # - Drop bits with different polarization bases
    final_bits = [final_bits[i] for i in range(len(final_b_Alice)) if(final_b_Alice[i] == final_b_Bob[i])]
    # Simulation assumes error free transmission (except for quantum channel tampering)
    logger.log_ECC(len(final_bits))
    
    # Generate key (privacy amplification)
    if(args.hashed_key == True):
        n_efficient_bits = int(len(final_bits)/args.hash_ratio)
        n_keys = int((len(final_bits)/args.hash_ratio)/args.key_len)
    else:
        n_keys = int(len(final_bits)/args.key_len)
        n_efficient_bits = len(final_bits)
    logger.log_key_generation(
        n_keys, n_efficient_bits, args.key_len, args.hashed_key)
    
    if(args.verbose):
        print(logger.log, end='')
    
    # Log data into csv format
    data = pd.DataFrame({"seed": [args.seed],
                         "n_tx_bits": [args.n_tx_bits],
                         "eavesdropper": [args.eavesdropper],
                         "eavesdropper_check": [args.eavesdropper_check],
                         "check_bits": [args.check_bits],
                         "expected_error": [args.expected_error],
                         "drop_check": [args.drop_check],
                         "key_len": [args.key_len],
                         "hashed_key": [args.hashed_key],
                         "hash_ratio": [args.hash_ratio],
                         "n_final_bits": [len(final_bits)],
                         "n_efficient_bits": [n_efficient_bits],
                         "n_keys": [n_keys]})
    filepath = Path(args.outdir + "out_QKD_protocol_sim.csv")
    if(filepath.is_file()):
        data.to_csv(filepath, header=False, index=False, mode='a')
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(filepath, header=True, index=False, mode='a')


if(__name__ == "__main__"):
    main()

