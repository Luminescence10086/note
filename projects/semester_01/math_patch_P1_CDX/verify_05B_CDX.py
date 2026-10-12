"""Exact arithmetic checks for CDX 05B handout, 2026-10-12."""
from fractions import Fraction as F
from itertools import permutations, combinations

def mm(a,b):
    return [[sum(F(x)*F(y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def det(a):
    n=len(a); out=F(0)
    for p in permutations(range(n)):
        v=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n): v*=a[i][p[i]]
        out+=v
    return out
def minor(a,ii,jj): return [[a[i][j] for j in jj] for i in ii]
cases=[('example1',[[1,2,3,4],[3,4,5,6],[0,0,2,1],[0,0,1,3]],-10),('counterexample',[[1,0,2,0],[0,1,0,2],[2,0,1,0],[0,2,0,1]],9),('example2',[[1,1,1,0],[0,1,0,1],[2,0,3,1],[1,1,2,4]],1),('G1',[[1,2,5],[2,4,6],[0,0,3]],0),('G2',[[2,1,0],[1,2,1],[0,1,2]],4),('T2',[[1,2,0],[3,4,5],[0,6,7]],-44)]
for name,a,expected in cases:
    assert det(a)==expected,(name,det(a)); print(name,expected,'PASS')
Ai=[[1,-1],[0,1]]; C=[[2,0],[1,1]]
assert mm(C,Ai)==[[2,-2],[1,0]]
M=cases[2][1]; L=[[1,0,0,0],[0,1,0,0],[-2,2,1,0],[-1,0,0,1]]; R=[[1,0,-1,1],[0,1,0,-1],[0,0,1,0],[0,0,0,1]]
assert mm(mm(L,M),R)==[[1,1,0,0],[0,1,0,0],[0,0,1,3],[0,0,1,4]]
P=[[1,0],[1,F(-1,2)]]; Q=[[1,-1,-2],[0,0,1],[0,1,0]]; A=[[1,2,1],[2,4,0]]
assert mm(mm(P,A),Q)==[[1,0,0],[0,1,0]] and det(P)==F(-1,2) and det(Q)==-1
assert mm(A,[[-2],[1],[0]])==[[0],[0]]
P0=[[1,0],[-2,1]]; Q0=[[1,-2,-3],[0,1,0],[0,0,1]]
assert mm(mm(P0,[[1,2,3],[2,4,6]]),Q0)==[[1,0,0],[0,0,0]]
for t in [F(-2),F(0),F(1),F(3,2),F(4)]:
    N=[[1,0,t,0],[0,1,0,t],[1,0,1,0],[0,1,0,1]]
    assert det(N)==(1-t)**2
# Generalized Laplace: every row subset, including nonconsecutive ones.
H=[[2,3,1,4],[1,-1,2,0],[3,0,1,2],[2,1,4,1]]
for k in range(1,5):
    for ii in combinations(range(4),k):
        ic=[i for i in range(4) if i not in ii]; v=F(0)
        for jj in combinations(range(4),k):
            jc=[j for j in range(4) if j not in jj]
            v+=(-1)**(sum(ii)+sum(jj))*det(minor(H,ii,jj))*det(minor(H,ic,jc))
        assert v==det(H)
print('All exact numerical checks PASS; symbolic proofs reviewed in the handout.')
