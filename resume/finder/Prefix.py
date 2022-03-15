class Prefix(): 
    #infix=[ '(','Python', 'AND', 'Django',')' ,'OR','(','ROR','AND', 'JAva',')']
    stack=[]
    prefix=[]
    #global top 
    top = -1
    def __init__(self,infix) -> None:
        self.infix=infix
        
    def push(self,pos):
        #global top
        self.top+=1
        self.stack.append(self.infix[pos])

    def pop(self):
       # global top
        s=""
        if self.top<0:
            print("uf")
        else:
            s=s+self.stack[self.top]
            self.top-=1
        return(s)
    def infix_to_prefix(self):
        self.infix.reverse()
        for i,val in enumerate(self.infix):
            if not(self.infix[i]=='AND' or self.infix[i]=='OR' or self.infix[i]=='(' or self.infix[i]==')'):
                self.prefix.append(self.infix[i])
            elif self.infix[i]==')':
                self.push(i)
                self.prefix.append(')')
            elif self.infix[i]=='(':
                while self.stack[self.top]!=')':
                    self.prefix.append(self.pop())
                self.prefix.append('(')
                self.pop()

            else:
                self.push(i)
        while (self.top!=-1):
            self.prefix.append(self.pop())
        
        self.prefix.reverse()
        

   
# p = Prefix([ '(','Python', 'AND', 'Django',')' ,'OR','(','ROR','AND', 'JAva',')'])
# p.infix_to_prefix()
# print (p.prefix)