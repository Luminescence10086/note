"""Independent numerical/structural checks, not a substitute for the written proofs."""
from pathlib import Path
import hashlib
import json
import math
import re
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / 'professors/MATH/handout_MA404_CDX'
SUPPLEMENT = WORK / '20261024_连续部分正文_CDX.md'
FINAL = ROOT / 'lectures/math/approved/MA404_信息论_离散与连续十二讲.md'
LN2 = math.log(2)
nodes, weights = np.polynomial.legendre.leggauss(160)


def quad(fn, lo, hi):
    x = (lo + hi) / 2 + (hi - lo) * nodes / 2
    return float(np.dot(weights, fn(x)) * (hi - lo) / 2)


def close(x, y, tol=2e-9):
    assert math.isclose(float(x), float(y), rel_tol=tol, abs_tol=tol), (x, y)


def assert_less(a,b):
    assert a<b,(a,b)


def entropy(probs):
    return -sum(float(p) * math.log2(float(p)) for p in probs if p > 0)


def normal_pdf(x, mean=0., var=1.):
    return np.exp(-(x - mean)**2 / (2 * var)) / math.sqrt(2 * math.pi * var)


def normal_entropy(var):
    return .5 * math.log2(2 * math.pi * math.e * var)


def integrated_normal_entropy(var):
    sigma = math.sqrt(var)
    return quad(lambda x: -normal_pdf(x, var=var) *
                (-.5 * math.log(2 * math.pi * var) - x*x/(2*var))/LN2,
                -12*sigma, 12*sigma)


def normal_kl_shift(var, delta):
    s = math.sqrt(var)
    return quad(lambda x: normal_pdf(x, var=var) *
                ((x-delta)**2-x*x)/(2*var*LN2), -12*s, 12*s)


def gaussian_pair_mi(vx, vy, cov):
    # Integrate a conditional construction X, Y|X; compare the joint ratio directly.
    conditional_var = vy-cov*cov/vx
    sx, se = math.sqrt(vx), math.sqrt(conditional_var)
    def inner(x):
        vals=[]
        for xi in x:
            vals.append(quad(lambda e: normal_pdf(e, var=conditional_var) *
                (.5*math.log(vy/conditional_var) - e*e/(2*conditional_var)
                 + (cov/vx*xi+e)**2/(2*vy))/LN2, -12*se,12*se))
        return normal_pdf(x,var=vx)*np.asarray(vals)
    return quad(inner,-12*sx,12*sx)


records = {}


def case(label, action):
    action()
    records[label] = 'PASS: numerical/model checks; proof conditions audited in handout'


def c71():
    close(quad(lambda x: np.ones_like(x)*4,0,.25),1)
    close(quad(lambda x: -np.ones_like(x)*4*math.log2(4),0,.25),-2)
    close(math.log2(2)-math.log2(.25),3)
case('E7.1',c71)
case('E7.2',lambda: close(quad(lambda u: -2*np.exp(-2*u)*(LN2-u)/LN2,0,50),-1+1/(2*LN2)))
case('G7.1',lambda: (close(quad(lambda x: np.ones_like(x)/3,2,5),1),close(math.log2(6)-math.log2(3),1)))
case('G7.2',lambda: (close(entropy([1/16]*16),4),close(entropy([1/256]*256),8)))


def t71():
    for rate in [.2,1.,math.e,7.]:
        h=quad(lambda u: -np.exp(-u)*(math.log(rate)-u)/LN2,0,80)
        close(h,math.log2(math.e/rate))
case('T7.1',t71)
case('T7.2',lambda: (close(quad(np.exp,0,LN2),1),close(quad(lambda y:-y*np.exp(y)/LN2,0,LN2),1/LN2-2)))
case('T7.3',lambda: (close(entropy([.25]*4),entropy([.25]*4)),close(math.log2(2),1)))
case('E8.1',lambda: (close(quad(lambda u: 2*np.exp(-2*u)*(LN2-u)/LN2,0,50),1-1/(2*LN2)),close(quad(lambda u: -np.exp(-u)*(LN2-u)/LN2,0,80),-1+1/LN2)))
case('E8.2',lambda: (close(entropy([.5,.5]),1),close(math.log2(2),1)))


