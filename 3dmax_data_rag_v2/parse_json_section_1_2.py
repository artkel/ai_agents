import re
import json
from docx import Document
import os


def extract_media_references(text):
    """Extract media references (image files) from text"""
    # Pattern matches references like image1.gif, image15.png, etc.
    media_refs = []
    for match in re.finditer(r'image\d+\.(gif|png|jpg|jpeg)', text):
        media_refs.append(match.group(0))

    return list(set(media_refs))  # Remove duplicates


def clean_text(text):
    """Clean text while preserving formatting as HTML"""
    # Convert strong formatting
    text = re.sub(r'\[\*\*([^*]+)\*\*\]', r'<strong>\1</strong>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[([^\]]+)\]', r'<strong>\1</strong>', text)

    # Remove {.mark} tags
    text = re.sub(r'\{\.mark\}', '', text)

    return text.strip()


def process_document():
    """Process the document and extract content manually (no automatic parsing)"""
    # Manually define the structure based on your document
    result = {
        "sections": [
            {
                "id": 1,
                "title": "Основное руководство (единый алгоритм решения большинства задач)",
                "content": [
                    {
                        "id": "1.1",
                        "title": "Запуск и настройка интерфейса",
                        "content": "• Запустите программу, затем выберите [Customize (Настроить)]{.mark} → [Customize User Interface (Настроить пользовательский интерфейс)]{.mark} для проверки или восстановления стандартных настроек.\n\n• При необходимости смените рабочее пространство через [Workspace (Рабочее пространство)]{.mark} → [Reset To Default State (Сбросить рабочее пространство)]{.mark}.",
                        "media": ["image1.gif", "image2.gif"]
                    },
                    {
                        "id": "1.2",
                        "title": "Моделирование",
                        "content": "• Для создания объектов перейдите в [Create (Создать)]{.mark} → [Geometry (Геометрия)]{.mark} и выберите нужный примитив (например, [Box (Коробка)]{.mark} или [Sphere (Сфера)]{.mark}).\n\n• После создания преобразуйте примитив в Editable Poly через правый клик и выбор соответствующей опции или через [Convert To (Преобразовать в)]{.mark}.",
                        "media": ["image3.gif", "image4.gif"]
                    },
                    {
                        "id": "1.3",
                        "title": "Анимация",
                        "content": "• Выделите объект, затем откройте [Animation (Анимация)]{.mark} и нажмите [Set Key (Установить ключ)]{.mark} для записи ключевого кадра.\n\n• Для тонкой настройки откройте [Track View - Curve Editor (Редактор кривых)]{.mark} и отрегулируйте интерполяцию.",
                        "media": ["image5.gif", "image6.gif"]
                    },
                    {
                        "id": "1.4",
                        "title": "Материалы и текстуры",
                        "content": "• Запустите [Material Editor (Редактор материалов)]{.mark} через [Rendering (Рендер)]{.mark} → [Material Editor (Редактор материалов)]{.mark}, создайте или выберите материал, назначьте текстуру через слот [Diffuse (Диффузия)]{.mark} и перетащите его на объект.",
                        "media": ["image7.gif"]
                    },
                    {
                        "id": "1.5",
                        "title": "Освещение и рендеринг",
                        "content": "• Добавьте источники света через [Create (Создать)]{.mark} → [Lights (Свет)]{.mark} и настройте их в панели [Modify (Модифицировать)]{.mark}.\n\n• Настройте параметры рендера в [Rendering (Рендер)]{.mark} → [Render Setup (Настройка рендера)]{.mark}, выберите рендерер (например, [V-Ray]{.mark} или [Arnold]{.mark}) и нажмите [Render (Рендер)]{.mark}.",
                        "media": ["image8.gif", "image9.gif"]
                    },
                    {
                        "id": "1.6",
                        "title": "Скриптинг и автоматизация",
                        "content": "• Откройте [Scripting (Скриптинг)]{.mark} → [MaxScript Listener (Прослушиватель MaxScript)]{.mark} для тестирования скриптов или запустите [Macro Recorder (Запись макроса)]{.mark} для автоматизации повторяющихся действий.\n\nЕсли основной алгоритм не решил вашу задачу, обратитесь к дополнительным инструкциям ниже.",
                        "media": ["image10.gif"]
                    }
                ]
            },
            {
                "id": 2,
                "title": "Вспомогательные решения",
                "content": [
                    {
                        "id": "2.1",
                        "title": "Оптимизация производительности",
                        "content": "-- Примените модификатор [ProOptimizer (Оптимизатор)]{.mark} через [Modify (Модифицировать)]{.mark} для уменьшения количества полигонов.\n\n-- Включите режим [Wireframe Override (Каркас)]{.mark} в окне просмотра через настройки [Viewport (Просмотр)]{.mark}.",
                        "media": ["image11.gif", "image12.gif"]
                    },
                    {
                        "id": "2.2",
                        "title": "Работа с плагинами и расширениями",
                        "content": "-- Устанавливайте плагины через [Customize (Настроить)]{.mark} → [Customize User Interface (Настроить пользовательский интерфейс)]{.mark} и обновляйте их с официальных сайтов (например, V-Ray for 3Ds Max).",
                        "media": ["image13.gif", "image14.png"],
                        "subcontent": [
                            {
                                "id": "2.2.1",
                                "title": "Mouse (Мышь)",
                                "content": "Это меню настройки пользовательского интерфейса, где можно изменять управление навигацией и назначать горячие клавиши.\n\nОсновные элементы интерфейса:\n\nСписок действий и их горячие клавиши:\n\n• Arc Rotate -- Alt + MMB (вращение камеры)\n\n• Pan View -- MMB (перемещение камеры)\n\n• Zoom -- Ctrl + Alt + MMB (приближение/отдаление)\n\nMouse Control (Управление мышью):\n\n• AutoFocus Viewport -- автоматическая фокусировка вида\n\n• Zoom About Mouse Point (Orthographic/Perspective) -- зум относительно точки под курсором\n\n• Wheel Zoom Increment: -- настройка чувствительности колесика мыши\n\n• Поля для назначения новых горячих клавиш (Shortcut, Assigned to)\n\n• Кнопки Load, Save, Reset -- загрузка, сохранение и сброс настроек.",
                                "media": []
                            },
                            {
                                "id": "2.2.2",
                                "title": "Toolbars",
                                "content": "В этом меню можно создавать панели с кнопками и инструментами. Сначала нужно создать панель кнопкой New и ввести ее название. В созданную панель перетащите все нужные инструменты из окна с разделом Action. Теперь эту панель можно поместить на одной из сторон рабочей области обычным перетаскиванием. Кнопкой Delete можно удалить панель, выбранную в строке над кнопкой.\n\nОсновные элементы интерфейса:\n\n• Group: Main UI (Группа: Основной интерфейс)\n\n• Category: All Commands (Категория: Все команды)\n\n• Список доступных команд, которые можно назначить в контекстное меню (Quads). Среди них:\n\n• 2D Pan Zoom Mode -- режим 2D-панорамирования и зума\n\n• 3ds Max Developer Help -- справка для разработчиков\n\n• Activate Grid (Context) -- активация сетки в контексте\n\n• Active Viewport 1-4 -- активация конкретного вьюпорта\n\n• ActiveShade Mode -- режим ActiveShade (интерактивный рендер)\n\n• Панель управления слоями анимации (Animation Layers):\n\n• New... -- создание нового слоя\n\n• Delete... -- удаление слоя\n\n• Rename... -- переименование слоя\n\n• Hide -- скрытие слоя\n\n• Кнопки управления настройками интерфейса:\n\n• Load... -- загрузка конфигурации\n\n• Save... -- сохранение текущих настроек\n\n• Reset -- сброс до стандартных параметров.",
                                "media": []
                            },
                            {
                                "id": "2.2.3",
                                "title": "Quads",
                                "content": "Настройки меню, которое вызывает щелчком ПКМ в рабочей области. Здесь создается подобное меню, а не заменяется привычное. Чтобы не было проблем, в меню Quad Shortcut введите другие горячие клавиши. Создание панели происходит таким же образом, как и для меню Toolbars.\n\nОсновные элементы интерфейса:\n\n• Group: Main UI (Основной интерфейс)\n\n• Category: All Commands (Все команды)\n\n• Список доступных действий, которые можно добавить в контекстное меню.\n\n• Настройка Quad Menu (Контекстного меню):\n\n• Default Viewport Quad -- настройка стандартного квад-меню для вьюпорта\n\n• Quad Hotkey: можно назначить горячую клавишу для вызова меню\n\n• Show All Quads -- отображение всех секций квад-меню\n\n• Label: \"transform\" -- название текущей секции меню\n\n• Доступные команды в этом меню:\n\n• Move (Перемещение)\n\n• Rotate (Вращение)\n\n• Scale (Масштабирование)\n\n• Placement (Размещение)\n\n• Select Object (Выбор объекта)\n\n• Select Similar (Выбор похожих объектов)\n\n• Pivot настройки (Place, Align, Reset, Snap)\n\n• Clone (Клонирование)\n\n• Properties (Свойства)\n\n• Кнопки управления настройками:\n\n• New... -- создание нового квад-меню\n\n• Delete... -- удаление существующего\n\n• Assign -- назначение команды\n\n• Advanced Options... -- дополнительные параметры\n\n• Load..., Save..., Reset -- загрузка, сохранение и сброс настроек.",
                                "media": []
                            },
                            {
                                "id": "2.2.4",
                                "title": "Menu",
                                "content": "Menus -- это разворачиваемые свитки, в которых находятся кнопки инструментов или аналогичные подменю. Создается и настраивается меню аналогично предыдущим пунктам (Quads, Toolbars).\n\nОсновные элементы интерфейса:\n\n• Group: Main UI (Основной интерфейс)\n\n• Category: All Commands (Категория: Все команды)\n\n• Список доступных действий для добавления в меню (слева)\n\n• Main Menu Bar (Основное меню 3ds Max) -- показывает структуру главного меню программы (справа)\n\nЭлементы главного меню:\n\nВ списке представлены стандартные пункты главного меню 3ds Max, такие как:\n\n• File (Файл)\n\n• Edit (Правка)\n\n• Tools (Инструменты)\n\n• Group (Группировка)\n\n• Views (Виды)\n\n• Create (Создание)\n\n• Modifiers (Модификаторы)\n\n• Animation (Анимация)\n\n• Graph Editors (Графические редакторы)\n\n• Rendering (Рендеринг)\n\n• Customize (Настройки)\n\n• Scripting (Скрипты)\n\n• Help (Помощь)\n\n• Substance, Arnold -- интеграция с соответствующими рендер-движками\n\n• 3DGROUND -- возможно, пользовательская настройка\n\nДоступные действия:\n\n• New... -- создать новое меню\n\n• Delete... -- удалить выбранный элемент\n\n• Rename... -- переименовать пункт меню\n\n• Load... / Save... / Reset -- загрузка, сохранение и сброс настроек меню",
                                "media": []
                            },
                            {
                                "id": "2.2.5",
                                "title": "Color",
                                "content": "Это меню позволяет настраивать все цветовые изменения и цвет интерфейса. Для начала нужно выбрать элемент, цвет которого будет настраиваться. Это можно сделать в строке Elements, выбрав раздел из выпадающего списка. Затем в окне ниже выбрать элемент, который будете изменять. В строке Color при нажатии на прямоугольник откроется окно с палитрой (Color Selector), в котором можно поменять цвет. В нижней части меню находится список элементов пользовательского интерфейса. Выбор цвета аналогичен Elements. Чтобы увидеть изменения, нужно нажать кнопку Apply Color Now.",
                                "media": []
                            },
                            {
                                "id": "2.2.6",
                                "title": "установка плагинов",
                                "content": "Если в интерфейсе 3ds Max нет одного из установленных плагинов, выполните команду.",
                                "media": ["image15.gif"]
                            }
                        ]
                    },
                    {
                        "id": "2.3",
                        "title": "Продвинутые анимации и кинематографические эффекты",
                        "content": "Для движения по траектории используйте [Animation (Анимация)]{.mark} → [Constraint (Ограничение)]{.mark} → [Path Constraint (Ограничение по траектории)]{.mark}.\n\nНастройте кривые движения в [Track View - Curve Editor (Редактор кривых)]{.mark} для плавности анимации.",
                        "media": ["image16.gif", "image6.gif"]
                    },
                    {
                        "id": "2.4",
                        "title": "Импорт/экспорт и интеграция",
                        "content": "Импортируйте объекты через [File (Файл)]{.mark} → [Import (Импорт)]{.mark}\n\nЭкспортируйте через [File (Файл)]{.mark} → [Export (Экспорт)]{.mark}, выбирая нужные форматы (FBX, OBJ и т.д.).",
                        "media": ["image17.gif", "image18.gif"]
                    }
                ]
            }
        ]
    }

    # Clean the text and extract media references
    for section in result["sections"]:
        for item in section["content"]:
            item["content"] = clean_text(item["content"])

            # If there are subitems, clean their text too
            if "subcontent" in item:
                for subitem in item["subcontent"]:
                    subitem["content"] = clean_text(subitem["content"])

    return result


def main():
    output_path = "3ds_max_sections_1_2.json"  # Output JSON file

    try:
        # Process the document manually
        result = process_document()

        # Count items
        section1_items = len(result["sections"][0]["content"])
        section2_items = len(result["sections"][1]["content"])

        section2_subitems = 0
        for item in result["sections"][1]["content"]:
            if "subcontent" in item:
                section2_subitems += len(item["subcontent"])

        print(f"\nExtraction summary:")
        print(f"Section 1: {section1_items} items extracted")
        print(f"Section 2: {section2_items} main items and {section2_subitems} subitems extracted")

        # Write the JSON output
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"JSON file created and saved to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()