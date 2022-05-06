from pyrogram import Client, enums
import asyncio

app = Client('account_1')
app.start()
# Get members
for m in app.get_chat_members('pasha_no_111'):
    print(m)