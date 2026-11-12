from datetime import datetime,timezone
from .common import identifier,number,unique_ids
def instant(x):
 t=datetime.fromisoformat(x.replace('Z','+00:00'))
 if t.tzinfo is None:raise ValueError('timezone')
 return t.astimezone(timezone.utc)
def run(data):
 now=instant(data['now']);evidence=data['evidence'];decisions=data['decisions']
 if len(evidence)>1000 or len(decisions)>1000:raise ValueError('size')
 unique_ids(evidence);unique_ids(decisions);sources={r['id']:r for r in evidence};output=[]
 for d in decisions:
  results=[];requirements=d['requirements']
  if not isinstance(requirements,list)or not 1<=len(requirements)<=1000:raise ValueError('requirements')
  for req in requirements:
   key=identifier(req['evidence']);source=sources.get(key);op=req['operator']
   if op not in ['eq','lte','gte']:raise ValueError('operator')
   state='unknown';reason=None
   if source is None:reason='missing_evidence'
   elif instant(source['observed_at'])>now:reason='future_observation'
   elif instant(source['expires_at'])<=now:reason='expired_evidence'
   else:
    actual=source['value'];expected=req['expected']
    if op in ['lte','gte']:number(actual);number(expected)
    good=actual==expected if op=='eq'else actual<=expected if op=='lte'else actual>=expected;state='met'if good else'failed'
   results.append({'evidence':key,'state':state,'reason':reason})
  state='invalidated'if any(r['state']=='failed'for r in results)else'unconfirmed'if any(r['state']=='unknown'for r in results)else'conditions_currently_met'
  output.append({'id':d['id'],'state':state,'conditions':results})
 return {'decisions':output,'notifications_sent':False,'business_actions_executed':False,'optimal_decision_proven':False}
