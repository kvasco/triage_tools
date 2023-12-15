################################################################################
# Experimental code snippets in methods
################################################################################

import re
import argparse

# testinfo specific modules
from utils import apply_regex_list, print_separator

# Module variables
# args can be passed in to be used by these methods
args = None


def set_experiments_args(input_args):
    global args # use the module variable here, not a variable of the same name in this method
    args = input_args

    if (args.verbosity > 2):
        print(f'NONE: experiments.args = {args}')

    # Only extract the args needed by this module
    args = argparse.Namespace(verbosity=input_args.verbosity, dbg=input_args.dbg)

    if (args.verbosity > 2):
        print(f'experiments.args = {args}')

# Function to test UVM style verbosity
def test_uvm_verbosity():
    #from enum import Enum, auto
    #
    #class UVM_VERBOSITY(Enum):
    #    UVM_NONE = auto()
    #    UVM_LOW = auto()
    #    UVM_MEDIUM = auto()
    #    UVM_HIGH = auto()
    #    UVM_FULL = auto()
    #
    ## Set the desired verbosity level
    #requested_verbosity = UVM_VERBOSITY.UVM_MEDIUM
    #
    ## Simulate some log messages with different verbosity levels
    #log_messages = [
    #    ('UVM_LOW', 'This is a low-verbosity message.'),
    #    ('UVM_HIGH', 'This is a high-verbosity message.'),
    #    ('UVM_MEDIUM', 'This is a medium-verbosity message.'),
    #    ('UVM_NONE', 'This is a message with no verbosity specified.'),
    #]
    #
    ## Iterate through log messages and print those with verbosity levels less than or equal to the requested verbosity
    #for verbosity, message in log_messages:
    #    if UVM_VERBOSITY[verbosity] <= requested_verbosity:
    #        print(f'Verbosity level: {verbosity}, Message: {message}')

    from enum import Enum, auto

    class UVM_VERBOSITY(Enum):
        UVM_NONE = auto()
        UVM_LOW = auto()
        UVM_MEDIUM = auto()
        UVM_HIGH = auto()
        UVM_FULL = auto()

    # Set the desired verbosity level
    requested_verbosity = UVM_VERBOSITY.UVM_MEDIUM

    # Simulate some log messages with different verbosity levels
    log_messages = [
        (UVM_VERBOSITY.UVM_LOW, 'This is a low-verbosity message.'),
        (UVM_VERBOSITY.UVM_HIGH, 'This is a high-verbosity message.'),
        (UVM_VERBOSITY.UVM_MEDIUM, 'This is a medium-verbosity message.'),
        (UVM_VERBOSITY.UVM_NONE, 'This is a message with no verbosity specified.'),
    ]

    # Iterate through log messages and print those with verbosity levels less than or equal to the requested verbosity
    for verbosity, message in log_messages:
        if verbosity.value <= requested_verbosity.value:
            print(f'Verbosity level: {verbosity.name}, Message: {message}')

################################################################################

# Function to print a short command after simplification
def test_command_shortening():
    # Input string
    input_string = '+ignore_warnings+no_pcie_phy+no_vc_phy+A383+A2103+A2157+A2557+A2590+A2616+A2913'

    short_cmd_re_list = [
        (r'(\+A\d+)+\b', '+fc_workarounds'),
        (r'\+no_pcie_phy\+no_vc_phy', '+fc_speedups'),
        (r'\+ignore_warnings',''),
        (r'\+cov',''),
        # Add more command compresseion regex patterns here
    ]

    if (args.verbosity > 1):
        print(f'short cmd = {apply_regex_list(input_string, short_cmd_re_list)}')

################################################################################

