#! /usr/bin/env python3

"""
Pipeline for ...
"""
print(__doc__)
from scripts.modules import *
import argparse

parser = argparse.ArgumentParser(description='Pipeline to Score Data')
parser.add_argument('--ann_model', type=str, required=True)
args = parser.parse_args()

initial_preprocessing()
handle_anomalies()
window()
scale()
score_ann(args.ann_model)
score_rf('rf_model')
expand_predictions()
rename_scores()
remap_names()
zdb_preprocess()
zdb_conversion()
zdb_remap()
