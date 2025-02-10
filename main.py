import openai
from sqlalchemy import delete, select
from fsm import *   
import httpx
from os import getenv
from config import settings
from keyboards import *
from models import *
from asyncio import sleep
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2


storage = RedisStorage2(host='localhost', port=6379, db=5)
proxy_url = "http://3.126.147.182:80"

openai.aiosession.set(httpx.AsyncClient(proxy=proxy_url))
openai.api_key = settings.openai.token 
engine = create_async_engine(url=settings.db.url, echo=settings.db.echo)

session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
)

bot: Bot = Bot(token=settings.bot.token)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)

@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await message.answer("попа")
    await message.answer("""
Привет! Я, MetaMindBot предназначенный для школьников и студентов с целью формирования и развития метакогнитивных навыков, включая осознание собственных мыслительных процессов, рефлексию, самооценку и стратегическое планирование обучения (развитие критического мышления и стратегий обучения, а также тренировки работы с информацией.
Я — твой персональный помощник по развитию метакогнитивных навыков. Меня зовут MetaMindBot 🤖\n\n"
"🔹 Меня создала Елена Заподойникова, психолог, нейропсихолог, свободный исследователь, аспирант-экстерн, "
"автор проекта «Культура ИИ: умное обучение» для того, чтобы помочь тебе осознанно учиться, анализировать "
"свой прогресс и находить лучшие стратегии самостоятельного обучения.  Подписывайтесь на её канал: @eduneuro2025\n\n"
"📌 Важно: Конфиденциальность для пользователей гарантирована. Методика является образовательной, авторские права защищены. "
"🔹 Со мной ты научишься:\n"
"🔹 — Рефлексировать и анализировать свой день\n"
"🔹 — Улучшать учебные привычки\n"
"🔹 — Развивать концентрацию и осознанность\n"
"🔹 — Работать с информацией эффективно и быстро\n"
"🔹 — Готовиться к экзаменам без стресса\n"
"🔹 — Использовать эффективные методы запоминания\n"
"🔹 — Применять стратегии тайм-менеджмента\n\n"
"🔥 Давай начнем! Выбери кнопку ниже, чтобы зарегистрироваться! 🔥"
    )
Как работает бот?
1.	Пройди входное тестирование – это обязательный шаг перед началом работы.
2.	После теста получишь доступ к функциям бота.
3.	Следуй рекомендуемому графику (3 занятия в неделю): 
o	Метакогнитивные упражнения (/train)
o	Тренинг работы с информацией (🧠 InfoTraining)
o	Рефлексия (/reflect)
o	Помодоро-таймер для продуктивного обучения (/pomodoro)
4.	Через 3 месяца бот предложит повторное тестирование (/retest).
5.	Используй поддержку: 
o	Если у тебя проблемы с мотивацией — напиши в психологический чат (/psych_chat).
6.	Не забывай про бонусы! 
o	Чем активнее ты проходишь тренировки, тем больше награды и достижения (/achievements) ты получишь!
🚀 Давай начнем! Для регистрации пройди входные тесты по кнопке ниже.""", reply_markup=start_keyboard())


@dp.message_handler(commands="help")
async def help_cmd(message: types.Message):
    await message.answer("""📌 Помощь по MetaMindBot

Привет! 👋 Я **MetaMindBot**, твой помощник в развитии **метакогнитивных навыков**. Я помогу тебе улучшить память, концентрацию, критическое мышление и научиться осознанно подходить к обучению.  

Вот список доступных команд:  

**📊 Тестирование и прогресс**  
🔹 **/test** – Пройти входное тестирование.  
🔹 **/retest** – Повторное тестирование через 3 месяца.  
🔹 **/progress** – Оценка динамики навыков.  

**🧠 Обучение и тренировки**  
🔹 **/reflect** – Рефлексия дня (анализ успехов и трудностей).  
🔹 **/train** – Метакогнитивные упражнения (логика, внимание, креативность).  
🔹 **/info_training** – Тренинг работы с информацией (критическое мышление, анализ данных).  
🔹 **/quiz** – Квизы по разным предметам.  
🔹 **/courses** – Подборка полезных онлайн-курсов.  

**💡 Поддержка и продуктивность**  
🔹 **/psych_chat** – Чат с психологом (ИИ поможет справиться со стрессом).  
🔹 **/pomodoro** – Pomodoro-таймер для продуктивной учебы.  
🔹 **/reminders** – Напоминания о задачах и занятиях.  


**📚 Полезные материалы**  
🔹 **/resources** – Полезные статьи, исследования, образовательные платформы.  

📌 **Совет:** Начни с тестирования **/test**, проходи **тренировки 3 раза в неделю**, используй **Pomodoro-таймер** и не забывай **рефлексировать**!  

Если у тебя возникли вопросы, просто напиши мне! 🚀""")


@dp.callback_query_handler(text="start_test")
async def start_test_callback_cmd(call: types.CallbackQuery):
    await call.message.edit_text("""Сообщение для отправки тестирования
    
""", reply_markup=auth_code())


@dp.callback_query_handler(text="auth_code")
async def auth_code_callback_command(call: types.CallbackQuery):
    await call.message.edit_text("Введите код:")
    await Auth.code.set()


