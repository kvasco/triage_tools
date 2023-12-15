##############################################################################
# utils - methods for use by the testinfo module
##############################################################################

import re
import argparse
import json
import os
import sys
import datetime
import pprint

# Module variables
# args can be passed in to be used by these methods
args = None


def set_utils_args(input_args):
    global args # use the module variable here, not a variable of the same name in this method
    args = input_args

    if (args.verbosity > 2):
        print(f'NONE: utils.args = {args}')

    args = argparse.Namespace(verbosity=input_args.verbosity, dbg=input_args.dbg)

    if (args.verbosity > 2):
        print(f'utils.args = {args}')

# Function to exit script
def rtb():
    # Exit the script without error
    print('RTB - Roger')
    sys.exit()

# Function to print a separator line
def print_separator(sep_char=None, repeat_count=50):
    if sep_char is None:
        sep_char = '-'
    print('\n' + (sep_char * repeat_count) + '\n');
#    if sep_char is None:
#        print(f'\n--------------------------------------------------\n')
#    else:
#        print('\n' + (sep_char * repeat_count) + '\n');

# Function to perform various processing tasks on the input data
def process_results(list_data):
    for object in list_data:
        add_short_error(object)
        add_testname(object)
        add_short_command(object)

# Function to add ShortErrorSig to dictionary
def add_short_error(object): # object is a dictionary
    if 'ErrorSignature' in object:
        long_err = object['ErrorSignature']
        # Check if the value for the 'ErrorSignature' key is an empty string
        if long_err == '':
            #continue  # Skip this for loop iteration if the value is an empty string
            return  # Exit the function if the value is an empty string

        ##long_err = object.get('ErrorSignature', '') # grabbed above in a different way
        if (args.verbosity > 3):
            print(f'Long Error Signature: {long_err}')

        # move to external regex list as first pass shortener
        short_err = re.sub(r'UVM_ERROR[\w\d\s\/\(\)\.@-]*:', '', long_err)

        if (args.verbosity > 3):
            print(f'Short Error Signature: {short_err}')

        if args.dbg:
            if (args.verbosity > 3):
                print(f'dbg:')
                print(f'Type of long_err:        {type(long_err)}')
                print(f'Type of short_err:       {type(short_err)}')
     
        # apply the external regex list here
        short_err_re_list = [
            (r'(\+A\d+)+\b', '+fc_workarounds'),
            (r'\+no_pcie_phy\+no_vc_phy', '+fc_speedups'),
            (r'\+ignore_warnings',''),
            (r'\+cov',''),
            # Add more command compresseion regex patterns here
        ]
     
        # apply the external regex list here
        short_err = apply_regex_list(short_cmd, short_cmd_re_list)
     
        if (args.verbosity > 1):
            print(f'short err = {short_err}')

        # Add the short error signature to the dictionary object
        object['ShortErrorSig'] = short_err

# Function to add TestName to dictionary for simulation runs
def add_testname(object): # object is a dictionary
    if 'CompleteJobName' in object:
        job_name = object.get('CompleteJobName', '')

        if 'vcs_sim' in job_name:
            # Define the regular expression pattern
            #   Start with a plus sign.
            #   Are followed by one or more characters that are not plus signs.
            #     [^\+]+: This part is used to match one or more characters that are not plus signs.
            #       The caret symbol at the beginning of the character set inverts the selection.
            #       In other words, it matches characters that are not specified within the brackets.
            #   End with "_test".
            #   End with a trailing plus sign.
            pattern = r'\+[^\+]+_test\+'

            # Find all matches in the text
            matches = re.findall(pattern, job_name)
            if args.dbg:
                if (args.verbosity > 2):
                    print(f'dbg:')
                    print(f'Length of matches:           {len(matches)}')

            # Print the matches
            for match in matches:
                if args.dbg:
                    if (args.verbosity > 2):
                        print(f'dbg:')
                        print(f'Type of match:           {type(match)}')
                if (args.verbosity > 2):
                    print_separator()
                    print(f'job_name: {job_name}')
                    print(f'>>> {match}')
                extracted_string = match[1:-1]  # Remove the start and end +
                if (args.verbosity > 2):
                    print(f'TestName: {extracted_string}')
                    print()
            else:
                if (args.verbosity > 2):
                    print(f'No match in {job_name[:15]}')

            if (len(matches) == 1):
                my_match = ''.join(matches)
                # Strip leading and trailing +
                my_match = my_match[1:-1]

            if args.dbg:
                if (args.verbosity > 2):
                    print(f'dbg:')
                    print(f'Type of job_name:        {type(job_name)}')
                    print(f'Type of matches:         {type(matches)}')
                    print(f'my_match:                {my_match}')

            # Add the TestName to the dictionary object
            object['TestName'] = my_match

