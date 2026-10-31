import csv
from pathlib import Path
from xml.etree import ElementTree as ET
root=Path(__file__).resolve().parent
rows=list(csv.DictReader((root/'logistic_bifurcation.csv').open()))
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="650" viewBox="0 0 1000 650">','<rect width="1000" height="650" fill="white"/>','<text x="80" y="30" font-family="sans-serif" font-size="20">Logistic map: finite parameter-grid experiment</text>','<path d="M80 60V580H960" fill="none" stroke="black"/>']
for k in range(7):
 r=2.8+0.2*k;x=80+(r-2.8)/1.2*880
 parts.append(f'<text x="{x-12}" y="605" font-size="14">{r:.1f}</text>')
for k in range(6):
 v=k/5;y=580-v*520
 parts.append(f'<text x="45" y="{y+5}" font-size="14">{v:.1f}</text>')
for row in rows:
 r,v=float(row['r']),float(row['x']);assert 2.8<=r<=4 and 0<=v<=1
 parts.append(f'<circle cx="{80+(r-2.8)/1.2*880:.3f}" cy="{580-v*520:.3f}" r="0.65" fill="#123a75" fill-opacity="0.35"/>')
parts+=['<text x="500" y="635" font-size="16">parameter r</text>','<text x="15" y="45" font-size="16">x</text>','</svg>']
out=root/'logistic_bifurcation.svg';out.write_text('\n'.join(parts),encoding='utf-8');ET.parse(out)
print(f'validated_points={len(rows)}; SVG_XML=valid')
