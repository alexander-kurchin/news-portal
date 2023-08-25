from django import template


register = template.Library()


@register.filter()
def pretty_rating(value, param='&#x2B50;'):
    return value * param


@register.filter()
def censor(value):
    BAD_WORDS = {'Oxxxymiron ': 'O*********',
                 'Говно': 'Г****',
                 'залупа': 'з*****',
                 'пенис': 'п****',
                 'хер': 'х**',
                 'хуй': 'х**',
                 'блядина': 'б******',
                 'шлюха': 'ш****',
                 'жопа': 'ж***',
                 'еблан': 'е****',
                 'Мудила': 'М*****',
                 'мудила': 'м*****',
                 'Рукоблуд': 'Р*******',
                 'ссанина': 'с******',
                 'блядун': 'б*****',
                 'вагина': 'в*****',
                 'Сука': 'С***',
                 'ебланище': 'е*******',
                 'влагалище': 'в********',
                 'пердун': 'п*****',
                 'дрочила': 'д******',
                 'Пидор': 'П****',
                 'пизда': 'п****',
                 'Гомик': 'Г****',
                 'пилотка': 'п******',
                 'манда': 'м****',
                 'педрила': 'п******',
                 'Шалава': 'Ш*****',
                 'хуило': 'х****',
                 'мошонка': 'м******',
                 'елда': 'е***'}
    v = value[:]
    for word in BAD_WORDS.keys():
        v = v.replace(word, BAD_WORDS[word])
    return v
