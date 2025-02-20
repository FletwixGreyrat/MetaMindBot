import datetime
import openai
from openai import OpenAI
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



client = openai.OpenAI(
    api_key=settings.openai.token,
    base_url="https://api.proxyapi.ru/openai/v1",
)


engine = create_async_engine(url=settings.db.url, echo=settings.db.echo)

session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
)

bot: Bot = Bot(token=settings.bot.token)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)





async def ask_gpt(messages: list):
    chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
    )

    response_content = chat_completion.choices[0].message.content
    return response_content


@dp.callback_query_handler(text="main_menu")
async def return_to_main_menu(call: types.CallbackQuery):
    await call.message.answer("""
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
Как работает бот?z
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
🚀 Давай начнем! Для регистрации пройди входные тесты:
    <a href="https://onlinetestpad.com/s/academic-text-skills">Тест 1</a>
    <a href="https://onlinetestpad.com/t/borzova-text-test">Тест 2</a>
    <a href="https://onlinetestpad.com/t/starkey2004-lutsenko2014">Тест 3</a>
    <a href="https://onlinetestpad.com/t/arpov-reflection-test">Тест 4</a>
    <a href="https://onlinetestpad.com/t/Metacognition-activity">Тест 5</a>
    <a href="https://onlinetestpad.com/t/merkulova-ak-test">Тест 6</a>""", parse_mode="html", reply_markup=start_keyboard())




@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    async with session_factory() as session:
        stmt = select(User).where(User.user_id == message.from_user.id)
        res = await session.execute(statement=stmt)
        if res.scalar() is None:
            stmt = insert(User).values(user_id=message.from_user.id, datetime=datetime.datetime.now().strftime('%Y-%m-%d'))
            await session.execute(statement=stmt)
            await session.commit()
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
Как работает бот?z
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
🚀 Давай начнем! Для регистрации пройди входные тесты:
    <a href="https://onlinetestpad.com/s/academic-text-skills">Тест 1</a>
    <a href="https://onlinetestpad.com/t/borzova-text-test">Тест 2</a>
    <a href="https://onlinetestpad.com/t/starkey2004-lutsenko2014">Тест 3</a>
    <a href="https://onlinetestpad.com/t/arpov-reflection-test">Тест 4</a>
    <a href="https://onlinetestpad.com/t/Metacognition-activity">Тест 5</a>
    <a href="https://onlinetestpad.com/t/merkulova-ak-test">Тест 6</a>""", parse_mode="html", reply_markup=start_keyboard())
            
        else:
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
Как работает бот?z
1.	Пройди входное тестирование – это обязательный шаг перед началом работы.
2.	После теста получишь доступ к функциям бота.
3.	Следуй рекомендуемому графику (3 занятия в неделю): 
    o	Метакогнитивные упражнения (/train)
    o	Тренинг работы с информацией (🧠 InfoTraining)
    o	Рефлексия (/reflect)
    o	Помодоро-таймер для продуктивного обучения (/pomodoro)
4.	Через 3 месяца бот предложит повторное тестирование (/retest).
5.	Используй поддержку: 
    o	Если у тебя проблемы с мотивацией — напиши в психологический чат (/psych_chat).""", reply_markup=start_keyboard())


    await sleep(90 * 24 * 60 * 60)

    await message.answer("""Привет!
У тебя все отлично получается. Ты занимаешься уже 3 месяца, супер!
Настало время зафиксировать прогресс, пройдя заново тесты. Смело пиши /retest""", parse_mode="html")





@dp.message_handler(commands="courses")
async def courses_command(message: types.Message):
    await message.answer("""
🎓 **Рекомендованные онлайн-курсы:**\n\n"
📘 [Stepik](https://stepik.org/)\n"
💡 [Coursera](https://www.coursera.org/)\n"
👨‍💻 [Harvard CS50](https://cs50.harvard.edu/)\n"
📖 [OpenEdu](https://openedu.ru/)\n\n"
🎓 **Курсы ведущих российских университетов:**\n"
🏛 [Томский государственный университет (ТГУ)](https://mooc.tsu.ru/)\n"
📚 [МГУ – Открытое образование](https://openedu.ru/university/msu/)\n"
🏫 [Высшая школа экономики (ВШЭ) – Онлайн-курсы](https://elearning.hse.ru/)\n\n"

📌 Выбери платформу и начни обучение! 🚀""", parse_mode="Markdown", reply_markup=main_menu_keyboard())