def g81():
    p=np.array([.375,.125,.125,.375]); q=np.full(4,.25)
    d=float(np.sum(p*np.log2(p/q)))
    close(d,1-entropy([.25,.75])); assert d>0
    close(np.sum(q*np.log2(q/q)),0)
case('G8.1',g81)
case('G8.2',lambda: (close(entropy([.5,.5]),1),close(entropy([1.]),0)))
case('T8.1',lambda: close(-2-2-(-4),0))
case('T8.2',lambda: close(entropy([.75,.25]),.8112781244591328))
case('T8.3',lambda: [close(entropy([1/n]*n),math.log2(n)) for n in [2,16,256]])
case('E9.1',lambda: (close(integrated_normal_entropy(1),normal_entropy(1)),close(quad(lambda x:x*x/(2*math.sqrt(3)),-math.sqrt(3),math.sqrt(3)),1),assert_less(math.log2(2*math.sqrt(3)),normal_entropy(1))))


case('E9.2',lambda: (close(gaussian_pair_mi(1,1,.6),math.log2(1.25)),close(1-.6**2,16/25)))
case('G9.1',lambda: close(integrated_normal_entropy(9),normal_entropy(9)))
case('G9.2',lambda: (close(np.mean(np.array([-1,0,1])*np.array([1,0,1])),0),assert_less(0,entropy([1/3,2/3]))))
case('T9.1',lambda: [close(gaussian_pair_mi(1,1,r),math.log2(5/3)) for r in [.8,-.8]])


def t92():
    close(quad(lambda x:x*x/4,-2,2),4/3)
    d=quad(lambda x:(-math.log(4)+.5*math.log(2*math.pi*4/3)+x*x/(2*4/3))/(4*LN2),-2,2)
    close(d,normal_entropy(4/3)-2)
case('T9.2',t92)
case('T9.3',lambda: close(np.linalg.det(np.array([[1.,2.],[2.,4.]])),0))
case('E10.1',lambda: close(.5*math.log2(1+300/100),1))


def e102():
    f=lambda y:.5*(normal_pdf(y,math.sqrt(3))+normal_pdf(y,-math.sqrt(3)))
    h=quad(lambda y:-f(y)*np.log2(f(y)),-15,15)
    assert_less(h-normal_entropy(1),1)
    close(quad(lambda y:y**4*f(y),-15,15),30)
case('E10.2',e102)
case('G10.1',lambda: [close(.5*math.log2(1+p),a) for p,a in zip([0,1,3,15],[0,.5,1,2])])
case('G10.2',lambda: close(.5*math.log2(1+30/2),2))
case('T10.1',lambda: close(.5*math.log2(1+75/25),1))
case('T10.2',lambda: (close(gaussian_pair_mi(4,5,4),.5*math.log2(5)),close(gaussian_pair_mi(4,8,4),.5)))


def t103():
    p=np.linspace(0,4,4001)
    value=.5*np.log2((1+p)*(7-p)/3)
    close(p[int(np.argmax(value))],3)
    close(value.max(),.5*math.log2(16/3))
case('T10.3',t103)
case('E11.1',lambda: (close(quad(lambda x:normal_pdf(x,var=4)*(x/4)**2,-24,24),.25),close(normal_kl_shift(4,.2),.2**2/(8*LN2))))


def e112():
    rate=4.; k=np.arange(0,100,dtype=float)
    probs=np.array([math.exp(-rate+i*math.log(rate)-math.lgamma(i+1)) for i in k])
    close(np.dot(probs,(k/rate-1)**2),1/rate)
    close((1/rate)*(2*math.sqrt(rate))**2,4)
case('E11.2',e112)
case('G11.1',lambda: [close((n/4)*(4/n),1) for n in [1,10,100]])
case('G11.2',lambda: close(normal_kl_shift(4,.2),1/(200*LN2)))


