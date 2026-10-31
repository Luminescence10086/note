"""Independent finite group enumeration. No lecture file is modified."""
import itertools, cmath, json, pathlib
TOL=1e-8
checks=[]
def near(a,b,label):
    assert abs(a-b)<TOL,(label,a,b)
    checks.append(label)
def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p): return tuple(p.index(i) for i in range(len(p)))
def parity(p): return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def fixed(p): return sum(i==p[i] for i in range(len(p)))
def classes(G,mul,iv):
    unseen=set(G); out=[]
    while unseen:
        g=min(unseen,key=str); C={mul(mul(x,g),iv(x)) for x in G};out.append(C);unseen-=C
    return out
def validate(name,G,mul,iv,chars):
    C=classes(G,mul,iv);N=len(G); rows=[[f(g) for g in G] for f in chars]
    assert len(chars)==len(C)
    for i,r in enumerate(rows):
        for j,s in enumerate(rows):near(sum(x.conjugate()*y for x,y in zip(map(complex,r),s))/N,int(i==j),f'{name} row {i},{j}')
    for i,c in enumerate(C):
        g=next(iter(c))
        for j,d in enumerate(C):
            h=next(iter(d));near(sum(complex(f(g)).conjugate()*f(h) for f in chars),N/len(c) if i==j else 0,f'{name} col {i},{j}')
        for f in chars:
            for h in c:near(f(g),f(h),f'{name} class constant')
    e=next(g for g in G if all(mul(g,h)==h for h in G))
    near(sum(f(e)**2 for f in chars),N,f'{name} squares')
    return {'order':N,'class_sizes':sorted(map(len,C)),'degrees':[round(f(e).real if isinstance(f(e),complex) else f(e)) for f in chars]}
def decompose(G,chars,values,label):
    m=[sum(complex(f(g)).conjugate()*values(g) for g in G)/len(G) for f in chars]
    for x in m:near(x,round(x.real),label+' integral'); assert x.real> -TOL
    for g in G:near(sum(x*f(g) for x,f in zip(m,chars)),values(g),label+' reconstruct')
    return [round(x.real) for x in m]
S3=list(itertools.permutations(range(3)));S4=list(itertools.permutations(range(4)));A4=[p for p in S4 if parity(p)==1]
c3=[lambda p:1,parity,lambda p:fixed(p)-1]
# S4 acts on the three partitions into two unordered pairs.
parts={frozenset((frozenset((0,i)),frozenset(set(range(4))-{0,i}))) for i in (1,2,3)}
def pairchar(p):return sum(frozenset(frozenset(p[x] for x in pair) for pair in part)==part for part in parts)-1
c4=[lambda p:1,parity,lambda p:fixed(p)-1,lambda p:parity(p)*(fixed(p)-1),pairchar]
# Construct A4 -> C3 using actual cosets of the Klein subgroup.
K={p for p in A4 if p==tuple(range(4)) or (fixed(p)==0 and compose(p,p)==tuple(range(4)))}
a=(1,2,0,3); reps=[tuple(range(4)),a,compose(a,a)]
cosets=[{compose(t,k) for k in K} for t in reps];w=cmath.exp(2j*cmath.pi/3)
def ac(p):return w**next(i for i,C in enumerate(cosets) if p in C)
ca=[lambda p:1,ac,lambda p:ac(p)**2,lambda p:fixed(p)-1]
# D4: actual square vertex permutations; rotations and reflections.
r=(1,2,3,0);s=(0,3,2,1);e=(0,1,2,3)
powers=[e]
for _ in range(3):powers.append(compose(r,powers[-1]))
D=[compose(p,s) if b else p for b in (0,1) for p in powers]
coords={compose(p,s) if b else p:(i,b) for b in (0,1) for i,p in enumerate(powers)}
cd=[lambda p,a=a,b=b:a**coords[p][0]*b**coords[p][1] for a,b in itertools.product((1,-1),repeat=2)]
cd.append(lambda p:0 if coords[p][1] else (2,0,-2,0)[coords[p][0]])
# Quaternion multiplication from basis multiplication, independent of character table.
Q=list(itertools.product((1,-1),range(4)))
def qm(x,y):
    a,i=x;b,j=y
    if i==0:return a*b,j
    if j==0:return a*b,i
    if i==j:return -a*b,0
    sign=1 if (i,j) in ((1,2),(2,3),(3,1)) else -1
    return a*b*sign,6-i-j
