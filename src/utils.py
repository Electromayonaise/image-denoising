import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

def load_image(image_path):
    """
    Carga una imagen en formato de escala de grises.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image

def save_image(image, output_path):
    """
    Guarda una imagen en el disco.
    """
    cv2.imwrite(output_path, image)

def show_image(image, title="Image"):
    """
    Muestra la imagen usando matplotlib.
    """
    import matplotlib.pyplot as plt
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def add_noise(image, noise_factor=0.2):
    """
    Agrega ruido gaussiano a la imagen.
    """
    noise = np.random.randn(*image.shape) * noise_factor * 255
    noisy_image = np.clip(image + noise, 0, 255)
    return noisy_image.astype(np.uint8)

def evaluate_denoising(original, denoised):
    """
    Calcula PSNR y SSIM entre la imagen original y la denoised.
    """
    psnr = peak_signal_noise_ratio(original, denoised)
    ssim = structural_similarity(original, denoised, data_range=denoised.max() - denoised.min())
    return psnr, ssim