def t111():
    for theta in [.1,.25,.6,.9]:
        score=np.array([-1/(1-theta),1/theta]); p=np.array([1-theta,theta])
        close(np.dot(p,score),0); close(np.dot(p,score**2),1/(theta*(1-theta)))
case('T11.1',t111)
case('T11.2',lambda: (close(quad(lambda x:np.full_like(x,-1/2)/2,0,2),-.5),close(quad(lambda x:(2*x-2)**2/2,0,2),4/3)))


def t113():
    theta=.4
    p=np.array([1-theta,theta]); score=np.array([-1/(1-theta),1/theta])
    channel=np.array([[.8,.2],[.3,.7]])
    py=p@channel
    sy=(p*score)@channel/py
    jx=np.dot(p,score**2); jy=np.dot(py,sy**2)
    assert_less(jy,jx)
    close(np.dot(py,sy),0)
case('T11.3',t113)
case('E12.1',lambda: [close(max(0,.5*math.log2(4/d)),r) for d,r in [(1,1),(.25,2),(4,0)]])
case('E12.2',lambda: (close(4-16/5,.8),close(gaussian_pair_mi(4,5,4),.5*math.log2(5))))
case('G12.1',lambda: [close(max(0,.5*math.log2(1/d)),r) for d,r in [(1,0),(.25,1),(.0625,2)]])
case('G12.2',lambda: close(.5*math.log2(10),1.660964047443681))
case('T12.1',lambda: (close(9/81+8/9,1),close(gaussian_pair_mi(9,8,8),math.log2(3))))
case('T12.2',lambda: (close(1-1/4,.75),close(gaussian_pair_mi(1,4,1),.5*math.log2(4/3))))
case('T12.3',lambda: (close(4-16/5,.8),close(4-16/8,2),close(.08*10,.8),close(gaussian_pair_mi(4,8,4),.5)))

text=SUPPLEMENT.read_text(encoding='utf-8')
body,answers=text.split('## 附录 F',1)
expected={f'{k}{n}.{i}' for n in range(7,13) for k,count in [('E',2),('G',2),('T',3)] for i in range(1,count+1)}
assert set(records)==expected,(expected-set(records),set(records)-expected)
for key in expected:
    assert len(re.findall(r'\*\*(?:示范 )?'+re.escape(key)+r'[（：]',body))==1,key
    if not key.startswith('E'):
        assert len(re.findall(r'\*\*'+re.escape(key)+r'。',answers))==1,key
assert '$$' not in text
assert all(line.count('$')%2==0 for line in text.split('\n'))
assert not re.search(r'\\log(?!_2)',text)
assert not re.search(r'\\sum(?!_)',text)
assert not re.search(r'[\u4e00-\u9fff]\$|\$[\u4e00-\u9fff]',text)
assert text.count('```')%2==0
assert not any(ord(c)<32 and c not in '\n\r\t' for c in text)

if FINAL.exists():
    combined=FINAL.read_text(encoding='utf-8')
    baseline=(WORK/'20261024_original_six_lectures_CDX.md').read_text(encoding='utf-8')
    anchor='## 第一讲\u3000把问题变成概率表'
    original_body=baseline[baseline.index(anchor):].rstrip()
    merged_body=combined[combined.index(anchor):combined.index('## 第二部分导读')].rstrip()
    assert original_body==merged_body,'original six lectures changed'
    assert combined.count('## 第七讲')==1 and combined.count('## 第十二讲')==1
    assert '$$' not in combined
    assert all(line.count('$')%2==0 for line in combined.split('\n'))
    final_hash=hashlib.sha256(FINAL.read_bytes()).hexdigest()
else:
    final_hash=None

summary={'date':'2026-10-24','author':'CDX','units_checked':len(records),'status':'PASS',
         'method':'deterministic quadrature, exact algebra/model checks, authored proof-condition audit; not independent review',
         'cases':records,'final_sha256':final_hash}
(WORK/'20261024_连续部分核验_CDX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'units_checked':len(records),'status':'PASS','final_sha256':final_hash},ensure_ascii=False))
