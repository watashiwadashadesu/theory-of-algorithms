-- Схема базы данных для PRF Constructor

-- Таблица для хранения определений функций
CREATE TABLE IF NOT EXISTS functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    definition TEXT NOT NULL,  -- JSON строка
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Таблица для истории вычислений
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    function_id INTEGER,
    arguments TEXT NOT NULL,  -- JSON массив аргументов
    result TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(function_id) REFERENCES functions(id) ON DELETE CASCADE
);

-- Таблица для базовых примитивов (справочная)
CREATE TABLE IF NOT EXISTS primitives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,  -- 'zero', 'succ', 'proj'
    arity INTEGER,  -- для проекции
    proj_index INTEGER,  -- для проекции (index - зарезервированное слово)
    name TEXT
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_functions_name ON functions(name);
CREATE INDEX IF NOT EXISTS idx_history_function_id ON history(function_id);
CREATE INDEX IF NOT EXISTS idx_history_timestamp ON history(timestamp);

