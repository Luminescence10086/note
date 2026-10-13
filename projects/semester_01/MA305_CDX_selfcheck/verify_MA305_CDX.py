"""CDX author checks: finite/exact examples and deterministic quadrature, not theorem proofs."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations
import math, re, json, hashlib
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'professors/MATH/handout_MA305_CDX/MA305_数理统计_16讲_自校稿_CDX.md'
results=[]
def check(name,actual,expected,tol=0):
    ok=abs(float(actual)-float(expected))<=tol if isinstance(actual,(int,float,Q)) and isinstance(expected,(int,float,Q)) else actual==expected
    results.append(dict(name=name,actual=str(actual),expected=str(expected),tolerance=tol,passed=ok))
def mean(v):return sum(v)/len(v)
def ss(v):return sum((x-mean(v))**2 for x in v)
def transpose(A):return [list(x) for x in zip(*A)]
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sub(A,B):return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def inv(A):
 n=len(A);M=[list(map(Q,A[i]))+eye(n)[i] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if M[k][j]);M[j],M[k]=M[k],M[j]
  c=M[j][j];M[j]=[x/c for x in M[j]]
  for i in range(n):
   if i!=j:
    c=M[i][j];M[i]=[x-c*y for x,y in zip(M[i],M[j])]
 return [r[n:] for r in M]
def mv(A,v):return [sum(a*b for a,b in zip(r,v)) for r in A]
def simpson(f,a,b,n=12000):
 h=(b-a)/n
 return h/3*(f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*h) for i in range(1,n)))
def normal_cdf(z):return .5*(1+math.erf(z/math.sqrt(2)))
def tpdf(x,nu):return math.gamma((nu+1)/2)/(math.sqrt(nu*math.pi)*math.gamma(nu/2))*(1+x*x/nu)**(-(nu+1)/2)
def tcdf(x,nu):return .5+simpson(lambda y:tpdf(y,nu),0,x,n=2000)
def quantile(cdf,u,a,b):
 for _ in range(45):
  m=(a+b)/2
  if cdf(m)<u:a=m
  else:b=m
 return (a+b)/2
# Lectures 1-4, direct finite observations and risk formulas.
x=list(map(Q,[1,2,3]))
check('example1_mean',mean(x),Q(2));check('example1_S2',ss(x)/2,Q(1));check('example1_ML_variance',ss(x)/3,Q(2,3))
for t,e in [(1.5,Q(1,3)),(2,Q(2,3)),(4,Q(1))]:check('G1_EDF_'+str(t),Q(sum(z<=t for z in x),3),e)
check('G2_F_scaling',Q(8,4)/Q(14,7),Q(7*8,4*14));check('example2_df',6-1,5)
check('example3_Exp_MLE',Q(len(x),sum(x)),Q(1,2));check('G3_Bern_MLE',mean([Q(z) for z in [1,0,1,1,0]]),Q(3,5))
check('I3_uniform_MOM',2*mean(x),Q(4));check('I3_uniform_MLE',max(x),Q(3));check('G4_MSE',Q(1,5)**2+Q(9,100),Q(13,100))
for n in [2,3,5,10]:
 for p in [Q(1,5),Q(1,2),Q(4,5)]:
  vals=[(Q(k+1,n+2),Q(math.comb(n,k))*p**k*(1-p)**(n-k)) for k in range(n+1)]
  m=sum(v*w for v,w in vals);v=sum(w*(z-m)**2 for z,w in vals)
  check(f'I4_bias_n{n}_p{p}',m-p,(1-2*p)/(n+2));check(f'I4_var_n{n}_p{p}',v,n*p*(1-p)/(n+2)**2)
 for nu in [n-1]:
  check(f'T1.2_ML_MSE_n{n}',Q(2*(n-1)+1,n*n),Q(2*n-1,n*n))
  check(f'T1.2_ML_less_n{n}',Q(2*n-1,n*n)<Q(2,n-1),True)
# S2 unbiased under a finite, non-normal model, not assuming Gaussianity.
vals=[Q(0),Q(1),Q(3)];mu=mean(vals);var=mean([(z-mu)**2 for z in vals])
for n in [2,3,4]:
 samples=list(product(vals,repeat=n))
 check(f'lecture4_S2_unbiased_nonNormal_n{n}',mean([ss(s)/(n-1) for s in samples]),var)
# Sufficiency / RB and Fisher information in finite models.
for n in [2,4]:
 for k in range(n+1):
  samples=[s for s in product([0,1],repeat=n) if sum(s)==k]
  check(f'I5_RaoBlackwell_n{n}_sum{k}',mean([Q(s[0]) for s in samples]),Q(k,n))
for p in [Q(1,5),Q(1,2),Q(4,5)]:
 score=[(Q(x)-p)/(p*(1-p)) for x in [0,1]]
 check(f'CR_Bern_score_mean_p{p}',(1-p)*score[0]+p*score[1],Q(0))
 check(f'CR_Bern_info_p{p}',(1-p)*score[0]**2+p*score[1]**2,1/(p*(1-p)))
# Poisson convergent sum validates numeric information calculation.
for lam in [0.5,2.,7.]:
 masses=[math.exp(-lam)*lam**k/math.factorial(k) for k in range(100)]
 check(f'G6_Pois_score_mean_{lam}',sum(w*(k/lam-1) for k,w in enumerate(masses)),0,1e-12)
 check(f'G6_Pois_info_{lam}',sum(w*(k/lam-1)**2 for k,w in enumerate(masses)),1/lam,1e-12)
check('Uniform_CR_counterexample_var',Q(4,12),Q(1,3))
# Density quadratures: square-root / trigonometric transformations avoid singular endpoints.
for nu in [1,2,5,10]:
 c=2/(2**(nu/2)*math.gamma(nu/2))
 f=lambda z:c*z**(nu-1)*math.exp(-z*z/2)
 for power,expected in [(0,1),(1,nu),(2,nu*(nu+2))]:
  check(f'chi2_df{nu}_moment{power}',simpson(lambda z:f(z)*z**(2*power),0,15),expected,2e-7)
for nu in [1,2,5,9]:
 c=math.gamma((nu+1)/2)/(math.sqrt(math.pi)*math.gamma(nu/2))
 # t=sqrt(nu)*tan(theta), transformed density proportional to cos(theta)^(nu-1)
 check(f't_df{nu}_normalization',simpson(lambda a:c*math.cos(a)**(nu-1),-math.pi/2,math.pi/2),1,2e-8)
 if nu>2:
  check(f't_df{nu}_variance',simpson(lambda a:nu*c*math.sin(a)**2*math.cos(a)**(nu-3),-math.pi/2,math.pi/2),nu/(nu-2),2e-8)
for r,s in [(1,1),(4,7),(1,5),(3,8)]:
 a,b=r/2,s/2;c=2*math.gamma(a+b)/(math.gamma(a)*math.gamma(b))
 check(f'F_{r}_{s}_normalization',simpson(lambda u:c*math.sin(u)**(r-1)*math.cos(u)**(s-1),0,math.pi/2),1,2e-8)
 if s>2:
  check(f'F_{r}_{s}_mean',simpson(lambda u:s/r*c*math.sin(u)**(r+1)*math.cos(u)**(s-3),0,math.pi/2),s/(s-2),2e-8)
# CI algebra and quantile directions, not a student coverage simulation.
check('example7_known_sigma_SE',Q(2,4),Q(1,2));check('G7_SE_squared',(ss(x)/2)/3,Q(1,3))
check('I7_length_ratio',math.sqrt(16/64),.5)
z=quantile(normal_cdf,.975,0,5);check('normal_95_quantile',z,1.95996398454,1e-10)
for n,k in [(10,0),(10,3),(10,10),(100,40)]:
 p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z/den*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
 for q in [center-half,center+half]:
  check(f'Wilson_boundary_n{n}_k{k}_q{q:.6f}',n*(p-q)**2-z*z*q*(1-q),0,2e-12)
# NP finite sample exact levels and alternative power. Enumerate all rules on a grid.
p0=[Q(1,4),Q(1,2),Q(1,4)];p1=[Q(1,16),Q(6,16),Q(9,16)]
for name,phi,level,power in [('example8_basic',[Q(0),Q(0),Q(1)],Q(1,4),Q(9,16)),('example8_rand',[Q(0),Q(0),Q(2,5)],Q(1,10),Q(9,40)),('G8',[Q(0),Q(1),Q(1)],Q(3,4),Q(15,16)),('T2.3',[Q(0),Q(1,2),Q(1)],Q(1,2),Q(3,4))]:
 check(name+'_level',sum(a*b for a,b in zip(phi,p0)),level);check(name+'_power',sum(a*b for a,b in zip(phi,p1)),power)
 if name in ['example8_rand','T2.3']:
  feasible=[sum(a*b for a,b in zip(v,p1)) for v in product([Q(i,10) for i in range(11)],repeat=3) if sum(a*b for a,b in zip(v,p0))<=level]
  check(name+'_best_on_grid',max(feasible),power)
check('example9_Pearson',sum(Q((c-25)**2,25) for c in [30,20,25,25]),Q(2))
check('G9_pooled',Q(2+2,4),Q(1));check('G9_t_squared',Q(4)/Q(2,3),Q(6));check('G9_df',3+3-2,4)
check('example10_GLR',16*1/4,4);check('example10_chi1_tail',math.erfc(math.sqrt(4/2)),2*(1-normal_cdf(2)),1e-15)
check('G10_unknown_GLR',10*math.log(1+4/9),10*math.log(13/9),1e-14)
check('G10_t9_p_two_tail',2*(1-tcdf(2,9)),0.07655282377,2e-10)
# Exact projection and restriction matrices.
D=[[Q(1),Q(-1)],[Q(1),Q(0)],[Q(1),Q(1)]];y=[Q(1),Q(2),Q(4)]
B=inv(mm(transpose(D),D));A=mm(B,transpose(D));H=mm(D,A);E=sub(eye(3),H)
b=mv(A,y);fitted=mv(H,y);e=mv(E,y)
check('example11_beta',b,[Q(7,3),Q(3,2)]);check('example11_fitted',fitted,[Q(5,6),Q(7,3),Q(23,6)])
check('example11_residual',e,[Q(1,6),Q(-1,3),Q(1,6)]);check('example11_RSS',sum(z*z for z in e),Q(1,6))
check('hat_symmetric',H,transpose(H));check('hat_idempotent',mm(H,H),H);check('hat_trace',sum(H[i][i] for i in range(3)),Q(2))
check('residual_orthogonal',mv(transpose(D),e),[Q(0),Q(0)])
check('projection_cross_cov',mm(H,E),[[Q(0)]*3 for _ in range(3)])
# Nontrivial alternative unbiased linear estimator: C D=0 and PSD covariance increment.
C=[[Q(1),Q(-2),Q(1)],[Q(2),Q(-4),Q(2)]]
check('GaussMarkov_CDzero',mm(C,D),[[Q(0)]*2 for _ in range(2)])
Ap=[[a+c for a,c in zip(r,s)] for r,s in zip(A,C)]
check('GaussMarkov_cov_increment',sub(mm(Ap,transpose(Ap)),B),mm(C,transpose(C)))
for av in [[Q(1),Q(0)],[Q(0),Q(1)],[Q(1),Q(-1)]]:
 check('GaussMarkov_nonnegative_'+str(av),sum(u*v for u,v in zip(av,mv(mm(C,transpose(C)),av)))>=0,True)
# Test slope zero: constrained model has constant fit, extra RSS=quadratic restriction.
RSS1=sum(v*v for v in e);RSS0=ss(y);extra=b[1]**2/B[1][1]
check('lecture12_restricted_RSS_difference',RSS0-RSS1,extra)
check('lecture12_F_equals_t_squared',extra/RSS1,b[1]**2/(RSS1*B[1][1]))
check('G11_intercept_mean',mean(y),Q(7,3));check('G12_intercept_s2',ss(y)/2,Q(7,3))
def anova(groups):
 flat=[Q(z) for g in groups for z in g];grand=mean(flat)
 between=sum(len(g)*(mean([Q(z) for z in g])-grand)**2 for g in groups)
 within=sum(ss([Q(z) for z in g]) for g in groups)
 return between,within,(between/(len(groups)-1))/(within/(len(flat)-len(groups)))
check('example12_ANOVA',anova([[1,3],[3,5]]),(Q(4),Q(4),Q(2)))
check('T3.3_ANOVA',anova([[1,3],[3,5],[5,7]]),(Q(16),Q(6),Q(4)))
# Conjugate updates from normalized likelihood-prior products.
for a,b,n,s,label in [(2,2,4,3,'example13'),(1,1,10,8,'T3.2_flat'),(5,5,10,8,'T3.2_concentrated')]:
 A0,B0=a+s,b+n-s
 density=lambda p:p**(A0-1)*(1-p)**(B0-1)
 norm=simpson(density,0,1)
 check(label+'_mean_by_integral',simpson(lambda p:p*density(p),0,1)/norm,A0/(A0+B0),1e-10)
 mode=(A0-1)/(A0+B0-2)
 check(label+'_mode_stationarity',(A0-1)/mode-(B0-1)/(1-mode),0,1e-12)
check('example13_mean',Q(2+3,2+2+4),Q(5,8));check('example13_MAP',Q(2+3-1,2+2+4-2),Q(2,3))
# Gamma posterior G13: exp(lambda*sum log prior ...) reduces Gamma(7,5).
f=lambda l:l**6*math.exp(-5*l)
norm=simpson(f,0,20)
check('G13_gamma_posterior_mean',simpson(lambda l:l*f(l),0,20)/norm,1.4,1e-10)
check('I13_normal_v',1/(4+1),.2,1e-15);check('I13_normal_m',8/(4+1),1.6,1e-15)
check('I13_predictive_variance',1+1/(4+1),1.2,1e-15)
check('lecture14_excess_square_loss',(Q(2,3)-Q(5,8))**2,Q(1,576))
posterior=[(Q(0),Q(3,4)),(Q(10),Q(1,4))]
m=sum(v*p for v,p in posterior);check('G14_mean',m,Q(5,2))
check('G14_absolute_best',sum(p*abs(v) for v,p in posterior)<=sum(p*abs(v-m) for v,p in posterior),True)
check('I14_positive_risk',Q(9)*Q(1,5),Q(9,5));check('I14_negative_risk',Q(4,5),Q(4,5))
# Bootstrap mean exact enumeration of 27 ordered draws, permutation all 6 allocations.
means=[mean(s) for s in product(x,repeat=3)]
check('example15_boot_mean',mean(means),Q(2));check('example15_boot_var',mean([(v-mean(means))**2 for v in means]),Q(2,9))
for n in [2,3,5]:
 draws=list(product(range(n),repeat=n))
 check(f'bootstrap_max_atom_n{n}',Q(sum(n-1 in s for s in draws),len(draws)),1-Q(n-1,n)**n)
vals=[Q(1),Q(2),Q(3),Q(4)];stats=[]
for comb in combinations(range(4),2):
 stats.append(abs(mean([vals[i] for i in comb])-mean([vals[i] for i in range(4) if i not in comb])))
check('example15_perm_stats',stats,[Q(2),Q(1),Q(0),Q(0),Q(1),Q(2)])
check('example15_perm_p',Q(sum(t>=2 for t in stats),len(stats)),Q(1,3))
check('G15_basic_interval',(2*5-8,2*5-3),(2,7))
# Model selection arithmetic and Poisson exposures.
check('example16_AIC_A',200+2*2,204);check('example16_AIC_B',194+2*5,204)
check('example16_BIC_difference',(-2*(-97)+5*math.log(100))-(-2*(-100)+2*math.log(100)),-6+3*math.log(100),1e-12)
check('G16_AIC_diff',2*3,6);check('example16_exposure_rate',Q(2+4,1+2),Q(2))
check('lecture16_train_trace',sum(E[i][i] for i in range(3)),Q(1));check('lecture16_new_trace',3+sum(H[i][i] for i in range(3)),Q(5))
# Self-tests T1.1 integration and T1.3 / T2.4 exact observations.
for n in [1,2,5,10]:
 m1=simpson(lambda z:n*z**n,0,1);m2=simpson(lambda z:n*z**(n+1),0,1)
 check(f'T1.1_max_mean_n{n}',m1,n/(n+1),1e-10)
 check(f'T1.1_max_var_n{n}',m2-m1*m1,n/((n+2)*(n+1)**2),1e-10)
 check(f'T1.1_MSE_n{n}',m2-2*m1+1,2/((n+1)*(n+2)),1e-10)
check('T1.3_mean',mean([Q(1),Q(2),Q(3),Q(4)]),Q(5,2));check('T1.3_RSS',ss([Q(1),Q(2),Q(3),Q(4)]),Q(5))
check('T1.3_mean_SE_squared',Q(5,3)/4,Q(5,12));check('T2.4_Pearson',sum(Q((z-25)**2,25) for z in [30,20,20,30]),Q(4))
# Independent posterior and predictive moment integrals, and exact-CDF interval calibration.
f=lambda m:math.exp(-sum((z-m)**2 for z in [1.,2.,2.,3.])/2-m*m/2)
normalizer=simpson(f,-10,10)
pmean=simpson(lambda m:m*f(m),-10,10)/normalizer
pvar=simpson(lambda m:(m-pmean)**2*f(m),-10,10)/normalizer
check('I13_posterior_mean_integrated',pmean,1.6,1e-12)
check('I13_posterior_variance_integrated',pvar,.2,1e-12)
check('I13_predictive_variance_integrated',pvar+1,1.2,1e-12)
for nu in [2,3,9]:
 tq=quantile(lambda v:tcdf(v,nu),.975,0,10)
 check(f'mean_t_CI_coverage_via_density_df{nu}',simpson(lambda v:tpdf(v,nu),-tq,tq,n=6000),.95,5e-10)
# Discrete permutation p-values obey superuniformity on this finite conditional orbit.
ps=[Q(sum(s>=v for s in stats),len(stats)) for v in stats]
for alpha in [Q(1,10),Q(1,3),Q(1,2),Q(2,3),Q(9,10)]:
 check('permutation_superuniform_'+str(alpha),Q(sum(p<=alpha for p in ps),len(ps))<=alpha,True)
# Markdown check bound to submitted source, not a visual renderer.
t=DOC.read_text(encoding='utf-8');lines=t.splitlines()
check('format_16_lectures',len(re.findall(r'^## 第 \d+ 讲',t,re.M)),16)
check('format_16_mermaid',t.count('```mermaid'),16);check('format_fence_pairing',t.count('```')%2,0)
check('format_no_double_dollars','$$' in t,False)
check('format_dollars_paired_per_line',[i+1 for i,l in enumerate(lines) if l.count('$')%2],[])
check('format_sum_bounds',[m.group(0) for m in re.finditer(r'\\sum(?!_\{[^\n]*?\}\^\{)',t)],[])
check('format_no_replacement_character','\ufffd' in t,False);check('format_final_newline',t.endswith('\n'),True)
check('format_headers_separated',[i+1 for i,l in enumerate(lines) if re.match(r'^#{1,3} ',l) and i>0 and lines[i-1].strip()],[])
check('format_16_guided_hints',t.count('**提示**：'),16)
for k in range(1,17):
 check(f'format_G{k}',bool(re.search(r'\*\*G'+str(k)+r'\*\*：',t)),True)
 check(f'format_I{k}',bool(re.search(r'\*\*I'+str(k)+r'\*\*：',t)),True)
for label in ['T1.1','T1.2','T1.3','T1.4','T2.1','T2.2','T2.3','T2.4','T3.1','T3.2','T3.3']:
 check('format_'+label+'_question_answer',t.count('**'+label+'**'),2)
failed=[r for r in results if not r['passed']]
output=dict(author='Codex 侧数学教授分身 CDX',document=str(DOC.relative_to(ROOT)),document_sha256=hashlib.sha256(DOC.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=len(results),passed=len(results)-len(failed),failed=failed,limitations='Finite enumerations and quadratures are author evidence, not proofs of general theorems or student project completion.',results=results)
(Path(__file__).parent/'numerical_results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=len(results),passed=output['passed'],failed=failed),ensure_ascii=False))
raise SystemExit(bool(failed))