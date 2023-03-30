# Парсинг статусов PEP документов
## Описание
---
Программа собирает данные с главной страницы документации PEP, берет статус документа из общей таблицы и сравнивает со страничным статусом документа.

---
## Установка и запуск
- Скачайте репозиторий через терминал
  - ```git clone https://github.com/Semyonov-K/bs4_parser_pep.git```
- Установите виртуальное окружение
  - ```python -m venv venv```
- Запустите виртуальное окружение
  - ```. venv/scripts/activate```
- Установите необходимые зависимости
  - ```pip install -r requirements.txt```
- Для старта парсинга, находясь в директории с проектом введите
  - ```python main.py pep```
- Для подробной информации введите
  - ```python main.py -h```
  - ```python main.py --help```
- Результаты будут сохранены в папке ***results***, в формате *csv* файла.

---
## Автор: Semyonov-K