@dp.message_handler(commands="pomodoro")
async def pomodoro_CMD(message: types.Message):
    async with session_factory() as session:
        stmt = select(PomodoroUser).where(PomodoroUser.user_id == message.from_user.id)
        user = await session.execute(statement=stmt)
        user = user.scalar()
        await session.commit()
    print(user)
    if user is not None:
        print(1)
        async with session_factory() as session:
            stmt = delete(PomodoroUser).where(PomodoroUser.user_id == message.from_user.id)
            await session.execute(statement=stmt)
            await session.commit()
            return
    if user is None:
        async with session_factory() as session:
            stmt = insert(PomodoroUser).values(user_id=message.from_user.id)
            user = await session.execute(statement=stmt)
            await session.commit()
        while True:
            await message.answer("Start1")
            await sleep(5) #TODO 20 * 60
            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == message.from_user.id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                print("3")
                return
            
            await message.answer("Start2")
            await sleep(2) #TODO 5 * 60

            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == message.from_user.id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                print("2")
                return


# @dp.message_handler(commands="train")
# async def train_CMD(message: types.Message):
#     await message.answer("""Приветствую тебя! Ты на верном пути!
# Запомни, что  эти универсальные упражнения развивают несколько метакогнитивных навыков: осознание мышления, самоконтроль, критическое мышление, планирование, саморегуляция, развитие памяти и обучение.
# Выполняй их 3 раза в неделю на протяжении 3 месяцев и ты почувствуешь, как прокачиваются твои навыки раз за разом""",)












































import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from sqlalchemy.orm import sessionmaker


# Настройки


# Определяем состояния FSM
class ExerciseStates(StatesGroup):
    waiting_for_answer1 = State()
    waiting_for_answer2 = State()
    waiting_for_answer3 = State()
    waiting_for_answer4 = State()

# Функция проверки ответа (не менее 6 слов)
def is_valid_answer(text):
    return len(text.split()) >= 6

# Старт бота
@dp.message_handler(commands=['train'])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Давай проведем упражнение 'Экзамен через 3 дня'.\n"
        "Я задам тебе несколько вопросов, а ты ответь развернуто (не менее 6 слов)."
    )
    await ask_question1(message)

# Вопрос 1
async def ask_question1(message: types.Message):
    await message.answer("1️⃣ Что ты знаешь по этой теме? (не менее 6 слов)")
    await ExerciseStates.waiting_for_answer1.set()

@dp.message_handler(state=ExerciseStates.waiting_for_answer1)
async def process_answer1(message: types.Message, state: FSMContext):
    if not is_valid_answer(message.text):
        await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
        return

    await state.update_data(answer1=message.text)
    await message.answer("✅ Хорошо! Теперь следующий вопрос.")
    await ask_question2(message)

# Вопрос 2
async def ask_question2(message: types.Message):
    await message.answer("2️⃣ Какие пробелы есть? Как ты это понял?")
    await ExerciseStates.waiting_for_answer2.set()

@dp.message_handler(state=ExerciseStates.waiting_for_answer2)
async def process_answer2(message: types.Message, state: FSMContext):
    if not is_valid_answer(message.text):
        await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
        return

    await state.update_data(answer2=message.text)
    await message.answer("✅ Отлично! Переходим к следующему вопросу.")
    await ask_question3(message)

# Вопрос 3
async def ask_question3(message: types.Message):
    await message.answer("3️⃣ Какие методы подготовки ты используешь? Какие лучше работают?")
    await ExerciseStates.waiting_for_answer3.set()

@dp.message_handler(state=ExerciseStates.waiting_for_answer3)
async def process_answer3(message: types.Message, state: FSMContext):
    if not is_valid_answer(message.text):
        await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
        return

    await state.update_data(answer3=message.text)
    await message.answer("✅ Хороший ответ! Теперь последний вопрос.")
    await ask_question4(message)

# Вопрос 4
async def ask_question4(message: types.Message):
    await message.answer("4️⃣ Как ты распределишь время на подготовку?")
    await ExerciseStates.waiting_for_answer4.set()

@dp.message_handler(state=ExerciseStates.waiting_for_answer4)
async def process_answer4(message: types.Message, state: FSMContext):
    if not is_valid_answer(message.text):
        await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
        return

    # Сохраняем все ответы в БД
    user_data = await state.get_data()
    async with session_factory as session:
        session.add(UserAnswer(
            user_id=message.from_user.id,
            answer1=user_data["answer1"],
            answer2=user_data["answer2"],
            answer3=user_data["answer3"],
            answer4=message.text
        ))
        session.commit()
        session.close()

    await message.answer(
        "✅ Ты молодец! Отлично отвечаешь на все вопросы.\n\n"
        "📌 Совет по подготовке:\n"
        "• Сначала повтори главные темы, затем проработай сложные.\n"
        "• Сделай тест на самопроверку.\n"
        "• Через день оцени, что запомнил, повтори слабые места.\n\n"
        "📅 Выполняй это упражнение 3 раза в неделю!"
    )
    await state.finish()













































if __name__ == "__main__":
    executor.start_polling(skip_updates=True, dispatcher=dp)