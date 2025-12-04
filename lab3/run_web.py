#!/usr/bin/env python3
"""
Скрипт для запуска веб-приложения книжного клуба.
"""
import uvicorn
import argparse


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Веб-приложение книжного клуба")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Хост для запуска сервера (по умолчанию: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Порт для запуска сервера (по умолчанию: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Включить автоматическую перезагрузку при изменении кода"
    )
    return parser.parse_args()


def main():
    """Основная функция запуска веб-приложения."""
    args = parse_args()

    print("🚀 Запуск веб-приложения книжного клуба...")
    print(f"📡 Адрес: http://{args.host}:{args.port}")
    print(f"📊 API: http://{args.host}:{args.port}/docs")
    print("Нажмите Ctrl+C для остановки")

    uvicorn.run(
        "web_app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()