import cv2
import numpy as np
import Controlo_carro as ctrl_carro

# Função para encontrar o centro de um retângulo
def centro_retangulo(retangulo):
    x, y, w, h = retangulo
    centro_x = x + (w // 2)
    centro_y = y + (h // 2)
    if centro_x > 400:
        angulo = ((centro_x-400)*60)/400
    elif centro_x < 400:
        angulo = 60-(centro_x*60)/400
        angulo = 0 - angulo
    else:
        angulo = 0
    print(angulo)
    return centro_x, centro_y
# Função para encontrar o ângulo em relação ao centro



# Inicializar a webcam
cap = cv2.VideoCapture(0)

# Variável global para armazenar o centro do retângulo sob o cursor do mouse
centro_retangulo_atual = None


# Função de callback para o evento do mouse
def callback_mouse(event, x, y, flags, params):
    global centro_retangulo_atual


    # Se o evento for movimento do mouse
    if event == cv2.EVENT_MOUSEMOVE:
        # Verificar se o mouse está sobre algum retângulo
        for retangulo in retangulos:
            x_rect, y_rect, w_rect, h_rect = retangulo
            # Se o mouse estiver sobre o retângulo, calcular e armazenar o centro
            if x_rect <= x <= x_rect + w_rect and y_rect <= y <= y_rect + h_rect:
                centro_retangulo_atual = centro_retangulo(retangulo)
                return
        # Se o mouse não estiver sobre nenhum retângulo, limpar o centro
        centro_retangulo_atual = None



# Configurar o callback do mouse
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', callback_mouse)

#------------------------------------------------------------------------------------------------
ctrl_carro.controlo(20.0)

while True:

    # Capturar frame da webcam
    ret, frame = cap.read()

    largura_janela = 800
    altura_janela = 600
    imagem_redimensionada = cv2.resize(frame,(largura_janela,altura_janela))

    # Converter frame para espaço de cores HSV
    hsv = cv2.cvtColor(imagem_redimensionada, cv2.COLOR_BGR2HSV)

    # Definir o intervalo de cor azul em HSV
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([120, 255, 255])

    # Criar uma máscara para filtrar apenas a cor azul
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Armazenar os retângulos
    retangulos = []

    # Iterar sobre os contornos encontrados
    for contour in contours:
        # Calcular a área do contorno
        area = cv2.contourArea(contour)

        # Se a área for maior que um valor mínimo, consideramos como nosso adesivo
        if area > 1000:
            # Encontrar retângulo delimitador ao redor do adesivo
            x, y, w, h = cv2.boundingRect(contour)

            # Desenhar retângulo ao redor do adesivo
            cv2.rectangle(imagem_redimensionada, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Armazenar o retângulo
            retangulos.append((x, y, w, h))

    # Se houver um centro de retângulo sob o cursor do mouse, imprimir na tela
    if centro_retangulo_atual:
        cv2.putText(imagem_redimensionada, "Centro e angulo do retangulo: {}".format(centro_retangulo_atual), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Exibir o frame com o retângulo desenhado
    cv2.imshow('Frame', imagem_redimensionada)

    # Parar o loop quando a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

	

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
