import tensorflow as tf

# Print TensorFlow version
print("TensorFlow version:", tf.__version__)

# Test a simple operation to check if TensorFlow is working
a = tf.constant(2)
b = tf.constant(3)
result = a + b
print("Result of a + b:", result.numpy())  # Convert the result to a NumPy array for printing
