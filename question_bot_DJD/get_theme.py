import pymorphy3


def get_theme(applic):
    zap = ["документ", "записать", "записаться", "запись"]
    age = ["год", "возраст"]
    rent = ["прокатиться", "прокатить", "проехать", "билет", "прокат"]
    excur = ["экскурсия"]
    schedule = ["когда", "занятие", "расписание"]
    place = ["где", "местоположение"]
    th = [zap, age, rent, excur, schedule, place]
    morph = pymorphy3.MorphAnalyzer()
    res = {
        "прокат": 0,
        "экскурсия": 0,
        "запись": 0,
        "расписание": 0,
        "возраст": 0,
        "местоположение": 0,
    }
    for word in applic.split():
        word = "".join(list(filter(lambda x: x.isalpha(), word)))
        word = morph.parse(word.lower())[0].normal_form
        for them in th:
            if word.lower() in them:
                res[them[-1]] += 1
    return res
