import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import csv

# получение токена:
with open('token.txt') as f:
    token = f.readline()

# доступ:
vk = vk_api.VkApi(token=token)
api = VkLongPoll(vk)
vks = vk.get_api()
admin_id = '278386986'

# инструкция:
with open('README.txt', encoding="cp1251") as tutorial_file:
    tutorial = ''.join(tutorial_file.readlines())

# темы для формул:
themes = ['Кинематика', 'Динамика', 'Статика', 'Законы сохранения в механике',
          'Механические колебания и волны',
          'МКТ', 'Термодинамика', 'Электростатика', 'Магнитизм', 'Электрический ток',
          'Электромагнитные колебания и волны', 'Атомная и ядерная физика',
          'Квантовая физика', 'Оптика']

# все формулы:
formulas = []
sp_themes = []


def grep_formulas():
    for theme in themes:
        sp = {}
        with open('Формулы/{}.csv'.format(theme), encoding="utf-8-sig") as csv_file:
            data = csv.DictReader(csv_file, delimiter=";", quotechar="'")
            for i in data:
                sp[i['id'] + ')' + i['name']] = i['photo']
            formulas.append(sp)
            sp_themes.append([x for x in sp])


grep_formulas()  # оформил в виде функции, чтобы потом обновлять список возможных формул

# темы для законов:
themes2 = ['Закон сохранения и превращения энергии', 'Механика',
           'Молекулярная физика и термодинамика', 'Электричество и магнетизм',
           'Оптика_', 'Атомная и ядерная физика_']

# все законы:
laws = {}
id_s = []
sp_themes2 = []
for law in themes2[1:-1]:
    lt = []
    laws_2 = {}
    with open('Законы/{}.csv'.format(law)) as csv_file:
        info = csv.DictReader(csv_file, delimiter=";", quotechar="'")
        for i in info:
            laws['15.' + i['id'] + ')' + i['name']] = i['photo']
            laws_2['15.' + i['id'] + ')' + i['name']] = i['photo']
            lt.append(i['id'])
        id_s.append(lt)
        sp_themes2.append([y for y in laws_2])


# вспомогательная функция для отправки сообщений:
def send_msg(vk_session, id_type, iid, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send', {id_type: iid, 'message': message, 'random_id': 0,
                                        "attachment": attachment, 'keyboard': keyboard})


# начальная клавиатура:
def main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Формулы', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Справочные материалы', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Законы', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Лекции', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


