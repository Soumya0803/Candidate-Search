from jinjasql import JinjaSql
#from copy import deepcopy
from six import string_types
import re
from . import Prefix
from . import MongoInfix
import os

def strip_blank_lines(text):
    '''
    Removes blank lines from the text, including those containing only spaces.
    '''
    return os.linesep.join([s for s in text.splitlines() if s.strip()]).strip()

def SearchCandidate(keywords, query_type="sql"):
    parsed_keywords=parse_keywords(keywords)

    parameters=quote_string(parsed_keywords,query_type)

    params = {
    'text': parameters,   
    }
        
    #Poll.objects.get(
    #Q(question__startswith='Who'),
    #Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
    if query_type=='sql':  
        search_candidate_template_sql = '''
        select id, name, text from Resume_Resume where {{ transform_dimensions_sql(dimensions) }}
        '''
        return strip_blank_lines(apply_template(search_candidate_template_sql, parameters={'dimensions':params},func_list=[transform_dimensions_sql]))
    elif query_type=='django_orm':
        search_candidate_template_django_orm = '''
        Resume.objects.get({{ transform_dimensions_django_orm(dimensions) }})
        '''
        return strip_blank_lines(apply_template(search_candidate_template_django_orm, parameters={'dimensions':params},func_list=[transform_dimensions_django_orm]))
    else:
        return f"db.Resume.find({{ {transform_dimensions_mongodb(params)} }})"
        

   
def parse_keywords(keywords):
    #k='(Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR))' 
    #print(re.split('([^a-zA-Z0-9])',keywords)) 
    return re.split('(".+?"|\'.+?\'|\W)', keywords) 
    # "Ruby on Rails"
    # k=""
    # for i in keywords:
    #     #if i in re.search('"([^a-zA-Z0-9])"', keywords):
    #         k.append(i)
    # return k
                     
def quote_string(parsed_keywords,query_type):
    '''
    If `value` is a string type, escapes single quotes in the string
    and returns the string enclosed in single quotes.
    '''
    parsed_keywords_quote=[]
    #params = deepcopy(parsed_keywords)
    for  val in parsed_keywords:
        if isinstance(val, string_types):
            #val = str(val)
            #val = val.replace("'", "''")
            #print(val)
            if val==" " or val=="" or val==' 'or val=='':
                pass        
            elif val=='(' or val==')' or val=='(' or val==')'or val=='AND' or  val=='OR':
                parsed_keywords_quote.append(val) 
            else:
                if query_type=='sql':
                    parsed_keywords_quote.append("'%{},%'".format(val))    
                elif query_type=='django_orm':
                    parsed_keywords_quote.append("'{},'".format(val))    
                else:
                    parsed_keywords_quote.append("/{},/".format(val))    

                
    return parsed_keywords_quote
    

def transform_dimensions_sql(dimensions: dict) -> str:
    '''
    Generate SQL for aliasing or transforming the dimension columns.
    '''
    query_end=""
    for key, val in dimensions.items():
        for i in val:
             
            if i=='('  or i==')' or i=='AND' or i=='OR':
                 query_end=query_end + ' ' + i

            else:
                query_end= query_end+' text like ' + i
        
    # q=""
    # for key, val in dimensions.items():
    #      q=" text like ".join( val)        
    return query_end

def transform_dimensions_django_orm(dimensions: dict) -> str:
    '''
    Generate SQL for aliasing or transforming the dimension columns.
    '''
    #Poll.objects.get(
    #Q(question__startswith='Who'),
    #Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
    query_end=""
    for key, val in dimensions.items():
        for i in val:
            if i=='('  or i==')':
                 query_end=query_end + ' ' + i
            elif i=='OR':
                query_end=query_end + ' ' + '|'
            elif i=='AND':
                query_end=query_end + ' ' + ','

            else:
                query_end= query_end+" Q(text_contains= " + i + ')'
    return query_end


def transform_dimensions_mongodb(dimensions: dict) -> str:
   #db.things.find({$and: [{$or : [{'a':1},{'b':2}]},{$or : [{'a':2},{'b':3}]}] })
   #{ $or: [ { <expression1> }, { <expression2> }, ... , { <expressionN> } ] }
   #{ $or: [ {text:  }, { text:}] }
   #OR (AND JAVA Python) RUby
    dim=dimensions['text']
    #add wilcard
    #for key, val in dimension.items():
    query_end = MongoInfix.evaluate(dim)
    return query_end    




def apply_template(template, parameters,func_list):
    '''
    Apply a JinjaSql template (string) substituting parameters (dict) and return
    the final SQL.
    '''
    j = JinjaSql(param_style='pyformat')
    
    if func_list:
        for func in func_list:
            j.env.globals[func.__name__] = func

    query, bind_params = j.prepare_query(template, parameters)
    print( query % bind_params)
    return (query % bind_params)
  


    
if __name__ == "__main__":
    keywords = input("Enter keywords:")
    query_type = input("Enter Query Type:")
    SearchCandidate(keywords, query_type)
#select * from resume where text like "%java%"  and  text like  "%SPRING%"  OR text like "%Python%" AND  text like "%Djang%" OR 
 #text like "%Ruby%" AND  text like '%"Ruby on Rails"%' OR text like  "%ROR%";