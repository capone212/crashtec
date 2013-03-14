'''
Created on 14.03.2013

@author: capone
'''
from crashtec.db.schema.types import DBSchemaTypes


TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string()
        } 
 
    
SYMBOLS_TABLE = 'binary_symbols'
SYMBOLS_URL = 'url'
SYMBOLS_LOCAL_DIR = 'lical_dir_path'
SYMBOLD_TRANSACTION_ID = 'symsrv_transaction_id'


_symbols = {
            SYMBOLS_URL : DBSchemaTypes.long_string(),
            SYMBOLS_LOCAL_DIR :  DBSchemaTypes.long_string(),
            SYMBOLD_TRANSACTION_ID :  DBSchemaTypes.short_string()
           }

model = {SYMBOLS_TABLE : _symbols, TASKS_TABLE : _task }