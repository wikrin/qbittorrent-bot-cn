import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters

from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


HELP_MESSAGE = """<b>命令</b>:

<i>只读</i>
• /start 或 /help: 获取帮助信息
• /available_filters: 列出按状态筛选种子的命令
• /overview: 当前正在下载和上传的概览
• /filter or /f <code>[substring]</code>: 通过字符串过滤种子列表
• /settings or /s: 获取当前设置
• /transferinfo: 获取当前速度、队列和分享比率的概览
• /atm: 自动 Torrents 管理设置的概览
• /atmyes or /atmno: 列出启用或未启用自动 Torrents 管理的种子
• /json: 获取包含所有种子列表的JSON文件
• /version: 获取qBittorrent和API版本

<i>只写</i>
• <code>.torrent</code> : 通过文件添加种子
• magnet url: 通过磁力链接添加种子

<i>编辑</i>
• /altdown: 变更最大下载速度
• /altdown <code>[kb/s]</code>: 变更最大下载速度,单位kb/s
• /altup <code>[kb/s]</code>: 变更最大上传速度,单位kb/s
• /pauseall: 暂停所有种子
• /resumeall: 恢复所有种子
• /set <code>[setting] [new value]</code>: 变更设置
• <code>+tag</code> 或 <code>-tag</code>: 添加或移除tag "<code>+some tags</code>" 或 \
"<code>-some tags</code>" 可以传递多个tag , 用 ',' 分隔\
(标签可以包含空格)

<i>管理</i>
• /permissions: 获取当前权限配置
• /pset <code>[key] [val]</code>: 变更权限
• /freespace: 获取 qBittorrent 下载路径的剩余空间

<i>自由</i>
• /rmkb: 移除键盘，如果存在的话
"""


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_help(update: Update, context: CallbackContext):
    logger.info("/help from %s", update.message.from_user.first_name)

    update.message.reply_html(HELP_MESSAGE)


updater.add_handler(
    CommandHandler("help", on_help), bot_command=BotCommand("help", "帮助")
)
updater.add_handler(MessageHandler(Filters.regex(r"^\/start$"), on_help))
