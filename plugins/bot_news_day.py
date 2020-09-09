import requests

from iotbot import Action, GroupMsg
from iotbot.decorators import equal_content, not_botself
from iotbot.sugar import Text

@not_botself
@equal_content('新闻')
def receive_group_msg(ctx: GroupMsg):
	try:
		temp = []
		rep = requests.get('http://api.tianapi.com/world/index?key=9ce8f79f3ad7ce68c6471bda7c4e2863&num=15', timeout=10)
		rep.raise_for_status()
		for i in range(len(rep.json()['newslist'])):
			temp.append(rep.json()['newslist'][i]['title'])
			temp.append(rep.json()['newslist'][i]['url'])
		max_len = max([len(x) for x in temp])
		Text('\n'.join([x.center(max_len) for x in temp]))
	except Exception as e:
		print(e)
