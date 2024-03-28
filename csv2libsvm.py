#!/usr/bin/env python

"""
Convert CSV file to libsvm format. Works only with numeric variables.
Put -1 as label index (argv[3]) if there are no labels in your file.
Expecting no headers. If present, headers can be skipped with argv[4] == 1.

"""

import sys
import csv
from collections import defaultdict
from optioner import options


def helper():
    print('csv2libsvm. by zygmuntz. edited by d33pster')
    print('\nHELP TEXT\n')
    print('  |     -h or --help          : show this help text and exit.')
    print('     COMPULSORY ARGUMENTS:')
    print('  |     -i or --infile        : specify input file.')
    print('  |     -o or --outfile       : specify output file.')
    print('     OPTIONAL ARGUMENTS:')
    print('  |     -li or --label-index  : specify label index. if no labels in input file, set to -1.')
    print('  |     -sh or --skip-headers : takes 0 or 1. if there are headers in input file, set to 1.')
    print('END')
    exit(0)

# create arguments
shortargs = ['i', 'o', 'li', 'sh', 'h']
longargs = ['infile', 'outfile', 'label-index', 'skip-headers', 'help']
compulsory_short_args = ['i', 'o']
compulsory_long_args = ['infile', 'outfile']

argCTRL = options(shortargs, longargs, sys.argv[1:], compulsory_short_args, compulsory_long_args, ['-h', '--help'])

actualargs, check, error, falseargs = argCTRL._argparse()

if not check:
    print(f'ERROR: {error}')
    exit(1)
else:
    if '-h' in actualargs or '--help' in actualargs:
        helper()
    
    # check optional args first
    if '-li' in actualargs:
        label_index = argCTRL._what_is_('li')
    elif '--label-index' in actualargs:
        label_index = argCTRL._what_is_('label-index')
    else:
        pass
    
    if '-sh' in actualargs:
        skip_headers = argCTRL._what_is_('sh')
    elif '--skip-headers' in actualargs:
        skip_headers = argCTRL._what_is_('skip-headers')
    else:
        pass
    
    # compulsory args
    if '-i' in actualargs:
        input_file = argCTRL._what_is_('i')
    else:
        input_file = argCTRL._what_is_('infile')
    
    if '-o' in actualargs:
        output_file = argCTRL._what_is_('o')
    else:
        output_file = argCTRL._what_is_('outfile')
    

def construct_line( label, line ):
	new_line = []
	if float( label ) == 0.0:
		label = "0"
	new_line.append( label )

	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

# ---

# input_file = sys.argv[1]
# output_file = sys.argv[2]

# try:
# 	label_index = int( sys.argv[3] )
# except IndexError:
# 	label_index = 0

# try:
# 	skip_headers = sys.argv[4]
# except IndexError:
# 	skip_headers = 0

i = open( input_file, 'rb' )
o = open( output_file, 'wb' )

reader = csv.reader( i )

if skip_headers:
	headers = reader.next()

for line in reader:
	if label_index == -1:
		label = '1'
	else:
		label = line.pop( label_index )

	new_line = construct_line( label, line )
	o.write( new_line )

