"""Plot every accepted floating start without averaging or clustering outcomes."""
import csv,pathlib,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from approximate_queue import ROOT,read,verify,identity,write_new,now

out=pathlib.Path(r'C:\Users\Admin\Documents\Codex\2026-09-23\explore-and-implement-performance-improvements-to\outputs\Multiple-equilibrium-outcome-diagram-British')
out.mkdir(exist_ok=False)
source=ROOT/'reporting/approximate-stable-200-grouping-v1/catalog.json'
fields=[('MeritoriousPlaintiffShortfall','Meritorious plaintiff\nshortfall'),('NonliableDefendantBurden','Nonliable defendant\nburden'),('LiableDefendantExcessBurden','Liable defendant\nexcess burden'),('GrossOutcomeError','Gross outcome\nerror'),('RealLitigationExpenditures','Real litigation\nexpenditures')]
rows=[]
for a in read(source)['Attempts']:
    if not a['Accepted']:continue
    r=read(verify(a['Result']));assert r['Validation']['Passed']
    parts=a['Case'].split('__')
    rows.append(dict(Risk=parts[3],Rule=parts[2],Start=a['StartIndex'],AverageGain=a['AverageGain'],**r['Validation']['Welfare']['Headline']))
assert len(rows)==199
colors={'american':'#24699c','complete':'#a44464'};markers={'american':'o','complete':'s'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,5,figsize=(15,11.5))
fig.subplots_adjust(left=.095,right=.98,top=.83,bottom=.11,wspace=.26,hspace=.40)
fig.suptitle('Multiple equilibria: outcomes at cost multiplier 1',x=.095,ha='left',y=.983,fontsize=20,weight='bold')
fig.text(.095,.948,'Every accepted start shown separately • Five monetary measures • Agreement enabled',fontsize=11)
fig.legend(handles=[Line2D([0],[0],marker=markers[r],color=colors[r],linestyle='',label=l,markersize=6) for r,l in [('american','American'),('complete','British')]],loc='upper left',bbox_to_anchor=(.087,.931),ncol=2,frameon=False)
for ri,risk in enumerate(['rn','ra']):
    for j,(field,title) in enumerate(fields):
        ax=axes[ri,j];bound=max(r[field] for r in rows)*1.08
        ax.set_xlim(0,bound);ax.set_ylim(49.8,-.8)
        ax.set_yticks([0,10,20,30,40,49],['0','10','20','30','40','49'] if j==0 else [])
        ax.set_title(title,fontsize=11,pad=9);ax.grid(alpha=.15);ax.set_axisbelow(True)
        for rule in ['american','complete']:
            data=sorted((r for r in rows if r['Risk']==risk and r['Rule']==rule),key=lambda r:r['Start'])
            # Vertical offsets separate symbols without changing the outcome axis.
            offset=-.15 if rule=='american' else .15
            ax.scatter([r[field] for r in data],[r['Start']+offset for r in data],c=colors[rule],marker=markers[rule],s=15,alpha=.88,linewidths=0,zorder=3)
            assert len(data)==(49 if risk=='ra' and rule=='complete' else 50)
        if j==0:ax.set_ylabel('Start index',labelpad=9)
        ax.tick_params(axis='x',labelsize=9)
    axes[ri,0].text(0,1.18,'Risk neutral — 50 American, 50 British' if risk=='rn' else 'Risk averse — 50 American, 49 British',transform=axes[ri,0].transAxes,fontsize=14,weight='bold')
fig.text(.095,.064,'199 accepted approximate profiles from 200 starts. British risk-averse start 12 did not pass and is omitted.',fontsize=10)
fig.text(.095,.036,'Rows identify starts, not matched equilibrium pairs. Repeated outcomes remain separate dots. No averaging or grouping.\nScales match between risk panels within each measure. Monetary units: damages = 1. These are not exact-equilibrium certificates.',fontsize=9,color='#444444')
fig.savefig(out/'multiple-outcomes.png',dpi=160);fig.savefig(out/'multiple-outcomes.svg');plt.close(fig)
with (out/'all-outcomes.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
shutil.copy2(__file__,out/'reproduce.py')
write_new(out/'manifest.json',dict(CreatedUtc=now(),Source=identity(source),Generator=identity(__file__),Accepted=199,Expected=200,Files=[identity(p) for p in out.iterdir() if p.is_file()]))
print(out)
