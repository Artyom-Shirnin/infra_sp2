import csv
import os

import django.db.utils
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review, Category, Genre, Title
from users.models import User

DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def read_csv(name_file):
    """Считывает данные из csv и возвращает список строк таблицы"""
    path = os.path.join('static/data', name_file)
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        return list(reader)


def get_list_fields_model(model):
    """
    Принимает объект модели, и возвращает словарь с полями в виде:
    {<поле модели>: <поле в таблице>}
    """
    fields_obj_list = model._meta.fields
    fields = {
        field.name: field.attname for field in fields_obj_list
    }
    return fields


def changes_fields(fields_model, table):
    """
    Изменяет название полей прочитанной таблицы
    для корректной записи в БД
    """
    for row in table:
        for name_field in list(row):
            if (
                    name_field in fields_model
                    and name_field
                    != fields_model[name_field.replace("_id", "")]
            ):
                row[fields_model[name_field]] = row.pop(name_field)


def load_data(model, name_file):
    """
    Загрузка данных по имени модели.
    Не загружает данные во вспомогательную таблицу
    со связью многие ко многим
    """
    table = read_csv(name_file)
    changes_fields(get_list_fields_model(model), table)
    model.objects.bulk_create(model(**row) for row in table)


def load_genre_title():
    """
    Загружает данные во вспомогательную таблицу
    для моделей со связью многие ко многим
    """
    data_list = read_csv('genre_title.csv')
    [
        Title.objects.get(id=row['title_id']).genre.add(row['genre_id'])
        for row in data_list
    ]


def del_data():
    """Удаляет все таблицы из базы данных"""
    for model in DATA:
        model.objects.all().delete()


class Command(BaseCommand):
    help = 'Импортирует таблицы из csv в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Импортирует все таблицы из csv в базу данных'
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            help='Удаляет все данные из базы данных'
        )

    def handle(self, *args, **options):
        try:
            if options['all']:
                for model, name_file in DATA.items():
                    load_data(model, name_file)
                load_genre_title()
                self.stdout.write(
                    self.style.SUCCESS('Таблицы загружены в базу данных.'))
            elif options['clear']:
                del_data()
                self.stdout.write(
                    self.style.SUCCESS('База данных успешно очищена.'))
            else:
                self.stdout.write(
                    self.style.SQL_KEYWORD('Команда используется с ключом,'
                                           ' список всех ключей: --help'))
        except django.db.utils.IntegrityError as e:
            self.stdout.write(
                self.style.ERROR('Ошибка загрузки. База данных не пуста. '
                                 'Совпадение уникальных полей. "%s"' % e))
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.NOTICE('Нет данных из связанных таблиц'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Ошибка загрузки данных:'
                                               ' "%s"' % e))
