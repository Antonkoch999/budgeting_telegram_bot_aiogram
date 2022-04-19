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


class AnswerEnum(enum.Enum):
    ANSWER_INCOME_EXPENSE = 'Вы хотите записать доход или расход?'
    CATEGORY_INCOME_EXPENSE = 'Вы хотите добавить категорию для дохода или расхода?'
    NO_ACCESS = 'У вас нет доступа!'
    CHOICE_CATEGORY = 'Выберие категорию из категории {message_text}:'
    SET_AMOUNT = 'Введите сумму категории: {message_text} в BYN:'
    SET_CATEGORY = 'Введите название категории: '
    INCORRECT_AMOUNT = 'Некорретный формат ввода суммы, попробуйте снова!. Пример: 25.37'
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
    NEW_ENTRY = 'Сделать новую запись'
    START = 'Начало работы с ботом'
    HELP = 'Просмотр меню'
    HISTORY_MONTH = 'История за месяц'
    CANCEL = 'Отменить действие'
    NEW_USER = 'Добро пожаловать, {username}!\n\n'
    ADD_CATEGORY = 'Добавить новую категорию.'
    TOTAL_MONTH = 'Итого за месяц'


class CommandEnum(enum.Enum):
    NEW = 'new'
    HISTORY_MONTH = 'history_month'
    START = 'start'
    HELP = 'help'
    CANCEL = 'cancel'
    ADD_CATEGORY = 'add_category'


HELP_COMMANDS = {
    f'/{CommandEnum.START.value}': AnswerEnum.START.value,
    f'/{CommandEnum.HELP.value}': AnswerEnum.HELP.value,
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
    f'/{CommandEnum.HISTORY_MONTH.value}': AnswerEnum.HISTORY_MONTH.value,
    f'/{CommandEnum.CANCEL.value}': AnswerEnum.CANCEL.value,

}

START_COMMANDS = {
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
}

MENU_COMMANDS = {
    f'/{CommandEnum.NEW.value}': AnswerEnum.NEW_ENTRY.value,
    f'/{CommandEnum.HISTORY_MONTH.value}': AnswerEnum.HISTORY_MONTH.value,
    f'/{CommandEnum.CANCEL.value}': AnswerEnum.CANCEL.value,
    f'/{CommandEnum.ADD_CATEGORY.value}': AnswerEnum.ADD_CATEGORY.value,
}
