"""Обучающая машина Тьюринга - Педагогический редизайн v4.

ПОРЯДОК (снизу вверх, отложенное введение состояний):
1. Магический трюк - Хук
2. Лента - Как выглядят данные
3. Головка - Как читает/пишет/двигается
4. Простые правила - Правила которые работают (переворот бита)
5. Загадка замка - ТЕПЕРЬ вводим состояния через метафору замка
6. Состояния решают всё - Решение
7. Финал
"""

# 7 Модулей: Открытие снизу вверх с отложенным введением состояний
LESSONS = [
    # ============================================================
    # МОДУЛЬ 1: МАГИЧЕСКИЙ ТРЮК (Демо СНАЧАЛА - смотрим до теории)
    # ============================================================
    {
        "id": "magic-trick",
        "title": "Магический трюк",
        "practice_type": "magic-demo",
        "content": """
            <div class="hook-intro">
                <p class="hook-line">Смотри.</p>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 2: ЛЕНТА (Хранение данных - теперь раньше)
    # ============================================================
    {
        "id": "tape",
        "title": "Лента",
        "practice_type": "explore-tape",
        "content": """
            <div class="concept-intro">
                <p class="lead">Теперь посмотрим на машину, которую ты только что видел.</p>
                <p>У неё есть <strong>лента</strong> &mdash; ряд ячеек, которые хранят символы.</p>
            </div>

            <div class="tape-visual-demo horizontal">
                <div class="tape-cell blank">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell blank">_</div>
            </div>

            <div class="insight-box">
                <p>Каждая ячейка хранит ровно <strong>ОДИН символ</strong>:</p>
                <ul>
                    <li><strong>0</strong> или <strong>1</strong> &mdash; двоичные цифры</li>
                    <li><strong>_</strong> &mdash; пустая ячейка</li>
                </ul>
            </div>

            <div class="wow-connection">
                <p>Та фотка в твоём телефоне? <strong>10 миллионов ячеек</strong> как эта.</p>
                <p>В каждой только 0 или 1. Компьютер не "видит" фото &mdash; он просто читает символы.</p>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 3: ГОЛОВКА (Управление - одна ячейка за раз)
    # ============================================================
    {
        "id": "head",
        "title": "Головка",
        "practice_type": "control-head",
        "content": """
            <div class="concept-intro">
                <p class="lead">У машины есть <strong>головка</strong> &mdash; как палец, указывающий на одну ячейку.</p>
            </div>

            <div class="tape-visual-demo horizontal with-head">
                <div class="tape-cell blank">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell head">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell blank">_</div>
            </div>
            <div class="head-pointer">ГОЛОВКА</div>

            <div class="constraint-box">
                <p class="constraint-title">Фишка:</p>
                <p>Головка видит только <strong>ОДНУ ячейку</strong> за раз.</p>
                <p class="analogy"><em>Как читать книгу через замочную скважину &mdash; по одной букве.</em></p>
            </div>

            <div class="actions-box">
                <p>Головка умеет делать ровно <strong>3 вещи</strong>:</p>
                <div class="action-list">
                    <div class="action-item">
                        <span class="action-icon">👁️</span>
                        <span class="action-text"><strong>ЧИТАТЬ</strong> символ</span>
                    </div>
                    <div class="action-item">
                        <span class="action-icon">✏️</span>
                        <span class="action-text"><strong>ПИСАТЬ</strong> новый символ</span>
                    </div>
                    <div class="action-item">
                        <span class="action-icon">👆</span>
                        <span class="action-text"><strong>ДВИГАТЬСЯ</strong> влево или вправо</span>
                    </div>
                </div>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 4: ПРОСТЫЕ ПРАВИЛА (Правила которые работают БЕЗ состояний)
    # ============================================================
    {
        "id": "simple-rules",
        "title": "Простые правила",
        "practice_type": "simple-rules",
        "content": """
            <div class="concept-intro">
                <p class="lead">Машина следует <strong>правилам</strong>.</p>
                <p>Начнём просто: <strong>перевернём каждый бит</strong>.</p>
            </div>

            <div class="rules-display simple">
                <div class="rule">Вижу <strong>0</strong> → пишу <strong>1</strong>, иду вправо</div>
                <div class="rule">Вижу <strong>1</strong> → пишу <strong>0</strong>, иду вправо</div>
                <div class="rule">Вижу <strong>_</strong> → стоп</div>
            </div>

            <div class="insight-box">
                <p>Вот и всё. <strong>"Когда вижу X, делаю Y."</strong></p>
                <p>Любая программа &mdash; от Instagram до Excel &mdash; это просто такие правила. Много правил.</p>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 5: ЗАГАДКА ЗАМКА (ТЕПЕРЬ вводим состояния)
    # ============================================================
    {
        "id": "lock-puzzle",
        "title": "Загадка замка",
        "practice_type": "lock-puzzle",
        "content": """
            <div class="puzzle-intro">
                <p class="lead">Вот замок с кодом <strong>1-2-3-4</strong>.</p>
                <p>Попробуй открыть его.</p>
            </div>

            <div class="puzzle-question">
                <p>Подумай: если бы замок работал по <strong>простым правилам</strong>...</p>
                <p class="dim">"Когда вижу 1 → проверить. Когда вижу 2 → проверить..."</p>
                <p>...он бы открылся когда ты нажмёшь <strong>любую</strong> правильную цифру!</p>
            </div>

            <div class="puzzle-insight">
                <p>Но замки так не работают.</p>
                <p>Замок должен <strong>помнить</strong> какую цифру он ждёт.</p>
                <p class="dim">Сначала он ждёт 1. Потом 2. Потом 3. Потом 4.</p>
            </div>

            <div class="puzzle-reveal">
                <p>Эта память &mdash; знание <em>чего ожидать дальше</em> &mdash; называется <strong>СОСТОЯНИЕ</strong>.</p>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 6: СОСТОЯНИЯ РЕШАЮТ ВСЁ
    # ============================================================
    {
        "id": "states",
        "title": "Состояния решают всё",
        "practice_type": "states-solve",
        "content": """
            <div class="solution-intro">
                <p class="lead">Помнишь замок?</p>
                <p>Он помнил какую цифру ожидать следующей. Эта память называется <strong>СОСТОЯНИЕ</strong>.</p>
            </div>

            <div class="lock-timeline">
                <div class="lock-timeline-title">Замок проходит через состояния:</div>
                <div class="lock-timeline-flow">
                    <div class="lock-step">
                        <div class="lock-step-label">ЖДУ_1</div>
                        <div class="lock-step-meaning">жду<br>1-ю цифру</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">ЖДУ_2</div>
                        <div class="lock-step-meaning">жду<br>2-ю цифру</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">ЖДУ_3</div>
                        <div class="lock-step-meaning">жду<br>3-ю цифру</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">ЖДУ_4</div>
                        <div class="lock-step-meaning">жду<br>4-ю цифру</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step open">
                        <div class="lock-step-label">ОТКРЫТ</div>
                        <div class="lock-step-meaning">разблокирован!</div>
                    </div>
                </div>
            </div>

            <div class="key-insight">
                <div class="key-insight-header">КЛЮЧЕВАЯ МЫСЛЬ</div>
                <div class="key-insight-content">
                    <p>Одно и то же нажатие &rarr; <strong>разный результат</strong></p>
                    <p class="dim">в зависимости от состояния замка</p>
                </div>
            </div>

            <div class="transition-box">
                <p>Нашей машине Тьюринга нужно то же самое!</p>
                <p class="dim">Разные состояния = разное поведение для одного символа</p>
            </div>

            <div class="tm-states-showcase">
                <div class="tm-state-card cyan">
                    <div class="tm-state-icon">🔍</div>
                    <div class="tm-state-name">СКАН</div>
                    <div class="tm-state-desc">Ищу конец числа</div>
                </div>
                <div class="tm-states-arrow"></div>
                <div class="tm-state-card orange">
                    <div class="tm-state-icon">➕</div>
                    <div class="tm-state-name">СЛОЖЕНИЕ</div>
                    <div class="tm-state-desc">Прибавляю 1</div>
                </div>
                <div class="tm-states-arrow"></div>
                <div class="tm-state-card green">
                    <div class="tm-state-icon">✅</div>
                    <div class="tm-state-name">ГОТОВО</div>
                    <div class="tm-state-desc">Закончил!</div>
                </div>
            </div>

            <div class="conclusion-box">
                <p>Теперь машина знает что делать:</p>
                <p class="highlight">В <strong>СКАН</strong> + вижу <strong>1</strong> &rarr; иду вправо</p>
                <p class="highlight">В <strong>СЛОЖЕНИЕ</strong> + вижу <strong>1</strong> &rarr; пишу 0, несу влево</p>
                <p class="dim">Один символ, разные состояния = разные действия!</p>
            </div>
        """
    },

    # ============================================================
    # МОДУЛЬ 7: ТЫ ТЕПЕРЬ ПОНИМАЕШЬ КОМПЬЮТЕРЫ
    # ============================================================
    {
        "id": "finale",
        "title": "Ты теперь понимаешь компьютеры",
        "practice_type": "finale",
        "content": """
            <div class="finale-intro">
                <h2>Полная картина</h2>
            </div>

            <div class="recap-box">
                <div class="recap-item">
                    <span class="num">1</span>
                    <strong>Лента</strong> = память (нули и единицы)
                </div>
                <div class="recap-item">
                    <span class="num">2</span>
                    <strong>Головка</strong> = процессор (читать, писать, двигаться)
                </div>
                <div class="recap-item">
                    <span class="num">3</span>
                    <strong>Состояния</strong> = о чём "думает" процессор
                </div>
                <div class="recap-item">
                    <span class="num">4</span>
                    <strong>Правила</strong> = программа
                </div>
            </div>

            <div class="wow-box">
                <p>Та игра в телефоне? Это просто правила.</p>
                <p>Очень сложные правила, но правила.</p>
                <p>Процессор читает данные, проверяет в каком режиме находится, и следует правилам.</p>
            </div>

            <div class="final-revelation">
                <p><strong>ЕДИНСТВЕННАЯ</strong> разница между этой машиной Тьюринга и твоим iPhone?</p>
                <p class="revelation-answer"><strong>СКОРОСТЬ.</strong></p>
                <p>Твой телефон делает это <strong>3,000,000,000</strong> раз в секунду.</p>
            </div>
        """
    }
]

# Основной пример с обучающим контентом
EXAMPLES = {
    "binary_increment": {
        "name": "Прибавить 1 к двоичному числу",
        "description": "Взять двоичное число и прибавить к нему 1",
        "goal": "Прибавить 1 к двоичному числу",
        "initial_state": "scan",
        "accept_states": ["done"],
        "reject_states": [],
        "blank_symbol": "_",
        "default_input": "1011",

        "states": {
            "scan": {
                "label": "СКАН",
                "emoji": "🔍",
                "description": "Ищу конец числа"
            },
            "add": {
                "label": "СЛОЖЕНИЕ",
                "emoji": "➕",
                "description": "Прибавляю 1 и обрабатываю перенос"
            },
            "done": {
                "label": "ГОТОВО",
                "emoji": "✅",
                "description": "Закончил!"
            }
        },

        "next_action_explanations": {
            "scan,0": {
                "action": "Оставляю 0, иду ВПРАВО, остаюсь в СКАН",
                "why": "Всё ещё ищу конец числа."
            },
            "scan,1": {
                "action": "Оставляю 1, иду ВПРАВО, остаюсь в СКАН",
                "why": "Всё ещё ищу конец числа."
            },
            "scan,_": {
                "action": "Остаюсь здесь, иду ВЛЕВО, переключаюсь на СЛОЖЕНИЕ",
                "why": "Нашёл конец! Пора возвращаться и начинать сложение."
            },
            "add,0": {
                "action": "Пишу 1, СТОП, переключаюсь на ГОТОВО",
                "why": "0 + 1 = 1. Перенос не нужен. Готово!"
            },
            "add,1": {
                "action": "Пишу 0, иду ВЛЕВО, остаюсь в СЛОЖЕНИЕ",
                "why": "1 + 1 = 2 = '10' в двоичной. Пишу 0, переношу 1 влево."
            },
            "add,_": {
                "action": "Пишу 1, СТОП, переключаюсь на ГОТОВО",
                "why": "Цифр больше нет, но остался перенос. Пишу 1 сюда."
            }
        },

        "rules": [
            {"state": "scan", "see": "0", "write": "0", "move": "right", "goto": "scan"},
            {"state": "scan", "see": "1", "write": "1", "move": "right", "goto": "scan"},
            {"state": "scan", "see": "_", "write": "_", "move": "left", "goto": "add"},
            {"state": "add", "see": "0", "write": "1", "move": "stay", "goto": "done"},
            {"state": "add", "see": "1", "write": "0", "move": "left", "goto": "add"},
            {"state": "add", "see": "_", "write": "1", "move": "stay", "goto": "done"}
        ],

        "transitions": {
            "scan,0": ["scan", "0", "R"],
            "scan,1": ["scan", "1", "R"],
            "scan,_": ["add", "_", "L"],
            "add,0": ["done", "1", "N"],
            "add,1": ["add", "0", "L"],
            "add,_": ["done", "1", "N"]
        }
    },

    "bit_flip": {
        "name": "Перевернуть все биты",
        "description": "Превратить каждый 0 в 1 и каждую 1 в 0",
        "goal": "Инвертировать все биты",
        "initial_state": "flip",
        "accept_states": ["done"],
        "reject_states": [],
        "blank_symbol": "_",
        "default_input": "1010",

        "states": {
            "flip": {
                "label": "ПЕРЕВОРОТ",
                "emoji": "🔄",
                "description": "Переворачиваю биты по одному"
            },
            "done": {
                "label": "ГОТОВО",
                "emoji": "✅",
                "description": "Закончил!"
            }
        },

        "rules": [
            {"state": "flip", "see": "0", "write": "1", "move": "right", "goto": "flip"},
            {"state": "flip", "see": "1", "write": "0", "move": "right", "goto": "flip"},
            {"state": "flip", "see": "_", "write": "_", "move": "stay", "goto": "done"}
        ],

        "transitions": {
            "flip,0": ["flip", "1", "R"],
            "flip,1": ["flip", "0", "R"],
            "flip,_": ["done", "_", "N"]
        }
    }
}


def get_lessons():
    """Get all lessons for onboarding."""
    return LESSONS


def get_example_list():
    """Get list of available examples."""
    return [
        {
            "id": key,
            "name": example["name"],
            "description": example["description"],
            "default_input": example["default_input"]
        }
        for key, example in EXAMPLES.items()
    ]


def get_example(example_id: str):
    """Get a specific example by ID."""
    return EXAMPLES.get(example_id)
