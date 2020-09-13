import requests
from iotbot import IOTBOT, Action, GroupMsg

bot_qq = 3571557174
bot = IOTBOT(bot_qq, use_plugins=True, plugin_dir='plugins')
action = Action(bot)
groupid = [1131414079]


# 群消息中间件使用示例
def group_ctx_middleware(ctx):
	ctx.master = [1076012962, 1305392603]  # 主人qq


bot.register_group_context_middleware(group_ctx_middleware)


####################


@bot.on_group_msg
def on_group_msg(ctx: GroupMsg):
	content = ctx.Content
	# 召唤群友(回执消息)
	if ctx.FromUserId in ctx.master and content == '召唤群友':
		card = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="107" templateID="1" action="viewReceiptMessage" brief="[回执消息]" m_resid="1tko/MQMaPR0jedOx6T8tbleZtAZudGqTFakakLqukDzuTjrZS1/1V1QEUnZ8/2Y" m_fileName="6828184148041033822" sourceMsgId="0" url="" flag="3" adverSign="0" multiMsgFlag="0"><item layout="29" advertiser_id="0" aid="0"><type>1</type></item><source name="" icon="" action="" appid="-1" /></msg>"""
		action.send_group_xml_msg(ctx.FromGroupId, content=card)
		return

	# nmsl
	if content == 'nmsl':
		action.send_group_text_msg(
			ctx.FromGroupId,
			requests.get('https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn').text,
		)
		return

	# 舔我
	if content == '舔我':
		action.send_group_text_msg(
			ctx.FromGroupId,
			'\n' + requests.get('https://chp.shadiao.app/api.php').text,
			ctx.FromUserId,
		)
		return


@bot.on_group_msg
def manage_plugin(ctx: GroupMsg):
	if ctx.FromUserId not in ctx.master:
		return
	c = ctx.Content
	if c == '插件管理':
		action.send_group_text_msg(
			ctx.FromGroupId,
			(
				'插件列表 => 发送启用插件列表\n'
				'已停用的插件 => 发送停用插件列表\n'
				'刷新插件 => 刷新所有插件,包括新建文件\n'
				'重载插件+插件名 => 重载指定插件\n'
				'停用插件+插件名 => 停用指定插件\n'
				'启用插件+插件名 => 启用指定插件\n'
			),
		)
		return
	# 发送启用插件列表
	if c == '插件列表':
		action.send_group_text_msg(ctx.FromGroupId, '\n'.join(bot.plugins))
		return
	# 发送停用插件列表
	if c == '已停用的插件':
		action.send_group_text_msg(ctx.FromGroupId, '\n'.join(bot.removed_plugins))
		return
	with __import__('threading').Lock():
		try:
			if c == '刷新插件':
				bot.refresh_plugins()
			# 重载指定插件 重载py插件+[插件名]
			elif c.startswith('重载插件'):
				plugin_name = c[6:]
				bot.reload_plugin(plugin_name)
			# 停用指定插件 停用py插件+[插件名]
			elif c.startswith('停用插件'):
				plugin_name = c[6:]
				bot.remove_plugin(plugin_name)
			# 启用指定插件 启用py插件+[插件名]
			elif c.startswith('启用插件'):
				plugin_name = c[6:]
				bot.recover_plugin(plugin_name)
		except Exception as e:
			action.send_group_text_msg(ctx.FromGroupId, '操作失败: %s' % e)


@bot.on_group_msg
def get_group_id(ctx: GroupMsg):
	if ctx.FromGroupId not in groupid:
		groupid.append(ctx.FromGroupId)


def receive_group_msg():
	try:
		temp = []
		rep = requests.get('http://api.tianapi.com/world/index?key=9ce8f79f3ad7ce68c6471bda7c4e2863&num=10',
						   timeout=10)
		rep.raise_for_status()
		for i in range(len(rep.json()['newslist'])):
			temp.append(rep.json()['newslist'][i]['title'])
		# temp.append(rep.json()['newslist'][i]['url'])
		max_len = max([len(x) for x in temp])
		for id in groupid:
			action.send_group_text_msg(int(id), '\n'.join([x for x in temp]))
	except Exception as e:
		print(e)
	return


bot.scheduler.every().day.at("14:17").do(receive_group_msg)

if __name__ == "__main__":
	bot.run()