# Function to scan dictionary and count passes and fails
def test_pass_fail_counting():
    # Sample list of dictionaries
    data_list = [
        {'JobName': 'vcs_comp', 'Status': 'PASS'},
        {'JobName': 'vcs_comp', 'Status': 'FAIL'},
        {'JobName': 'vcs_sim', 'Status': 'PASS'},
        {'JobName': 'vcs_sim', 'Status': 'FAIL'},
        {'JobName': 'post_script.hfi_fc', 'Status': 'PASS'},
        {'JobName': 'post_script.spc', 'Status': 'FAIL'},
        {'JobName': 'vcs_comp', 'Status': 'PASS'},
    ]

    # Initialize counters for 'PASS' and 'FAIL' for vcs_comp and vcs_sim
    comp_pass_count = 0
    comp_fail_count = 0
    sim_pass_count = 0
    sim_fail_count = 0
    post_script_pass_count = 0
    post_script_fail_count = 0

    # Iterate over the list of dictionaries
    for entry in data_list:
        job_name = entry.get('JobName', '')
        status = entry.get('Status', '')

        if 'vcs_comp' in job_name:
            if status == 'PASS':
                comp_pass_count += 1
            elif status == 'FAIL':
                comp_fail_count += 1
        elif 'vcs_sim' in job_name:
            if status == 'PASS':
                sim_pass_count += 1
            elif status == 'FAIL':
                sim_fail_count += 1
        elif 'post_script' in job_name:
            if status == 'PASS':
                post_script_pass_count += 1
            elif status == 'FAIL':
                post_script_fail_count += 1

    # Calculate total counts for vcs_comp and vcs_sim
    total_comp_matches = comp_pass_count + comp_fail_count
    total_sim_matches = sim_pass_count + sim_fail_count

    # Print the counts for vcs_comp and vcs_sim, including the totals
    print(f'vcs_comp - Total: {total_comp_matches: >5}, PASS: {comp_pass_count: >5}, FAIL: {comp_fail_count: >5}')
    print(f'vcs_sim  - Total: {total_sim_matches: >5}, PASS: {sim_pass_count: >5}, FAIL: {sim_fail_count: >5}')
    print(f'post_script -            PASS: {post_script_pass_count: >5}, FAIL: {post_script_fail_count: >5}')

################################################################################

# Function to iterate and find regex matches in different categories
def test_category_regex_matching():
    # Define regular expressions for different categories
    regex_patterns = {
        'email': [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
            r'\b[\w.-]+@[\w.-]+\.\w+\b'
        ],
        'phone_number': [
            r'\(\d{3}\)\s?\d{3}-\d{4}', # fixed re via debug by cg
            r'\b\d{3}-\d{3}-\d{4}\b',
            r'\b\(\d{3}\)\s?\d{3}-\d{4}\b'
        ],
        'date': [
            r'\b\d{2}/\d{2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]
    }

    # Sample text to search for matches
    text = 'Contact us at test@example.com or call (123) 456-7890. The date is 2023-10-07.'
    print(text)
    print()

    # Iterate through the regular expressions and search for matches
    for category, patterns in regex_patterns.items():
        print(f'Category: {category}')
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                print(f"Matches for '{pattern}': {matches}")

################################################################################

# Function to test enum options
def test_enum():
    # Sample string
    my_string = 'This is a sample string.'

    # Debug verbosity level (change as needed)
    debug_verbosity = 'low'

    # Check if debug verbosity is high
    if debug_verbosity == 'high':
        # Print the first 10 characters
        print(my_string[:10])

        verb  = {100:'LOW', 200:'MEDIUM', 300:'HIGH'}
        verb2 = {'LOW':100, 'MEDIUM':200, 'HIGH':300}
        print(f'verb enum is {verb[100]}')
        print(f'verb2 enum is {verb2["LOW"]}')

################################################################################

# See also: https://www.techieclues.com/blogs/convert-enum-to-int-in-python

# Function to test enum class options
def test_enum_class():
    from enum import Enum

    class Verbosity(Enum):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

        # Usage examples
        current_verbosity = Verbosity.MEDIUM

        if current_verbosity == Verbosity.HIGH:
            print('Debug verbosity is set to high.')
        elif current_verbosity == Verbosity.MEDIUM:
            print('Debug verbosity is set to medium.')
        elif current_verbosity == Verbosity.LOW:
            print('Debug verbosity is set to low.')

################################################################################

# Function to print a dictionary showing all keys by value
def print_keys_by_value():
    print('print_keys_by_value():')
    # Sample dictionary
    my_dict = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value1',
        'key4': 'value3',
        'key5': 'value2',
    }

    # Create a dictionary to store keys by value
    keys_by_value = {}
    for key, value in my_dict.items():
        if value in keys_by_value:
            keys_by_value[value].append(key)
        else:
            keys_by_value[value] = [key]

    # Print keys grouped by value
    print('Keys by Value:')
    for value, keys in keys_by_value.items():
        print(f"{value}: {', '.join(keys)}")

    # Print all keys and their values
    print('\nAll Keys and Their Values:')
    for key, value in my_dict.items():
        print(f'{key}: {value}')

