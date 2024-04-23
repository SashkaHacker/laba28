#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from datetime import datetime
from pathlib import Path

from validation import ListWorkers


def add_worker(lst: list, surname: str, name: str, phone: str, date: str):
    dct = {
        "surname": surname,
        "name": name,
        "phone": phone,
        "date": date.split(":"),
    }
    lst.append(dct)


def phone(lst: list, numbers_phone: int):
    numbers_phone = int(numbers_phone)
    fl = True
    for i in lst:
        if i["phone"] == numbers_phone:
            print(
                f"Фамилия: {i['surname']}\n"
                f"Имя: {i['name']}\n"
                f"Номер телефона: {i['phone']}\n"
                f"Дата рождения: {':'.join(i['date'])}"
            )
            fl = False
            break
    if fl:
        print("Человека с таким номером телефона нет в списке.")


def instruction():
    print(
        "add - добавление нового работника\n"
        "phone - данные о работнике по его номеру телефона\n"
        "exit - завершение программ\n"
        "list - список работников\n"
        "save filename - сохранить данные в json файл\n"
    )


def save_workers(file_name: str, staff: list):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name: str):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)
    try:
        ListWorkers(lst=data)
        data.sort(
            key=lambda x: datetime.strptime("-".join(x["date"]), "%d-%m-%Y")
        )
        return data
    except Exception:
        print("Invalid JSON")


def show_workers(lst: list):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if lst:
        # Блок заголовка таблицы
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 15, "-" * 15
        )
        print(line)
        print(
            f'| {"№":^4} | {"Фамилия":^30} | {"Имя":^20} | '
            f'{"Номер телефона":^15} | {"Дата рождения":^15} |'
        )

        print(line)
        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(lst, 1):
            print(
                f'| {idx:>4} | {worker.get("surname", ""):<30} | '
                f'{worker.get("name", ""):<20}'
                f' | {worker.get("phone", 0):>15}'
                f' | {":".join(worker.get("date", 0)):>15} |'
            )

        print(line)
    else:
        print("Список работников пуст.")


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser(description="workers")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new worker"
    )
    add.add_argument(
        "-n", "--name", action="store", required=True, help="Имя работника"
    )
    add.add_argument(
        "-s", "--surname", action="store", help="Фамилия работника"
    )
    add.add_argument(
        "-p",
        "--phone",
        action="store",
        required=True,
        help="Номер телефона работника",
    )
    add.add_argument(
        "-d",
        "--date",
        action="store",
        required=True,
        help="Дата в формате: (число:месяц:год)",
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all workers"
    )

    # Добавление субпарсера для выбора работника по номеру телефона.
    select_phone = subparsers.add_parser(
        "select", parents=[file_parser], help="Select worker by phone"
    )
    select_phone.add_argument("-p", "--phone", action="store", required=True)

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False

    # Добавление домашней директории к пути.
    path_to_home = Path.home() / args.filename
    if path_to_home.exists():
        lst = load_workers(path_to_home)
    else:
        lst = []

    # Добавить работника.
    match args.command:
        case "add":
            add_worker(lst, args.surname, args.name, args.phone, args.date)
            is_dirty = True
        case "display":
            show_workers(lst)
        case "select":
            phone(lst, args.phone)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_workers(path_to_home, lst)


if __name__ == "__main__":
    main()
