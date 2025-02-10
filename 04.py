import cv2
import numpy as np

# Функция для определения цвета
def detect_color(frame, lower_bound, upper_bound, color_name):
    # Преобразуем изображение в HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Создаем маску для заданного диапазона цвета
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Находим контуры объектов на маске
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_colors = []
    
    # Рисуем контуры и выводим текст с названием цвета
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Игнорируем маленькие области
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            detected_colors.append((x, y, color_name))  # Добавляем координаты и название цвета
    
    return detected_colors

# Диапазоны цветов в HSV
red_lower = np.array([0, 120, 70])
red_upper = np.array([10, 255, 255])

orange_lower = np.array([10, 120, 70])
orange_upper = np.array([25, 255, 255])

blue_lower = np.array([100, 150, 50])
blue_upper = np.array([140, 255, 255])

green_lower = np.array([0, 140, 0])
green_upper = np.array([255, 255, 69])

black_lower = np.array([0, 0, 0])
black_upper = np.array([61, 133, 69])

# Захват видео с камеры
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    all_detected_colors = []
    
    # Определяем цвета
    all_detected_colors.extend(detect_color(frame, red_lower, red_upper, "Red"))
    all_detected_colors.extend(detect_color(frame, orange_lower, orange_upper, "Orange"))
    all_detected_colors.extend(detect_color(frame, green_lower, green_upper, "Green"))
    all_detected_colors.extend(detect_color(frame, black_lower, black_upper, "Black"))
    all_detected_colors.extend(detect_color(frame, blue_lower, blue_upper, "Blue"))
    
    # Сортируем цвета сначала по Y, затем по X
    all_detected_colors.sort(key=lambda color: (color[1], color[0]))  # Сортировка по Y, затем по X (color[1] — это координата Y, color[0] — это координата X)
    
    # Выводим порядок цветов в терминал
    color_order = [color[2] for color in all_detected_colors]
    print("Порядок цветов:", ", ".join(color_order))
    
    # Показываем результат
    cv2.imshow('Color Detection', frame)
    
    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()