def precedence(op):
	
	if op == 'AND' or op == 'OR':
		return 1
	return 0

def strget(a):
  if str(a).startswith("$"): return f"{{{a}}}"
  return f"{{\"text\":\"{a}\"}}"

def applyOp(a, b, op):
	
	if op == 'AND': 
		return f"$and:[{strget(a)}, {strget(b)}]"
	if op == 'OR': 
		return f"$or:[{strget(a)}, {strget(b)}]"

def evaluate(tokens):
  # stack to store integer values.
  values = []
  # stack to store operators.
  ops = []
  i = 0
  while i < len(tokens):
    # print(tokens[i], values, ops)
    if tokens[i] == '(':
      ops.append(tokens[i])
  
    elif not(tokens[i] in ["AND", "OR", "(", ")"]):
      values.append(tokens[i])
      
    elif tokens[i] == ')':
      while len(ops) != 0 and ops[-1] != '(':
      
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        
        values.append(applyOp(val1, val2, op))
      
      # pop opening brace.
      ops.pop()
    
    # Current token is an operator.
    else:
      while (len(ops) != 0 and
        precedence(ops[-1]) >=
        precedence(tokens[i])):
            
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        
        values.append(applyOp(val1, val2, op))
      
      # Push current token to 'ops'.
      ops.append(tokens[i])
    
    i += 1
  while len(ops) != 0:
    
    val2 = values.pop()
    val1 = values.pop()
    op = ops.pop()
        
    values.append(applyOp(val1, val2, op))
  
  return values[-1]

if __name__ == "__main__":
	
	print(evaluate(["python", "OR", "java"]))
	

