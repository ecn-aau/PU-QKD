# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:36:52 2024

@author: Mieszko Ferens

Script to theoretically calculate a QKD key exchange using BB84.
"""

import argparse
import pandas as pd
from pathlib import Path

def main():
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=str, default="./Results/")
    parser.add_argument("--n-tx-bits", type=int, default=100000,
                        help="Number of data bits to transmit.")
    parser.add_argument("--n-check-bits", type=int, default=20000,
                        help="The number of bits used to detect the " +
                        "eavesdropper.")
    parser.add_argument("--key-len", type=int, default=4096,
                        help="Length of generated key.")
    parser.add_argument("--hash-ratio", type=int, default=3,
                        help="The input-output ratio of bits to the hash " +
                        "function.")
    parser.add_argument("--QKD-rate", type=float, default=1,
                        help="The pulse rate of the underling QKD system in " +
                        "Gbps.")
    parser.add_argument("--PUF-rate", type=float, default=0.1,
                        help="The output rate of the physically integrated " +
                        "PUF in Gbps.")
    args = parser.parse_args()
    
    # Calculate ratio of tx bits to check bits
    k = args.n_tx_bits/args.n_check_bits
    
    # Assuming no eavesdropper and no tx errors, calculate the number of usable bits
    # - For PUQKD (no post-processing loss):
    n_PUQKD_bits = int((args.n_tx_bits*(args.PUF_rate/args.QKD_rate))/2)
    n_PUQKD_keys = int(n_PUQKD_bits/args.key_len)
    # - For QKD (with post processing loss):
    n_QKD_bits = int((1/args.hash_ratio) * ((k - 1)/k) * (args.n_tx_bits/2))
    n_QKD_keys = int(n_QKD_bits/args.key_len)
    
    # Log data into csv format
    data = pd.DataFrame({"n_tx_bits": [args.n_tx_bits],
                         "n_check_bits": [args.n_check_bits],
                         "key_len": [args.key_len],
                         "hash_ratio": [args.hash_ratio],
                         "n_QKD_bits": [n_QKD_bits],
                         "n_QKD_keys": [n_QKD_keys],
                         "n_PUQKD_bits": [n_PUQKD_bits],
                         "n_PUQKD_keys": [n_PUQKD_keys]})
    filepath = Path(args.outdir + "out_QKD_protocol_theoretical.csv")
    if(filepath.is_file()):
        data.to_csv(filepath, header=False, index=False, mode='a')
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(filepath, header=True, index=False, mode='a')


if(__name__ == "__main__"):
    main()

