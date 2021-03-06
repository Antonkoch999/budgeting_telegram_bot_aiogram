"""Constant."""
import enum
from aenum import MultiValueEnum


class BaseEnum(enum.Enum):

    @classmethod
    def list_value(cls):
        return [i.value for i in cls]


class StatisticsChoiceEnum(BaseEnum):

    STATISTICS_BY_DAY = 'Статистика за день'
    STATISTICS_BY_MONTH = 'Статистика за месяц'
    STATISTICS_BY_YEAR = 'Статистика за год'
    STATISTICS_BY_PERIOD = 'Статистика за период'


class StatisticsChoiceMonthEnum(MultiValueEnum):

    JANUARY = 'Январь', 1
    FEBRUARY = 'Февраль', 2
    MARCH = 'Март', 3
    APRIL = 'Апрель', 4
    MAY = 'Май', 5
    JUNE = 'Июнь', 6
    JULY = 'Июль', 7
    AUGUST = 'Август', 8
    SEPTEMBER = 'Сентябрь', 9
    OCTOBER = 'Октябрь', 10
    NOVEMBER = 'Ноябрь', 11
    DECEMBER = 'Декабрь', 12

    @classmethod
    def list_value_name_month(cls):
        return [i.value for i in cls]


class HistoryChoiceEnum(BaseEnum):

    HISTORY_BY_DAY = 'История за день'
    HISTORY_BY_MONTH = 'История за месяц'
    HISTORY_BY_YEAR = 'История за год'
    HISTORY_BY_PERIOD = 'История за период'


class IncomeExpenseEnum(BaseEnum):

    INCOME = 'Доход'
    EXPENSE = 'Расход'


class BackEnum(BaseEnum):
    BACK = 'Назад'
    CANCEL = 'Отмена'


class CategoryIncomeEnum(BaseEnum):
    SALARY = 'Зарплата'


class CategoryExpenseList(BaseEnum):
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
    BEAUTY = 'Красота'


class ChoiceDateType(enum.Enum):
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'


class AnswerEnum(enum.Enum):
    ANSWER_INCOME_EXPENSE = 'Вы хотите записать доход или расход?'
    CATEGORY_INCOME_EXPENSE = 'Вы хотите добавить категорию для дохода или расхода?'
    NO_ACCESS = 'У вас нет доступа!'
    CHOICE_CATEGORY = 'Выберие категорию:'
    SET_AMOUNT = 'Введите сумму категории: {message_text} в BYN:'
    SET_CATEGORY = 'Введите название категории: '
    INCORRECT_AMOUNT = 'Некорретный формат ввода суммы, попробуйте снова! Пример: 25.37'
    DATA_RECORDED = 'Данные записаны!'
    NAME = 'Имя:'
    CHAPTER = 'Раздел'
    CATEGORY = 'Категория'
    AMOUNT = 'Сумма'
    DATE = 'Дата'
    BYN = 'BYN'
    START_HEADER = 'Я бот бюджетирования как я могу тебе помочь?\n\n'
    HELP_HEADER = 'Доступны следующие команды: \n\n'
    CANCEL_MESSAGE = 'Действие отменено'
    NEW_ENTRY = 'Добавить расход'
    START = 'Начало работы с ботом'
    HELP = 'Просмотр меню'
    HISTORY = 'История расходов'
    CHOICE_VARIANT_HISTORY = 'Выберите какую историю хотите увидеть'
    CANCEL = 'Отменить действие'
    NEW_USER = 'Добро пожаловать, {username}!\n\n'
    ADD_CATEGORY = 'Добавить новую категорию.'
    TOTAL = 'Итого'
    CHOICE_VARIANT_STATISTICS = 'Выберите какую статистику хотите увидеть.'
    CHOICE_PERIOD = 'Введите период в формате: 21.12.2021-30.12.2021'
    STATISTICS = 'Статистика расходов'


class CommandEnum(enum.Enum):
    NEW = 'new'
    ADD_CATEGORY = 'add_category'
    STATISTICS = 'statistics'
    HISTORY = 'history'
    START = 'start'
    HELP = 'help'
    CANCEL = 'cancel'


HELP_COMMANDS = {
    f'/{CommandEnum.START.value}': AnswerEnum.START.value,
    f'/{CommandEnum.HELP.value}': AnswerEnum.HELP.value,
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
    f'/{CommandEnum.HISTORY.value}': AnswerEnum.HISTORY.value,
    f'/{CommandEnum.CANCEL.value}': AnswerEnum.CANCEL.value,
    f'/{CommandEnum.STATISTICS.value}': AnswerEnum.STATISTICS.value,
}

START_COMMANDS = {
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
}

MENU_COMMANDS = {
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
    f'/{CommandEnum.STATISTICS.value}': AnswerEnum.STATISTICS.value,
    f'/{CommandEnum.HISTORY.value}': AnswerEnum.HISTORY.value,
    f'/{CommandEnum.CANCEL.value}': AnswerEnum.CANCEL.value,
}
