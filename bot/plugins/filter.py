import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.qbtinstance import qb
from bot.updater import updater
from utils import u
from utils import Permissions
from qbt.custom import TORRENT_STRING_COMPACT

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_filter_command(update: Update, context: CallbackContext):
    logger.info(
        "/filter command used by %s (query: %s)",
        update.effective_user.first_name,
        context.args,
    )

    if not context.args[0:]:
        update.message.reply_text("请提供关键词")
        return

    query = " ".join(context.args[0:])

    torrents = qb.filter(query)

    if not torrents:
        update.message.reply_text('没有 "{}" 的结果'.format(query))
        return

    strings_list = [
        torrent.string(base_string=TORRENT_STRING_COMPACT) for torrent in torrents
    ]

    for strings_chunk in u.split_text(strings_list):
        update.message.reply_html("\n".join(strings_chunk))


updater.add_handler(
    CommandHandler(["filter", "f"], on_filter_command),
    bot_command=BotCommand("filter", "列出包含字符的种子"),
)
