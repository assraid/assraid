#!/usr/bin/env python3

import discord
import json
import random
import asyncio

config = json.loads(open("config.json", "rb").read().decode("utf-8"))
shit_lines = [x for x in open(config["shit file"], "rb").read().decode("utf-8").split("\n") if x]
client = discord.Client()
users_to_ass = list()
assed_users_who_blocked_us = list()


async def ass_task():
    total_users_count = len(users_to_ass)
    while True:
        for user in users_to_ass:
            try:
                print(f"Sending message to {user.name}")
                await client.send_message(user, random.choice(shit_lines))
            except Exception as e:
                assed_users_who_blocked_us.append(user)
                users_to_ass.remove(user)
                print(f"{user.name} blocked us (exception: {e}). Blocked rate: {len(assed_users_who_blocked_us) * 100 / total_users_count:.1f}%")
        if len(users_to_ass) == 0:
            print("All users blocked us. Exiting")
            await client.logout()
            break


@client.event
async def on_ready():
    # Try to resolve the role names to role IDs
    role_ids = list()
    for server in client.servers:
        for role in server.roles:
            if role.name.strip("@") in config["ignore roles"]:
                role_ids.append(role.id)
                config["ignore roles"].remove(role.name.strip("@"))
    print(role_ids)
    print(config["ignore roles"])

    # Determine the users to ass
    users_ignored = list()
    for member in client.get_all_members():
        if any(ignore in [x.id for x in member.roles] for ignore in role_ids):
            users_ignored.append(member)
            continue
        users_to_ass.append(member)

    print(f"Logged in as {client.user.name}")
    print(client.user.name)
    print(f"Bot can see {len(users_to_ass)} members ({len(users_ignored)} users ignored due to roles).")
    print("They are now being assed")
    asyncio.ensure_future(ass_task())


@client.event
async def on_member_ban(member):
    print(f"You were banned from server {member.server.name}")
    return ()


@client.event
async def on_message(message):
    return ()


client.run(config["login"]["email"], config["login"]["password"])
