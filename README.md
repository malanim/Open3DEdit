# Open3DEdit

## Описание проекта
Open3DEdit — это простой 3D-движок, написанный на языке Python, который работает в консоли и отображает 3D-объекты с использованием ASCII-графики. Движок поддерживает интерактивный интерфейс, позволяющий обрабатывать нажатия клавиш в реальном времени.

## Структура проекта
Проект состоит из следующих файлов:
- `main.py`: Главный файл для запуска движка.
- `engine.py`: Основной движок, управляющий рендерингом и логикой игры.
- `vector.py`: Класс для работы с векторами и матрицами.
- `object.py`: Класс для представления 3D-объектов.
- `camera.py`: Класс для управления положением и ориентацией камеры.
- `renderer.py`: Класс для рендеринга объектов на экране.
- `input_handler.py`: Класс для обработки ввода с клавиатуры.
- `scene.py`: Класс для управления сценами и объектами на них.

## Этапы разработки

### Этап 1: Подготовка окружения *(Завершен)*
- ✓ Установлен Python и необходимые инструменты
- ✓ Создана структура папок проекта
- ✓ Настроена система логирования
- ✓ Настроена система тестирования
- ✓ Тесты структуры проекта пройдены

### Этап 2: Реализация классов векторов *(Завершен)*
- ✓ Реализован класс `Vector3` для 3D-векторов
  - Добавлены базовые операции (сложение, вычитание, умножение)
  - Добавлены векторные операции (длина, нормализация, скалярное/векторное произведение)
- ✓ Реализован класс `Matrix4` для матричных преобразований
  - Добавлены матрицы трансформации (перемещение, поворот, масштаб)
  - Добавлено умножение матриц
- ✓ Все тесты векторной математики пройдены

### Этап 3: Реализация классов объектов *(Завершен)*
- ✓ Реализован базовый класс `Object3D`
  - Добавлены трансформации объектов
  - Добавлены свойства материалов
- ✓ Реализованы базовые 3D-примитивы
  - Добавлен класс `Cube`
  - Добавлен класс `Plane`
- ✓ Все тесты объектов пройдены

### Этап 4: Реализация класса камеры *(Завершен)*
- ✓ Реализован класс `Camera`
  - Добавлено управление позицией и ориентацией
  - Добавлены матрицы вида и проекции
  - Добавлены параметры камеры (FOV, near/far planes)
- ✓ Все тесты камеры пройдены

### Этап 5: Реализация класса рендерера *(Завершен)*
- ✓ Реализован базовый класс `Renderer` для рендеринга объектов
- ✓ Реализация системы освещения и затенения
  - ✓ Добавлен класс `Light` и `DirectionalLight`
  - ✓ Добавлены свойства материалов объектов (ambient, diffuse)
  - ✓ Реализовано specular освещение
  - ✓ Оптимизированы алгоритмы затенения
  - ✓ Улучшено тестовое покрытие

### Этап 6: Реализация обработки ввода *(Завершен)*
- ✓ Реализован базовый класс `InputHandler`
  - Добавлена обработка клавиатурного ввода
  - Добавлена система событий
- ✓ Реализовано управление
  - Добавлено управление камерой
  - Добавлено управление объектами
- ✓ Все тесты обработки ввода пройдены

### Этап 7: Главный файл и логика игры *(Текущий этап)*
- ✓ Реализован основной цикл
  - Добавлена структура `main.py`
  - Добавлен цикл обработки событий
- ✓ Управление состоянием игры
  - Добавлены состояния: initializing, running, paused, stopped
  - Реализованы переходы между состояниями
  - Добавлена обработка ошибок состояний
- ✓ Синхронизация компонентов
  - Добавлена проверка готовности компонентов
  - Реализована защита от несинхронизированных операций
- ✓ Улучшена обработка ошибок
  - Добавлена детальная обработка исключений
  - Реализовано безопасное завершение работы
- ✓ Расширено тестовое покрытие

### Этап 8: Тестирование и отладка *(В процессе)*
- ✓ Реализована система тестирования
  - Настроен фреймворк для тестов
  - Добавлены базовые тесты компонентов
  - Добавлены интеграционные тесты
    - Тесты переходов состояний движка
    - Тесты синхронизации компонентов
  - Добавлены стресс-тесты
    - Тесты стабильности частоты кадров
    - Тесты производительности рендеринга
- ⚡ В процессе:
  - Профилирование и оптимизация
  - Расширение покрытия тестами
- ✓ Документирование тестов

### Этап 9: Документация *(Текущий этап)*
- ⚡ Начата работа над документацией
  - Создан базовый README
  - Добавлены описания классов
- ⚠️ Требуется реализация:
  - Полная документация API
  - Примеры использования
  - Руководство пользователя
- ⚠️ Требуется перевод документации

## Дополнительные функции (по мере необходимости)
- Реализация текстурирования и материалов.
- Поддержка анимации объектов.
- Создание простого интерфейса для настройки параметров рендеринга.
- Оптимизация производительности для рендеринга больших сцен.

## Установка
1. Убедитесь, что у вас установлен Python версии 3.x.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/My3DEngine.git
   ```
3. Перейдите в каталог репозитория:
   ```bash
   cd My3DEngine
   ```

## Запуск
Для запуска движка выполните команду:
   ```bash
   python main.py
   ```

## Контрибьюция
Если вы хотите внести свой вклад в проект, пожалуйста, создайте pull request или откройте issue для обсуждения изменений.

## Лицензия
Этот проект лицензирован под MIT License. Пожалуйста, ознакомьтесь с файлом LICENSE для получения дополнительной информации.