################################################################################

#import argparse
#
#def main():
#    parser = argparse.ArgumentParser(description='Example script with a --tec switch')
#    parser.add_argument('--tec', action='store_true', help='Print a message')
#
#    args = parser.parse_args()
#
#    if args.tec:
#        print('TEC switch is active. The message is printed!')
#
#if __name__ == '__main__':
#    main()

################################################################################

#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument('square', type=int,
#                    help='display a square of a given number')
#parser.add_argument('-v', '--verbosity', type=int,
#parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2], # restricted options
#                    help='increase output verbosity')
#args = parser.parse_args()
#answer = args.square**2
#if args.verbosity == 2:
#    print(f'the square of {args.square} equals {answer}')
#elif args.verbosity == 1:
#    print(f'{args.square}^2 == {answer}')
#else:
#    print(answer)

################################################################################

# Function to print a string returned from a method
def test_method_return_string():
    def get_hello():
        return 'hello'

    # Call the function to get the string
    hello_string = get_hello()
    print(hello_string)
    print('direct use: ' + get_hello())

################################################################################

# Function to test a generic print message method (to be modified to do verbosity based printing
def test_method_print_message():
    def print_message(message):
        if (args.verbosity > 1):
            print(f'Message: {message}')

    # Test the print_message function with different types of inputs

    # String
    print_message('This is a simple string.')

    # Formatted string
    formatted_message = f'Hello, {1 + 2}!'
    print_message(formatted_message)

    # Object (e.g., a dictionary)
    obj = {'key': 'value', 'number': 42}
    print_message(obj)

    # Number
    print_message(123)

    # Custom class instance
    class MyObject:
        def __init__(self, data):
            self.data = data

    my_instance = MyObject('Custom Object Data')
    print_message(my_instance.data)

################################################################################

#my_variable = None
#
## Later in your code, you can assign a value to the variable
#my_variable = 'This is a string.'
#
## You can also reassign the variable to a different value
#my_variable = 42
#
## Checking if the variable has a value
#if my_variable is not None:
#    print('The variable has a value:', my_variable)
#else:
#    print('The variable is still None.')

################################################################################

# If you want to remove items, you can create a new Namespace object with only the items you want to keep. Here's an example of how to do this:

#import argparse
#
#def main():
#    parser = argparse.ArgumentParser(description='Main Program')
#    parser.add_argument('--option1', type=int, default=0, help='Option 1')
#    parser.add_argument('--option2', type=str, default='', help='Option 2')
#    parser.add_argument('--option3', action='store_true', help='Option 3')
#    args = parser.parse_args()
#
#    # Create a new Namespace with selected arguments
#    new_args = argparse.Namespace(option1=args.option1, option2=args.option2)
#
#    print('Original args:')
#    print(args)
#
#    print('Modified args:')
#    print(new_args)
#
#if __name__ == '__main__':
#    main()

################################################################################

#import datetime
#
## Get the current date and time
#current_datetime = datetime.datetime.now()
#
## Print the current date and time
#print('Current Date and Time:', current_datetime)
#
#formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
#print('Formatted Date and Time:', formatted_datetime)

################################################################################

# You can use Python's built-in getattr() function to call a method by providing the method name as a string argument.

#class MyClass:
#    def method1(self):
#        return "This is method1"
#
#    def method2(self):
#        return "This is method2"
#
#def call_method_by_name(class_instance, method_name):
#    # Use getattr to get the method by name and call it
#    method = getattr(class_instance, method_name, None)
#    if method is not None and callable(method):
#        return method()
#    else:
#        return "Method not found or not callable"
#
## Create an instance of MyClass
#my_instance = MyClass()
#
## Specify the method name as a string
#method_to_call = "method1"
#
## Call the method by name
#result = call_method_by_name(my_instance, method_to_call)
#
#print(result)

