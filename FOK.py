
import nltk
from nltk.sem import Expression, logic
from nltk.sem.logic import *
from nltk.inference import ResolutionProver
read_expr = Expression.fromstring
from nltk.sem.evaluate import Model

KBURI = 'highways_kb.txt'
def Load_KB():
    
    knowledge_base = []
    with open(KBURI, "r") as f:
        for line in f:
            lnstr = line.strip()
            assertion = read_expr(lnstr.strip())
            knowledge_base.append(assertion)
    return knowledge_base
test = Load_KB()
def validate_kb():
    try:
        with open(KBURI) as f:
            content = f.read()
    except IOError:
        print(f"Error: File {KBURI} not found")
        return False
    
    # Check if each line in the file is valid format
    for line in content.splitlines():
        if not re.match(r'^\s*[A-Za-z0-9]+\s*\([^)]*\)\s*(<->|->)\s*\([^)]*\)\s*$', line): #https://python.gotrained.com/nltk-regex/
            print(f"Error: Invalid line found in {KBURI}: {line}")
            return False
    
    # check if loading kb works
    try:
        nltk.sem.extract_rels('x', 'y', nltk.sem.Expression.fromstring(content), corpus='abc', pattern=None)
    except ValueError:
        print(f"Error: Failed to load {KBURI} as KB")
        return False
    
    return True
def confirmLogic(obj, subj, knowBase):
    obj = obj.replace(' ', '_')
    subj = subj.replace(' ', '_')
    expr = read_expr((subj + ' (' + obj + ')').lower())
    result = ResolutionProver().prove(expr, knowBase)
    if result == True:
        return ("You are correct")
    elif result == False:
        expr = read_expr('-' + subj + '(' + obj + ')')
        result = ResolutionProver().prove(expr, knowBase)
        if result == True:
            return ("This is incorrect")
        else:
            return ("I don't know enough about this to check if its true")
def Add_To_Knowledgebase(obj, subj, knowBase):
    obj = obj.replace(' ', '_')
    subj = subj.replace(' ', '_')
    strExpr = (subj + " (" + obj + ')').lower()
    if (ResolutionProver().prove(read_expr('-' + strExpr), knowBase)):
        return ("I am sorry but that contradicts my knowledgebase!")
    elif (ResolutionProver().prove(read_expr(strExpr), knowBase)):
        return ("I'm already aware this is true, thank you ")
    else:
        ## add to KB
        knowBase.append(read_expr(strExpr))
        filepath = KBURI
        with open(filepath, 'a') as kbf:
            kbf.write('\n'+ strExpr)
        return ("OK, I will remember that " + obj + " is " + subj)
# print(confirmLogic('bollard','has_id', test))
# newassrt = nltk.sem.Expression.fromstring('road(highway)')
# print(Add_To_Knowledgebase('road','highway', test))
def fopl_to_readable(fopl_statements):
    readable_statements = []
    for statement in fopl_statements:
        expr = Expression.fromstring(str(statement))
        readable_statement = str(expr)  
        readable_statement = readable_statement.replace("->", " implies ")
        readable_statement = readable_statement.replace("V", " or ")
        readable_statement = readable_statement.replace("^", " and ")
        readable_statement = readable_statement.replace("-", "Not ")
        readable_statement = readable_statement.replace("|", "or ")
        readable_statements.append(readable_statement)
    
    return "\n".join(readable_statements)
# print(fopl_to_readable(test))
