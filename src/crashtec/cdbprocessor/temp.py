'''
Created on 03.05.2013

@author: capone
'''
import os
from crashtec.cdbprocessor import signaturebuilder

def print_line(line):
    print line

def get_input_results(path_root):
    if (not path_root):
        return set()
    walk_path = os.walk(path_root)
    if (not walk_path):
        return set()
    result_files = set();
    for root, dirs, files in walk_path:
        if (not files):
            continue
        for file in files:
            if file == 'results.txt':
                result_files.add(os.path.join(root, file))
    return result_files;


# Redirect std output to file 
import sys
sys.stdout = open('D:/signatures.txt', 'w')

stack_parser = signaturebuilder.ProblemStackParser()
for file_name in get_input_results('D:/work/test/tasksRoot/tasksRoot'):
    file_object = open(file_name)
    lines = stack_parser.extrack_stack_lines(file_object.read())
    if not lines:
        continue
    refined = stack_parser.strip_additional_info(lines)
    print file_name, "\n"
    [print_line(signature) for signature in refined]
    print "-"*80, "\n"