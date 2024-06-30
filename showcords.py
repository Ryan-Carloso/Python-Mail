import pyautogui
import time


time.sleep(5)
# Obtém e imprime as coordenadas atuais do mouse
x, y = pyautogui.position(
)
print('Coordenadas do mouse:', x, y)