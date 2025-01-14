"""
A `tracker.management.commands.run_telegram_bot` command for running telegram bots.`
"""

import asyncio

from django.core.management.base import BaseCommand

from tracker.telegram.bot import start_tg_bot


class Command(BaseCommand):
    """
    Django management command to run the Telegram bot.

    This command initializes and starts the Telegram bot using asynchronous operations.

    Methods:
        - handle(self, *args, **options): Handles the execution of the command.
    """

    help = "Runs the Telegram bot"

    def handle(self, *args, **options) -> None:
        """
        Handles the execution of the command.

        This method is called when the management command is run. It starts the Telegram bot
        and outputs a message to the standard output indicating that the bot has started.

        :return: None
        """
        self.stdout.write("Starting Telegram bot...")
        asyncio.run(start_tg_bot())
