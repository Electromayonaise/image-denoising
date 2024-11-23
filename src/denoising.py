import numpy as np
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import cg

def compute_difference_matrices(M, N):
    """
    Construye las matrices dispersas de diferencias para una imagen de tamaño M x N.
    """
    # Diferencias horizontales: filas constantes, columnas adyacentes
    e_h = np.ones(N - 1)
    Dh_block = diags([-e_h, e_h], [0, 1], shape=(N - 1, N)).tocsc()
    D_h = kron(identity(M), Dh_block)

    # Diferencias verticales: filas adyacentes, columnas constantes
    e_v = np.ones(M - 1)
    Dv_block = diags([-e_v, e_v], [0, 1], shape=(M - 1, M)).tocsc()
    D_v = kron(Dv_block, identity(N))

    return D_h, D_v

def denoise_image(noisy_image, lambda_param=5.0):
    """
    Aplica reducción de ruido mediante inversión regularizada usando matrices dispersas.
    """
    M, N = noisy_image.shape
    x = noisy_image.flatten()

    # Construir matrices dispersas
    D_h, D_v = compute_difference_matrices(M, N)

    # Término de suavidad
    smooth_term = lambda_param * (D_h.T @ D_h + D_v.T @ D_v)

    # Matriz identidad
    I = identity(M * N, format="csc")

    # Resolver el sistema de ecuaciones: (I + smooth_term) @ x = b
    A = I + smooth_term
    b = x

    # Usar gradiente conjugado
    x_denoised, _ = cg(A, b, atol=1e-6, maxiter=1000)

    # Convertir de nuevo a una imagen 2D
    denoised_image = x_denoised.reshape(M, N).clip(0, 255).astype(np.uint8)

    return denoised_image
