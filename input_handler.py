import curses
from typing import Optional

class InputHandler:
    """Класс для обработки пользовательского ввода"""
    
    def __init__(self):
        self.screen: Optional[curses.window] = None
        self.keys_pressed = set()
        
    def initialize(self, screen) -> None:
        """Инициализация обработчика ввода"""
        self.screen = screen
        self.screen.nodelay(True)  # Неблокирующий режим ввода
        
    def process_input(self) -> None:
        """Обработка пользовательского ввода"""
        if not self.screen:
            return
            
        # Очищаем предыдущие нажатия
        self.keys_pressed.clear()
        
        # Получаем все доступные символы
        try:
            while True:
                key = self.screen.getch()
                if key == -1:  # Нет больше символов
                    break
                self.keys_pressed.add(key)
                
                # Проверяем выход
                if key == ord('q'):
                    raise KeyboardInterrupt
                    
        except curses.error:
            pass  # Игнорируем ошибки curses
            
    def is_key_pressed(self, key: int) -> bool:
        """Проверка нажатия клавиши"""
        return key in self.keys_pressed
