from redbot.core import commands, Config
import discord


class Counting(commands.Cog):
    """Counting Channel."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=14000605, force_registration=True)
        default_guild = {"toggle": True, "channel": None, "counter": 0, "role": None, "assignrole": False, "allowrepeats": False, "deleted": None}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener("on_message")
    async def _message_listener(self, message: discord.Message):
        counting_channel = await self.config.guild(message.guild).channel()

        # Ignore these messages
        if (
            not message.guild or  # Message not in a guild
            message.channel.id != counting_channel or  # Message not in counting channel
            await self.bot.cog_disabled_in_guild(self, message.guild) or  # Cog disabled in guild
            not await self.config.guild(message.guild).toggle() or  # Counting toggled off
            message.author.bot or  # Message author is a bot
            counting_channel is None  # Counting channel not set
        ):
            return

        counter = await self.config.guild(message.guild).counter()
        # Delete these messages
        try:
            # Incorrect number
            if not (int(message.content.strip())-1 == counter):
                await self.config.guild(message.guild).deleted.set(message.id)
                return await message.delete()

            # User repeated and allow repeats is off
            if not await self.config.guild(message.guild).allowrepeats():
                found = False
                last = message
                while not found:
                    last_m = (await message.channel.history(limit=1, before=last).flatten())[0]
                    if not last_m.author.bot:
                        found = True
                if last_m.author.id == message.author.id:
                    await self.config.guild(message.guild).deleted.set(message.id)
                    return await message.delete()

        except ValueError:  # Message contains non-numerical characters
            await self.config.guild(message.guild).deleted.set(message.id)
            return await message.delete()

        await self.config.guild(message.guild).counter.set(counter+1)

        # Assign a role the lastest user to count if toggled
        role_id = await self.config.guild(message.guild).role()
        if await self.config.guild(message.guild).assignrole() and role_id:
            role = message.guild.get_role(role_id)
            if role is not None:
                assigned = False
                for m in role.members:
                    if m.id == message.author.id:
                        assigned = True
                    else:
                        try:
                            await m.remove_roles(role, reason="Counter: no longer the latest user to count")
                        except discord.Forbidden:
                            pass
                if not assigned:
                    try:
                        await message.author.add_roles(role, reason="Counter: latest user to count")
                    except discord.Forbidden:
                        pass

    @commands.Cog.listener("on_message_delete")
    async def _message_deletion_listener(self, message: discord.Message):
        counting_channel = await self.config.guild(message.guild).channel()

        # Ignore these messages
        if (
                not message.guild or  # Message not in a guild
                message.channel.id != counting_channel or  # Message not in counting channel
                await self.bot.cog_disabled_in_guild(self, message.guild) or  # Cog disabled in guild
                not await self.config.guild(message.guild).toggle() or  # Counting toggled off
                message.author.bot or  # Message author is a bot
                counting_channel is None  # Counting channel not set
        ):
            return

        # Also ignore these
        try:
            _ = int(message.content.strip())
            if message.id == await self.config.guild(message.guild).deleted():
                return
        except ValueError:  # Message contains non-numerical characters
            return

        c = await self.bot.get_embed_colour(message.channel)
        e = discord.Embed(color=c, description=f"{message.author.mention} edited or deleted [their message]({message.jump_url}). Original message: ```{message.content}```")
        return await message.channel.send(embed=e)

    @commands.Cog.listener("on_message_edit")
    async def _message_edit_listener(self, before: discord.Message, after: discord.Message):
        await self._message_deletion_listener(before)

    @commands.guild_only()
    @commands.mod()
    @commands.group()
    async def counting(self, ctx: commands.Context):
        """Settings for Counting"""

    @counting.command(name="toggle")
    async def _toggle(self, ctx: commands.Context, true_or_false: bool):
        """Toggle Counting in this server."""
        await self.config.guild(ctx.guild).toggle.set(true_or_false)
        return await ctx.tick()

    @counting.command(name="channel")
    async def _channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Set the Counting channel."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        return await ctx.tick()

    @counting.command(name="starting")
    async def _starting(self, ctx: commands.Context, num: int):
        """Set the counter to start off with."""
        await self.config.guild(ctx.guild).counter.set(num)
        return await ctx.tick()

    @counting.command(name="role")
    async def _role(self, ctx: commands.Context, role: discord.Role):
        """Set the role to assign to the most recent user to count."""
        await self.config.guild(ctx.guild).role.set(role.id)
        return await ctx.tick()

    @counting.command(name="assignrole")
    async def _assignrole(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether to assign a role to the most recent user to count."""
        if not await self.config.guild(ctx.guild).role():
            return await ctx.send("Please set a role first using `[p]counting role <role>`!")
        await self.config.guild(ctx.guild).assignrole.set(true_or_false)
        return await ctx.tick()

    @counting.command(name="allowrepeats")
    async def _allow_repeats(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether users can count multiple times in a row."""
        await self.config.guild(ctx.guild).allowrepeats.set(true_or_false)
        return await ctx.tick()

    @counting.command(name="view")
    async def _view(self, ctx: commands.Context):
        """View the current Counting settings."""
        settings = await self.config.guild(ctx.guild).all()
        desc = f"""
            **Toggle:** {settings["toggle"]}
            **Channel:** {self.bot.get_channel(settings["channel"]).mention if settings["channel"] is not None else None}
            **Current #:** {settings["counter"]}
            **Role:** {ctx.guild.get_role(settings["role"]).mention if settings["role"] is not None else None}
            **Allow Repeats:** {settings["allowrepeats"]}
            **Assign Role:** {settings["assignrole"]}
            """
        await ctx.send(embed=discord.Embed(title="Counting Settings", color=await ctx.embed_color(), description=desc))