# In this code:
#
# We have a MyClass class with two methods, method1 and method2.
#
# The call_method_by_name function takes two arguments: class_instance, which is an instance of the class, and method_name, which is a string representing the name of the method to call.
#
# Inside call_method_by_name, we use getattr() to dynamically retrieve the method based on its name. We then check if the method is callable (i.e., it's a function), and if so, we call it.
#
# We create an instance of MyClass, specify the method name as a string, and call the method using call_method_by_name.
#
# This approach allows you to call a method by providing its name as a string argument.
################################################################################

#data = [['external', 're_file'], ['thusly', 'thee'], ['mass', 'volume']]
#
#for inner_list in data:
#    for item in inner_list:
#        print(f"Length of '{item}': {len(item)}")
#
#Output:
#Length of 'external': 8
#Length of 're_file': 7
#Length of 'thusly': 6
#Length of 'thee': 4
#Length of 'mass': 4
#Length of 'volume': 6

#    for i in range(0, 10, 2):
#        result = 20 + i
#        print(f'pprint with width = {result}')
#        pp = pprint.PrettyPrinter(width=result, compact=True)  # Adjust width as needed
#        pp.pprint(regex_list)
#    print(f'Third check of regex_list: {regex_list}')
#    pp = pprint.PrettyPrinter(width=25, compact=True)  # Adjust width as needed
#    pp.pprint(regex_list)

################################################################################

# You can print the content of a docstring if you have access to the object (module, function, class, or method) that contains the docstring.

#def my_function():
#    """
#    This is a docstring for my_function.
#    It describes the purpose of the function.
#    """
#    pass
#
## Access and print the docstring of my_function
#print(my_function.__doc__)

################################################################################

# ensure that the replacement is done only when the match contains "Channel," you can use a regular expression pattern to match and replace the numbers only when they are preceded by "Channel." 

#import re
# 
## Input string
#input_string = "Channel 5, Channel 42, Channel 123, BBC News 24"
# 
## Regular expression pattern to match and replace numbers when preceded by "Channel"
#pattern = r"(Channel )(\d+)"
# 
## Use re.sub() to replace the matched numbers with an asterisk '*' when preceded by "Channel"
#output_string = re.sub(pattern, r"\1*", input_string)
# 
#print(output_string)

#<-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><-><->
# Example with array (tuple) containing the re and the substitution

#import re
# 
## Input string
#input_string = "Channel 5, Channel 42, Channel 123, BBC News 24"
# 
## List of regular expression patterns and their corresponding substitutions
#pattern_substitution_pairs = [
#    (r"(Channel )(\d+)", r"\1*"),  # Match "Channel" followed by digits
#    # Add more pairs as needed
#]
# 
## Iterate through the list and apply the substitutions
#for pattern, substitution in pattern_substitution_pairs:
#    input_string = re.sub(pattern, substitution, input_string)
# 
## Print the array of regular expression patterns and substitutions
#for pattern, substitution in pattern_substitution_pairs:
#    print(f"Pattern: {pattern}, Substitution: {substitution}")
# 
#print(input_string)  # Print the modified input_string

##<-><-><-><-><->
## When stored into a JSON file, this re tuple becomes:

#[
#    [
#        "(Channel )(\\d+)",
#        "\\1*"
#    ]
#]

################################################################################

# Data checking using exceptions

#try:
#    aa = 10  # Replace with your actual value for aa
#    bb = 5   # Replace with your actual value for bb
# 
#    if aa > bb:
#        raise Exception("CustomException: aa is greater than bb")
#    else:
#        print("aa is not greater than bb")
#except Exception as e:
#    print(e)

################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################


################################################################################

# Function to run the defined snippets
def execute_code_snippets():
    print_separator()
    print('##################################################')
    print('### Executing experimental code snippets')
    print('##################################################')

    # 2023-10-15 13:15
    if args.dbg:
        print_separator()
        print('### test_uvm_verbosity')
        test_uvm_verbosity()

    print_separator()
    print('### print_keys_by_value')
    print_keys_by_value()

    # 2023-10-21
    if args.dbg:
        print_separator()
        print('### test_command_shortening')
        test_command_shortening()

    print_separator()
    print('### test_pass_fail_counting')
    test_pass_fail_counting()

    print_separator()
    print('### test_category_regex_matching')
    test_category_regex_matching()

    if args.dbg:
        print_separator()
        print('### test_method_return_string')
        test_method_return_string()

    if args.dbg:
        print_separator()
        print('### test_method_print_message')
        test_method_print_message()

    print_separator()