def qi(x):return (x[0],0) if x[1]==0 else (-x[0],x[1])
cq=[lambda x,a=a,b=b:(1,a,b,a*b)[x[1]] for a,b in itertools.product((1,-1),repeat=2)]
cq.append(lambda x:2*x[0] if x[1]==0 else 0)
out={}
for name,G,mul,iv,cs in [('S3',S3,compose,inv,c3),('S4',S4,compose,inv,c4),('A4',A4,compose,inv,ca),('D4',D,compose,inv,cd),('Q8',Q,qm,qi,cq)]:out[name]=validate(name,G,mul,iv,cs)
out['decompositions']={}
for name,G,mul,cs in [('S3',S3,compose,c3),('A4',A4,compose,ca),('D4',D,compose,cd),('Q8',Q,qm,cq)]:
    f=cs[-1]
    for typ,values in [('tensor',lambda g,f=f:f(g)**2),('sym2',lambda g,f=f,mul=mul:(f(g)**2+f(mul(g,g)))/2),('wedge2',lambda g,f=f,mul=mul:(f(g)**2-f(mul(g,g)))/2)]:
        out['decompositions'][name+' '+typ]=decompose(G,cs,values,name+' '+typ)
# Induced traces counted by all conjugating elements, not preset expected rows.
H2=[(0,1,2),(1,0,2)];H3=[p for p in S3 if parity(p)==1];a3=(1,2,0);h3=[(0,1,2),a3,compose(a3,a3)]
for name,H,psi in [('C2 trivial',H2,lambda h:1),('C2 sign',H2,parity),('C3 trivial',H3,lambda h:1),('C3 nontrivial',H3,lambda h:w**h3.index(h))]:
    def induced(g,H=H,psi=psi):
        ys=[compose(compose(inv(x),g),x) for x in S3]
        return sum(psi(y) for y in ys if y in H)/len(H)
    out['decompositions']['ind '+name]=decompose(S3,c3,induced,name)
# Nonabelian Fourier check uses actual 2D standard matrices, not just characters.
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return sum(A[i][i] for i in range(len(A)))
def std(p):
    cols=[]
    for v in ((1,0,-1),(0,1,-1)):
        y=[0,0,0]
        for i in range(3):y[p[i]]=v[i]
        cols.append(y[:2])
    return [[cols[j][i] for j in range(2)] for i in range(2)]
rhos=[lambda p:[[1]],lambda p:[[parity(p)]],std]
for p in S3:
    for q in S3:
        A=mm(std(p),std(q));B=std(compose(p,q))
        for i in range(2):
            for j in range(2):near(A[i][j],B[i][j],'standard homomorphism')
f={g:complex(i*i-2*i,(-1)**i) for i,g in enumerate(S3)};h={g:complex(3-i,i%3) for i,g in enumerate(S3)}
def hat(f,rho):
    d=len(rho(S3[0]));return [[sum(f[g]*rho(inv(g))[i][j] for g in S3)/6 for j in range(d)] for i in range(d)]
F=[hat(f,rho) for rho in rhos]
for g in S3:near(sum(len(B)*tr(mm(rho(g),B)) for rho,B in zip(rhos,F)),f[g],'nonabelian inversion')
conv={g:sum(f[a]*h[compose(inv(a),g)] for a in S3)/6 for g in S3}
for rho in rhos:
    C=hat(conv,rho);P=mm(hat(h,rho),hat(f,rho)) # inverse convention reverses matrix order
    for i in range(len(C)):
        for j in range(len(C)):near(C[i][j],P[i][j],'nonabelian convolution reversed order')
out['fourier']={'group':'S3','function':'f(g_i)=i^2-2i+(-1)^i sqrt(-1), lexicographic permutations','normalization':'1/6; inverse rho in transform','convolution_order':'hat(f*h)=hat(h)hat(f)','warning':'Lecture only asserts scalar abelian version; this is an extra nonabelian boundary check.'}
out['checks']=len(checks);out['status']='PASS';out['scope']='S4 complete table independently constructed here; lecture only uses S4 permutation and standard rows.'
path=pathlib.Path(__file__).with_name('verification_results.json');path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
