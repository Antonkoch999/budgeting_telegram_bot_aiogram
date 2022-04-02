"""Constant."""
import enum


class BaseEnum(enum.Enum):

    @classmethod
    def list_value(cls):
        return [i.value for i in cls]


class IncomeExpenseEnum(BaseEnum):

    INCOME = 'Доход'
    EXPENSE = 'Расход'


class BackEnum(BaseEnum):
    BACK = 'Назад'
    CANCEL = 'Отмена'


class CategoryIncomeEnum(BaseEnum):
    SALARY = 'Зарплата'
    INDIVIDUAL_ENTREPRENEUR = 'ИП'
    HERMES = 'Hermes'
    OTHER = 'Другое'
    CARE_ALLOWANCE = 'Пособие'
    CURRENCY_EXCHANGE = 'Обмен валют доход'


class CategoryExpenseList(BaseEnum):
    CHILDREN = 'Ребенок'
    CAR = 'Машина'
    HEALTH = 'Лечение'
    PRODUCT = 'Продукты'
    FAST_FOOD = 'Fast-Food'
    CREDIT = 'Кредиты'
    HOUSEHOLD_GOODS = 'Хозяйственные товары'
    UTILITIES = 'Коммунальные услуги, связь'
    LEISURE = 'Досуг'
    CLOTHES = 'Одежда'
    PRESENT = 'Подарки'
    CURRENCY_EXCHANGE = 'Обмен валют расход'


class AnswerEnum(enum.Enum):
    ANSWER_NEW_ENTRY = 'Как вас зовут?'
    ANSWER_INCOME_EXPENSE = 'Вы хотите записать доход или расход?'
    NO_ACCESS = 'У вас нет доступа!'
    CHOICE_CATEGORY = 'Выберие категорию из категории {message_text}:'
    SET_AMOUNT = 'Введите сумму категории: {message_text} в BYN:'
    INCORRECT_AMOUNT = 'Некорретный формат ввода суммы, попробуйте снова!. Пример: 25.37'
    DATA_RECORDED = 'Данные записаны!'
    NAME = 'Имя:'
    CHAPTER = 'Раздел:'
    CATEGORY = 'Категория:'
    AMOUNT = 'Сумма:'
    BYN = 'BYN'
    START_HEADER = 'Привет. Я бот бюджетирования как я могу тебе помочь?\n\n'
    HELP_HEADER = 'Доступны следующие команды: \n\n'
    CANCEL_MESSAGE = 'Действие отменено'
    NEW_ENTRY = 'Сделать новую запись.'
    START = 'Начало работы с ботом.'
    HELP = 'Просмотр меню.'


HELP_COMMANDS = {
    '/help': AnswerEnum.HELP.value,
    '/new': AnswerEnum.NEW_ENTRY.value,
}

START_COMMANDS = {
    '/new': AnswerEnum.NEW_ENTRY.value,
}

USER_IDS = {333252589: "Кристина", 409501763: "Антон"}
