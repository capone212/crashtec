'''
Created on 03.05.2013

@author: capone
'''
import os
from crashtec.cdbprocessor import signaturebuilder

def print_line(line):
    print line


# self.problem_class = problem_class
# self.image_name = image_name
# self.symbol_name = symbol_name
# self.failure_bucket_id = failure_bucket_id


def print_signature(signature):
    print 'problem_class=', signature.problem_class
    print 'image_name=', signature.image_name
    print 'symbol_name=', signature.symbol_name
    print 'failure_bucket_id=', signature.failure_bucket_id

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
#sys.stdout = open('D:/signatures.txt', 'w')

stack_parser = signaturebuilder.ProblemStackParser()
sig_tool = signaturebuilder.CrashSignatureParser()
for file_name in get_input_results('D:/work/test/tasksRoot/tasksRoot'):
    file_object = open(file_name)
    raw_cdb_output = file_object.read()
    lines = stack_parser.extrack_stack_lines(raw_cdb_output)
    if not lines:
        continue
    refined = stack_parser.strip_additional_info(lines)
    if not refined:
        print file_name
        continue
    continue
    signature = sig_tool.parse(raw_cdb_output)
    [print_line(line) for line in refined]
    print ""
    print_signature(signature)
    print "-"*80, "\n"