# клавиатура с темами для формул:
def get_formules():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(themes[0], color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(themes[1], color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(themes[2], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes[3], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes[4], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes[5], color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(themes[6], color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(themes[7], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(themes[8], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(themes[9], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(themes[10], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(themes[11], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(themes[12], color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(themes[13], color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


# клавиатура с индексами формул;
def get_photos(file_theme):
    keyboard = VkKeyboard(one_time=False)

    # определение темы:
    arr = []
    with open('Формулы\\{}.csv'.format(file_theme), encoding="utf-8-sig") as csv_f:
        data_id = csv.DictReader(csv_f, delimiter=";", quotechar="'")
        for x in data_id:
            arr.append(x['id'])

    # Max 4 buttons on a line:
    id_counter = -1
    for ids in arr:
        if id_counter == 3:
            id_counter = 0
            keyboard.add_line()
            keyboard.add_button(ids, color=VkKeyboardColor.SECONDARY)
        else:
            id_counter += 1
            keyboard.add_button(ids, color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


# клавиатура с темами для законов:
def get_laws():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(themes2[0], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes2[1], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes2[2], color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(themes2[3], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(themes2[4], color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(themes2[5], color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


# клавиатура с индексами законов:
def get_law(num):
    keyboard = VkKeyboard(one_time=False)

    id_counter = -1
    for iid in id_s[num]:
        if id_counter == 3:
            id_counter = 0
            keyboard.add_line()
            keyboard.add_button('15.' + str(iid), color=VkKeyboardColor.SECONDARY)
        else:
            id_counter += 1
            keyboard.add_button('15.' + str(iid), color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


# функция добавления новой формулы:
def add_formula(csv_file_name, csv_line):
    with open(f'Формулы/{csv_file_name}.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(csv_line)


# напоминание:
remind = 'Чтобы вернуться, отправь боту "+".'


# текст и фото в сообщениях:
def main():
    for sms in api.listen():
        if sms.type == VkEventType.MESSAGE_NEW:
            msg = sms.text
            user_get = vks.users.get(user_ids=sms.user_id)
            full_name = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']

            # начало
            if msg == 'Начать' or msg == '+':
                send_msg(vk, 'user_id', sms.user_id, message='↓', keyboard=main_keyboard())

            # инструкция:
            elif msg == '?':
                send_msg(vk, 'user_id', sms.user_id,
                         message=tutorial + '\nЖелаю удачи, {}.'.format(full_name))

            # запрос на добавление новых формул:
            elif '!' in msg and len(msg) > 1:
                if msg[0] == '!':
                    send_msg(vk, 'user_id', sms.user_id,
                             message="Запрос обработан.")
                    vks.messages.send(peer_id=admin_id, random_id=0,
                                      message=f'запрос от пользователя({full_name}) -> {msg}')

            # формулы:
            elif msg == 'Формулы':
                send_msg(vk, 'user_id', sms.user_id,
                         message='Выбери раздел физики ↓', keyboard=get_formules())
                send_msg(vk, 'user_id', sms.user_id, message=remind)
            elif msg in themes:
                nm = themes.index(msg)
                send_msg(vk, 'user_id', sms.user_id, message='\n'.join(sp_themes[nm]))
                send_msg(vk, 'user_id', sms.user_id,
                         message='Выбери номер формулы ↓', keyboard=get_photos(msg))
                send_msg(vk, 'user_id', sms.user_id, message=remind)

            # константы:
            elif msg == 'Справочные материалы':
                send_msg(vk, 'user_id', sms.user_id, attachment='photo-182670376_457239845')

            # TODO -> добавить лекции:
            elif msg == 'Лекции':
                send_msg(vk, 'user_id', sms.user_id,
                         message='Этот раздел находится в стадии разработки.')

            # основные физические законы:
            elif msg == 'Законы':
                send_msg(vk, 'user_id', sms.user_id,
                         message='Выбери раздел физики ↓', keyboard=get_laws())
                send_msg(vk, 'user_id', sms.user_id, message=remind)
            elif msg in themes2:
                if msg == themes2[0]:
                    send_msg(vk, 'user_id', sms.user_id, attachment='photo-182670376_457239846')
                elif msg == themes2[-1]:
                    send_msg(vk, 'user_id', sms.user_id, attachment='photo-182670376_457239878')
                else:
                    nm = themes2.index(msg) - 1
                    send_msg(vk, 'user_id', sms.user_id, message='\n'.join(sp_themes2[nm]))
                    send_msg(vk, 'user_id', sms.user_id, message='Выбери номер закона ↓',
                             keyboard=get_law(themes2.index(msg) - 1))
                send_msg(vk, 'user_id', sms.user_id, message=remind)

            # вывод запроса:
            elif '.' in msg and len(msg) < 6 and msg.replace('.', '').isdigit():
                f1 = int(msg[:msg.index('.')]) - 1
                f2 = int(msg[msg.index('.') + 1:]) - 1
                # Если требуются формулы:
                if f1 < 14:
                    try:
                        send_msg(vk, 'user_id', sms.user_id, attachment=formulas[f1][sp_themes[f1][f2]])
                    except IndexError:
                        print("[REMINDER]: добавилась формула")
                # Если требуются законы:
                elif f1 == 14:
                    send_msg(vk, 'user_id', sms.user_id, attachment=laws[[y for y in laws][f2]])
                send_msg(vk, 'user_id', sms.user_id, message=remind)

            # /add_formula (csv_file_name) -> (csv_line)
            # 'id';'name';'photo'
            # id смотреть по клавиатуре
            elif msg.startswith('/add_formula') and str(sms.user_id) == admin_id:
                add_formula(msg[14:msg.index(')')], msg[msg.index(')') + 9:-1].split(";"))
                grep_formulas()
                print("[REMINDER]: добавилась формула")


if __name__ == "__main__":
    main()
