#!/bin/python3
##############################################################################
# testinfo - an improved regression reporting script
##############################################################################

"""
To Do:
[X] Complete adding entries to dictionary
[ ] Print updated dictionary object & save to file.new
[ ] Seed regex list file with actual substitution patterns
[ ] Fix add_short_error()
[ ] Short term, add ASIC and Owner to fail sigs via re & dict match
[ ] Team fullname, firstname, surname, initials dict?
[ ] Add simple json list of lists input file with [error_str, owner, jira_num] 
      that can be used to process the regression/triage report 
[ ] Alphabetize by testname in the passing test list
[ ] Make sure to indicate the comp model used for a test e.g. Cn as ID to list
[ ] Add reference to full command by ID
[ ] Account for special options in testnames e.g. "vc_stub" or "with vc", "has_phy", etc.

Example:
Cmd Build Testname
(3) C2    hfi_fc_spc_*
"""

import re
import argparse
import json
import os
import sys

# testinfo specific modules
import utils # the testinfo utilities (method) library
import experiments # a library of demo/experimental code snippets


# Command line argument parser
parser = argparse.ArgumentParser(description='Process a file and apply regex patterns.')
parser.add_argument('filename', type=str, help='Name of the JSON file to process')
parser.add_argument('--json_re_file', type=str, help='JSON file with regex patterns')
parser.add_argument('-v', '--verbosity', default=0, type=int, choices=[0, 1, 2, 3, 4], help='Increase output verbosity')
parser.add_argument('--tag', action='store_true', default=False, help='Add timestamp to output file(s)')
parser.add_argument('--dbg', action='store_true', help='Show debug content')
parser.add_argument('--dbg2', action='store_true', help='Show second level debug content')
parser.add_argument('--eec', action='store_true', help='Execute Experimental Code snippets')
args = parser.parse_args()

# Module variables
regex_list = None

# Pass args to utils and experiments
utils.set_utils_args(args)
experiments.set_experiments_args(args)


#-----------------------------------------------------------
# Load and check the JSON file with regex patterns
# The regex patterns simplify simulation error messages
# For example, "Mismatch on channel 4" would become "Mismatch on channel *"
# This allow better and more natural groupings of error signatures
# that are the same but vary based on some identifier like channel
#-----------------------------------------------------------
print() # add a blank line after the command for clarity

# Check if a JSON file is specified and load regex list from it
if args.json_re_file:
    regex_list = utils.load_from_json(args.json_re_file)

if (args.verbosity > 3):
    print(f'Inital check of regex_list: {regex_list}')

regex_list = utils.verify_regex_list(regex_list)

if args.dbg:
    print(f'dbg: regex_list:')
    utils.print_list_of_lists(regex_list)

#-----------------------------------------------------------
# Load the JSON results file for processing
#-----------------------------------------------------------
# Grab the filename provided by the user in the arguments
file_name = args.filename

json_data = utils.load_from_json(file_name)

if args.dbg2:
    print(f'dbg:')
    utils.print_separator('<-Pre->', 10)
    #utils.print_json_objects(json_data, 3) # first three objects
    #utils.print_json_objects(json_data, num_objects=2, offset=2) # first two vcs_sim
    #utils.print_json_objects(json_data, num_objects=1, offset=3) # first failing vcs_sim
    utils.print_json_objects(json_data, num_objects=1, offset=1) # first failing vcs_sim in test data
    #utils.print_json_objects(json_data, num_objects=3, offset=1) # one vcs_comp and the first two vcs_sim

#-----------------------------------------------------------
# A.2
#-----------------------------------------------------------
utils.process_results(json_data)

if args.dbg:
    print(f'dbg:')
    utils.print_separator('<-Post->', 8)
    #utils.print_json_objects(json_data, 3) # first three objects
    #utils.print_json_objects(json_data, num_objects=2, offset=2) # first two vcs_sim
    #utils.print_json_objects(json_data, num_objects=1, offset=3) # first failing vcs_sim
    utils.print_json_objects(json_data, num_objects=1, offset=1) # first failing vcs_sim in test data
#    utils.print_json_objects(json_data, num_objects=3, offset=1) # one vcs_comp and the first two vcs_sim

#-----------------------------------------------------------
# Get model build pass/fail counts
#-----------------------------------------------------------
 
#-----------------------------------------------------------
# Get test pass/fail counts
#-----------------------------------------------------------

#-----------------------------------------------------------
# xxx: apply to the short_error field only?
# Apply the regexes to the input file ShortErrorSig field
#-----------------------------------------------------------
# Apply the regular expressions to the content

# Update to work on data field - file_content no longer used 
#modified_content = utils.apply_regex_list(file_content, regex_list)
modified_content = json_data

if args.dbg:
    if (args.verbosity > 2):
        print(f'dbg:')
        print(f'Type of json_data:        {type(json_data)}')
        print(f'Type of modified_content: {type(modified_content)}')

#-----------------------------------------------------------
# xxx: save after all processing and data accumulation? 
# Save the modified file contents to a new file
#-----------------------------------------------------------
# Update to write updated json objects #utils.write_file(modified_content, file_name, '.new', args.tag)
utils.save_as_json(modified_content, file_name, '.new', args.tag)

if (args.verbosity > 0):
    print(f'Regular expressions applied successfully. Modified content saved!')

#-----------------------------------------------------------
# Run code snippets if requested
# Code snippets capture features or concepts used to develope
# this script/module
#-----------------------------------------------------------
# Check if the experimental code snippets should be run
if args.eec:
    experiments.execute_code_snippets()