@dp.message_handler(commands="resources")
async def resources_command(message: types.Message):
     await message.answer("""
📚 **Полезные научные ресурсы:**\n\n"
🔎 [Google Scholar](https://scholar.google.com/)\n"
📖 [SciSpace](https://www.scispace.com/)\n"
📚 [eLibrary](https://elibrary.ru/)\n"
🔬 [PubMed](https://pubmed.ncbi.nlm.nih.gov/)\n"
📄 [SpringerLink](https://link.springer.com/)\n"
🧠 [ResearchGate](https://www.researchgate.net/)\n\n"

📌 Используй эти сайты для поиска научных статей и исследований.
""", parse_mode="Markdown", reply_markup=main_menu_keyboard())





@dp.callback_query_handler(text_startswith="s:")
async def start_keyboard_handler(call: types.CallbackQuery, state: FSMContext):
    dat = call.data.split(":")[1]

    if dat == "help":
        await help_cmd(message=call.message)


    if dat == "pomodoro":
        await pomodoro_logic(message=call.message, user_id=call.from_user.id)

    if dat == "metakog":
        await train_start_cmd(message=call.message, state=state)
    
    if dat == "info":
        await info_training_command(message=call.message, state=state)
    
    if dat == "reflect":
        await reflect_command(message=call.message, state=state)
    
    if dat == "psycho":
        await psych_chat(message=call.message, state=state)
    
    if dat == "retest":
        await retest_logic(message=call.message, user_id=call.from_user.id)
    
    if dat == "profile":
        await profile_logic(message=call.message, user_id=call.from_user.id)


@dp.message_handler(commands="help")
async def help_cmd(message: types.Message):
    await message.answer("""📌 Помощь по MetaMindBot

Привет! 👋 Я **MetaMindBot**, твой помощник в развитии **метакогнитивных навыков**. Я помогу тебе улучшить память, концентрацию, критическое мышление и научиться осознанно подходить к обучению.  

Вот список доступных команд:  

**📊 Тестирование и прогресс**  
🔹 **/retest** – Повторное тестирование через 3 месяца.  
🔹 **/profile** – Оценка динамики навыков.  

**🧠 Обучение и тренировки**  
🔹 **/reflect** – Рефлексия дня (анализ успехов и трудностей).  
🔹 **/train** – Метакогнитивные упражнения (логика, внимание, креативность).  
🔹 **/info_training** – Тренинг работы с информацией (критическое мышление, анализ данных).  
🔹 **/quiz** – Квизы по разным предметам.  
🔹 **/courses** – Подборка полезных онлайн-курсов.  

**💡 Поддержка и продуктивность**  
🔹 **/psych_chat** – Чат с психологом (ИИ поможет справиться со стрессом).  
🔹 **/pomodoro** – Pomodoro-таймер для продуктивной учебы.  


**📚 Полезные материалы**  
🔹 **/resources** – Полезные статьи, исследования, образовательные платформы.  

📌 **Совет:** Начни с тестирования **/test**, проходи **тренировки 3 раза в неделю**, используй **Pomodoro-таймер** и не забывай **рефлексировать**!  

Если у тебя возникли вопросы, просто напиши мне! 🚀""", reply_markup=main_menu_keyboard())



@dp.message_handler(commands="pomodoro")
async def pomodoro_CMD(message: types.Message):
    await pomodoro_logic(message=message, user_id=message.from_user.id)



async def pomodoro_logic(message: types.Message, user_id: int):
    async with session_factory() as session:
        stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
        user = await session.execute(statement=stmt)
        user = user.scalar()
        await session.commit()
    print(user)
    if user is not None:
        async with session_factory() as session:
            stmt = delete(PomodoroUser).where(PomodoroUser.user_id == user_id)
            await session.execute(statement=stmt)
            await session.commit()
            await message.answer("⏹ Pomodoro-таймер остановлен. Если хочешь снова запустить, напиши /pomodoro", reply_markup=main_menu_keyboard())
            return
    if user is None:
        async with session_factory() as session:
            stmt = insert(PomodoroUser).values(user_id=user_id)
            user = await session.execute(statement=stmt)
            await session.commit()

            await message.answer("🍅 Pomodoro-таймер запущен! Работай 25 минут, затем будет 5 минут отдыха.")
            await sleep(25 * 60)
            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                print("3")
                return
            
            await message.answer("⏳ Перерыв 5 минут! Отдохни и расслабься. ☕")
            await sleep(5 * 60)

            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("🚀 Новый Pomodoro-цикл! Работай еще 25 минут.")
            await sleep(25 * 60)

            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("⏳ Перерыв 5 минут! Отдохни и расслабься. ☕")
            await sleep(5 * 60)

            
            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("🚀 Новый Pomodoro-цикл! Работай еще 25 минут.")
            await sleep(25 * 60)

            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("⏳ Перерыв 5 минут! Отдохни и расслабься. ☕")
            await sleep(5 * 60)



            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("🚀 Новый Pomodoro-цикл! Работай еще 25 минут.")
            await sleep(25 * 60)

            async with session_factory() as session:
                stmt = select(PomodoroUser).where(PomodoroUser.user_id == user_id)
                user = await session.execute(statement=stmt)
                user = user.scalar()
            if user is None:
                return
            
            await message.answer("🎉 Ты завершил 4 Pomodoro-цикла! Отличная работа!", reply_markup=main_menu_keyboard())

            





