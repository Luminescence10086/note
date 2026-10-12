"""Exact checks for CDX 05A, standard library only."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import re,hashlib

def trim(a):
    a=list(map(F,a))
    while len(a)>1 and not a[-1]: a.pop()
    return a

def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,c): return trim([x*c for x in a])
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)
def div(a,b):
    a=trim(a);b=trim(b);q=[F(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]/b[-1];q[k]+=c
        a=add(a,[0]*k+scale(b,-c))
    return trim(q),a
def gcd(a,b):
    while trim(b)!=[0]: a,b=b,div(a,b)[1]
    return scale(a,1/F(a[-1]))
def der(a): return trim([i*a[i] for i in range(1,len(a))] or [0])
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def ev(p,A):
    n=len(A); out=[[0]*n for _ in range(n)]; power=eye(n)
    for c in p:
        out=[[out[i][j]+c*power[i][j] for j in range(n)] for i in range(n)]
        power=mm(power,A)
    return out
def char(A):
    n=len(A);out=[0]
    for p in permutations(range(n)):
        term=[(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))]
        for i in range(n):term=mul(term,[-A[i][p[i]],int(i==p[i])])
        out=add(out,term)
    return out
A=[[1,1,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,2]]
chi=[4,-12,13,-6,1];mini=[-2,5,-4,1]
assert char(A)==chi
assert ev(chi,A)==ev(mini,A)==[[0]*4 for _ in range(4)]
assert mul(mul([-1,1],[-1,1]),[-2,1])==mini
assert mul(mini,[-2,1])==chi
assert div([1,-2,0,1],[-1,0,1])==([0,1],[1,-1])
assert gcd([-1,0,1],[0,-1,1])==[-1,1]
g=[2,-3,0,1];assert gcd(g,der(g))==[-1,1]
assert gcd([-1,0,0,1],[-1,0,1])==[-1,1]
E=[[2,1,0],[0,2,0],[0,0,-1]]
assert char(E)==[4,0,-3,1]
assert ev([4,0,-3,1],E)==[[0]*3 for _ in range(3)]
h=[3,6,0,1];assert gcd(h,der(h))==[1]
g=mul(mul([1,0,1],[1,0,1]),[-2,1]);assert g==[-2,1,-4,2,-2,1]
assert der(g)==[1,-8,6,-8,5]
assert gcd(g,der(g))==[1,0,1]
for f,p in [([2,2,0,0,1],2),([3,6,0,1],3)]:
    assert f[-1]%p and all(c%p==0 for c in f[:-1]) and f[0]%(p*p)
assert add(scale([3,-1],F(1,2)),scale([-1,1],F(1,2)))==[1]
assert mul([-1,1],scale([3,-1],F(1,2)))==scale(mul([-1,1],[-3,1]),F(-1,2))
assert mul([-3,1],scale([-1,1],F(1,2)))==scale(mul([-1,1],[-3,1]),F(1,2))
print('Characteristic polynomials, annihilation, divisions, gcds, Eisenstein, projectors: PASS')
p=next(Path('professors/MATH/handout_05A_CDX').glob('05A*.md'));s=p.read_text(encoding='utf-8')
assert '$$' not in s and '\ufffd' not in s
assert all(line.count('$')%2==0 for line in s.splitlines())
for match in re.finditer(r'\\sum',s):
    assert re.match(r'\\sum_\{[^}]+\}\^\{[^}]+\}',s[match.start():])
assert len(re.findall(r'^## ',s,re.M))==8 and s.count('```')==2
print('Formatting: PASS')
print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest(),'bytes',p.stat().st_size)