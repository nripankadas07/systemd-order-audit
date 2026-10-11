"""Inspect explicit ordering and pull-in relations in a normalized unit snapshot."""
import argparse,heapq,json,re,sys
from pathlib import Path

def audit(data):
    if not isinstance(data,dict) or set(data)!={'roots','units'}: raise ValueError('roots and units required')
    units=data['units'];roots=data['roots']
    if not isinstance(units,dict) or not 1<=len(units)<=500 or not isinstance(roots,list) or not roots: raise ValueError('1..500 units and nonempty roots required')
    valid=lambda n:isinstance(n,str) and bool(re.fullmatch(r'[A-Za-z0-9_.@:-]+\.(service|target|socket|timer|mount|path|slice|scope|device|automount|swap)',n))
    for n,u in units.items():
        if not valid(n) or not isinstance(u,dict) or set(u)!={'after','before','requires','wants'}: raise ValueError('invalid unit record')
        for ds in u.values():
            if not isinstance(ds,list) or len(ds)>500 or not all(valid(x) for x in ds) or len(set(ds))!=len(ds): raise ValueError('invalid or duplicate dependency')
    if not all(valid(n) and n in units for n in roots) or len(set(roots))!=len(roots): raise ValueError('roots must be unique known units')
    active=set(roots);pending=list(roots);missing=set()
    while pending:
        n=pending.pop()
        for dep in units[n]['requires']+units[n]['wants']:
            if dep not in units: missing.add(dep)
            elif dep not in active: active.add(dep);pending.append(dep)
    edges=set();inactive=set()
    for n in active:
        for dep in units[n]['after']:
            if dep in active:edges.add((dep,n))
            else:inactive.add(dep)
        for dep in units[n]['before']:
            if dep in active:edges.add((n,dep))
            else:inactive.add(dep)
    adj={n:set() for n in active};ind={n:0 for n in active}
    for a,b in edges:adj[a].add(b);ind[b]+=1
    heap=[n for n in active if ind[n]==0];heapq.heapify(heap);order=[]
    while heap:
        n=heapq.heappop(heap);order.append(n)
        for dep in sorted(adj[n]):
            ind[dep]-=1
            if ind[dep]==0:heapq.heappush(heap,dep)
    blocked=sorted(n for n in active if ind[n]>0)
    # Find one concrete cycle using iterative DFS to avoid Python recursion limits.
    cycle=[];color={};parent={}
    for start in sorted(active):
        if color.get(start):continue
        color[start]=1;stack=[(start,iter(sorted(adj[start])))]
        while stack and not cycle:
            n,it=stack[-1];dep=next(it,None)
            if dep is None:color[n]=2;stack.pop();continue
            if not color.get(dep):parent[dep]=n;color[dep]=1;stack.append((dep,iter(sorted(adj[dep]))))
            elif color[dep]==1:
                chain=[n]
                while chain[-1]!=dep:chain.append(parent[chain[-1]])
                cycle=list(reversed(chain))+[dep]
        if cycle:break
    return {'active':sorted(active),'missing_pull_ins':sorted(missing),'inactive_order_targets':sorted(inactive),'edges':[list(e) for e in sorted(edges)],'acyclic':not blocked,'order':order if not blocked else None,'cycle':cycle,'blocked':blocked,'complete':not missing,'scope':'explicit startup subset only; not systemd verification or default dependencies'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('snapshot');a=p.parse_args()
    try:
        with Path(a.snapshot).open('rb') as f:raw=f.read(1048577)
        if len(raw)>1048576:raise ValueError('snapshot exceeds 1 MiB')
        print(json.dumps(audit(json.loads(raw)),sort_keys=True));return 0
    except (ValueError,OSError,TypeError,KeyError,UnicodeError) as e:print(json.dumps({'error':str(e)}));return 2
if __name__=='__main__':sys.exit(main())
