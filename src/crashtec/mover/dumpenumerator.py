import os

def get_input_dumps(path_root):
    if (not path_root):
        #print("WARNING: empty input param in getNonEmptySubDirrectoriesList")
        #TODO: log here
        return set()
    walk_path = os.walk(path_root)
    if (not walk_path):
        return set()
    dumps_list = set();
    for root, dirs, files in walk_path:
        if (not files):
            continue
        for file in files:
            dumps_list.add(os.path.join(root, file))
    return dumps_list;

        
#from crashtec.config.mooverconfig import INPUT_DIR
#print get_input_dumps(INPUT_DIR)    