from .rolesync import RoleSync

def setup(bot):
    cog = RoleSync(bot)
    bot.add_cog(cog)