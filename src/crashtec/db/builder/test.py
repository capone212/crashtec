from crashtec.db.schema.types import DBSchemaTypes
import logging

_logger = logging.getLogger("db.builder")

def disctionary():
    task = {
            "dumpFileName" : DBSchemaTypes.long_string(), 
            "pubDate" : DBSchemaTypes.datetime(),
            "finishTime" : DBSchemaTypes.datetime(),
            "status" : DBSchemaTypes.short_string(),
            "analyseAgent" : DBSchemaTypes.string(),
            "user" : DBSchemaTypes.short_string()        
            }
    return {'task' : task}

def dictionary2():
        task = {
                "dumpFileName" : DBSchemaTypes.long_string(), 
                "pubDate" : DBSchemaTypes.datetime(),
                "finishTime" : DBSchemaTypes.datetime(),
                "logFile" : DBSchemaTypes.long_string(),
                "resultFile" : DBSchemaTypes.long_string(),        
                }
        return {'task' : task}



def agregate_discts():
    aggregatedList = disctionary()
    news = dictionary2()
    
    for element_name in news.keys():
        if element_name in aggregatedList:
            # TODO: add fault when types is not equal
            aggregatedList[element_name].update(news[element_name])
        else:
            aggregatedList[element_name] = news[element_name]

#from crashtec.infrastructure.db_model import model 

def collect_model_descriptions(packages_list):
    result = []
    for module_name in packages_list:
        try:
            temp = __import__( module_name + '.db_model', 
                                globals(), locals(), ['model'], -1)
            result.append(temp.model)
        except ImportError:
            # TODO: log error. 
            # TODO: return empty result or fault??
            pass
    return result

packages_list = ['crashtec.processor', 'crashtec.infrastructure']        
print collect_model_descriptions(packages_list)