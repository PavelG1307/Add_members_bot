from pyrogram import Client, idle
import time
import asyncio
from pyrogram.errors import PeerFlood, FloodWait, ChatAdminRequired
from pyrogram.handlers import MessageHandler
import os, sys

def default_set():
    global id_targer_group, id_linked_chat, mode, count, id_target_group, bot, acc, members, work_acc, id_user, id_message, limit_subscribe
    id_targer_group=0
    id_linked_chat=0
    mode="None"
    count=0
    id_target_group=0
    members=[]
    id=[12580131]
    hash=['09bcadf4428d8e962f201b8e3ae186e3']

    bot=Client(
        "bot",
        bot_token="5217724819:AAHH4p7q7jMul8aYueArEWbLfoZ4VlPLCpo",
        api_id=id[0],
        api_hash=hash[0]
    )

    acc=Client(
            "acc1",
            api_id=id[0],
            api_hash=hash[0]
    )

    id_user=0
    id_message=0
    limit_subscribe=20


async def add_mem(member):
    global acc, count
    try:
        if (await acc.add_chat_members(chat_id=id_targer_group, user_ids=member.user.id)):
            count+=1
            print(str(count) + " подписчик:",member.user.first_name,"украден!")
            return "True"
    except PeerFlood:
        print(acc.session_name + " заморозили, меняю аккаунт")
        return "Flood"
    except FloodWait as a:
        print("Меня заморозили, жду " + str(a.x) + " сек")
        return "Flood"
    except Exception as e:
        print(e)
        print("Подписчик:",member.user.first_name,"не хочет вас!")
        return "Next"

    
async def hello(client, message):
    global id_targer_group, id_linked_chat,count, mode, members, members_list, id_user, id_message, limit_subscribe, id_chat
    id_user=message.chat.id
    
    if message.text == "/restart":
        os.execv(sys.executable, ['python'] + sys.argv)
        return

    if message.text == "/new_target_channel":
        mode = "None"

    if mode == "None":
        await message.reply("Введите username целевого канала")
        mode="TgChannel"
        return

    if mode == "TgChannel":
        count=0
        id_targer_group=(await acc.get_chat(message.text)).id
        print(id_targer_group)
        mode = "Count"
        try:
            my_members = await acc.get_chat_members(id_targer_group)
        except ChatAdminRequired:
            await message.reply("Рабочий аккаунт не является адмнистратором! Добавьте в список администраторов и заного введите username!")
            mode = "TgChannel"
            return
        else:
            for member in my_members:
                members.append(member.user.id)
            await message.reply("Введите канал с аудиторей!")
            mode = "Channel"
        return

    if mode == "Channel":
        try:
            id_chat=(await acc.get_chat(message.text)).id
            members_list = await(acc.get_chat_members(id_chat))
            await message.reply("Буду воровать подписчиков с канала: " + message.text)
            await message.reply("Введите желаемый прирост подписчиков")
            mode = "Count"
            return
        except Exception as e:
            print(e)
            try:
                id_linked_chat=(await acc.get_chat(message.text)).linked_chat.id
                members_list = await(acc.get_chat_members(id_linked_chat))
                await message.reply("Буду воровать подписчиков со связаного канала!")
                await message.reply("Введите желаемый прирост подписчиков")
                mode = "Count"
                return
            except Exception:
                await message.reply("Увы и ах, не получилось! Введите username другого канала!")
                mode = "TgChannel"
                return

    if mode == "Count":
        limit_subscribe=int(message.text)
        # id_message=(await message.reply('Добавлено 0 аккаунтов')).message_id
        for member in members_list:
            if not member.user.id in members:
                res = await add_mem(member)
                if res=="True" or res=="Next":
                    # await acc.edit_message_text(id_user,id_message,"Украл " + str(count) + " подписчиков!")
                    await asyncio.sleep(60)
                if count>=20:
                    await message.reply("Украл " + str(count) + " подписчиков!\nНа сегодня все!")
                    mode = "None"
                    return
                elif res=="Flood":
                    print("Flood")
                    await message.reply("Украл " + str(count) + " подписчиков!\nВремено заморожен!")
                    mode = "None"
                    return
            else:
                print("Уже")
        await message.reply("Украл " + str(count) + " подписчиков!")
        await message.reply("Введите новый канал с аудиторией\n/new_target_channel – выбрать новый целевой канал")
        mode = "TgChannel"
        return
    
if __name__ == "__main__":
    global bot, acc
    default_set()
    bot.add_handler(MessageHandler(hello)) 
    bot.start()
    acc.start()
    print("Bot started!")
    idle()
    bot.stop()
    acc.stop()
