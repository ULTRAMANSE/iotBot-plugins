import requests

from iotbot import Action, GroupMsg
from iotbot.decorators import equal_content, not_botself
from iotbot.sugar import Text

@not_botself
@equal_content('鸡汤')
def receive_group_msg(ctx: GroupMsg):
	try:
		rep = requests.get('http://api.btstu.cn/yan/api.php?charset=utf-8&encode=json', timeout=10)
		rep.raise_for_status()
		content: str = rep.json()['text']
		Text(content)
	except Exception as e:
		print(e)