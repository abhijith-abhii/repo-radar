import pytest
from core import analyze,load,fetch_pages

def test_sample_reconciliation():
 d=analyze({});assert sum(x['commits'] for x in d['rows'])==36
 assert sum(x['value'] for x in d['bars'])==36
 assert d['metrics']['Issues sampled']==15
@pytest.mark.parametrize('repo',['../foo','https://github.com/a/b','a/b/c',''])
def test_invalid_repo(repo):
 with pytest.raises(ValueError):load(repo,'live')
class Response:
 status_code=429
class Session:
 def get(self,*a,**kw):return Response()
def test_rate_limit():
 with pytest.raises(ValueError,match='rate limit'):fetch_pages('https://api.github.com/repos/a/b/commits',Session())
