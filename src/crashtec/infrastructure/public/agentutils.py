'''
Created on 20.02.2013

@author: anzor.apshev
'''
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilters
from crashtec.infrastructure import dbmodel 
import datetime

GROUP_ID_UNSET = '*'

# Create short name alias
_f = dbfilters.FieldFilterFactory

# TODO: unit test this methods

def register_agent(class_type, instance_name, group_id = GROUP_ID_UNSET):
    d = dbmodel
    cursor = dbroutines.select_from(d.AGENTS_TABLE, 
                    db_filter = _f(d.AGENTS_INSTANCE_FIELD) == instance_name)
    record = cursor.fetch_one()
    is_exists = True
    if not record:
        record = dbroutines.Record()
        record[d.AGENTS_INSTANCE_FIELD] = instance_name
        is_exists = False
    record[d.AGENTS_CLASS_TYPE_FIELD] = class_type
    record[d.AGENTS_REGISTRED_TIME_FIELD] = datetime.datetime.now()
    record[d.AGENTS_KEEPALIVE_FIELD] = datetime.datetime.now()
    record[d.AGENTS_GROUP_FIELD] = group_id
    if is_exists:
        dbroutines.update_record(d.AGENTS_TABLE, record)
    else:      
        dbroutines.create_new_record(d.AGENTS_TABLE, record)

def send_keepalive_message(instance_name):
    d = dbmodel
    record = dbroutines.Record()
    record[d.AGENTS_INSTANCE_FIELD] = instance_name
    record[d.AGENTS_KEEPALIVE_FIELD] = datetime.datetime.now()
    dbroutines.update_record(d.AGENTS_TABLE, record,
                             key_field = d.AGENTS_INSTANCE_FIELD)
        