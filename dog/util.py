import discord


def make_profile_embed(member):
    embed = discord.Embed()
    embed.set_author(name=f'{member.name}#{member.discriminator}',
                     icon_url=member.avatar_url)
    return embed


def american_datetime(datetime):
    return datetime.strftime('%m/%d/%Y %I:%M:%S %p')


def pretty_timedelta(delta):
    big = ''

    if delta.days >= 7 and delta.days < 21:
        weeks = round(delta.days / 7, 2)
        plural = 's' if weeks == 0 or weeks > 1 else ''
        big = f'{weeks} week{plural}'

    # assume that a month is 31 days long, i am not trying
    # to be aware
    if delta.days >= 21 and delta.days < 365:
        days = round(delta.days / 31, 2)
        plural = 's' if days == 0 or days > 1 else ''
        big = f'{days} month{plural}'

    if delta.days >= 365:
        years = round(delta.days / 365)
        plural = 's' if years == 0 or years > 1 else ''
        big = f'{years} year{plural}'

    m, s = divmod(delta.seconds, 60)
    h, m = divmod(m, 60)

    return '{}, {:02d}h{:02d}m{:02d}s'.format(big, h, m, s)
