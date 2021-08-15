import discord
from discord.ext import commands


class Help(commands.HelpCommand):

    def __init__(self, **kwargs):
        self.color = 0x800080
        command_attrs = {"help": "the help command.\nalso shown when a command is misused"}
        super().__init__(command_attrs=command_attrs, **kwargs)

    async def send_bot_help(self, mapping):
        mapping.pop(None)
        await self.get_destination().send(
            embed=discord.Embed(
                title="Help",
                description=f"""**usage:**\n```{self.context.prefix}help [command]```
                    modules loaded:\n```{f" {chr(10)}".join([i.qualified_name for i in mapping])}```""",
                color=self.color))

    async def send_cog_help(self, cog):
        await self.get_destination().send(
            embed=discord.Embed(
                title=f"{cog.qualified_name} module",
                description=f"""{cog.description if cog.description else ""}
                    **command list:**\n```{f" {chr(10)}".join([i.name for i in cog.get_commands() if not i.hidden])}```""",
                color=self.color))

    async def send_command_help(self, command):
        if command.hidden:
            return
        await self.get_destination().send(
            embed=discord.Embed(
                title=command.qualified_name,
                description=f"""{command.help if command.help else "no help provided for this command"}
                    **usage:**\n```{self.get_command_signature(command).replace("...", "")}```""",
                color=self.color)
            .set_footer(text="arguments are: <required> [optional]"))

    async def send_group_help(self, group):
        if group.hidden:
            return
        await self.get_destination().send(
            embed=discord.Embed(
                title=group.qualified_name,
                description=f"""{group.short_doc if group.short_doc else ""}
                    **usage:**
                    ```{self.context.prefix}{group.name} {group.signature.replace(" ", ", ") + (", " if group.signature else "")}<sub command>```
                    list of sub command:\n```{f" {chr(10)}".join([i.name for i in group.commands if not i.hidden])}```""",
                color=self.color)
            .set_footer(text="arguments are: <required> [optional]" if group.signature else ""))

    async def command_not_found(self, name):
        return f"no command, group or module named \"{name}\""

    async def subcommand_not_found(self, command, name):
        cmdlist = ""
        if hasattr(command, "commands") and command.commands:
            cmdlist = f""" named {name}\n**list of subcommand for {command}**:\n\n```{f" {chr(10)}".join([i.name for i in command.commands])}```"""
        return f"command {command} have no subcommand{cmdlist}"

    async def send_error_message(self, msg):
        await self.get_destination().send(
            embed=discord.Embed(
                title="Help",
                description=msg,
                color=self.color))
