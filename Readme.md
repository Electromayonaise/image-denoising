# Image Denoising Project README

## **Introduction**
This project focuses on image denoising using numerical optimization techniques. The method leverages sparse matrices and a regularized inversion approach to minimize noise in grayscale images. Additionally, the project includes tools for noise evaluation using metrics such as Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).

## **How It Works**
The process involves the following key steps:

1. **Adding Noise to an Image**: Gaussian noise is artificially introduced to simulate noisy images.
2. **Noise Reduction (Denoising)**:
   - A regularization-based approach is used to solve a sparse system of linear equations.
   - Horizontal and vertical difference matrices are constructed to enforce smoothness in the image.
   - A conjugate gradient solver (`scipy.sparse.linalg.cg`) efficiently computes the denoised image.
3. **Quality Evaluation**: Metrics like PSNR and SSIM are used to compare the original and denoised images, providing objective measures of the denoising performance.

## **Theoretical Background**
1. **Noise in Images**:
   - Digital images often suffer from noise due to various factors like sensor imperfections, low light, or transmission errors.
   - Gaussian noise, characterized by its bell-curve distribution, is a common type of noise.

2. **Regularized Denoising**:
   - Denoising is formulated as an optimization problem:

    $$
     \text{minimize} \quad \| I_{\text{noisy}} - I_{\text{denoised}} \|^2 + \lambda \| D_h I + D_v I \|^2
      $$

   where:
   - `I_noisy` is the noisy image.
   - `I_denoised` is the denoised image.
   - `D_h` and `D_v` are horizontal and vertical difference matrices.
   - `λ` (lambda) is the regularization parameter.


3. **Sparse Matrices**:
   - Sparse matrices efficiently represent operations like finite differences, reducing memory usage and computational cost.

4. **Conjugate Gradient Solver**:
   - The optimization problem results in a large linear system. The conjugate gradient method provides an iterative solution.

## **Features**
- **Noise Simulation**: Adds Gaussian noise to any input grayscale image.
- **Denoising Algorithm**: Implements regularized noise reduction using sparse matrix operations.
- **Performance Metrics**: Computes PSNR and SSIM for objective evaluation.
- **Visualization Tools**: Displays original, noisy, and denoised images for visual comparison.

## **Dependencies**
- Python 3.x
- OpenCV (`opencv-python`)
- SciPy (`scipy`)
- NumPy (`numpy`)
- Scikit-image (`scikit-image`)
- Matplotlib (`matplotlib`)

Install dependencies using (or install the requirements from `requirements.txt`):
```bash
pip install opencv-python scipy numpy scikit-image matplotlib
```

## **Usage**
1. Clone the repository:
   ```bash
   git clone https://github.com/Electromayonaise/image-denoising
   cd image-denoising
   ```

2. Prepare an input image (grayscale, e.g., `cat.png`) and place it in the `data/` directory.

3. Run the main script:
   ```bash
   python main.py
   ```

4. Outputs:
   - `cat_noisy.png`: Image with added Gaussian noise.
   - `cat_denoised.png`: Image after denoising.

## **Example**
### **Original Image**
![Original Image](data/cat.png)

### **Noisy Image**
![Noisy Image](data/cat_noisy.png)

### **Denoised Image**
![Denoised Image](data/cat_denoised.png)

### **Performance**
- **PSNR**: Measures how much the denoised image resembles the original.
- **SSIM**: Evaluates perceived structural similarity.

Example Output:
```
PSNR: 30.25, SSIM: 0.85
```

## **Customization**
- Adjust `lambda_param` in `denoise_image` to control the regularization strength.
- Modify `noise_factor` in `add_noise` to simulate different levels of noise.

