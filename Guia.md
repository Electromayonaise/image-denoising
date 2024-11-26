# Estimación e Inversión 

La **estimación** o **inversión** en problemas de mínimos cuadrados multiobjetivo busca determinar un conjunto de parámetros $x$ a partir de mediciones $y$. Esto se describe con la ecuación: 

$$
y = Ax + v,
$$

donde $A$ es una matriz conocida que relaciona los parámetros con las mediciones, y $v$ es un vector de ruido o error. En escenarios ideales, sin ruido y con $A$ de rango completo, $x$ se podría calcular exactamente como $x = A^{\dagger}y$ usando la pseudo-inversa de $A$. Sin embargo, en la práctica, el ruido ($v \neq 0$) y problemas como la dependencia lineal en las columnas de $A$ hacen que este cálculo directo no sea viable, requiriendo métodos más robustos para estimar $x$.  

## Inversión Regularizada  

La **inversión regularizada** aborda estas limitaciones incorporando términos adicionales que reflejan suposiciones o restricciones sobre la solución. Esto se formula minimizando la función de costo:  

$$ 
\|Ax - y\|^2 + \lambda_2 J_2(x) + \cdots + \lambda_p J_p(x),
$$  

donde:  
- $\|Ax - y\|^2$: Garantiza que la solución sea consistente con los datos observados.  
- $J_i(x)$: Son términos de regularización que reflejan supuestos sobre $x$, como su suavidad o proximidad a valores previos.  
- $\lambda_i$: Son parámetros que equilibran la importancia relativa entre fidelidad a los datos y regularización.  

**Ejemplos de regularizaciones comunes:**  
1. **Norma de $x$ ($\|x\|^2$):** Suponer que $x$ tiene valores pequeños.  
2. **Diferencias finitas ($\|Dx\|^2$):** Favorece soluciones suaves, donde valores consecutivos de $x$ son cercanos.  
3. **Energía de Dirichlet:** Para grafos, favorece variaciones suaves entre nodos conectados.  

Al elegir $\lambda_i$ adecuadamente, se obtiene una estimación $\hat{x}$ que balancea los datos con las suposiciones impuestas, logrando mayor robustez frente al ruido o singularidades en $A$.  

## De-blurring de Imágenes  

En el contexto del desenfoque de imágenes, $x$ representa la imagen original (convertida a un vector), $A$ modela el desenfoque aplicado, y $y$ es la imagen observada con ruido. La meta es recuperar $x$ minimizando:  

$$
\|Ax - y\|^2 + \lambda (\|D_hx\|^2 + \|D_vx\|^2),
$$  

donde $\|Ax - y\|^2$ mide la fidelidad a los datos, y $\|D_hx\|^2 + \|D_vx\|^2$ asegura que la solución sea suave.  

**Construcción de las matrices $D_h$ y $D_v$**  

1. **Diferencias horizontales ($D_h$):**  
Esta matriz mide diferencias entre píxeles consecutivos en una fila. Si $x$ representa una imagen de tamaño $M \times N$, $D_h$ es de tamaño $M(N-1) \times MN$ . Cada bloque dentro de $D_h$ es:  
   - $-I$ y $I$ representan que cada diferencia corresponde al valor actual menos el siguiente en la fila.  
   - La estructura por bloques refleja que las diferencias horizontales son independientes entre filas.  

2. **Diferencias verticales ($D_v$):**  
Evalúa diferencias entre píxeles consecutivos en una columna. En este caso, la matriz $D_v$ tiene tamaño $(M-1)N \times MN$ y se organiza en bloques diagonales. Cada bloque $D$ calcula las diferencias entre filas consecutivas dentro de una columna.  
   - El bloque $D$ tiene una estructura escalonada, donde cada fila representa $-1$ en el píxel actual y $1$ en el siguiente.  
   - La organización en bloques captura que las diferencias verticales están agrupadas por columnas.  

**Razón de estas estructuras:**  
- $D_h$ y $D_v$ reflejan conexiones locales en la imagen: horizontalmente, cada píxel se compara con el siguiente; verticalmente, con el de abajo.  
- La regularización $\|D_hx\|^2 + \|D_vx\|^2$ minimiza las variaciones entre píxeles adyacentes, logrando reconstrucciones más suaves que eliminan artefactos del ruido y el desenfoque.  

