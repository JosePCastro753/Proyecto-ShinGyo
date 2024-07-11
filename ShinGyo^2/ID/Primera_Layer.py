"""
Proyecto Shin DMS^2
@author: Jose Pablo Castro
"""

#Instalar paquetes necesarios
#https://www.tensorflow.org/install/pip#windows-native
#https://stackoverflow.com/questions/60542475/confirm-that-tf2-is-using-my-gpu-when-training

#tensorflow-gpu 2.10 for CUDA aceleration
#Python 3.10
#CuDNN 8.1
#CUDA 11.2

#guias baicas de layers
#https://www.tensorflow.org/tutorials/quickstart/beginner
#https://www.tensorflow.org/tutorials/quickstart/advanced
#https://www.tensorflow.org/tutorials/customization/custom_layers

# In the tf.keras.layers package, layers are objects. To construct a layer,
# simply construct the object. Most layers take as a first argument the number
# of output dimensions / channels.
#layer = tf.keras.layers.Dense(100)
# The number of input dimensions is often unnecessary, as it can be inferred
# the first time the layer is used, but it can be provided if you want to
# specify it manually, which is useful in some complex models.
#layer = tf.keras.layers.Dense(10, input_shape=(None, 5))

#Documentacion de layers de keras
#https://www.tensorflow.org/api_docs/python/tf/keras/layers
#https://keras.io/api/layers/





import tensorflow as tf

#Loggea la deteccion y uso de la gpu para entrenamiento y carga de pesos [True para mostrar]
tf.debugging.set_log_device_placement(False)

l1 = tf.keras.layers.Dense(10)
l1(tf.zeros([10, 5]))
print(l1.variables)

class example(tf.keras.layers.Layer):
    def __init__ (self, num_outputs):
        super(example, self).__init__()
        self.num_outputs = num_outputs
    
    def build(self, input_shape):
        self.kernel = self.add_weight("kernel",
                                        shape=[int(input_shape[-1]),
                                        self.num_outputs])
    
    def call(self, inputs):
        return tf.matmul(inputs, self.kernel)

l2 = example(10)
_ = l2(tf.zeros([10, 5]))
print([var.name for var in l2.trainable_variables])