train_dict = {
    "Задание 1. «Экзамен через 3 дня»": {"""Представь ситуацию, что ты обнаружил(а), что через 3 дня у тебя важный экзамен, но ты знаешь тему лишь наполовину, либо вообще её не знаешь, что более вероятно. Времени совсем мало, а ещё нужно успеть подготовиться по другим предметам.  3 раза в неделю используй это упражнение и каждый раз меняй стратегии в поисках самой оптимальной для себя.
Ответь на вопросы и запиши их в боте""" : ["1️. Что ты знаешь по этой теме?", "2️. Какие пробелы есть? Как ты это понял?", "3. Какие методы подготовки ты используешь? Какие лучше работают?", "4. Как ты распределишь время на подготовку?", "5️. Оцени свою уверенность по шкале от 1 до 4. Как можно повысить её?"]},
    "Задание 2. «Ты преподаёшь!»": {"""Представь, что тебе нужно объяснить тему, например «Энергия в физике» или любую тему на твоё усмотрение,  другу, который совсем её не понимает. Но есть ограничение: у тебя только 2 минуты!  3 раза в неделю используй это упражнение и каждый раз меняй время и  стратегии в поисках самой оптимальной для себя.
Ответь на вопросы и запиши их в боте""": ["1️. Какие ключевые понятия нужно объяснить?", "2️. Как объяснить максимально просто?", "3️. Какие примеры помогут понять тему?", "4️. Как ты проверишь, что друг понял?", ]},
    "Задание 3. «Что не так с этим текстом?»": {"""Представь, что ты читаешь статью в интернете: «Чем больше кофе ты пьёшь, тем выше IQ» (либо выбери любую другую статью на выбор). Заголовок звучит сомнительно.  3 раза в неделю используй это упражнение и каждый раз меняй стратегии  и статьи (любую информацию в интернете и иных источниках) в поисках самой оптимальной для себя.
Ответь на вопросы и запиши их в боте""": ["1️. Какие доводы приводятся?", "2️. Есть ли у автора доказательства? Где он взял эти данные?", "3️. Как бы ты проверил, правда ли это?", "4️. Что изменится, если мы добавим фразу: «По данным исследования Гарварда или другого авторитетного источника»?"]},
    "Задание 4. «Развитие навыков прогнозирования»": {"""Ситуация: Представь, что преподаватель выдает новый текст (возьми любую статью в интернете, либо параграф в учебнике) для изучения, но перед чтением ты должен предсказать его содержание. 3 раза в неделю используй это упражнение и каждый раз меняй стратегии в поисках самой оптимальной для себя.
Ответь на вопросы и запиши их в боте""": ["1. Посмотри на заголовок и ключевые слова текста.", "2. Спрогнозируй, о чем в нем пойдет речь.", "3. После чтения сравни ожидания с реальным содержанием, напиши что получилось, а что нет."]}
}



@dp.message_handler(commands='s', state=ExerciseStates)
async def s(message: types.Message, state: FSMContext):
    await state.finish()

@dp.message_handler(commands='s', state=Exercise)
async def ss(message: types.Message, state: FSMContext):
    await state.finish()

@dp.message_handler(commands='s', state=ExerciseInfoTraining)
async def ss(message: types.Message, state: FSMContext):
    await state.finish()




@dp.message_handler(commands=['train'])
async def train_start_cmd(message: types.Message, state: FSMContext):

    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton("Задание 1. «Экзамен через 3 дня»"))
    kb.add(types.KeyboardButton("Задание 2. «Ты преподаёшь!»"))
    kb.add(types.KeyboardButton("Задание 3. «Что не так с этим текстом?»"))
    kb.add(types.KeyboardButton("Задание 4. «Развитие навыков прогнозирования»"))


    await message.answer("""Приветствую тебя! Ты на верном пути! Запомни, что  эти универсальные упражнения  развивают несколько метакогнитивных навыков: осознание мышления, самоконтроль, критическое мышление, планирование, саморегуляция, развитие памяти и обучение. Выполняй их 3 раза в неделю на протяжении 3 месяцев и ты почувствуешь, как прокачиваются твои навыки раз за разом. 
Для эффективности используй Pomodoro таймер (кнопка /pomodoro – Pomodoro-таймер)""", reply_markup=kb)
    await Exercise.answers.set()

    async with state.proxy() as data:
        data["questions"] = ["Задание 1. «Экзамен через 3 дня»", \
        "Задание 2. «Ты преподаёшь!»", \
        "Задание 3. «Что не так с этим текстом?»", \
        "Задание 4. «Развитие навыков прогнозирования»"]
        data["active_question"] = None
        data["all_answers"] = []
        data["only_answers"] = []


    

