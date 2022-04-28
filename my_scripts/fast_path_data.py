# Plot # of cycles spent on fast path calls, % speedup on fast path calls.

import argparse
import sqlite3
import numpy as np
import sys
import os.path
sys.path.append("../scripts")
from db_common import *


def plot_stacked_speedup(db):
	'''
	Get data from the database for comparing average # of cycles / average % speedup for fast-path malloc() calls.
	'''
	opts = ["baseline", "realistic"]

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	bmarks, _ = get_ubenchmarks(db)
	runs = get_all_runs(db)

	# All total cycles across runs in a 3D array.
	all_runs_avg_call_length = np.zeros((len(runs), len(opts), len(bmarks)))
	for run in runs:
		avg_call_length = [[] for opt in opts]
		bmk_labels = []
		for bmark in bmarks:
		    # print "Getting data for", bmark
		    bmk_labels.append(bmark)
		    for i, opt in enumerate(opts):
		        data, num_calls = get_total_cycles_data(
		            cursor, bmark, malloc_funcs + free_funcs, opt, run,
		            fastpath_only=True)
		        # print num_calls
		        if num_calls > 0:
		            avg_call_length[i].append(data / num_calls)
		        else:
		            avg_call_length[i].append(float("NaN"))

	avg_call_length = np.array(avg_call_length)
	all_runs_avg_call_length[run, :, :] = avg_call_length

	# Compute mean and std call length
	mean_cycles = np.nanmean(all_runs_avg_call_length, axis=0)
	mean_std = np.nanstd(all_runs_avg_call_length, axis=0) # all std. devs. will be 0 if there is only 1 run

	print mean_cycles
	print mean_std

	conn.close()

def plot_hit_rates(db):
	'''
	Get data from database for comparing malloc cache hit rates 
	'''

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	bmarks, _ = get_ubenchmarks(db)
	cache_sizes = get_cache_sizes(cursor)
	runs = get_all_runs(db)

	baseline = "baseline"
	realistic = "realistic"
	stats = ["size_hits", "size_misses", "head_hits", "head_misses"]

	# TODO
	bmark_labels = []
    all_data = []
    all_run_size = np.zeros((len(runs), len(cache_sizes), len(bmarks)))
    all_run_head = np.zeros((len(runs), len(cache_sizes), len(bmarks)))

    # Collect all data across all runs.
    print "Collecting data for all realistic speedups."
    for run in runs:
        all_size_data = []
        all_head_data = []
        for size in cache_sizes:
            bmark_size_data = []
            bmark_head_data = []
            for bmark in bmarks:
                # print "Getting data for", bmark
                bmark_labels.append(bmark[7:])
                data = get_sim_stats(cursor, stats, bmark, realistic, run, cache_size=size)
                size_hit_rate = 100*float(data[0])/(data[0] + data[1])
                head_hit_rate = 100*float(data[2])/(data[2] + data[3])
                bmark_size_data.append(size_hit_rate)
                bmark_head_data.append(head_hit_rate)
            all_size_data.append(bmark_size_data)
            all_head_data.append(bmark_head_data)
        all_run_size[run, :] = np.array(all_size_data)
        all_run_head[run, :] = np.array(all_head_data)

    mean_size_data = np.mean(all_run_size, axis=0).astype(float)
    mean_head_data = np.mean(all_run_head, axis=0).astype(float)
    print mean_size_data
    print mean_head_data
    std_size = np.std(all_run_size, axis=0).astype(float)
    std_head = np.std(all_run_head, axis=0).astype(float)

	conn.close()

def plot_cache_size_sweep(db):
	'''
	Get data from database for comparing Mallacc performance (avg. # of cycles) for each cache size.
	'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        choices=["speedup",
                                 "cache-sweep",
                                 "hit-rates"])
    parser.add_argument("--db", help="SQLite3 DB.")
    args = parser.parse_args()

    if args.mode == "speedup":
        plot_stacked_speedup(args.db)
    elif args.mode == "hit-rates":
        pass
    elif args.mode == "cache-sweep":
        pass


if __name__ == "__main__":
    main()
