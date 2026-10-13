"""MA301 independent checks, CDX, 2026-10-13. Standard library only."""
from fractions import Fraction as F
from itertools import product,combinations
from math import comb,exp,log,log2,sqrt,pi,lgamma,ceil,factorial
from pathlib import Path
import json
results=[]
def check(name,actual,expected,tol=0):
    assert abs(actual-expected)<=tol,(name,actual,expected)
    results.append({'check':name,'actual':str(actual),'expected':str(expected),'tolerance':tol})
def moments(values,weights):
    m=sum(x*p for x,p in zip(values,weights)); v=sum((x-m)**2*p for x,p in zip(values,weights));return m,v

def integrate(f,a,b,n=4000):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+4*sum(f(a+(2*k-1)*h) for k in range(1,n//2+1))+2*sum(f(a+2*k*h) for k in range(1,n//2)))

def solve(A,b):
    A=[list(map(F,row))+[F(v)] for row,v in zip(A,b)]; n=len(A)
    for i in range(n):
        j=next(j for j in range(i,n) if A[j][i]); A[i],A[j]=A[j],A[i]
        c=A[i][i];A[i]=[v/c for v in A[i]]
        for j in range(n):
            if j!=i:
                c=A[j][i];A[j]=[x-c*y for x,y in zip(A[j],A[i])]
    return [row[-1] for row in A]

def ruin(N,p):
    q=1-p; A=[[F(int(i==j))-p*int(j==i+1)-q*int(j==i-1) for j in range(N-1)] for i in range(N-1)]
    b=[F(0)]*(N-1);b[-1]=p
    return solve(A,b),solve(A,[1]*(N-1))

def pois(lam,k):return exp(-lam)*lam**k/factorial(k)
def entropy(p):return -sum(x*log2(x) for x in p if x)
# Enumeration of finite sample spaces rather than substitution in claimed answers.
pairs=list(combinations(range(5),2))
check('G1 committee',F(sum(0 in s or 1 in s for s in pairs),len(pairs)),F(7,10))
for c in [F(1,10),F(1,2)]:
    cells=[c,F(3,5)-c,F(1,2)-c,1-F(3,5)-F(1,2)+c]
    assert min(cells)>=0 and sum(cells)==1
results.append({'check':'I1 intersection bounds','actual':'both endpoints realized by nonnegative four-cell tables'})
check('L1 dice example',F(sum(a+b==7 for a,b in product(range(1,7),repeat=2)),36),F(1,6))
check('L2 Bayes example',F(9,100)/(F(9,100)+F(9,100)),F(1,2))
check('G2 Bayes',F(3,8)/(F(3,8)+F(1,8)),F(3,4))
for a,b in product([F(0),F(1,3),F(1)],repeat=2):check('I2 complement independence',a-a*b,a*(1-b))
check('G3 left limit',F(1,4),F(1,4));check('G3 at zero',F(1,4)+F(1,2),F(3,4));check('G3 at one',F(1,4)+F(1,2)+F(1,4),1)
assert [(1-x) for x in [0,1]]==[1,0]
check('G4 geometric tail',1-sum(F(1,4)*F(3,4)**(k-1) for k in range(1,4)),F(27,64))
check('G5 exponential conditional tail',exp(-2*3)/exp(-2*1),exp(-4),1e-14)
check('I5 density normalization',F(1,2)*F(2**2,2),1)
check('I5 probability',F(1,2)*F(1,2),F(1,4))
m,v=moments([0,1,2],[F(1,4),F(1,2),F(1,4)])
check('G6 mean',m,1);check('G6 variance',v,F(1,2))
check('I6 shifted Poisson square',sum((k+1)**2*pois(3,k) for k in range(100)),19,1e-11)
check('G7 sufficient sample bound',2*exp(-2*ceil(log(40)/(.02))*.01)<=.05,True)
check('I7 Markov equality',F(1,5)*10,2)
coins=list(product([0,1],repeat=2))
for k,p in enumerate([F(1,4),F(1,2),F(1,4)]):check('G8 convolution',F(sum(sum(c)==k for c in coins),4),p)
J={(0,0):F(3,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(3,8)}
mx=sum(x*p for (x,y),p in J.items());my=sum(y*p for (x,y),p in J.items())
cov=sum(x*y*p for (x,y),p in J.items())-mx*my
cond=[sum(x*p for (x,z),p in J.items() if z==y)/sum(p for (x,z),p in J.items() if z==y) for y in [0,1]]
check('I8/G9 condition0',cond[0],F(1,4));check('I8/G9 condition1',cond[1],F(3,4));check('G9 covariance',cov,F(1,8));check('G9 correlation',cov/F(1,4),F(1,2))
residual=sum((x-cond[y])**2*p for (x,y),p in J.items())
predvar=sum((cond[y]-mx)**2*p for (x,y),p in J.items())
check('I9 total variance',residual+predvar,F(1,4))
check('L9 projection cross term',sum((x-cond[y])*(cond[y]-mx)*p for (x,y),p in J.items()),0)
check('G10 random sum mean',sum(3*k*pois(2,k) for k in range(100)),6,1e-11)
check('G10 random sum variance',sum((3*k-6)**2*pois(2,k) for k in range(100)),18,1e-10)
for k in range(6):
    val=sum(F(comb(2,j),4)*F(comb(3,k-j),8) for j in range(3) if 0<=k-j<=3)
    check('I10 binomial sum',val,F(comb(5,k),32))
check('G11 Chebyshev sample size',F(4,8000)/F(1,100),F(1,20))
check('G12 standardization n=9 mean=3',sqrt(9)*(3-2)/3,1)
check('I12 incorrectly scaled variance n=9',F(9,9*9),F(1,9))
h,e=ruin(5,F(1,2));check('L13 h2',h[1],F(2,5));check('L13 e2',e[1],6);check('G13 h4',h[3],F(4,5));check('G13 e4',e[3],4)
h,e=ruin(10,F(1,2));check('T3.1 probability',h[2],F(3,10));check('T3.1 duration',e[2],21)
h,e=ruin(7,F(3,5)); r=F(2,3)
for i,v in enumerate(h,1):check('L13 biased ruin formula',v,(1-r**i)/(1-r**7))
# Exhaustive reflection counts over short paths, every reachable b<a.
for n in range(1,9):
    paths=list(product([-1,1],repeat=n))
    endings=[]
    for path in paths:
        cur=0;ma=0
        for x in path:cur+=x;ma=max(ma,cur)
        endings.append((cur,ma))
    for a in range(1,n+1):
        for b in range(-n,a):
            check('L13 reflection enumeration',sum(end==b and ma>=a for end,ma in endings),sum(end==2*a-b for end,ma in endings))
check('G14 mean waiting',integrate(lambda t:exp(-3*t),0,12),1/3,1e-8)
check('G14 tail',exp(-3*2),exp(-6))
# Poisson thinning joint mass via conditioning on total count.
for r,b in product(range(5),repeat=2):
    lhs=pois(2,r+b)*comb(r+b,r)*(.25**r)*(.75**b)
    check('L14 thinning independence',lhs,pois(.5,r)*pois(1.5,b),1e-14)
check('L14 conditional thinning covariance',-4*F(1,4)*F(3,4),F(-3,4))
for a,target in [(F(1,4),F(1,3)),(F(1,2),F(1)),(F(1,3),F(1,2))]:check('L15/G15/T3 branch fixed point',a+(1-a)*target**2,target)
q=F(0)
for _ in range(8):q=q*q
check('I15 deterministic branching minimal point',q,0)
check('G16 minimum exponentials',exp(-2*.7)**3,exp(-6*.7),1e-14)
check('I16 median density integral',integrate(lambda x:6*x*(1-x),0,1),1,1e-12)
check('I16 median mean',integrate(lambda x:6*x*x*(1-x),0,1),.5,1e-12)
check('L16 maximum mean',integrate(lambda x:2*x*x,0,1),2/3,1e-12)
check('G17 integral mean',F(1,3),F(1,3));check('G17 variance',F(1,5)-F(1,3)**2,F(4,45))
check('I17 rejection mean attempts',sum(k*.5**k for k in range(100)),2,1e-12)
for epsilon,target in [(0,1),(.5,0),(1,1)]:check('G18 binary mutual information',1-entropy([epsilon,1-epsilon]),target)
weights=[F(4,7),F(3,7)];lams=[.5,4.0]
mean=sum(float(w)*sum(k*pois(l,k) for k in range(100)) for w,l in zip(weights,lams))
var=sum(float(w)*sum((k-2)**2*pois(l,k) for k in range(100)) for w,l in zip(weights,lams))
check('I18 mixed Poisson mean',mean,2,1e-11);check('I18 mixed Poisson variance',var,5,1e-10)
triples=list(product([0,1],repeat=3)); A=[c for c in triples if sum(c)>=2];B=[c for c in triples if c[0]==1]
check('T1.1 P(A)',F(len(A),8),F(1,2));check('T1.1 conditional',F(len([c for c in A if c in B]),len(B)),F(3,4))
choices=list(combinations(range(10),2));check('T1.2 hypergeom',F(sum(sum(v<3 for v in c)==1 for c in choices),len(choices)),F(7,15))
check('T1.3 density integral',integrate(lambda x:3*x*x,0,1),1,1e-12);check('T1.3 density at half',3*.5**2,.75)
check('T2.1 variance',sum((x-mx)**2*p for (x,y),p in J.items()),F(1,4))
# Integral and moment checks beyond individual answers.
check('L5 Gaussian normalization',integrate(lambda x:exp(-x*x/2)/sqrt(2*pi),-9,9),1,1e-12)
check('L6 Gaussian variance',integrate(lambda x:x*x*exp(-x*x/2)/sqrt(2*pi),-9,9),1,1e-11)
check('L8 triangular convolution integral',integrate(lambda z:z,0,1)+integrate(lambda z:2-z,1,2),1,1e-12)
for N,K,n in [(10,3,2),(5,2,2),(12,5,7)]:
    lo=max(0,n-(N-K)); hi=min(n,K); values=list(range(lo,hi+1))
    ps=[F(comb(K,k)*comb(N-K,n-k),comb(N,n)) for k in values]
    m,v=moments(values,ps);check('L6 hypergeom mean',m,F(n*K,N));check('L6 hypergeom variance',v,n*F(K,N)*(1-F(K,N))*F(N-n,N-1))
for prob in [F(1,5),F(1,2),F(4,5)]:
    for t in [-3,-1,.2,1,3]:
        m=float(prob);mgf=(1-m)*exp(-t*m)+m*exp(t*(1-m))
        assert mgf<=exp(t*t/8)+1e-12
results.append({'check':'Hoeffding bounded Bernoulli numerical spotchecks','actual':'15 parameter pairs passed; proof remains analytic'})
# DML local approximation: numerical evidence, not proof of a limit.
errors=[]
for n in [100,1000,10000]:
    p=.4;q=.6; k=round(n*p+sqrt(n*p*q));z=(k-n*p)/sqrt(n*p*q)
    mass=exp(lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)+k*log(p)+(n-k)*log(q))
    approx=exp(-z*z/2)/sqrt(2*pi*n*p*q);errors.append(abs(mass/approx-1))
assert errors[-1]<.01
results.append({'check':'DML local approximation samples n=100,1000,10000','actual':str(errors),'note':'finite numerical evidence only'})
# Deterministic numerical validation of inverse-transform and rejection laws.
check('L17 inverse exponentials F(1)',1-exp(-2),1-exp(-2))
check('L17 rejection acceptance',integrate(lambda y:y,0,1),.5,1e-12)
check('L17 accepted first moment',integrate(lambda y:y*y,0,1)/.5,2/3,1e-12)
Path(__file__).with_name('numerical_results.json').write_text(json.dumps({'status':'PASS','count':len(results),'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(results),'checks. Exact rational enumeration + deterministic quadrature; no project simulations run.')
# Check the actual submission version after all edits.
import re,hashlib
root=Path.cwd()
doc=root/'professors'/'MATH'/'handout_MA301_CDX'
# Resolve by content status, independent of localized file name.
candidates=[p for p in doc.glob('*.md') if 'v0.1-selfchecked' in p.read_text(encoding='utf-8')]
assert len(candidates)==1
text=candidates[0].read_text(encoding='utf-8')
assert '$$' not in text and '\ufffd' not in text
assert all(line.count('$')%2==0 for line in text.splitlines())
assert len(re.findall(r'^## \u7b2c \d+ ',text,re.M))==18
assert text.count('```mermaid')==18 and text.count('```')==36
for m in re.finditer(r'\\sum',text):assert re.match(r'\\sum_\{[^}]+\}\^\{[^}]+\}',text[m.start():])
assert '\\\\' not in text  # No unintended doubled LaTeX escapes; no matrices in this handout.
print('Submission UTF-8/math delimiters/sum bounds/18 lectures/18 diagrams: PASS')
print('Submission SHA256',hashlib.sha256(candidates[0].read_bytes()).hexdigest())