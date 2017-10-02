import config_bot
import telebot
import pars
import requests
import json

bot = telebot.TeleBot(config_bot.token)
group = ''
def number_less():
    i = '%d' %pars.now_time.isoweekday()
    lesson = ''
    if i in range(830,1000):        #
        lesson = '1'
    elif i in range(1025,1155):     #
        lesson = '2'
    elif i in range(1220,1350):     #
        lesson = '3'
    elif i in range(1415,1545):     #
        lesson = '4'
    elif i in range(1610,1805):     #
        lesson = '5'
    else:
        print('Зараз немає пари')
    return lesson
def get_shedule(group,message):
    try:
        url = 'https://api.rozklad.hub.kpi.ua/groups/?name=%s' %group.lower()
        s = requests.session()
        z = s.get(url)
        global parsed
        parsed = json.loads(z.text)
        id_group = parsed['results'][0]['id']
        url = 'https://api.rozklad.hub.kpi.ua/groups/%s/timetable/' %id_group
        y = s.get(url)
        parsed = json.loads(y.text)
        return parsed
    except IndexError:
        bot.send_message(message.chat.id,'<b>Упс, ви ввели неіснуючу группу:((</b>',parse_mode='HTML')

@bot.message_handler(commands=['set'])
def set_group(message):
    print(message.from_user.first_name)
    global group
    try:
        _, group = message.text.split(' ')
    except ValueError:
        None
    bot.send_message(message.chat.id,'Твоя група - {}.\n Якщо помилився, пиши /set номер_групи(іо-65,ік-42)'.format(group),parse_mode='HTML')
    return group

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.first_name)
    bot.send_message(message.chat.id,'<i>Привіт</i>, <b>{}</b>!\n<i>Це бот для швидкого та зручного доступу до розкладу.\nПиши команду</i> /set <i>номер_групи</i> (/set іо-65)'.format(message.from_user.first_name), parse_mode='HTML')

@bot.message_handler(commands=['contacts'])
def start(message):
    bot.send_message(message.chat.id,"<i>Звя'зок з розробником</i> @iantoshkai".format(message.from_user.first_name), parse_mode='HTML')
    print(message.from_user.first_name)
@bot.message_handler(commands=['today'])
def rozklad_now(message):
    print(message.from_user.first_name)
    get_shedule(group,message)
    y = ''
    if pars.day == '7':
        bot.send_message(message.chat.id, '<i>Сьогодні пар немає, відпочивай :)</i>', parse_mode='HTML')
    else:
        for i in range(1,6):
            try:
                predmet = parsed['data'][pars.week][pars.day]['%d' %i]['discipline']['full_name']
                prepod = parsed['data'][pars.week][pars.day]['%d' %i]['teachers'][0]['short_name'] #ФИО викладача
                corpus = parsed['data'][pars.week][pars.day]['%d' %i]['rooms'][0]['building']['name'] #Номер корпуса
                audience = parsed['data'][pars.week][pars.day]['%d' %i]['rooms'][0]['name']
                y +='{}) <b>{}</b>\n<i>{} копрус, {} аудиторія</i>\n<em>{}</em>\n'.format(i,predmet,corpus,audience,prepod)
                i=i+1
            except KeyError:
                None
            except IndexError:
                None
        bot.send_message(message.chat.id, '{}'.format(y),parse_mode='HTML')

@bot.message_handler(commands=['tomorrow'])
def rozklad_tomorrow(message):
    print(message.from_user.first_name)
    get_shedule(group,message)
    if pars.week == '1' and pars.day == '7':
        week = '2'
        day = '1'
    elif pars.week == '2' and pars.day == '7':
        week = '1'
        day = '1'
    else :
        week = pars.week
        day = '{}'.format(int(pars.day)+1)
    y = ''
    for i in range(1,6):
        try:
            predmet = parsed['data'][week][day]['%d' %i]['discipline']['full_name']
            prepod = parsed['data'][week][day]['%d' %i]['teachers'][0]['short_name'] #ФИО викладача
            corpus = parsed['data'][week][day]['%d' %i]['rooms'][0]['building']['name'] #Номер корпуса
            audience = parsed['data'][week][day]['%d' %i]['rooms'][0]['name']
            type1 = parsed['data'][week][day]['%d' %i]['type']
            t = '%s'%type1
            def types(t):
                if t == '0':
                    t = 'Лек'
                elif t == '1':
                    t = 'Прак'
                elif t == '2':
                    t = 'Лаб'
                return t
            y +='{}) <b>{}</b><i>({})</i>\n<i>{} копрус, {} аудиторія</i>\n<em>{}</em>\n'.format(i,predmet,types(t),corpus,audience,prepod)
            i=i+1
        except KeyError:
            None
        except IndexError:
            None
    bot.send_message(message.chat.id, '{}'.format(y),parse_mode='HTML')

@bot.message_handler(commands=['name'])
def name_teacher(message):
    print(message.from_user.first_name)
    get_shedule(group,message)
    try:
        prepod = parsed['data'][pars.week][pars.day]['{}'.format(number_less())]['teachers'][0]['full_name'] #ФИО викладача
        bot.send_message(message.chat.id, '<b>{}</b>'.format(prepod),parse_mode='HTML')
    except KeyError:
        bot.send_message(message.chat.id, '<i>Зараз немає пари:)</i>',parse_mode='HTML')
    except IndexError:
        bot.send_message(message.chat.id, '<i>Зараз немає пари:)</i>',parse_mode='HTML')

@bot.message_handler(commands=['which'])
def which_less(message):
    print(message.from_user.first_name)
    get_shedule(group,message)
    try:

        predmet = parsed['data'][pars.week][pars.day]['{}'.format(number_less())]['discipline']['full_name']
        prepod = parsed['data'][pars.week][pars.day]['{}'.format(number_less())]['teachers'][0]['full_name'] #ФИО викладача
        corpus = parsed['data'][pars.week][pars.day]['{}'.format(number_less())]['rooms'][0]['building']['name'] #Номер корпуса
        audience = parsed['data'][pars.week][pars.day]['{}'.format(number_less())]['rooms'][0]['name']
        bot.send_message(message.chat.id, 'Зараз  <b>{}</b>\n<i>{} копрус, {} аудиторія</i>\n<em>{}</em>\n'.format(predmet,corpus,audience,prepod),parse_mode='HTML')
    except KeyError:
        bot.send_message(message.chat.id, '<i>Зараз немає пари:)</i>',parse_mode='HTML')
    except IndexError:
        None

if __name__ == '__main__':
     bot.polling(none_stop=True)
