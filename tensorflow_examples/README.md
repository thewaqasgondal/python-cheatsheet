# TensorFlow Examples

This directory contains TensorFlow examples and tutorials.

## Files

### tf.py
Basic TensorFlow setup and verification script.

**Features:**
- TensorFlow version check
- Basic tensor operations
- Simple arithmetic operations
- Environment verification

**Usage:**
```bash
python tf.py
```

## Getting Started with TensorFlow

### Installation:
```bash
# CPU version
pip install tensorflow

# GPU version (requires CUDA)
pip install tensorflow-gpu
```

### Basic Concepts:

**Tensors**
Multi-dimensional arrays that represent data in TensorFlow.

**Operations**
Mathematical operations on tensors (addition, multiplication, etc.)

**Graphs**
Computational graphs that define the flow of operations.

## Common TensorFlow Tasks

### 1. Basic Operations
```python
import tensorflow as tf

a = tf.constant(2)
b = tf.constant(3)
result = a + b
```

### 2. Creating Tensors
```python
# Scalar
scalar = tf.constant(42)

# Vector
vector = tf.constant([1, 2, 3, 4])

# Matrix
matrix = tf.constant([[1, 2], [3, 4]])

# Tensor
tensor = tf.constant([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
```

### 3. Variables
```python
# Mutable tensors for model parameters
var = tf.Variable([1.0, 2.0, 3.0])
var.assign([4.0, 5.0, 6.0])
```

## Machine Learning with TensorFlow

### Building a Simple Model:
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

## GPU Support

Check GPU availability:
```python
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
```

## Resources

- [TensorFlow Official Documentation](https://www.tensorflow.org/)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Keras Guide](https://www.tensorflow.org/guide/keras)
- [TensorFlow Hub](https://www.tensorflow.org/hub)

## Best Practices

1. **Use Keras API** for high-level model building
2. **Batch your data** for efficient training
3. **Use GPU** when available for faster computation
4. **Monitor training** with TensorBoard
5. **Save models** regularly during training
6. **Validate** on separate test data

## Common Use Cases

- Image Classification
- Object Detection
- Natural Language Processing
- Time Series Forecasting
- Recommendation Systems
- Generative Models
