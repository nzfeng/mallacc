# My own script to help plot profiling data, since the original is a mess and contains stuff we don't need + produces 
# ugly plots.
# Final plots will show the distribution of # of cycles it takes for each malloc() or free() call.
# This script actually just extracts data from a *.prof.* file to copy-paste into Mathematica, since it's easier to 
# generate good-looking plots in Mathematica than in Matplotlib.

import argparse

def read_prof_file(filepath):
	'''
	Read the data from a *.prof.* file, which contains # of cycles for each call during the microbenchmark.
	The filename is of the form [benchmark name].prof.[0.fid] where fid represents the function being measured.
	0.0 = tc_malloc, 0.1 = tc_free
	'''

	# Filepath will initially be something like <../../malloc_out/ubench.gauss/realistic/0/ubench.gauss.prof.0.0>
	directories = filepath.split("/") 
	# Get the filename, which will be something like <ubench.gauss.prof.0.0>
	filename = directories[-1]

	# Read from this file, and print out a list ready to be copy-pasted into my Mathematica template.
	f = open(filepath, "r")
	data = f.readlines()
	f.close()
	# Each element in data is a string with an attached newline character; need to convert to an int
	data = [int(item.strip("\n")) for item in data]
	# Output this to a file.
	

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Full filepath of the file containing profiling data.")
    args = parser.parse_args()

    read_prof_file(args.filepath)

if __name__ == "__main__":
	main()