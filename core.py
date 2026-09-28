import json,re,time,os
from pathlib import Path
from collections import Counter
import requests
ROOT=Path(__file__).parent

def fetch_pages(url,session=None,max_pages=3):
 session=session or requests.Session();items=[]
 for page in range(1,max_pages+1):
  r=session.get(url,params=({'per_page':100,'page':page,'state':'all','sort':'updated','direction':'desc'} if url.endswith('/issues') else {'per_page':100,'page':page}),headers={'Accept':'application/vnd.github+json','User-Agent':'repo-radar-portfolio'},timeout=15)
  if r.status_code in (403,429):raise ValueError('GitHub rate limit reached; use sample mode or retry later')
  if r.status_code==404:raise ValueError('Public repository not found')
  if not r.ok:raise ValueError(f'GitHub returned HTTP {r.status_code}')
  data=r.json()
  if not isinstance(data,list):raise ValueError('Unexpected GitHub response')
  items.extend(data)
  if len(data)<100:break
 return items

def load(repo,mode):
 if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise ValueError('Use owner/repository format')
 if mode=='sample':return json.loads((ROOT/'data/sample.json').read_text())
 if mode!='live':raise ValueError('Choose sample or live')
 cache=Path(os.environ.get('RADAR_CACHE',ROOT/'var/cache'));cache.mkdir(parents=True,exist_ok=True);path=cache/(repo.replace('/','--')+'.json')
 if path.exists() and time.time()-path.stat().st_mtime<300:return json.loads(path.read_text())
 try:
  data={'commits':fetch_pages('https://api.github.com/repos/'+repo+'/commits'),'issues':fetch_pages('https://api.github.com/repos/'+repo+'/issues'),'retrieved_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 except requests.RequestException as e:raise ValueError('Network request failed; cached/sample data remain available') from e
 temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data));temp.replace(path);return data

def analyze(p):
 mode=p.get('mode','sample');repo=p.get('repository','pallets/flask');data=load(repo,mode)
 commits=data['commits'];issues=[x for x in data['issues'] if 'pull_request' not in x]
 authors=Counter((x.get('author') or {}).get('login') or 'unlinked' for x in commits)
 days=Counter(x['commit']['author']['date'][:10] for x in commits)
 return dict(notice=('Synthetic sample: counts demonstrate the analysis and are not claims about '+repo) if mode=='sample' else 'Public API snapshot. Limited to 300 commits and 300 recently updated issue/PR records; issue counts exclude PRs. Not a productivity score.',metrics={'Commits sampled':len(commits),'Linked/unlinked identities':len(authors),'Issues sampled':len(issues),'Open in sample':sum(x['state']=='open' for x in issues)},bars=[dict(label=k,value=v) for k,v in sorted(days.items())],chart_title='Commits by author timestamp (UTC)',rows=[dict(contributor=k,commits=v) for k,v in authors.most_common()],details={'retrieved_at':data['retrieved_at'],'repository':repo,'limits':'First 3 pages per endpoint; not complete historical coverage'})