@dp.message_handler(content_types="text", state=Exercise.answers)
async def select_task_command(message: types.Message, state: FSMContext):

    kb = types.ReplyKeyboardMarkup()
    async with state.proxy() as data:
        for i in data["questions"]:
            kb.add(i)
        

        if not message.text in data["questions"] and data["active_question"] is None:
            await message.answer("Выберите одно из заданий по кнопкам ниже", reply_markup=kb)
            return
        
        if message.text in data["questions"] and data["active_question"] is None:
            if message.text == "Задание 1. «Экзамен через 3 дня»":
                data["amount_of_questions"] = 5
                data["n"] = 1


            elif message.text == "Задание 2. «Ты преподаёшь!»":
                data["amount_of_questions"] = 4
                data["n"] = 2

            elif message.text == "Задание 3. «Что не так с этим текстом?»":
                data["amount_of_questions"] = 4
                data["n"] = 3

            else:
                data["amount_of_questions"] = 3
                data["n"] = 4

            data["all_answers"].append(message.text)

            data["count"] = 1

            data["questions"].remove(message.text)
            data["active_question"] = message.text
            data["dct"] = train_dict[message.text]
            
            for i in data["dct"]:
                await message.answer(i)
                data["all_answers"].append(i)
                data["all_answers"].append(data["dct"][i][0])
                await message.answer(data["dct"][i][0])
            
            return
        
        if not message.text in data["questions"] and data["active_question"] is not None:
            
            if len(message.text.split()) < 6:
                await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
                return
            
            if data["count"] == data["amount_of_questions"]:
                
                await message.answer("Ты молодец, отлично отвечаешь на все вопросы. Продолжай в том же духе!", reply_markup=kb)
                data["all_answers"].append(message.text)
                data["active_question"] = None
                data["only_answers"].append(message.text)


                dat = "\n".join(data["all_answers"])

                messages = [
                    {"role": "user", "content": "Привет. Представь, что ты психолог и занимаешься этим уже 40 лет. Пользователь дал разрешение на обработку информации. Сейчас производится метакогнитивный тренинг. Ниже будут вопросы и ответы к нему"},
                    {"role": "user", "content": dat}
                ]




                if len(data["questions"]) == 0:
                    res = await ask_gpt(messages=messages)
                    await message.answer(res, reply_markup=main_menu_keyboard())
                    async with session_factory() as session:
                        stmt = insert(Train).values(user_id=message.from_user.id, answers="RAZDELITEL".join(data["all_answers"]))
                        await session.execute(statement=stmt)
                        await session.commit()
                    await state.finish()
                return

            data["all_answers"].append(message.text)
            data["only_answers"].append(message.text)
            for i in data["dct"]:
                await message.answer(data["dct"][i][data["count"]])
                data["all_answers"].append(data["dct"][i][data["count"]])


            data["count"] += 1
        