Este enfoque, conocido como regularización Laplaciana, asegura que la imagen reconstruida sea consistente con los datos, suave, y visualmente plausible.  


### Sobre el código de de noising 

### Resumen del código de denoising

#### 1. **Construcción de matrices de diferencias: `compute_difference_matrices(M, N)`**
Esta función genera matrices dispersas para calcular diferencias horizontales y verticales en una imagen de tamaño $M \times N$.  
- **Entrada:** Dimensiones de la imagen (M, N).  
- **Salida:** Matrices dispersas \( D_h \) y \( D_v \).  

- **¿Qué hace?**  
  - **Diferencias horizontales (\(D_h\)):**  
    - Para cada fila, mide diferencias entre columnas adyacentes.  
    - Se construye como el producto de Kronecker entre la matriz identidad (para filas) y un bloque de diferencias en las columnas.  
  - **Diferencias verticales (\(D_v\)):**  
    - Para cada columna, mide diferencias entre filas adyacentes.  
    - Se construye como el producto de Kronecker entre un bloque de diferencias en las filas y la matriz identidad (para columnas).  

- **¿Por qué es importante?** Estas matrices permiten aplicar regularización, asegurando que la imagen procesada sea suave, ya que las diferencias locales (ruido) serán penalizadas.

---

#### 2. **Denoising de la imagen: `denoise_image(noisy_image, lambda_param)`**
Aplica una técnica de denoising basada en inversión regularizada para suavizar una imagen con ruido.  

- **Entrada:**  
  - `noisy_image`: Imagen ruidosa como un arreglo 2D.  
  - `lambda_param`: Parámetro de regularización para controlar la suavidad.  

- **Pasos:**  
  1. **Convertir la imagen:**  
     - La imagen \( M \times N \) se aplana a un vector 1D \( x \).  
  2. **Construir matrices de diferencias:**  
     - Llama a `compute_difference_matrices` para obtener \( D_h \) y \( D_v \).  
  3. **Calcular el término de suavidad:**  
     - Combina las transpuestas y productos de \( D_h \) y \( D_v \), escaladas por el parámetro de regularización \( \lambda \). Esto penaliza las diferencias grandes entre píxeles adyacentes.  
  4. **Definir el sistema lineal:**  
     - La matriz \( A = I + \lambda (D_h^T D_h + D_v^T D_v) \) combina fidelidad a los datos (identidad) con suavidad.  
  5. **Resolver el sistema usando Gradiente Conjugado (CG):**  
     - Resuelve \( Ax = b \), donde \( b \) es el vector imagen ruidoso \( x \).  
  6. **Reconstruir la imagen:**  
     - Convierte \( x \) a una matriz \( M \times N \) y recorta valores entre 0 y 255.  

- **Salida:**  
  - La imagen denoised como una matriz 2D.

---

#### 3. **Evaluación del denoising: `evaluate_denoising(original, denoised)`**
Mide la calidad del denoising mediante indicadores de desempeño como **PSNR** y **SSIM**.

- **Entrada:**  
  - `original`: Imagen original sin ruido.  
  - `denoised`: Imagen procesada después del denoising.  

- **Indicadores:**  
  - **PSNR (Peak Signal-to-Noise Ratio):**  
    - Relación entre la potencia de la señal y el ruido presente. Se mide en decibelios (dB).  
    - **Interpretación:** Valores altos indican mayor similitud entre las imágenes. Típicamente >30 dB es bueno.  
  - **SSIM (Structural Similarity Index):**  
    - Mide la similitud estructural entre las imágenes considerando luminancia, contraste y estructura.  
    - **Interpretación:** Valores cercanos a 1 indican alta similitud.  

- **Salida:**  
  - Los valores de PSNR y SSIM para comparar la calidad del denoising.

---

#### 4. **Agregar ruido a la imagen: `add_noise(image, noise_factor=0.2)`**
Introduce ruido gaussiano a una imagen para simular el efecto de distorsión.

- **Entrada:**  
  - `image`: Imagen original como matriz 2D.  
  - `noise_factor`: Factor que escala la magnitud del ruido (por defecto 0.2).  

- **Funcionamiento:**  
  - Genera un ruido gaussiano usando `np.random.randn`, escalado por `noise_factor` y \(255\).  
  - Suma el ruido a la imagen original.  
  - Recorta valores entre 0 y 255 para mantener el rango válido.  

- **Salida:**  
  - Imagen con ruido como matriz 2D.

