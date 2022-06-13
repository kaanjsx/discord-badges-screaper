import discum, time 
from discord_webhook import DiscordWebhook
guild_id = 'server id'
channel_id = 'channel id'
bot = discum.Client(token= "USER TOKEN", log=True)

bot.gateway.fetchMembers(guild_id, channel_id, keep=['public_flags','username','discriminator','premium_since'],startIndex=0, method='overlap')
@bot.gateway.command
def memberTest(resp):
    if bot.gateway.finishedMemberFetching(guild_id):
        lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
        print(str(lenmembersfetched)+' members fetched')
        bot.gateway.removeCommand(memberTest)
        bot.gateway.close()

bot.gateway.run()

def __get_badges(flags):

        BADGES = {
            1 << 0:  'Discord Employee',
            1 << 1:  '<:dc_partner:920013628588040212>',
            1 << 2:  '<:discord_hype:920012101395836949>',
            1 << 3:  '<:discord_bughunter:920012064490160128>',
            1 << 9:  '<:early_supporter:920012134526631946>',
            1 << 10: 'Team User',
            1 << 12: 'System',
            1 << 14: '<:dc_hunterlvl2:920310366016262155>',
            1 << 16: '<:dc_verified:920310231165173810>',
            1 << 17: '<:discord_dev:920012086652842004>',
            1 << 18: '<:dc_mod:920310053368631317>'
        }
        badges = []
        
        for badge_flag, badge_name in BADGES.items():
            if flags & badge_flag == badge_flag:
                badges.append(badge_name)
        return badges

with open('result.txt', 'w', encoding="utf-8") as file :
    for memberID in bot.gateway.session.guild(guild_id).members:
        id = str(memberID)
        temp = bot.gateway.session.guild(guild_id).members[memberID].get('public_flags')
        user = str(bot.gateway.session.guild(guild_id).members[memberID].get('username'))
        disc = str(bot.gateway.session.guild(guild_id).members[memberID].get('discriminator'))
        username = f'{user}#{disc}'
        creation_date = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(((int(id) >> 22) + 1420070400000) / 1000)))
        if temp != None:
            z = __get_badges(temp)
            if len(z) != 0:
                badges = ', '.join(z)
                print(f'Username: {username} - Badges: {badges}\n')
                file.write(f'Username: {username} - Badges: {badges}\n')
                webhook = DiscordWebhook(url='discord server webhook', rate_limit_retry=True, content=f'Username: {username} - Badges: {badges}')
                resp = webhook.execute()
                
