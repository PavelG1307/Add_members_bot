max_invite_of_accounts = 35
timeout=300

from soupsieve import escape
from pyrogram import Client, idle, compose, enums
import time
from pyrogram.errors import PeerFlood, FloodWait, ChatAdminRequired, UserPrivacyRestricted
from pyrogram.handlers import MessageHandler
from pyrogram.raw.functions import account
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import os, sys

def default_set():
    global id_targer_group, peer, num_acc, accounts, id_linked_chat, count_invite, mode, count, id_target_group, bot, acc, members, id_user, id_message, limit_subscribe, timeout, last_usernames
    id_targer_group=0
    id_linked_chat=0
    mode="None"
    count=0
    num_acc = 4
    last_usernames=[None, None]
    peer = None
    # timeout=3
    id_target_group=0
    members=[]
    count_invite = []
    id=[17929149, 18729884, 18487388, 19852069, 19852685, 12580131, 13972561, 12580131, 13972561, 13972561, 18487388]
    hash=['bf4d900c115a3f2ac85385f5a0bfd330','9aaedfe34d59c34fda27109453b8907e','fb455c9f2f7977f7634dee86ce2784d8',
     '65d7c1bc5b165ab8624b6c61e45de265','724fe0f06ef691717c16d28c39430506','09bcadf4428d8e962f201b8e3ae186e3',
     '47c97545504481e30fe812e626a1967b','09bcadf4428d8e962f201b8e3ae186e3','47c97545504481e30fe812e626a1967b',
     '47c97545504481e30fe812e626a1967b','fb455c9f2f7977f7634dee86ce2784d8']
    phone_n = ['+5511965325728', '+5511944126691', '+5511944035669', '+6283831261899',
               '+79633862924', '+79308893807', '+6287746615643','5511952621157','5511957111503','+5511961022806', '+79935592808']
    
    # id=[ 18729884, 19852069, 19852685, 13972561]
    # hash=['9aaedfe34d59c34fda27109453b8907e',
    #  '65d7c1bc5b165ab8624b6c61e45de265','724fe0f06ef691717c16d28c39430506',
    #  '47c97545504481e30fe812e626a1967b']
    # phone_n = [ '+5511944126691', '+6283831261899',
    #            '+79633862924', '+6287746615643']
    accounts=[]
    for i in range(len(id)):
        accounts.append(Client(f'account_{i}', api_id=id[i], api_hash=hash[i], phone_number=phone_n[i]))
        count_invite.append(0)
    bot=Client(
        "bot",
        bot_token="5206831411:AAH3_lnU98drAyS97s-MUfDjr5gYQnyT56E",
        api_id=12580131, api_hash='09bcadf4428d8e962f201b8e3ae186e3'
    )


    id_user=0
    id_message=0
    limit_subscribe=20

def work_acc(id_peer = None, change = False, add = False):
    global num_acc, peer, count_invite
    # if add:
    #     count_invite[num_acc]+=1
    #     if peer is None:
    #         peer = accounts[num_acc].resolve_peer(id_peer)
    # if num_acc == -1 or change or count_invite[num_acc] > max_invite_of_accounts:
    #     num_acc += 1
    #     if num_acc >= len(accounts)-1:
    #         num_acc = 0
    #     # delete
    #     if num_acc == 4 or num_acc == 2:
    #         num_acc+=1
    #     # delete
    if not id_peer is None and peer is None:
        peer = accounts[num_acc].resolve_peer(id_peer)
    print(f'В работе аккаунт {num_acc}')
    return accounts[num_acc], peer

    
def add_mem(member,id):
    global acc, count
    acc = work_acc(id_peer = id, add = True)
    print(f'Рабочий аккаунт: {acc[0].phone_number}')
    try:
        try:
            pass
            # acc.add_contact(member.user.id, member.user.first_name)
            # print(account.index)
        except Exception:
            pass
        success = False
        # peer = acc.resolve_peer('@pasha_no_111')
        print(f'Peer: {acc[1]}')
        if (acc[0].add_chat_members(chat_id=-1001763606822, user_ids=member.user.id, peer_chat = acc[1])):
            count+=1
            print(str(count) + " подписчик:",member.user.first_name,"украден!")
            success = True
        try:
            pass
            # acc.delete_contacts(member.user.id)
            # print('delete contact')
        except Exception:
            pass
        if success:
            return "True"
        else:
            return 'Next'
    except PeerFlood as e:
        print(e)
        print("Заморозили, меняю аккаунт")
        acc = work_acc(change = True, id_peer = id,  add = True)
        return "Flood"
    except UserPrivacyRestricted:
        print("Подписчик:",member.user.first_name,"не хочет вас!")
        return "Next"
    except FloodWait as a:
        print(a)
        print("Меня заморозили")
        return "Flood"
    except Exception as e:
        print(e)
        print("Ошибка!")
        return "Next"

                
