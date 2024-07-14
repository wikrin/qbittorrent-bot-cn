import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.qbtinstance import qb
from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_atm_command(update: Update, context: CallbackContext):
    logger.info("/atm command used by %s", update.effective_user.first_name)
    preferences = qb.preferences()

    zh_cn: dict = {}
    zh_cn["auto_tmm_enabled"] = (
        "已启用" if preferences["auto_tmm_enabled"] else "未启用"
    )
    zh_cn["torrent_changed_tmm_enabled"] = (
        "是" if preferences["torrent_changed_tmm_enabled"] else "否"
    )
    zh_cn["save_path_changed_tmm_enabled"] = (
        "是" if preferences["save_path_changed_tmm_enabled"] else "否"
    )
    zh_cn["category_changed_tmm_enabled"] = (
        "是" if preferences["category_changed_tmm_enabled"] else "否"
    )

    text = (
        "自动 Torrent 管理默认状态: {auto_tmm_enabled}\n\n"
        "- 若 Torrent 类别改变则重新定位: {torrent_changed_tmm_enabled}\n"
        "- 当默认保存路径改变时，重新定位受影响的 Torrents : {save_path_changed_tmm_enabled}\n"
        "- 当 Torrent 所属分类的保存路径改变时，"
        "    重新定位受影响的 Torrents : {category_changed_tmm_enabled}".format(**zh_cn)
    )

    update.message.reply_html(text)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_atm_list_command(update: Update, context: CallbackContext):
    logger.info(
        "/atmyes or /atmno command used by %s", update.effective_user.first_name
    )

    torrents = qb.torrents()

    atm_enabled = update.message.text.lower().endswith("atmyes")

    base_string = '• <code>{short_name}</code> ({size_pretty}, {state_pretty}) [<a href="{info_deeplink}">info</a>]'
    strings_list = [
        torrent.string(base_string=base_string)
        for torrent in torrents
        if torrent["auto_tmm"] is atm_enabled
    ]

    update.message.reply_html(
        f"有 <b>{len(strings_list)}/{len(torrents)}</b> 个torrents"
        f"{'启用' if atm_enabled else '未启用'} 自动 Torrent 管理 :"
    )

    if not strings_list:
        update.message.reply_text("-")
        return

    for strings_chunk in u.split_text(strings_list):
        update.message.reply_html("\n".join(strings_chunk))


updater.add_handler(
    CommandHandler(["atm"], on_atm_command),
    bot_command=BotCommand("atm", "ATM 设置详情"),
)
updater.add_handler(
    CommandHandler(["atmyes"], on_atm_list_command),
    bot_command=BotCommand("atmyes", "列出已启用 ATM 的Torrents"),
)
updater.add_handler(
    CommandHandler(["atmno"], on_atm_list_command),
    bot_command=BotCommand("atmno", "列出已禁用 ATM 的Torrents"),
)
