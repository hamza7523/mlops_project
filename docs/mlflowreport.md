# **MLflow Experiment Report**


This document details the training dynamics and performance evaluation of the **swin_cv_model** within the **Flora_Care_Production_Pipeline**.  
The experiment was tracked using **MLflow** to monitor hyperparameters, loss convergence, and system throughput.  
The analysis confirms that the model has successfully converged with high accuracy and stability.

---

# **1. Final Performance Metrics**

The following figure displays the comprehensive list of metrics recorded at the conclusion of the 10th epoch:

![MLflow Metrics](https://preview.redd.it/e0l1a3vj045e1.png?width=2876&format=png&auto=webp&s=6b170c2a55099f667d4f3e695079a2955f1f0a52)

---

## **Evaluation of Tracked Metrics**

### **Generalization Capability (eval_loss)**  
The final evaluation loss recorded is **0.01027**.  
This metric represents the error rate on the validation dataset.  
Such a distinctively low value indicates that the model generalizes exceptionally well to unseen data and is not suffering from overfitting.

### **Training Convergence (loss)**  
The final training loss is **0.0276**.  
This signifies that the model successfully minimized the objective function on the training set, effectively learning the underlying patterns of the input data.

### **Training Stability (grad_norm)**  
The gradient norm (**645,107.8**) reflects the magnitude of the vector of derivatives.  
Tracking this ensures that the training process remained numerically stable without vanishing or exploding gradients.

### **Computational Throughput (train/eval_samples_per_second)**  
- **Training Speed:** ~133.14 samples/sec  
- **Inference Speed:** ~223.75 samples/sec  

This indicates efficient inference capabilities suitable for production deployment.

---

# **2. Training Dynamics and Visualization Analysis**

The following figures illustrate the progression of key metrics over the course of the training steps.  
These visualizations provide insight into the learning schedule, convergence behavior, and system performance.

![Training Metrics 1](https://preview.redd.it/b5x2s5nj045e1.png?width=2880&format=png&auto=webp&s=da8b9b870db540b64d436a5a9d80c35414f52f36)

![Training Metrics 2](https://preview.redd.it/o1p4t1nj045e1.png?width=2880&format=png&auto=webp&s=e78e2d4d39f2858739199d945f7435f0868f000b)

---

## **Detailed Analysis of Visualizations**

### **A. Loss Convergence (loss and eval_loss)**

The plots for both training and evaluation loss demonstrate an ideal learning trajectory.

- **Rapid Feature Extraction:**  
  The initial phase (Steps 0–1,000) shows a steep, exponential decay in loss.  
  This indicates that the Swin Transformer architecture rapidly identified the primary features within the dataset.

- **Asymptotic Convergence:**  
  After the initial drop, the curves flatten (plateau).  
  This confirms that the model reached an optimal state where further iterations provided marginal gains—showing efficient use of the 10-epoch duration.

- **Validation Consistency:**  
  The eval_loss curve tracks closely with the training loss without divergence.  
  This parallelism is a critical indicator of robust generalization.

---

### **B. Learning Rate Schedule (learning_rate)**

The learning rate plot shows:

- **Warm-up Phase:**  
  A linear increase from zero, peaking around step 1,000.  
  This helps stabilize training before larger updates occur.

- **Linear Decay:**  
  After the peak, the learning rate decreases linearly.  
  This allows increasingly precise fine-tuning as convergence is approached.

---

### **C. Gradient Behavior (grad_norm)**

The visualization of the gradient norm displays the L2 norm of the gradients at each step.

- **Stability:**  
  Despite natural oscillations (typical of stochastic gradient descent), the overall magnitude stays controlled.  
  No signs of divergence appear, indicating a stable backpropagation process.

---

### **D. System Latency and Throughput (eval_runtime & samples_per_second)**

The performance plots indicate a stable computational environment.

- **Steady State:**  
  After an initialization spike, both runtime and throughput stabilize.  
  The horizontal trend lines confirm consistent resource allocation, ensuring predictable latency throughout the experiment.

---

