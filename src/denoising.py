import numpy as np
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import cg

def compute_difference_matrices(M, N):
    """
    Construye las matrices dispersas de diferencias para una imagen de tamaño M x N.
    """
    # Diferencias horizontales: filas constantes, columnas adyacentes
    # Crea un vector de unos de tamaño N - 1 para representar diferencias entre columnas adyacentes
    e_h = np.ones(N - 1)
    # Genera una matriz dispersa donde cada fila calcula la diferencia entre dos columnas consecutivas
    Dh_block = diags([-e_h, e_h], [0, 1], shape=(N - 1, N)).tocsc()
    # Extiende las diferencias horizontales a toda la imagen
    D_h = kron(identity(M), Dh_block)

    # Diferencias verticales: filas adyacentes, columnas constantes
    # Crea un vector de unos de tamaño M - 1 para representar diferencias entre filas adyacentes
    e_v = np.ones(M - 1)
    # Genera una matriz dispersa donde cada fila calcula la diferencia entre dos filas consecutivas
    Dv_block = diags([-e_v, e_v], [0, 1], shape=(M - 1, M)).tocsc()
    # Extiende las diferencias verticales a toda la imagen
    D_v = kron(Dv_block, identity(N))

    return D_h, D_v

def denoise_image(noisy_image, lambda_param):
    """
    Aplica reducción de ruido mediante inversión regularizada usando matrices dispersas.
    """
    # Obtener dimensiones de la imagen
    M, N = noisy_image.shape
    # Convertir la imagen a un vector 1D
    x = noisy_image.flatten()

    # Construir matrices dispersas
    D_h, D_v = compute_difference_matrices(M, N)

    # Término de suavidad
    smooth_term = lambda_param * (D_h.T @ D_h + D_v.T @ D_v)

    # Matriz identidad
    I = identity(M * N, format="csc")

    # Resolver el sistema de ecuaciones: (I + smooth_term) @ x = b
    A = I + smooth_term # Matriz del sistema
    b = x # Vector de la imagen ruidosa

    # Usar gradiente conjugado
    x_denoised, _ = cg(A, b, atol=1e-6, maxiter=700)

    # Convertir de nuevo a una imagen 2D
    denoised_image = x_denoised.reshape(M, N).clip(0, 255).astype(np.uint8)

    return denoised_image
