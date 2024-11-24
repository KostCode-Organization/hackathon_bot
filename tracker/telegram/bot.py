import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandObject, CommandStart
from aiogram.types.message import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from dotenv import load_dotenv

from tracker import ISSUES_URL, PULLS_URL, get_issues_without_pull_requests
from tracker.utils import (
    create_telegram_user,
    get_all_available_issues,
    get_all_repostitories,
    get_user,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bot = Bot(
    token=os.environ.get("TELEGRAM_BOT_TOKEN", str()),
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()


@dp.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def auth_link_handler(message: Message, command: CommandObject) -> None:
    """
    deep link handler saving the uuid and tracked repos by this user into db
    :param message: aiogram.types.Message object
    :param command: aiogram.filters.CommandObject object
    :return: None
    """
    uuid = command.args
    user = await get_user(uuid)

    await create_telegram_user(
        user=next(iter(user)), telegram_id=str(message.from_user.id)
    )
    await message.answer(
        f"Hello {message.from_user.mention_html()}!\n"
        f"Would you like to check some issues?",
        reply_markup=main_button_markup(),
    )


@dp.message(CommandStart())
async def start_message(message: Message) -> None:
    """
    A function that starts the bot.
    :param message: Message that starts the bot.
    :return: None
    """
    await message.answer(
        f"Hello {message.from_user.mention_html()}!\n"
        f"Would you like to check some issues?",
        reply_markup=main_button_markup(),
    )


@dp.message(F.text == "📓get missed deadlines📓")
async def send_deprecated_issue_assignees(msg: Message) -> None:
    """
    Sends information about assignees that missed the deadline.
    :param msg: Message instance for communication with a user
    :return: None
    """
    all_repositories = await get_all_repostitories(msg.from_user.id)

    for repository in all_repositories:
        issues = get_issues_without_pull_requests(
            issues_url=ISSUES_URL.format(
                owner=repository.get("author", str()),
                repo=repository.get("name", str()),
            ),
            pull_requests_url=PULLS_URL.format(
                owner=repository.get("author", str()),
                repo=repository.get("name", str()),
            ),
        )

        message = (
            "=" * 50
            + "\n"
            + f'<b>Repository: {repository.get("author", str())}/{repository.get("name", str())}</b>'
            + "\n"
            + "=" * 50
            + "\n\n"
        )

        for issue in issues:
            message += (
                "-----------------------------------\n"
                "Issue: " + issue.get("title", str()) + "\n"
                "User: " + issue.get("assignee", dict()).get("login", str()) + "\n"
                "Assigned:" + "\n"
                "\t\t\t\tDays ago: " + str(issue["days"]) + "\n"
                "-----------------------------------\n"
            )

        if not issues:
            message += "No missed deadlines.\n"

        await msg.reply(f"<blockquote>{message}</blockquote>")


def escape_html(text: str) -> str:
    """
    Escapes HTML symbols in the text to ensure proper rendering in Telegram messages.

    :param text: The input string that may contain HTML symbols.
    :return: A string with HTML symbols escaped, replacing '&' with '&amp;', '<' with '&lt;',
             and '>' with '&gt;'.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@dp.message(F.text == "📖get available issues📖")
async def send_available_issues(msg: Message) -> None:
    """
    Sends all the available issues
    :param msg: Message instance for communication with a user
    :return: None
    """
    all_repositories = await get_all_repostitories(msg.from_user.id)

    for repository in all_repositories:
        issues = get_all_available_issues(
            ISSUES_URL.format(
                owner=repository.get("author", str()),
                repo=repository.get("name", str()),
            ),
        )

        message = (
            "=" * 50
            + "\n"
            + f'<b>Repository: {repository.get("author", str())}/{repository.get("name", str())}</b>'
            + "\n"
            + "=" * 50
            + "\n\n"
        )

        for issue in issues:
            description = issue.get("body", "No description provided.")
            escaped_description = escape_html(description)

            message += (
                "-----------------------------------\n"
                f"Issue #{issue.get('number', 'Unknown')}: {issue.get('title', 'No title provided')}\n"
                f"Author: {issue.get('user', {}).get('login', 'Unknown')}\n"
                f"Description: <blockquote expandable>{escaped_description}</blockquote>\n"
                "-----------------------------------\n"
            )

        if not issues:
            message += "No available issues.\n"

        await msg.reply(message, parse_mode="HTML")


async def send_revision_messages(telegram_id: str, reviews_data: list[dict]) -> None:
    """
    Send message for all open PR revisions and approvals
    :params tele_id: The telegram user id of the user to send to
    :reviews_data: A list of all the reviews data for all pull requests associated to the user repos
    """
    message = (
        "=" * 50 + "\n" + "<b>Revisions and Approvals</b>" + "\n" + "=" * 50 + "\n\n"
    )
    for data in reviews_data:
        message += (
            "-------------------------------"
            f"Repo: <b>{data['repo']}</b>"
            "\n"
            f"Pull Request: <b>{data['pull']}/</b>" "\n"
            f"<b>Reviews:</b>"
            "\n"
        )
        for review in data["reviews"]:
            message += (
                f"User: <b>{review['user']['login']}</b>"
                "\n"
                f"State: {review['state']}"
                "\n\n"
            )
        message += "-------------------------------"
    # Send bot message
    await bot.send_message(telegram_id, message)


async def get_contributor_tasks(github_username: str) -> ...:
    ...


def main_button_markup() -> ReplyKeyboardMarkup:
    """
    A function that generates a button
    :return: ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    builder.button(text="📓get missed deadlines📓")
    builder.button(text="📖get available issues📖")

    return builder.as_markup(resize_keyboard=True)


async def create_tg_link(uuid) -> str:
    return await create_start_link(bot=bot, payload=uuid, encode=True)


async def start_tg_bot() -> None:
    """
    A function that starts the bot.
    :return: None
    """
    try:
        await dp.start_polling(bot, polling_timeout=0)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_tg_bot())