def hello(client, message):
    print(message.chat.id, message.id)
    # print(message)
    global id_targer_group, id_linked_chat,count, mode, members, members_list, id_user, id_message, limit_subscribe, id_chat, timeout, last_usernames
    id_user=message.chat.id
    acc = work_acc()[0]
    print(f'Аккаунт: {accounts.index(acc)}')
    if message.text == "/restart":
        os.execv(sys.executable, ['python'] + sys.argv)
        return

    if message.text == "/new_target_channel":
        mode = "None"

    if mode == "None":
        if not last_usernames[0] is None:
            message.reply(text = "Введите username целевого канала", reply_markup=ReplyKeyboardMarkup([[KeyboardButton(last_usernames[0])]]))
        else:
            message.reply(text = "Введите username целевого канала", reply_markup=ReplyKeyboardRemove())
        mode="TgChannel"
        return

    if mode == "TgChannel":
        count=0
        last_usernames[0]=message.text
        id_targer_group=(acc.get_chat(message.text)).id
        print(f'ID группы назначения: {id_target_group}')
        # id_targer_group = '@pasha_no_111'
        print(id_targer_group)
        mode = "Count"
        try:
            my_members = acc.get_chat_members(id_targer_group)
        except ChatAdminRequired:
            message.reply("Рабочий аккаунт не является адмнистратором! Добавьте в список администраторов и заного введите username!")
            mode = "TgChannel"
            return
        else:
            for member in my_members:
                members.append(member.user.id)
            # message.reply("Введите канал с аудиторей!")
            if not last_usernames[1] is None:
                message.reply(text = "Введите канал с аудиторей!", reply_markup=ReplyKeyboardMarkup([[KeyboardButton(last_usernames[1])]]))
            else:
                message.reply(text = "Введите канал с аудиторей!", reply_markup=ReplyKeyboardRemove())
            mode = "Channel"
        return

    if mode == "Channel":
        try:
            last_usernames[1]=message.text
            # id_chat= acc.get_chat(message.text).id
            # members_list = acc.get_chat_members(id_chat)
            id_linked_chat=acc.get_chat(message.text).linked_chat.id
            members_list = acc.get_chat_members(id_linked_chat)
            message.reply("Буду воровать подписчиков с канала: " + message.text, reply_markup=ReplyKeyboardRemove())
            message.reply("Введите желаемый прирост подписчиков")
            mode = "Count"
            return
        except Exception as e:
            print(e)
            try:
                id_linked_chat=acc.get_chat(message.text).linked_chat.id
                members_list = acc.get_chat_members(id_linked_chat)
                message.reply("Буду воровать подписчиков со связаного канала!", reply_markup=ReplyKeyboardRemove())
                message.reply("Введите желаемый прирост подписчиков")
                mode = "Count"
                return
            except Exception:
                message.reply("Увы и ах, не получилось! Введите username другого канала!", reply_markup=ReplyKeyboardRemove())
                mode = "TgChannel"
                return

    if mode == "Count":
        limit_subscribe=int(message.text)
        id_message=message.reply('Украл 0 подписчиков!').id
        # peer_f = acc.resolve_peer(id_targer_group)
        # print(peer_f)
        count_try = 1
        for member in members_list:
            if not member.user.id in members:
                res = add_mem(member, id = id_targer_group)
                count_try+=1
                if res == "Next":
                    try:
                        bot.edit_message_text(id_user, id_message, f"Украл {count} подписчика(-ов)\nПопытка {count_try}")
                    except Exception as e:
                        print(e)
                    time.sleep(100)
                if res =="True":
                    try:
                        bot.edit_message_text(id_user, id_message, f"Украл {count} подписчика(-ов)\nПопытка {count_try}")
                    except Exception as e:
                        print(e)
                    time.sleep(timeout)
                if count>=limit_subscribe:
                    message.reply(f"Всего было украдено {count} подписчика(-ов)!\nНа сегодня все!")
                    mode = "None"
                    return
                elif res=="Flood":
                    print("Flood")
                    message.reply(f"Мороз!")
                    # mode = "None"
                    # return
                    time.sleep(100)
            else:
                print("Уже")
        return
    
if __name__ == "__main__":
    global bot, accounts, num_acc
    default_set()
    bot.add_handler(MessageHandler(hello)) 
    bot.start()
    print("Bot started!")
    print(bot.get_me())
    accounts[num_acc].start()
    idle()
    # compose(accounts)
    
    # print(bot.get_messages(1002363042, 291))
    bot.stop()
