from crashtec.db.schema.types import DBSchemaTypes
import logging
from crashtec.utils.exceptions import GeneralError, BaseException
import sys
from crashtec.db.schema.fields import *
import postgres_binding

_logger = logging.getLogger("db.builder")

def collect_model_descriptions(packages_list):
    result = []
    for package_name in packages_list:
        try:
            temp = __import__(package_name + '.dbmodel', 
                                globals(), locals(), ['model'], -1)
            result.append(temp.model)
        except ImportError:
            _logger.error("can't import dbmodule.py for %s package", [package_name])
            raise GeneralError()
    return result

def _init_logging():
    # Set Log level
    _logger.setLevel(logging.DEBUG)
    #Set handler11111
    log_handler = logging.StreamHandler(sys.stdout)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    _logger.addHandler(log_handler)

def agregate_descriptions(model_descriptions):
    aggregated_list = dict()
    for db_model in model_descriptions:
        for element_name in db_model.keys():
            if element_name in aggregated_list:
                # TODO: add fault when types is not equal
                aggregated_list[element_name].update(db_model[element_name])
            else:
                #we should take copy here
                aggregated_list[element_name] = dict(db_model[element_name])
    return aggregated_list
    

def main():
    try:
        _init_logging()
        # TODO: get package lists
        packages_list = ['crashtec.crashmover', 'crashtec.infrastructure']
        # enumerate all db model definitions from all packages
        model_descriptions = collect_model_descriptions(packages_list)
        # aggregate all definitions to single updated db definition
        aggregated_list = agregate_descriptions(model_descriptions)
        
        for table_name in aggregated_list.keys() :
            fields = aggregated_list[table_name]
            # add primary key field
            fields[PRIMARY_KEY_FIELD] = DBSchemaTypes.autoincrement()
            sql = postgres_binding.generate_table_sql(table_name, fields)
            print sql 
        
    except BaseException:
        _logger.error("Unexpected error occurred. DB schema was not created")
        sys.exit(1)
        
main()