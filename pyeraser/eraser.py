from time import sleep
import pyautogui
import pyperclip
import logging
import sys
import re

# Configuração do logger
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        
# Obtêm as coordenadas do campo desejado
class UserIteractionsHandler:
    def alert_user(self, message):
        logging.info(message)
        print(message)
        
    def get_coordinates(self, name):
        self.alert_user('Movo o mouse para o ponto desejado.\n3s...')
        sleep(3)
        x, y = pyautogui.position()
        self.alert_user(f'{name}: {x}, {y}.')
        print()
        return x, y
    
    
class Eraser:
    def __init__(self, current_words, new_word, quantity_products, wait_time, last_product_id):
        self.current_words = [word.upper() for word in current_words]
        self.new_word = new_word.upper()
        self.quantity_products = quantity_products
        self.wait_time = wait_time
        self.last_product_id = last_product_id
        self.speed_mouse = 0.3
        self.iteration_count = 0
        self.user_handler = UserIteractionsHandler()    
        self.field_positions = self.get_field_positions()
        
        # Tratamento de falhas
        pyautogui.PAUSE = self.wait_time
        pyautogui.FAILSAFE = True
        
        # Prepara o ambiente
        pyautogui.hotkey('ctrl', 'e')
        self.skip_to('skip_start')
        
        
    # Obtêm as posições dos campos
    def get_field_positions(self):
        field_names = ['skip_start', 'skip_up', 'skip_down', 'save_field', 'id_field', 'start_field_name', 'end_field_name']
        positions = {}
        for name in field_names:
            positions[name] = self.user_handler.get_coordinates(name)
        return positions
        
        
    # Função para clicar e mover para determinada posição
    def move_and_click(self, position):
        pyautogui.moveTo(position, duration=self.speed_mouse)
        pyautogui.click()
        
    def skip_to(self, button):
        self.move_and_click(self.field_positions[button])
        
    
    def select_text(self, field_names):
        start_field_name, end_field_name = field_names
        self.move_and_click(self.field_positions[start_field_name])
        pyautogui.mouseDown(button='left')
        self.move_and_click(self.field_positions[end_field_name])
        sleep(1)
        pyautogui.mouseUp(button='left')
        
        
    # Verifica se ainda está no intervalo correto
    def check_range(self, last_product_id=None):
        if self.last_product_id is not None:
            self.move_and_click(self.field_positions['id_field'])
            pyautogui.click(clicks=2)
            pyautogui.hotkey('ctrl', 'c')
            current_id = pyperclip.paste()
            if current_id == last_product_id:
                self.user_handler.alert_user('Fluxo finalizado!')
                sys.exit(0)
    
    
    # Escreve o novo texto
    def writer_text(self, text):
        self.move_and_click(self.field_positions['start_field_name'])
        pyautogui.write(text.upper())
    
    # Salva as alterações
    def save_changes(self):
        self.move_and_click(self.field_positions['save_field'])
        self.user_handler.alert_user('Alterações salvas!')
        print()
    
    # Troca o texto pelo novo
    def change_text(self):
        self.check_range(self.last_product_id)
        self.select_text( ['start_field_name', 'end_field_name'] )
        pyautogui.hotkey('ctrl', 'c')
        current_name = pyperclip.paste()
        self.user_handler.alert_user(f'Texto copiado: {current_name}')
        new_name = self.modify_text(current_name)
        self.writer_text(new_name)
        self.save_changes()
        self.skip_to('skip_up')
        
        
    # Modifica o texto
    def modify_text(self, current_name):
        for word in self.current_words:
            pattern = re.compile(r'\b' + word + r'\b', re.IGNORECASE)
            new_name = re.sub(pattern, self.new_word, current_name).upper()
        self.user_handler.alert_user(f'novo nome: {new_name}')
        return new_name
                
    
    # Faz o fluxo do código
    def run(self):
        while True:
            self.change_text()
            self.iteration_count += 1
            if self.iteration_count == self.quantity_products:
                break