# Function to undo the jobm cfg unrolling and create a more compact job name
def add_short_command(object):
    if 'CompleteJobName' in object:
        job_name = object.get('CompleteJobName', '')

        if (args.verbosity > 1):
            print(f' Long cmd = {job_name}')
     
        short_cmd_re_list = [
            (r'(\+A\d+)+\b', '+fc_workarounds'),
            (r'\+no_pcie_phy\+no_vc_phy', '+fc_speedups'),
            (r'\+ignore_warnings',''),
            (r'\+cov',''),
            # Add more command compresseion regex patterns here
        ]
     
        short_cmd = apply_regex_list(job_name, short_cmd_re_list)
     
        if (args.verbosity > 1):
            print(f'short cmd = {short_cmd}')
     
        # Add the TestName to the dictionary object
        object['ShortCommand'] = short_cmd

# Function to apply a list of regular expressions to text
def apply_regex_list(text, regex_list):
    for regex_pattern, replacement in regex_list:
        text = re.sub(regex_pattern, replacement, text)
    return text

# Function to load data from JSON file
def load_from_json(json_filename):
    if os.path.isfile(json_filename) and os.path.getsize(json_filename) > 0:
        with open(json_filename, 'r') as json_file:
            try:
                json_data = json.load(json_file)
                return json_data
            except json.JSONDecodeError:
                print('Failed to parse JSON content in the input file.')
    return None

# Function to save data as JSON file
# Used by testinfo to save regex list as JSON file
def save_as_json(data, json_filename, opt_extension=None, opt_tag=None):
    new_file_name = f'{json_filename}{opt_extension}'
    if (args.verbosity > 1):
        print(f'save_as_json(): {__name__}.write_file: new_file_name is {new_file_name}')
    with open(new_file_name, 'w') as json_file:
        if opt_tag:
            json_file.write(str(datetime.datetime.now()) + '\n')
        json.dump(data, json_file, indent=4)
        # Add ending newline to file
        json_file.write('\n')
    if (args.verbosity > 1):
        print(f"{__name__}.write_file: Content saved to '{new_file_name}'!")

# Function to read a file and return the contents
def read_file(file_name):
    try:
        # Open the file for reading
        with open(file_name, 'r') as file:
            # Read the content of the file
            file_content = file.read()
        return file_content

    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return None
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None

# Function to read a file and return the contents
def write_file(content, file_name, opt_extension=None, opt_tag=None):
    new_file_name = f'{file_name}{opt_extension}'
    if (args.verbosity > 2):
        print(f'{__name__}.write_file: new_file_name is {new_file_name}')
    with open(new_file_name, 'w') as new_file:
        if opt_tag:
            new_file.write(str(datetime.datetime.now()) + '\n')
        new_file.write(content)
    if (args.verbosity > 1):
        print(f"{__name__}.write_file: Content saved to '{new_file_name}'!")

# Function to print N lines of content read from a file
def print_lines(content, num_lines):
    # Split the file_content into lines and print the first five lines
    lines = content.split('\n')
    print(f'The first {num_lines} lines of the content are:')
    for line in lines[:num_lines]:
        print(line)