info_training_dict = {
    "Задание 1. «Выдели главное»": {"Ситуация: Представь, что тебе нужно подготовить краткий конспект по сложной теме. Однако текст очень длинный и содержит много ненужных деталей. Твоя задача — выделить из него только самое важное, чтобы запомнить быстрее и эффективнее.": ["1. О чём этот текст?", "2. Какие 3 главные идеи ты выделил(а)?", "3. Какие примеры или доказательства использует автор?", "4. Если бы тебе нужно было объяснить этот текст другу в 2-3 предложениях, что бы ты сказал(а)?", "5. Как можно использовать эту информацию в реальной жизни?", ]},
    "Задание 2. «Правда или манипуляция?»": {"""Ситуация: В интернете ежедневно появляется множество новостей. Некоторые из них содержат правдивую информацию, а некоторые могут быть манипуляцией или фейком. Твоя задача — научиться отличать достоверные источники от ложных.  
Используй это упражнение 3 раза в неделю, анализируя разные источники информации.""": ["1️. Кто автор новости? Есть ли у него компетенция?", "2️. Есть ли ссылки на первоисточники? Где их можно проверить?", "3️. Есть ли в тексте эмоции, кликбейт, обобщения?", "4️. Оцените, подтверждают ли другие надёжные источники эту информацию?", ""]},
    "Задание 3. «Составь карту знаний»": {"""Ситуация: Представь, что тебе нужно быстро разобрать длинную научную статью/книгу и выделить главное, ты разрабатываешь исследовательский проект и хочешь четко понять его структуру или ты готовишься к экзамену и тебе нужно запомнить большое количество информации по теме «Экономические теории» (или любая другая сложная тема).
Когда информация представлена в виде структурированной схемы, её легче запомнить. Использование ментальных карт поможет тебе лучше понять связи между понятиями и выделить главное.""": ["1️. Какова главная тема?", "2️. Какие ключевые аспекты можно выделить?", "3️. Как можно визуализировать информацию (графики, схемы, таблицы)?", ]},
    "Задание 4. «Проблема с разных сторон»": {"""Ситуация: В мире существует множество спорных вопросов, которые вызывают разные точки зрения. Рассмотри любой вопрос на выбор. Твоя задача — рассмотреть проблему с двух сторон, привести аргументы «за» и «против», а затем сделать обоснованный вывод. Используй это упражнение 3 раза в неделю, анализируя разные темы.
Ответь на вопросы и запиши их в боте:""": ["1️. Какую тему ты анализируешь? О чем она.", "2️. Какие аргументы можно привести в пользу точки зрения в данной теме?", "3️. Какие аргументы можно привести против этой точки зрения?", "4️. Какой твой окончательный вывод по этой теме?"]},
    "Задание 5. «Выяви скрытые смысловые связи»": {"""Ситуация: Часто в текстах, новостях и исследованиях присутствуют скрытые взаимосвязи между фактами и событиями. Твоя задача — выявить эти связи и объяснить их логическую природу.
Используй это упражнение 3 раза в неделю, анализируя разные типы информации.
Ответь на вопросы и запиши их в боте:""": ["1️. Какую тему ты анализируешь?", "2️. Какие основные факты или аргументы представлены?", "3️. Какие скрытые взаимосвязи можно выявить между этими фактами?", "4️. Как эта информация может повлиять на твои выводы?"]},
    "Задание 6. «Поиск информации по ключевым словам»": {"""Ситуация: Ты пишешь курсовую, дипломную работу или школьный проект, и тебе нужно найти нужные данные быстро и эффективно. Вместо чтения сотен страниц важно уметь выделять ключевые слова и использовать их для поиска.
Используй это упражнение 3 раза в неделю, чтобы развить навык быстрого поиска информации.
Ответь на вопросы и запиши их в боте:""": ["1️. Какая тема твоего исследования? (Сформулируй её кратко и точно)", "2️. Какие 5-7 ключевых слов или фраз можно использовать для поиска?", "3️. Какие источники лучше всего подходят для поиска (Яндекс, Google Scholar, eLibrary, , официальные сайты и др.)?", "4️. Какие из найденных источников кажутся наиболее достоверными и почему?"]},
    "Задание 7. «Быстрое изучение большого объёма информации»": {"""Ситуация: При написании научной или проектной работы важно не просто найти информацию, но и быстро её изучить, выделив ключевые идеи. Твоя задача — научиться структурированному чтению и анализу данных.
Используй это упражнение 3 раза в неделю, работая с разными типами текстов.
Ответь на вопросы и запиши их в боте:""": ["1️. Какой текст или источник ты анализируешь? (Название, автор, дата, ссылка)", "2️. Какую главную мысль передаёт этот текст? (Краткое изложение в 1-2 предложениях)", "3️. Какие 3-5 ключевых идей можно выделить?", "4️. Какую информацию можно использовать в своей работе? (Цитаты, выводы, ссылки)"]},
    "Задание 8. «Проверка достоверности текста нейросети»": {"""Ситуация:
Представь, что ты получил текст от ChatGPT или другой нейросети. На первый взгляд он кажется убедительным, но всегда важно проверять информацию, особенно если ты используешь её для учёбы или работы. Твоя задача — критически проанализировать текст, найти слабые места, логические ошибки, стереотипы, предвзятость и проверить, опирается ли текст на надёжные научные источники.""": ["Какие ключевые аргументы использует текст? (Перечисли основные тезисы, которые продвигает автор)", "Есть ли в тексте логические ошибки или противоречия? Какие именно? (Например, подмена понятий, ложная причинно-следственная связь, необоснованные обобщения)", "Обнаружил(а) ли ты признаки предвзятости или эмоциональной окраски текста? Приведи примеры.", "Есть ли в тексте стереотипные или шаблонные утверждения? Какие из них требуют доказательств?", "Удалось ли найти научные источники, подтверждающие или опровергающие информацию из текста? Какие именно? (Укажи авторов, названия статей или книг, сайты научных публикаций)"]}
}


