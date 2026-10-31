"""Finite exact checks supplement, but do not replace, the proofs in MA105 1-2."""
from pathlib import Path
from fractions import Fraction as F
import json

results = []
def record(name, ok, scope):
    assert ok, name
    results.append(dict(name=name, passed=ok, scope=scope))

record('G1 kernel', [a for a in range(12) if a % 4 == 0] == [0,4,8], 'all residues modulo 12')
record('G1 image', {a % 4 for a in range(12)} == set(range(4)), 'all residues modulo 12')
for modulus in (2,3):
    def phi(a,b): return a % modulus, b-2*a
    for a in range(-10,11):
        for b in range(-10,11):
            assert (phi(a,b)==(0,0)) == (a%modulus==0 and b==2*a)
            for k in range(-3,4):
                assert phi(a+modulus*k,b+2*modulus*k)==phi(a,b)
    for r in range(modulus):
        for c in range(-10,11):
            assert phi(r,c+2*r)==(r,c)
    record(f'quotient modulus {modulus}',True,'integer window: a,b=-10..10; k=-3..3; explicit lift c=-10..10')

def act(p,v):
    # T(v1,v2)=(v2,0), T^2=0; p is coefficient list.
    a = p[0] if len(p)>0 else F(0)
    b = p[1] if len(p)>1 else F(0)
    return a*v[0]+b*v[1], a*v[1]
def multiply(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): out[i+j]+=a*b
    return out
polys = [[F(a),F(b),F(c)] for a in range(-2,3) for b in range(-2,3) for c in range(-1,2)]
for p in polys:
    assert (act(p,(F(0),F(1)))==(0,0)) == (p[0]==0 and p[1]==0)
    for q in polys:
        v=(F(2,3),F(-3,5))
        assert act(multiply(p,q),v)==act(p,act(q,v))
record('polynomial action and kernel',True,'75 polynomials, 5625 products over rational exact arithmetic')

payload={'date':'2026-10-30','status':'PASS','checks':results,'boundary':'Finite examples only. General proofs are reviewed in prose; no formal proof verification claimed.'}
out=Path(__file__).with_name('verification.json')
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(payload,ensure_ascii=False))