# Function to load JSON objects from (text) file content
#   This is more of an extraction of data as JSON objects from text
def extract_json_objects(content):
    try:
        json_data = json.loads(content)
        return json_data

    except json.JSONDecodeError:
        print('Failed to parse JSON content in the input file/text string.')

# Function to print N lines of content read from a file
def print_json_objects(json_data, num_objects=0, offset=0):
    if isinstance(json_data, list) and len(json_data) >= 0:
    
#       if (args.verbosity > 1):
#           print(f'print_json_objects(): num_objects = {num_objects}, offset = {offset}, data_len = ' + str(len(json_data)))
    
        # Adjust number printed if range is too large
        max_obj = num_objects if ((num_objects + offset) <= len(json_data)) else (num_objects if (num_objects < len(json_data)) else len(json_data))
        if (args.verbosity > 2):
             print(f'print_json_objects(): max_obj = {max_obj}')
    
        # Argument checking (commented code below is a start to dynamically handle errors)
        try:
            if (num_objects + offset) > len(json_data):
                raise Exception(f'Bad request: {num_objects} objects + offset {offset} > data length ' + str(len(json_data)))
        except Exception as e:
            print(e)
    
#        # Adjust offset if out of bounds
#        mod_offset = offset if (max_obj == num_objects) else ((offset - max_obj) if ((offset - max_obj) > 0) else 0)
#        if (args.verbosity > 1):
#            print(f'print_json_objects(): mod_offset = {mod_offset}')
#        if (args.verbosity > 1 and num_objects != 0):
#            print(f'  Original: Request to print {num_objects} JSON objects starting at index {offset}')
#            print(f'Adjusted: Printing the first {max_obj} JSON objects starting at index {mod_offset}')
    
        for i in range(offset, max_obj + offset):
            print(json.dumps(json_data[i], indent=2))
    
            if (args.verbosity > 3):
                print(f'\nINFO:\njson_data[{i}]:\n{json_data[i]}\n')
    else:
        print('JSON content does not contain at least one object.')
    
    if (args.verbosity > 1 and num_objects != 0):
        print_separator()

# Function to verify the regex list loaded from a json file
def verify_regex_list(regex_list):
    # Define a list of regular expressions and replacements
    default_regex_list = [
        (r'default', 'internal_regex_list'), # Replace 'default' with 'internal_regex_list'
        (r'the', 'thee'),      # Example: Replace 'the' with 'thee'
        (r'mass', 'volume'),   # Replace 'mass' with 'volume'
        # Add more regex patterns and replacements as needed
    ]

    # If JSON regex file does not exist or is empty, use the internal default regex list
    if not isinstance(regex_list, list) or regex_list is None:
        regex_list = default_regex_list
        print('Invalid content in the input regex list. Using the internal regex list.')
    else:
        if (args.verbosity > 0):
            print('Input regex list verified')

    return regex_list

# Function to pretty print a list of lists
def print_list_of_lists(list_of_lists):
    max_sum_of_lengths = 0  # Initialize with 0

    for inner_list in list_of_lists:
        inner_list_length = sum(len(item) for item in inner_list)

        # Update max_sum_of_lengths if a larger sum is found
        if inner_list_length > max_sum_of_lengths:
            max_sum_of_lengths = inner_list_length

        for item in inner_list:
            if (args.verbosity > 3):
                print(f"Length of '{item}': {len(item)}")
        if (args.verbosity > 3):
            print(f"Sum of lengths in the inner list: {inner_list_length}")
    adjust = 10 + 4 # 10 to Account for square brackets, single quotes, and spaces; Adjust width as needed
                    #  4 for schmooing
    adj_max_sum = max_sum_of_lengths + adjust 
    if (args.verbosity > 3):
        print(f"Maximum sum of lengths found: max sum ({max_sum_of_lengths}) + adjustment ({adjust}) = {adj_max_sum}")

    pp = pprint.PrettyPrinter(width=adj_max_sum, compact=True)  # Auto adjusting
    pp.pprint(list_of_lists)