@dp.message_handler(commands="info_training")
async def info_training_command(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton("Задание 1. «Выдели главное»"))
    kb.add(types.KeyboardButton("Задание 2. «Правда или манипуляция?»"))
    kb.add(types.KeyboardButton("Задание 3. «Составь карту знаний»"))
    kb.add(types.KeyboardButton("Задание 4. «Проблема с разных сторон»"))
    kb.add(types.KeyboardButton("Задание 5. «Выяви скрытые смысловые связи»"))
    kb.add(types.KeyboardButton("Задание 6. «Поиск информации по ключевым словам»"))
    kb.add(types.KeyboardButton("Задание 7. «Быстрое изучение большого объёма информации»"))
    kb.add(types.KeyboardButton("Задание 8. «Проверка достоверности текста нейросети»"))


    await message.answer("""Приветствую тебя! Ты на верном пути! Запомни, что  эти универсальные упражнения  развивают несколько метакогнитивных навыков: осознание мышления, самоконтроль, критическое мышление, планирование, саморегуляция, развитие памяти и обучение. Выполняй их 3 раза в неделю на протяжении 3 месяцев и ты почувствуешь, как прокачиваются твои навыки раз за разом. 
Для эффективности используй Pomodoro таймер (кнопка /pomodoro – Pomodoro-таймер)""", reply_markup=kb)
    await ExerciseInfoTraining.answers.set()

    async with state.proxy() as data:
        data["questions"] = ["Задание 1. «Выдели главное»", \
        "Задание 2. «Правда или манипуляция?»", \
        "Задание 3. «Составь карту знаний»", \
        "Задание 4. «Проблема с разных сторон»", \
        "Задание 5. «Выяви скрытые смысловые связи»", \
        "Задание 6. «Поиск информации по ключевым словам»", \
        "Задание 7. «Быстрое изучение большого объёма информации»", \
        "Задание 8. «Проверка достоверности текста нейросети»"]
        data["active_question"] = None
        data["all_answers"] = []
        data["only_answers"] = []


@dp.message_handler(content_types="text", state=ExerciseInfoTraining.answers)
async def select_task_command_info_training(message: types.Message, state: FSMContext):

    kb = types.ReplyKeyboardMarkup()
    async with state.proxy() as data:
        for i in data["questions"]:
            kb.add(i)
        

        if not message.text in data["questions"] and data["active_question"] is None:
            await message.answer("Выберите одно из заданий по кнопкам ниже", reply_markup=kb)
            return
        
        if message.text in data["questions"] and data["active_question"] is None:
            if message.text ==  "Задание 1. «Выдели главное»":
                data["amount_of_questions"] = 5
                data["n"] = 1

            elif message.text == "Задание 2. «Правда или манипуляция?»":
                data["amount_of_questions"] = 4
                data["n"] = 2

            elif message.text == "Задание 3. «Составь карту знаний»":
                data["amount_of_questions"] = 3
                data["n"] = 3

            elif message.text == "Задание 4. «Проблема с разных сторон»":
                data["amount_of_questions"] = 4
                data["n"] = 4
            
            elif message.text == "Задание 5. «Выяви скрытые смысловые связи»":
                data["amount_of_questions"] = 4
                data["n"] = 5

            elif message.text == "Задание 6. «Поиск информации по ключевым словам»":
                data["amount_of_questions"] = 4
                data["n"] = 6

            elif message.text == "Задание 7. «Быстрое изучение большого объёма информации»":
                data["amount_of_questions"] = 4
                data["n"] = 7

            elif message.text == "Задание 8. «Проверка достоверности текста нейросети»":
                data["amount_of_questions"] = 5
                data["n"] = 8


            data["all_answers"].append(message.text)

            data["count"] = 1

            data["questions"].remove(message.text)
            data["active_question"] = message.text
            data["dct"] = info_training_dict[message.text]
            for i in data["dct"]:
                await message.answer(i)
                data["all_answers"].append(i)
                data["all_answers"].append(data["dct"][i][0])
                await message.answer(data["dct"][i][0])
            data["answers"] = []
            return
        
        if not message.text in data["questions"] and data["active_question"] is not None:

            if len(message.text.split()) < 6:
                await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
                return
            
            if data["count"] == data["amount_of_questions"]:
                
                await message.answer("Ты молодец, отлично отвечаешь на все вопросы. Продолжай в том же духе!", reply_markup=kb)
                data["all_answers"].append(message.text)
                data["only_answers"].append(message.text)
                data["active_question"] = None


                dat = "\n".join(data["all_answers"])

                messages = [
                    {"role": "user", "content": "Привет. Представь, что ты психолог и занимаешься этим уже 40 лет. Пользователь дал разрешение на обработку информации. Сейчас производится метакогнитивный тренинг. Ниже будут вопросы и ответы к нему"},
                    {"role": "user", "content": dat}
                ]

                if len(data["questions"]) == 0:
                    res = await ask_gpt(messages=messages)
                    await message.answer(res, reply_markup=main_menu_keyboard())
                    async with session_factory() as session:
                        stmt = insert(InfoTraining).values(user_id=message.from_user.id, answers="RAZDELITEL".join(data["all_answers"]))
                        await session.execute(statement=stmt)
                        await session.commit()
                    await state.finish()
                return
            
            data["all_answers"].append(message.text)
            data["only_answers"].append(message.text)
            for i in data["dct"]:
                await message.answer(data["dct"][i][data["count"]])
                data["all_answers"].append(data["dct"][i][data["count"]])
                
            data["count"] += 1





