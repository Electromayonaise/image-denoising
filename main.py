from src.denoising import denoise_image
from src.utils import load_image, save_image, add_noise, show_image, evaluate_denoising

def main():
    # Cargar la imagen original (cat.png)
    image_path = "data/cat.png"
    image = load_image(image_path)

    # Mostrar imagen original
    show_image(image, title="Imagen Original")

    # Agregar ruido a la imagen
    noisy_image = add_noise(image, noise_factor=0.2)
    noisy_image_path = "data/cat_noisy.png"
    save_image(noisy_image, noisy_image_path)
    print(f"Imagen ruidosa guardada en {noisy_image_path}")

    # Mostrar imagen ruidosa
    show_image(noisy_image, title="Imagen Ruidosa")

    # Reducir el ruido utilizando inversión regularizada
    denoised_image = denoise_image(noisy_image, lambda_param=4)

    # Guardar la imagen denoised
    denoised_image_path = "data/cat_denoised.png"
    save_image(denoised_image, denoised_image_path)
    print(f"Imagen denoised guardada en {denoised_image_path}")

    # Mostrar imagen denoised
    show_image(denoised_image, title="Imagen Denoised")

    # Evaluar la calidad del denoising
    psnr, ssim = evaluate_denoising(image, denoised_image)
    print(f"PSNR: {psnr:.2f}, SSIM: {ssim:.4f}")

if __name__ == "__main__":
    main()
