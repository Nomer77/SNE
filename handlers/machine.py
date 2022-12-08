from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMLieter(StatesGroup):
    menu = State()

class FSMDashboard(StatesGroup):
    menu = State()

class FSMNachtrag(StatesGroup):
    description = State()
    annahme = State()
    submit = State()

class FSMComplete(StatesGroup):
    auswalh = State()
    submit = State()

class FSMDelete(StatesGroup):
    auswalh = State()
    submit = State()

class FSMEdit(StatesGroup):
    auswalh = State()
    annahme = State()
    falte = State()
    submit = State()

class FSMListe(StatesGroup):
    submit = State()

class FSMFeedback(StatesGroup):
    annahme = State()
    submit = State()

class FSMHope(StatesGroup):
    hope = State()


class FSMBoard(StatesGroup):
    menu = State()


class FSMValute(StatesGroup):
    auswalh = State()
    submit = State()