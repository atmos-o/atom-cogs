import discord
from redbot.core import Config, commands
from redbot.core.bot import Red


class RoleSync(commands.Cog):
    def __init__(self, bot: Red):
        self.config = Config.get_conf(self, identifier=202005117)
        self.currently_checking = []
        self.bot = bot
        default_guild = {
            "category_roles": [],
            "nitro_only": []
        }
        self.config.register_guild(**default_guild)

# Commands

    @commands.group(name="rolesync")
    @commands.has_permissions(administrator=True)
    async def _rolesync(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @_rolesync.command(name="add", help="Adds a category role.")
    async def _add(self, ctx, role: discord.Role):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [int(r) for c in datas for r in c.keys()]
        if role.id in category_roles:
            await ctx.send("That role is already a category role.")
            return
        datas.append({f"{role.id}": []})
        await self.config.guild(ctx.guild).category_roles.set(datas)
        await ctx.send(f"Added **{role.name}** to category roles.\nYou may now add roles to this category through `{ctx.prefix}rolesync cadd {role.id} <role_to_add>` (with no <> around)")

    @_rolesync.command(name="remove", aliases=["rem"], help="Removes a category role.")
    async def _rem(self, ctx, role: discord.Role):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [int(r) for c in datas for r in c.keys()]
        if role.id not in category_roles:
            await ctx.send("That role is not a category role.")
            return
        for c in datas:
            if str(role.id) in c.keys():
                datas.remove(c)
        await self.config.guild(ctx.guild).category_roles.set(datas)
        await ctx.send(f"Removed **{role.name}** from category roles.")

    @_rolesync.command(name="list", help="Lists all category roles.")
    async def _list(self, ctx):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [[ctx.guild.get_role(int(r)), len(c[r])] for c in datas for r in c.keys()]
        text = ""
        for crole in category_roles:
            if not crole[0]:
                text += f"**Role not found** - {crole[1]} roles\n"
            else:
                text += f"{crole[0].mention} - {crole[1]} roles\n"
        e = discord.Embed(description=text, color=ctx.author.color)
        e.set_author(name="Category Roles List", icon_url=ctx.guild.icon_url)
        e.set_footer(text=f"{ctx.prefix}rolesync clist @category_role | for a list of roles in a category")
        await ctx.send(embed=e)

    @_rolesync.command(name="category_list", aliases=["clist"], help="Lists all roles in a category.")
    async def _category_list(self, ctx, role: discord.Role=None):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [(int(r), c[r]) for c in datas for r in c.keys() if int(r) == role.id]
        if not category_roles:
            await ctx.send("That is not a category role.")
            return
        category = role
        if not category:
            await ctx.send("Category no longer exists.")
            return
        text = ""
        for crole in category_roles[0][1]:
            role = ctx.guild.get_role(crole)
            if not role:
                text += f"**Role not found**\n"
            else:
                text += f"{role.mention}\n"
        e = discord.Embed(description=text if text else "No roles in this category", color=ctx.author.color)
        e.set_author(name=f"Roles in {category.name}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @_rolesync.command(name="category_add", aliases=["cadd"], help="Add a role to a category.")
    async def _category_add(self, ctx, category: discord.Role, role: discord.Role):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [(int(r), c[r]) for c in datas for r in c.keys() if int(r) == category.id]
        if not category_roles:
            await ctx.send("That is not a category role.")
            return
        if role.id in category_roles[0][1]:
            await ctx.send("That role is already in this category.")
            return
        if role.id in [int(r) for c in datas for r in c.keys()]:
            await ctx.send("Categories can't be included in other categories.")
            return
        for c in datas:
            if str(category.id) in c.keys():
                datas.remove(c)
        category_roles[0][1].append(role.id)
        datas.append({f"{category.id}": category_roles[0][1]})
        await self.config.guild(ctx.guild).category_roles.set(datas)
        await ctx.send(f"**{role.name}** was added to **{category.name}** category.")
    
    @_rolesync.command(name="category_remove", aliases=["crem"], help="Remove a role from a category.")
    async def _category_rem(self, ctx, category: discord.Role, role: discord.Role):
        datas = await self.config.guild(ctx.guild).category_roles()
        category_roles = [(int(r), c[r]) for c in datas for r in c.keys() if int(r) == category.id]
        if not category_roles:
            await ctx.send("That is not a category role.")
            return
        if role.id not in category_roles[0][1]:
            await ctx.send("That role is not in this category.")
            return
        for c in datas:
            if str(category.id) in c.keys():
                datas.remove(c)
        category_roles[0][1].remove(role.id)
        datas.append({f"{category.id}": category_roles[0][1]})
        await self.config.guild(ctx.guild).category_roles.set(datas)
        await ctx.send(f"**{role.name}** was removed from **{category.name}** category.")

    @_rolesync.command(name="user_check", aliases=["uc"], help="Fixes all roles on all users.")
    async def _user_check(self, ctx):
        await ctx.send("All user roles will be fixed.")
        guild = ctx.guild
        datas = await self.config.guild(guild).category_roles()
        for data in datas:
            for member in guild.members:
                for category, roles in data.items():
                    category_role = guild.get_role(int(category))
                    if not category_role:
                        continue
                    get_roles = []
                    for role_id in roles:
                        role = guild.get_role(role_id)
                        if not role:
                            continue
                        get_roles.append(role)
                    decide_roles = [r for r in get_roles if r in member.roles]
                    i = 0
                    if not decide_roles:
                        if category_role in member.roles:
                            await member.remove_roles(category_role)
                            i += 1
                    else:
                        if category_role not in member.roles:
                            await member.add_roles(category_role)
                            i += 1
                    if i > 0:
                        break
        datas = await self.config.guild(guild).nitro_only()
        for role_id in datas:
            role = ctx.guild.get_role(role_id)
            if not role:
                continue
            for member in role.members:
                if not member.premium_since:
                    try:
                        await member.remove_roles
                    except:
                        pass

    @_rolesync.command(name="role_check", aliases=["rc"], help="Fixes deleted roles in RoleSync.")
    async def _role_check(self, ctx):
        guild = ctx.guild
        datas = await self.config.guild(guild).category_roles()
        c = 0
        r = 0
        new_datas = []
        for data in datas:
            for category_id, roles in data.items():
                category = guild.get_role(int(category_id))
                if not category:
                    c += 1
                    r += len(roles)
                    continue
                new_roles = []
                for role_id in roles:
                    role = guild.get_role(role_id)
                    if role:
                        new_roles.append(role.id)
                    else:
                        r += 1
                new_datas.append({category_id: new_roles})
        await self.config.guild(ctx.guild).category_roles.set(new_datas)
        await ctx.send(f"{c} Categories removed and {r} roles removed.")
        datas = await self.config.guild(guild).nitro_only()
        r = 0
        new_datas = []
        for role_id in datas:
            role = ctx.guild.get_role(role_id)
            if not role:
                r += 1
                continue
            new_datas.append(role.id)
        await self.config.guild(ctx.guild).nitro_only.set(new_datas)
        await ctx.send(f"{r} nitro roles removed.")

    @_rolesync.command(name="nitro_add", help="Adds a nitro role.")
    async def _nitro_add(self, ctx, role: discord.Role):
        datas = await self.config.guild(ctx.guild).nitro_only()
        if role.id in datas:
            await ctx.send("That role is already a nitro role.")
            return
        datas.append(role.id)
        await self.config.guild(ctx.guild).nitro_only.set(datas)
        await ctx.send(f"Added **{role.name}** to nitro roles.")

    @_rolesync.command(name="nitro_remove", aliases=["nitro_rem"], help="Removes a nitro role.")
    async def _nitro_rem(self, ctx, role: discord.Role):
        datas = await self.config.guild(ctx.guild).nitro_only()
        if role.id not in datas:
            await ctx.send("That role is not a nitro role.")
            return
        datas.remove(role.id)
        await self.config.guild(ctx.guild).nitro_only.set(datas)
        await ctx.send(f"Removed **{role.name}** from nitro roles.")

    @_rolesync.command(name="nitro_list", help="Lists all nitro roles.")
    async def _nitro_list(self, ctx):
        datas = await self.config.guild(ctx.guild).nitro_only()
        category_roles = [ctx.guild.get_role(r) for r in datas]
        text = ""
        for crole in category_roles:
            if not crole:
                text += f"**Role not found**\n"
            else:
                text += f"{crole.mention}\n"
        e = discord.Embed(description=text, color=ctx.author.color)
        e.set_author(name="Nitro Roles List", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=e)

# Events

    @commands.Cog.listener("on_member_update")
    async def rolesync_handler(self, before, after):
        if before.roles == after.roles:
            return
        if before.id in self.currently_checking:
            return
        self.currently_checking.append(before.id)
        guild = before.guild
        datas = await self.config.guild(guild).category_roles()
        for data in datas:
            for category, roles in data.items():
                category_role = guild.get_role(int(category))
                if not category_role:
                    continue
                get_roles = []
                for role_id in roles:
                    role = guild.get_role(role_id)
                    if not role:
                        continue
                    get_roles.append(role)
                decide_roles = [r for r in get_roles if r in after.roles]
                if not decide_roles:
                    if category_role in after.roles:
                        try:
                            await after.remove_roles(category_role)
                        except:
                            pass
                else:
                    if category_role not in after.roles:
                        try:
                            await after.add_roles(category_role)
                        except:
                            pass
        datas = await self.config.guild(guild).nitro_only()
        for role_id in datas:
            role = guild.get_role(role_id)
            if not role:
                continue
            for member in role.members:
                if not member.premium_since:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
        self.currently_checking.remove(before.id)