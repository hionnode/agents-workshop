# ML Foundations — Lesson Plans

> Detailed lesson plans for notebooks 01–06. This track prepares you for [Karpathy's Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html).
> For the full track overview and Karpathy lecture cross-reference, see [`../roadmap.md`](../roadmap.md).

---

## 01. Calculus for Deep Learning

**File:** `01_calculus_for_deep_learning.ipynb`

### Overview
This notebook builds your calculus intuition from the ground up — not with proofs, but with code. You will implement derivatives numerically, visualize the chain rule on computational graphs, and hand-code a gradient descent optimizer that minimizes a loss function. Calculus is the engine behind every neural network's ability to learn: without derivatives, there is no backpropagation, and without backpropagation, an LLM cannot update its weights from data. Everything in Karpathy's micrograd lecture rests on the concepts you build here.

### Learning Objectives
By the end of this notebook, you will be able to:
- Compute numerical derivatives using the limit definition and verify them against analytical solutions
- Apply the chain rule to composite functions both symbolically and in code
- Calculate partial derivatives for multivariable functions and interpret them as gradient vectors
- Build a computational graph for a simple expression and trace the backward pass by hand
- Implement vanilla gradient descent from scratch in NumPy to minimize a loss surface
- Explain why gradients point in the direction of steepest ascent and how negating them drives learning

### Prerequisites
- [`../appendix/01_python_fundamentals.ipynb`](../appendix/01_python_fundamentals.ipynb) — variables, loops, basic control flow
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — array creation, element-wise operations, broadcasting basics

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | What Is a Derivative? | Implement `numerical_derivative(f, x, h)` using the limit definition; plot slopes as tangent lines on a curve |
| 2 | Derivatives of Common Functions | Verify power rule, exponential, and log derivatives numerically; build a table comparing analytical vs. numerical results |
| 3 | The Chain Rule | Decompose `f(g(x))` into an inner and outer function; compute `df/dx` step-by-step; show that `df/dx = df/dg * dg/dx` in code |
| 4 | Partial Derivatives and Gradients | Compute `df/dx` and `df/dy` for `f(x, y) = x²y + sin(y)`; assemble a gradient vector; visualize with a quiver plot on a contour map |
| 5 | Computational Graphs | Draw a DAG for `L = (a*b + c)**2`; label each node with its local derivative; walk the backward pass manually |
| 6 | Backpropagation by Hand | Implement a tiny `Value` class (inspired by micrograd) with `.data`, `.grad`, and `._backward`; propagate gradients through a 4-node graph |
| 7 | Gradient Descent from Scratch | Write a `gradient_descent(f, grad_f, x0, lr, steps)` loop; minimize Rosenbrock's function; plot the optimization trajectory |
| 8 | Why This Matters for Neural Networks | Connect derivatives to weight updates: show that a single neuron `y = wx + b` learns via `dL/dw` and `dL/db` |

### Putting It Together
You will build a minimal autograd engine — a `Value` class that tracks a computational graph and performs reverse-mode automatic differentiation. Using it, you will define a simple expression, call `.backward()`, and verify that the computed gradients match your numerical derivative checks from earlier sections. This is the exact foundation Karpathy builds in micrograd.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Derivative Drill | Starter | Compute numerical derivatives for 5 functions (polynomial, trig, exponential) and compare against known analytical results |
| 2 | Chain Rule Composition | Starter | Given three nested functions `h(g(f(x)))`, compute `dh/dx` both analytically and numerically; verify they match to 6 decimal places |
| 3 | Gradient Descent Visualizer | Synthesis | Minimize a 2D loss surface using gradient descent; produce an animated plot showing the parameter trajectory converging to the minimum |
| 4 | Extend the Value Class | Stretch | Add support for `__sub__`, `__truediv__`, `tanh`, and `exp` operations to the `Value` class; verify gradients on a 10-node expression graph |

### Key References
- [3Blue1Brown — Essence of Calculus (full playlist)](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) — the best visual introduction to derivatives, integrals, and the chain rule
- [Karpathy — The spelled-out intro to neural networks and backpropagation (micrograd)](https://www.youtube.com/watch?v=VMj-3S1tku0) — builds exactly the autograd engine this notebook prepares you for
- [Khan Academy — Multivariable Calculus: Gradient](https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/gradient-and-directional-derivatives/v/gradient) — clear worked examples of partial derivatives and gradient vectors
- [Calculus on Computational Graphs: Backpropagation — Chris Olah](https://colah.github.io/posts/2015-08-Backprop/) — the clearest written explanation of how backprop works on graphs
- [Python Numerical Methods — Numerical Differentiation](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter20.01-Numerical-Differentiation-Problem-Statement.html) — practical treatment of finite differences in Python

---

## 02. Linear Algebra Essentials

**File:** `02_linear_algebra_essentials.ipynb`

### Overview
This notebook gives you the linear algebra that neural networks actually use — vectors, dot products, matrix multiplication, and the transforms that move data through every layer of a network. You will implement these operations in NumPy, visualize what matrices do geometrically, and build a working softmax function from scratch. Linear algebra is the language of neural networks: every forward pass is a sequence of matrix multiplications, every attention head computes dot products between query and key vectors, and every embedding lookup is a matrix index. Without this, transformer architectures are opaque.

### Learning Objectives
By the end of this notebook, you will be able to:
- Perform vector addition, scalar multiplication, and dot products in NumPy and explain their geometric meaning
- Implement matrix multiplication from scratch using nested loops, then verify against `np.matmul` / the `@` operator
- Apply transpose, reshape, and broadcasting to manipulate array shapes for neural network operations
- Compute softmax over a vector and explain its role in converting logits to probabilities
- Explain how matrix multiplication maps inputs to outputs in a linear layer (`y = Wx + b`)
- Visualize 2D linear transformations (rotation, scaling, shear) as matrix operations

### Prerequisites
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — array creation, indexing, broadcasting
- [`01_calculus_for_deep_learning.ipynb`](01_calculus_for_deep_learning.ipynb) — numerical intuition, gradient vectors

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Vectors and Their Operations | Create vectors with `np.array`; implement dot product manually (`sum(a_i * b_i)`); compute norms with `np.linalg.norm`; visualize vector addition in 2D |
| 2 | Dot Products and Similarity | Compute cosine similarity between word embedding vectors; show that dot products measure alignment; connect to attention score computation |
| 3 | Matrix Multiplication | Implement `matmul(A, B)` with three nested loops; verify against `A @ B`; trace the shapes through `(m,n) @ (n,p) → (m,p)` |
| 4 | Transpose, Reshape, and Broadcasting | Use `.T`, `.reshape()`, and `np.broadcast_to`; practice reshaping a batch of vectors for batched matrix operations |
| 5 | Linear Transformations Visually | Apply 2x2 matrices to a grid of points; plot rotation, scaling, and shear; show that matrix multiply = applying a linear transformation |
| 6 | The Linear Layer: `y = Wx + b` | Build a `linear_forward(X, W, b)` function; pass a batch of inputs through it; verify output shapes match expectations |
| 7 | Softmax and Log-Softmax | Implement `softmax(logits)` with the numerical stability trick (`logits - max`); implement `log_softmax`; plot output distributions for different temperature values |
| 8 | Einsum and Batched Operations | Use `np.einsum` to express dot products, matrix multiply, and batch operations in a single notation; connect to PyTorch `torch.einsum` |

### Putting It Together
You will build a complete two-layer forward pass from scratch in NumPy: input data goes through a linear layer (`W1 @ x + b1`), a ReLU activation, another linear layer (`W2 @ h + b2`), and a softmax to produce class probabilities. You will verify shapes at each step and compute the cross-entropy loss against target labels — a miniature version of what happens in every neural network.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Shape Detective | Starter | Given 5 pairs of matrices with specified shapes, predict the output shape of their product (or explain why the multiply is invalid) |
| 2 | Cosine Similarity Search | Starter | Given a set of 20 word embeddings, find the 3 most similar pairs using cosine similarity; compare against Euclidean distance ranking |
| 3 | Batched Attention Scores | Synthesis | Implement `attention_scores(Q, K)` that computes `Q @ K.T / sqrt(d_k)` for a batch of queries and keys; apply softmax over the last dimension |
| 4 | Image as Matrix Transform | Stretch | Load a small image as a matrix of 2D coordinates; apply rotation, scaling, and shear transforms; display the warped results side-by-side |

### Key References
- [3Blue1Brown — Essence of Linear Algebra (full playlist)](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — the gold-standard visual introduction to vectors, linear transforms, and matrix multiplication
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — see how Q, K, V matrices and attention scores use every concept in this notebook
- [NumPy documentation — Linear Algebra](https://numpy.org/doc/stable/reference/routines.linalg.html) — official reference for `np.dot`, `np.matmul`, `np.linalg` functions
- [Stanford CS231n — Linear Classification](https://cs231n.github.io/linear-classify/) — connects linear algebra to the classification pipeline in neural networks
- [Jay Alammar — A Visual Guide to NumPy](https://jalammar.github.io/visual-numpy/) — excellent visual explanations of array operations and broadcasting
- [Lilian Weng — Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/) — deep dive into attention mechanisms, heavily dependent on linear algebra

---

## 03. Probability and Statistics

**File:** `03_probability_and_statistics.ipynb`

### Overview
This notebook covers the probability and statistics that underpin how neural networks make predictions and measure error. You will implement probability distributions, sample from them, compute cross-entropy and negative log-likelihood losses by hand, and build intuition for why these metrics work. Every language model is fundamentally a probability distribution over the next token — understanding distributions, sampling, and information-theoretic losses is essential to grasping how models like GPT are trained and how they generate text.

### Learning Objectives
By the end of this notebook, you will be able to:
- Compute basic probabilities, conditional probabilities, and apply Bayes' theorem in code
- Implement and sample from discrete (uniform, categorical) and continuous (normal, uniform) distributions using NumPy
- Calculate mean, variance, and standard deviation and explain their role in normalization techniques like BatchNorm
- Implement cross-entropy loss and negative log-likelihood (NLL) from scratch and explain why they are used for classification
- Relate entropy and KL divergence to model confidence and distribution matching
- Use `np.random` to sample from distributions and visualize convergence via the law of large numbers

### Prerequisites
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — array operations, random number generation
- [`01_calculus_for_deep_learning.ipynb`](01_calculus_for_deep_learning.ipynb) — derivatives (needed to understand gradient of log-likelihood)

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Probability Basics | Compute joint, marginal, and conditional probabilities on a toy dataset; verify Bayes' theorem numerically |
| 2 | Discrete Distributions | Implement a `Categorical` sampler with `np.random.choice`; visualize PMFs for uniform and weighted distributions; connect to token probability distributions in language models |
| 3 | Continuous Distributions and the Normal | Sample from `np.random.normal`; plot the PDF; compute z-scores; show how weight initialization uses `N(0, sigma)` |
| 4 | Mean, Variance, and Normalization | Compute running mean and variance over mini-batches; implement a `normalize(x)` function that maps data to zero mean and unit variance; connect to BatchNorm preprocessing |
| 5 | Entropy and Information | Implement `entropy(p)` as `-sum(p * log(p))`; compare entropy of peaked vs. uniform distributions; explain why high-entropy outputs mean the model is uncertain |
| 6 | Cross-Entropy Loss | Implement `cross_entropy(predictions, targets)` from scratch; show it equals NLL when targets are one-hot; trace through a concrete 3-class example |
| 7 | Negative Log-Likelihood | Implement `nll_loss(log_probs, target_indices)`; show equivalence to cross-entropy; explain why we minimize NLL to maximize the probability of correct labels |
| 8 | KL Divergence | Implement `kl_divergence(p, q)`; show it is non-negative and asymmetric; connect to knowledge distillation and VAEs |

### Putting It Together
You will build a complete evaluation pipeline for a toy language model: given a vocabulary of 50 tokens and a sequence of ground-truth next tokens, compute the model's predicted probability distribution at each step, calculate the per-token NLL, and aggregate into perplexity (`exp(mean NLL)`). This is exactly how language model quality is measured in practice — the metric Karpathy uses throughout the Zero to Hero series.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Distribution Sampler | Starter | Sample 10,000 values from a normal distribution; plot the histogram and overlay the analytical PDF; compute sample mean and variance |
| 2 | Cross-Entropy by Hand | Starter | Given a 4-class prediction `[0.7, 0.1, 0.1, 0.1]` and target class 0, compute cross-entropy manually; verify with your `cross_entropy` function |
| 3 | Perplexity Calculator | Synthesis | Compute perplexity for a bigram language model on a sample text; compare against a uniform-probability baseline to see how much the model has learned |
| 4 | Temperature Sampling | Stretch | Implement temperature-scaled sampling: divide logits by T before softmax; sample at T=0.5, 1.0, and 2.0; visualize how temperature controls the entropy of the output distribution |

### Key References
- [StatQuest with Josh Starmer (YouTube channel)](https://www.youtube.com/c/joshstarmer) — clear, visual explanations of probability distributions, Bayes' theorem, and statistical concepts
- [3Blue1Brown — But what is a convolution? (and probability context)](https://www.youtube.com/watch?v=HZGCoVF3YvM) — builds geometric intuition for probability operations
- [Chris Olah — Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/) — the best visual explanation of entropy, cross-entropy, and KL divergence
- [Karpathy — makemore Part 1 (bigram model)](https://www.youtube.com/watch?v=PaCmpygFfXo) — directly uses cross-entropy, NLL, and sampling concepts from this notebook
- [Wikipedia — Cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy) — concise formal definition and relationship to KL divergence
- [PyTorch documentation — CrossEntropyLoss](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) — see how the framework implements what you build by hand here

---

## 04. PyTorch Fundamentals

**File:** `04_pytorch_fundamentals.ipynb`

### Overview
This notebook transitions you from NumPy to PyTorch — the framework Karpathy uses for every lecture after micrograd. You will create tensors, perform operations, use autograd to compute gradients automatically, define a simple neural network with `nn.Module`, and write a complete training loop. PyTorch is the bridge between mathematical understanding and practical deep learning: it gives you autograd (so you do not have to hand-code backprop), GPU acceleration (so training is fast), and `nn.Module` (so networks are composable). Every remaining notebook and every Karpathy lecture depends on fluency with these fundamentals.

### Learning Objectives
By the end of this notebook, you will be able to:
- Create PyTorch tensors from Python lists, NumPy arrays, and using factory functions (`torch.zeros`, `torch.randn`)
- Perform element-wise, reduction, and matrix operations on tensors and manage dtypes and devices
- Use `requires_grad=True` and `.backward()` to compute gradients automatically and verify them against numerical estimates
- Define a multi-layer neural network by subclassing `nn.Module` with `__init__` and `forward`
- Write a complete training loop: forward pass, loss computation, `.backward()`, optimizer step, `.zero_grad()`
- Move tensors and models to GPU with `.to(device)` and explain why GPU parallelism accelerates matrix operations

### Prerequisites
- [`../appendix/07_classes_and_oop.ipynb`](../appendix/07_classes_and_oop.ipynb) — classes, `__init__`, inheritance (needed for `nn.Module` subclassing)
- [`../appendix/10_numpy_for_embeddings.ipynb`](../appendix/10_numpy_for_embeddings.ipynb) — NumPy arrays (PyTorch tensors mirror the NumPy API)
- [`01_calculus_for_deep_learning.ipynb`](01_calculus_for_deep_learning.ipynb) — derivatives and backpropagation (to understand what autograd automates)
- [`02_linear_algebra_essentials.ipynb`](02_linear_algebra_essentials.ipynb) — matrix operations (to understand tensor operations)

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Tensor Creation and Attributes | Create tensors with `torch.tensor`, `torch.zeros`, `torch.randn`, `torch.arange`; inspect `.shape`, `.dtype`, `.device`; convert to/from NumPy with `.numpy()` and `torch.from_numpy` |
| 2 | Tensor Operations | Perform element-wise (`+`, `*`, `torch.exp`), reduction (`sum`, `mean`, `max`), and comparison operations; practice indexing, slicing, and `torch.gather` |
| 3 | Reshaping and Broadcasting | Use `.view()`, `.reshape()`, `.unsqueeze()`, `.squeeze()`, `.permute()`; understand contiguous memory and when `.contiguous()` is needed |
| 4 | Autograd: Automatic Differentiation | Set `requires_grad=True`; build a computation; call `.backward()`; read `.grad`; verify against numerical derivatives from notebook 01; understand `torch.no_grad()` and `.detach()` |
| 5 | Building a Model with `nn.Module` | Subclass `nn.Module`; define `__init__` with `nn.Linear` layers; implement `forward`; inspect parameters with `.parameters()` and `.named_parameters()` |
| 6 | Loss Functions and Optimizers | Use `nn.CrossEntropyLoss` and `nn.MSELoss`; create `torch.optim.SGD` and `torch.optim.Adam`; explain the `zero_grad → forward → loss → backward → step` cycle |
| 7 | The Training Loop | Write a complete training loop on synthetic data: batching, forward pass, loss, backward, optimizer step; track and plot training loss over epochs |
| 8 | GPU Basics | Check `torch.cuda.is_available()`; move tensors and models with `.to('cuda')`; benchmark CPU vs. GPU on a large matrix multiply; discuss when GPU matters and when it does not |

### Putting It Together
You will train a 2-layer neural network to classify points in a synthetic spiral dataset (3 classes, 2D input). Starting from random weights, you will run the full training loop for 200 epochs, plot the decision boundary at epochs 0, 50, 100, and 200, and watch the network learn to separate the spiral arms. This exercise connects every section — tensor creation, `nn.Module`, loss functions, autograd, and the training loop — into a single working system.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | NumPy to PyTorch Translation | Starter | Rewrite 5 NumPy operations (dot product, matrix multiply, broadcasting add, softmax, argmax) using their PyTorch equivalents; verify identical results |
| 2 | Autograd Verification | Starter | Define `f(x, y) = x**2 * y + torch.sin(y)`; compute gradients with autograd; compare against your `numerical_derivative` from notebook 01 |
| 3 | Custom Training Loop | Synthesis | Train a 3-layer network on the moons dataset (`sklearn.datasets.make_moons`); implement early stopping when validation loss stops decreasing; plot train/val loss curves |
| 4 | Build `nn.Linear` from Scratch | Stretch | Implement a `MyLinear(nn.Module)` class using raw `nn.Parameter` for weight and bias; verify it produces the same output as `nn.Linear` with the same initial weights |

### Key References
- [PyTorch Official Tutorials — Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html) — the official gentle introduction to tensors, autograd, and `nn.Module`
- [Karpathy — The spelled-out intro to neural networks and backpropagation (micrograd)](https://www.youtube.com/watch?v=VMj-3S1tku0) — builds autograd from scratch, which this notebook then maps to PyTorch's autograd
- [PyTorch documentation — torch.Tensor](https://pytorch.org/docs/stable/tensors.html) — complete reference for tensor operations and attributes
- [PyTorch documentation — Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html) — explains the computation graph, gradient accumulation, and `no_grad`
- [Andrej Karpathy — makemore Part 2 (MLP)](https://www.youtube.com/watch?v=TCH_1BHY58I) — uses all the PyTorch patterns covered in this notebook
- [Deep Learning with PyTorch: A 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html) — fast-paced official tutorial covering tensors through training

---

## 05. Neural Network Building Blocks

**File:** `05_neural_network_building_blocks.ipynb`

### Overview
This notebook teaches you the components that make up modern neural networks — the layers, activations, and normalization techniques that appear in every architecture from MLPs to transformers. You will implement each building block from scratch in PyTorch, understand why it exists, and then compose them into a working network. These are the Lego bricks of deep learning: Karpathy's lectures introduce them one at a time (MLP in lecture 3, BatchNorm in lecture 4, embeddings in lecture 2), but this notebook gives you a unified reference so you recognize each piece when you encounter it.

### Learning Objectives
By the end of this notebook, you will be able to:
- Implement linear layers, ReLU, Tanh, and GELU activations from scratch and explain their gradients
- Build an embedding layer that maps integer indices to dense vectors and explain why this is a learnable lookup table
- Implement BatchNorm and LayerNorm from scratch, explain what statistics they normalize over, and describe when to use each
- Build a residual connection and explain how it solves the vanishing gradient problem
- Implement dropout and explain why it acts as regularization during training but is disabled at inference
- Compose these blocks into a multi-layer network and verify it trains correctly

### Prerequisites
- [`01_calculus_for_deep_learning.ipynb`](01_calculus_for_deep_learning.ipynb) — gradients and the chain rule (for understanding activation gradients and vanishing gradients)
- [`02_linear_algebra_essentials.ipynb`](02_linear_algebra_essentials.ipynb) — matrix multiplication and the linear layer
- [`03_probability_and_statistics.ipynb`](03_probability_and_statistics.ipynb) — mean, variance, normalization
- [`04_pytorch_fundamentals.ipynb`](04_pytorch_fundamentals.ipynb) — tensors, autograd, `nn.Module`, training loop

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | Linear Layers Revisited | Implement `MyLinear` with `nn.Parameter`; show `y = x @ W.T + b`; visualize weight matrices as heatmaps; trace gradients through a linear layer |
| 2 | Activation Functions | Implement ReLU, Tanh, Sigmoid, and GELU from their formulas; plot each function and its derivative; discuss dead ReLU neurons and why GELU is preferred in transformers |
| 3 | Embedding Layers | Implement `MyEmbedding` as a weight matrix indexed by integers; show equivalence to one-hot encoding followed by linear layer; embed a toy vocabulary and visualize with PCA |
| 4 | Batch Normalization | Implement `MyBatchNorm1d`: compute per-feature mean/variance over the batch, normalize, apply learnable `gamma` and `beta`; track running statistics for eval mode; plot activation distributions before and after |
| 5 | Layer Normalization | Implement `MyLayerNorm`: normalize over the feature dimension (not the batch); compare against BatchNorm; explain why LayerNorm is standard in transformers (works with variable sequence lengths) |
| 6 | Residual Connections | Implement `y = F(x) + x`; show how gradients flow through the skip connection; demonstrate that a 20-layer network with residuals trains while one without does not |
| 7 | Dropout | Implement `MyDropout`: randomly zero out activations during training, scale by `1/(1-p)`; show that dropout is identity at eval time; measure its regularization effect on a small overfitting experiment |
| 8 | Composing Blocks into a Network | Stack Linear → LayerNorm → GELU → Dropout into a reusable `Block` class; build a 4-block network; train on a classification task and inspect intermediate activations |

### Putting It Together
You will build a character-level language model backbone (without the training loop — that is notebook 06). The model takes a sequence of character indices, passes them through an embedding layer, two residual blocks (each containing Linear → LayerNorm → GELU → Dropout), and a final linear projection to vocabulary-sized logits. You will verify shapes at every stage, inspect the activation distributions after each normalization layer, and confirm that gradients flow healthily through all 6+ layers.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Activation Function Zoo | Starter | Implement Swish (`x * sigmoid(x)`) and Leaky ReLU; plot all activations on a single figure; compute and plot their derivatives |
| 2 | BatchNorm vs. LayerNorm | Starter | Apply both to the same tensor of shape `(batch=32, features=64)`; print which dimensions each normalizes over; verify the output means and variances |
| 3 | Residual Network Depth Test | Synthesis | Train a plain 10-layer MLP and a 10-layer residual MLP on the same dataset; plot training loss curves to demonstrate the residual advantage; inspect gradient norms per layer |
| 4 | Build a Transformer Block | Stretch | Combine `MultiHeadAttention` (using `nn.MultiheadAttention`), LayerNorm, a feed-forward network (Linear → GELU → Linear), residual connections, and dropout into a single `TransformerBlock` class; verify it processes a `(batch, seq_len, d_model)` tensor correctly |

### Key References
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — see how embeddings, LayerNorm, residual connections, and feed-forward blocks compose into a transformer
- [Ioffe & Szegedy — Batch Normalization: Accelerating Deep Network Training (2015)](https://arxiv.org/abs/1502.03167) — the original BatchNorm paper; read at least the introduction and Section 3
- [Ba, Kiros & Hinton — Layer Normalization (2016)](https://arxiv.org/abs/1607.06450) — the LayerNorm paper; essential for understanding the transformer design choice
- [Kaiming He et al. — Deep Residual Learning (2015)](https://arxiv.org/abs/1512.03385) — the ResNet paper that introduced skip connections; read Section 1 and 3
- [Karpathy — Building makemore Part 3 (activations, gradients, BatchNorm)](https://www.youtube.com/watch?v=P6sfmUTpUmc) — directly covers BatchNorm and activation distribution analysis from this notebook
- [Karpathy — Building makemore Part 4 (becoming a backprop ninja)](https://www.youtube.com/watch?v=q8SA3rM6ckI) — manual backprop through every building block covered here
- [PyTorch documentation — nn.Module reference](https://pytorch.org/docs/stable/nn.html) — official docs for all the layers you implement from scratch

---

## 06. Training Deep Networks

**File:** `06_training_deep_networks.ipynb`

### Overview
This notebook teaches you how to actually train a neural network well — not just get it to run, but get it to learn effectively and generalize. You will implement SGD and Adam from scratch, experiment with learning rate schedules, set up proper train/validation/test splits, diagnose overfitting and underfitting, and apply weight initialization strategies. Training is where theory meets practice: a network with perfect architecture will fail with bad hyperparameters, and a mediocre architecture can succeed with good training discipline. Karpathy's "Recipe for Training Neural Networks" blog post is the guiding philosophy — this notebook makes it concrete with code.

### Learning Objectives
By the end of this notebook, you will be able to:
- Implement SGD (with momentum) and Adam optimizers from scratch and explain how momentum and adaptive learning rates accelerate convergence
- Set up train/validation/test splits and explain the role of each in preventing overfitting and measuring generalization
- Diagnose overfitting (train loss low, val loss high) and underfitting (both losses high) from loss curves and apply appropriate remedies
- Implement and compare learning rate schedules: step decay, cosine annealing, and linear warmup
- Apply weight initialization strategies (Xavier, Kaiming) and explain why initialization matters for gradient flow
- Execute Karpathy's training recipe: overfit one batch, then scale up, then regularize

### Prerequisites
- [`01_calculus_for_deep_learning.ipynb`](01_calculus_for_deep_learning.ipynb) — gradient descent foundations
- [`02_linear_algebra_essentials.ipynb`](02_linear_algebra_essentials.ipynb) — matrix operations in forward/backward passes
- [`03_probability_and_statistics.ipynb`](03_probability_and_statistics.ipynb) — cross-entropy loss, mean/variance
- [`04_pytorch_fundamentals.ipynb`](04_pytorch_fundamentals.ipynb) — PyTorch training loop, autograd, optimizers
- [`05_neural_network_building_blocks.ipynb`](05_neural_network_building_blocks.ipynb) — network components to train

### Section Breakdown
| # | Section Title | What You Build / Learn |
|---|---------------|----------------------|
| 1 | SGD from Scratch | Implement `MySGD` that updates `param -= lr * param.grad`; add momentum with a velocity buffer; train a network and compare convergence with and without momentum |
| 2 | Adam from Scratch | Implement `MyAdam` with first moment (mean), second moment (variance), and bias correction; compare convergence against your SGD on the same task; explain why Adam is the default |
| 3 | Train / Validation / Test Splits | Split a dataset three ways; train on train, evaluate on val after each epoch, hold out test for final evaluation; explain why touching test more than once invalidates your results |
| 4 | Overfitting and Underfitting | Train a large network on a small dataset to demonstrate overfitting; train a tiny network on a large dataset to show underfitting; plot train/val curves for both; catalog fixes (more data, dropout, weight decay, smaller model) |
| 5 | Learning Rate Schedules | Implement step decay, cosine annealing (`lr * 0.5 * (1 + cos(pi * t / T))`), and linear warmup; plot the LR over time for each; train with each schedule and compare loss curves |
| 6 | Weight Initialization | Initialize the same network with zeros, random normal, Xavier (`1/sqrt(fan_in)`), and Kaiming (`sqrt(2/fan_in)`) schemes; plot activation distributions after one forward pass for each; show that bad init kills gradient flow |
| 7 | Weight Decay and Gradient Clipping | Add L2 regularization via weight decay in the optimizer; implement gradient clipping with `torch.nn.utils.clip_grad_norm_`; show their effect on training stability and generalization |
| 8 | The Karpathy Training Recipe | Walk through the full recipe: (1) understand the data, (2) set up the evaluation, (3) overfit a single batch, (4) overfit the training set, (5) regularize, (6) tune hyperparameters; apply each step to a character-level language model |
| 9 | Hyperparameter Search | Implement random search over learning rate (log-uniform) and hidden size; train short runs; plot results; explain why random search beats grid search |
| 10 | Putting It All Together: Training a Character-Level LM | Combine the network from notebook 05 with the training techniques from this notebook; train on a text dataset; generate samples at different checkpoints to watch quality improve |

### Putting It Together
You will train the character-level language model backbone from notebook 05 on a real text corpus (e.g., Shakespeare's works or a subset of names). You will follow Karpathy's training recipe step by step: first verify you can overfit a single batch to near-zero loss, then scale to the full training set, then add dropout and weight decay to regularize. You will use cosine annealing with linear warmup, track train and validation loss, generate text samples every 500 steps, and produce a final plot showing loss curves and sample quality over time.

### Exercises
| # | Title | Difficulty | Description |
|---|-------|-----------|-------------|
| 1 | Optimizer Comparison | Starter | Train the same 2-layer network with SGD, SGD+momentum, and Adam on the spiral dataset; plot all three loss curves on one figure; note convergence speed differences |
| 2 | Learning Rate Finder | Starter | Implement the "LR range test": start with a tiny LR and increase exponentially each batch; plot loss vs. LR; identify the optimal learning rate as the steepest descent region |
| 3 | Diagnose and Fix | Synthesis | Given a pre-configured training run that overfits badly, apply 3 fixes (dropout, weight decay, data augmentation) and show the val loss improvement for each; write up which fix helped most and why |
| 4 | Mini Karpathy Challenge | Stretch | Train a character-level language model on a dataset of your choice (baby names, song lyrics, code); achieve a validation loss below a target threshold; generate 20 samples and evaluate quality subjectively |

### Key References
- [Karpathy — A Recipe for Training Neural Networks (blog post)](https://karpathy.github.io/2019/04/25/recipe/) — the single most practical guide to training networks; this notebook implements its advice
- [Fast.ai — Practical Deep Learning for Coders](https://course.fast.ai/) — Jeremy Howard's course emphasizes practical training skills; Lessons 1-5 cover topics from this notebook
- [Karpathy — Building makemore Part 3 (activations, gradients, BatchNorm)](https://www.youtube.com/watch?v=P6sfmUTpUmc) — covers initialization, activation statistics, and training diagnostics
- [Karpathy — Building makemore Part 5 (building a WaveNet)](https://www.youtube.com/watch?v=t3YJ5hKiMQ0) — advanced training and architecture patterns that build on this notebook
- [Kingma & Ba — Adam: A Method for Stochastic Optimization (2014)](https://arxiv.org/abs/1412.6980) — the Adam paper; read Section 2 for the algorithm
- [PyTorch documentation — torch.optim](https://pytorch.org/docs/stable/optim.html) — official reference for all optimizers and learning rate schedulers
- [Loshchilov & Hutter — Decoupled Weight Decay Regularization (AdamW, 2017)](https://arxiv.org/abs/1711.05101) — explains why AdamW is preferred over Adam with L2 regularization
- [Smith — Cyclical Learning Rates for Training Neural Networks (2017)](https://arxiv.org/abs/1506.01186) — introduces the LR range test implemented in Exercise 2
