import logging
from discord.ext import commands
from dog import Cog

log = logging.getLogger(__name__)

class Config(Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permitted_keys = [
            'woof_command_enabled'
        ]

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        """ Manages server-specific configuration for the bot. """

    @config.command(name='set')
    async def config_set(self, ctx, name: str, value: str):
        """ Sets a config field for this server. """

        if name not in self.permitted_keys:
            await ctx.send('That configuration value is not allowed.')
            return

        await self.bot.redis.set(f'{ctx.guild.id}:{name}', value)
        await ctx.send('\N{OK HAND SIGN}')

    @config.command(name='permitted')
    async def config_permitted(self, ctx):
        """ Views permitted configuration keys. """
        await ctx.send(', '.join(self.permitted_keys))

    @config.command(name='is_set')
    async def config_is_set(self, ctx, name: str):
        """ Checks if a configuration key is set. """
        is_set = await self.bot.config_is_set(ctx.guild, name)
        await ctx.send('Yes, it is set.' if is_set else 'No, it is not set.')

    @config.command(name='list', aliases=['ls'])
    async def config_list(self, ctx):
        """ Lists set configuration keys for this server. """
        keys = [k.decode().split(':')[1] for k in await self.bot.redis.keys(f'{ctx.guild.id}:*')]
        await ctx.send('Set configuration keys in this server: ' + ', '.join(keys))

    @config.command(name='remove', aliases=['rm', 'del'])
    async def config_remove(self, ctx, name: str):
        """ Removes a config field for this server. """
        await self.bot.redis.delete(f'{ctx.guild.id}:{name}')
        await ctx.send('\N{OK HAND SIGN}')

def setup(bot):
    bot.add_cog(Config(bot))
