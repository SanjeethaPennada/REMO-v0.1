import tensorflow as tf
x = tf.constant(3.0)
b = 1.0
with tf.GradientTape() as tape:
        tape.watch(x)
        y = x ** 2
b = tape.gradient(y, x)
print(type(b))