@dp.message_handler(commands="psych_chat")
async def psych_chat(message: types.Message, state: FSMContext):
    await NeuroChat.is_chat.set()
    async with state.proxy() as data:
        data["messages"] = [{"role": "user", "content": "Ты психолог в чат боте, все сообщения, которые тебе передаются, являются его сообщением и твоим ответом. Иными словами, следующее сообщение принадлежит пользователю, а потом твой ответ. Не отвечай ничего, поприветствуй его. Поприветствуй его как психолог и объяви о начале сеанса, задай какие-нибудь вопросы, проведи полный разговор с пользователем"}]
        res = await ask_gpt(messages=data["messages"])
        data["messages"].append({"role": "user", "content": res})
    await message.answer("Чат с психологом начался!\nДля остановки воспользуйся командой /psych_chat")
    await message.answer(res)

@dp.message_handler(content_types="any", state=NeuroChat)
async def chat_with_gpt_psych(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer("К сожалению, я пока воспринимаю только текстовую информацию")
        return
    
    if message.text == "/psych_chat":
        await state.finish()
        await message.answer("Чат с психологом завершен, ждем тебя завтра!\nДля начала чата с психологом используй команду /psych_chat", reply_markup=main_menu_keyboard())
        return
    
    async with state.proxy() as data:
        data["messages"].append({"role": "user", "content": message.text})
        res = await ask_gpt(messages=data["messages"])
        await message.answer(res)
        data["messages"].append({"role": "user", "content": res})





reflect_lst = ["1. Какие упражнения тебе дались легче всего? Почему?", \
               "2. Какие задания показались наиболее сложными? Что вызвало затруднения?", \
                "3. Какие стратегии оказались наиболее эффективными при выполнении упражнений?", \
                "4. Какие техники работы с информацией ты будешь использовать в дальнейшем?", \
                "5. Какие ошибки ты совершил(а) при выполнении упражнений? Как их можно избежать в будущем?", \
                "6. Как выполнение упражнений повлияло на твоё мышление и анализ информации?", \
                "7. Как ты можешь применять полученные навыки в учёбе, работе и повседневной жизни?", \
                "8. Какие изменения ты заметил(а) в своём умении планировать, анализировать и критически оценивать информацию?", \
                "9. Какие упражнения тебе хотелось бы повторить или улучшить? Почему?", \
                "10. Как изменилось твоё отношение к информации в интернете после выполнения заданий?"]


@dp.message_handler(commands="reflect")
async def reflect_command(message: types.Message, state: FSMContext):
    await message.answer("""Привет! Ты славно потрудился пройдя занятия, теперь важно закрепить новые навыки с помощью рефлексивных вопросов
Начнем…""")
    
    await Reflect.qiestions.set()

    async with state.proxy() as data:
        data["index"] = 1
        data["answers"] = []

    await message.answer(reflect_lst[0])
    
@dp.message_handler(commands=["s"], state=Reflect)
async def asdkfjsdf(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(content_types="text", state=Reflect)
async def reflect_answers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        if data["index"] == len(reflect_lst):
            print(data["answers"])
            data["answers"].append(message.text)

            async with session_factory() as session:
                stmt = insert(ReflectAnswers).values(user_id=message.from_user.id, answers="RAZDELITEL".join(data["answers"]))
                await session.execute(statement=stmt)
                await session.commit()


            await state.finish()
            await message.answer("""Спасибо за выполнение задания! Надеюсь тебе понравилось. Занимайся регулярно 3 раза в неделю и не забывай рефлексировать. Также используй таймер Pomodoro по кнопке /pomodoro – Pomodoro-таймер. Обязательно пообщайся с психологом /psych_chat – Чат с психологом и не забудь пройти итоговое тестирование после 3 месяцев регулярных занятий по кнопке /retest – Повторное тестирование через 3 месяца. Удачи тебе!""")
            pr_lst = []
            for i in range(len(reflect_lst)):
                pr_lst.append(reflect_lst[i])
                pr_lst.append(data["answers"][i])
            pr_lst = "\n".join(pr_lst)

            messages = [{"role": "user", "content": "Привет. Представь, что ты психолог и занимаешься этим уже 40 лет. Только что была произведена рефлексия, сейчас я тебе все скину. Пользователь дал разрешение на обработку информации."},
                        {"role": "user", "content": pr_lst}]

            res = await ask_gpt(messages=messages)
            await message.answer(res, reply_markup=main_menu_keyboard())


    if len(message.text.split()) < 6:
        await message.answer("Напиши более развернутый ответ, содержащий не менее 6 слов")
        return
    

    async with state.proxy() as data:
        await message.answer(reflect_lst[data["index"]])
        data["index"] += 1
        data["answers"].append(message.text)



@dp.message_handler(commands="profile")
async def profile_command(message: types.Message):
    await profile_logic(message=message, user_id=message.from_user.id)





async def profile_logic(message: types.Message, user_id: int):
    async with session_factory() as session: 
        stmt = select(Train.answers).where(Train.user_id == user_id)
        res = await session.execute(statement=stmt)
        res = res.scalars().all()
        if res is not None:
            res1 = []
            for i in res:
                res1.append("\n".join(i.split("RAZDELITEL")))

        else:
            res1 = ["данных пока нет"]
    


        stmt = select(InfoTraining.answers).where(InfoTraining.user_id == user_id)
        res = await session.execute(statement=stmt)
        res = res.scalars().all()
        if res is not None:
            res_t_1 = []
            for i in res:
                res_t_1.append("\n".join(i.split("RAZDELITEL")))

        else:
            res_t_1 = ["данных пока нет"]



        stmt = select(ReflectAnswers.answers).where(ReflectAnswers.user_id == user_id)
        res = await session.execute(statement=stmt)
        res = res.scalars().all()
        if res is not None:
            ref = []
            for i in res:
                ref.append("\n".join(i.split("RAZDELITEL")))

        else:
            ref = ["данных пока нет"]

        

        messages = [
            {"role": "user", "content": "Привет. Представь, что ты психолог и занимаешься этим уже 40 лет. Ты предназначен для школьников и студентов с целью формирования и развития метакогнитивных навыков, включая осознание собственных мыслительных процессов, рефлексию, самооценку и стратегическое планирование обучения (развитие критического мышления и стратегий обучения, а также тренировки работы с информацией. Сейчас тебе передастся информация из метакогнитивных тренингов, тренингов с информацией и рефлексий, проанализируй пользователя, дай свой профессиональный ответ. Результаты тестов будут оставлены ниже."}
        ]

        for i in res1:
            messages.append({"role": "user", "content": i})

        for i in res_t_1:
            messages.append({"role": "user", "content": i})

        for i in ref:
            messages.append({"role": "user", "content": i})

        ans = await ask_gpt(messages=messages)
        await message.answer(ans, reply_markup=main_menu_keyboard())


@dp.message_handler(commands="retest")
async def retest_command(message: types.Message):
    await retest_logic(message=message, user_id=message.from_user.id)


async def retest_logic(message: types.Message, user_id: int):
    async with session_factory() as session:
        stmt = select(User.datetime).where(User.user_id == user_id)
        r = await session.execute(statement=stmt)
        date = r.scalar()

    date_format = "%Y-%m-%d"
    d1 = datetime.datetime.strptime(date, date_format)
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), date_format)
    
    days = abs((d2 - d1).days)

    if days <= 90:
        await message.answer("Ты пока что не можешь перепройти тестирования, должно пройти три месяца!!!", reply_markup=main_menu_keyboard())
    else:
        await message.answer("""Вот тебе ссылочки на тестирования:
    <a href="https://onlinetestpad.com/s/academic-text-skills">Тест 1</a>
    <a href="https://onlinetestpad.com/t/borzova-text-test">Тест 2</a>
    <a href="https://onlinetestpad.com/t/starkey2004-lutsenko2014">Тест 3</a>
    <a href="https://onlinetestpad.com/t/arpov-reflection-test">Тест 4</a>
    <a href="https://onlinetestpad.com/t/Metacognition-activity">Тест 5</a>
    <a href="https://onlinetestpad.com/t/merkulova-ak-test">Тест 6</a>""", parse_mode="html", reply_markup=main_menu_keyboard())


if __name__ == "__main__":
    executor.start_polling(skip_updates=True, dispatcher=dp)