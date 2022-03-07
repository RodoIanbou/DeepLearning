# -*- coding: utf-8 -*-
"""TP_MLP_MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JQ_XGXQCjLEbGQAnjxdM_YIfVjyMnqKL
"""

# Commented out IPython magic to ensure Python compatibility.

#Après avoir tester le réseau proposé sur le github de SebAmb, qui avait une accuracy de 0.90 au bout de 200 entraînements 
#avec les paramètres de l'apprentissage proposés, j'ai essayé en rajoutant une couche intermédiaire au réseau,  
#ce qui a permis d'augmenter l'accuracy a 0.92 après une centaine d'entraînement, au coût d'une augmentation du coup d'entraînement.


# %tensorflow_version 1.x
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plot
import cv2
from google.colab.patches import cv2_imshow

#On importe les datasets depuis les serveurs google.
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
mnist_train_images=mnist.train.images
mnist_train_labels=mnist.train.labels
mnist_test_images=mnist.test.images
mnist_test_labels=mnist.test.labels

#On défini les placeholders où seront placés les images d'entrée les prédictions du réseau.
ph_images=tf.placeholder(shape=(None, 784), dtype=tf.float32)
ph_labels=tf.placeholder(shape=(None, 10), dtype=tf.float32)

#Définition des paramètres de l'apprentissage
nbr_n0=784 #Pour la première couche du réseau
nbr_nint=100 #Pour la deuxième couche intermédiaire
learning_rate=0.0001
taille_batch=100
nbr_entrainement=130

#Première couche
wc0=tf.Variable(tf.truncated_normal(shape=(784, nbr_n0)), dtype=tf.float32)
bc0=tf.Variable(np.zeros(shape=int(nbr_n0)), dtype=tf.float32)
sc0=tf.matmul(ph_images, wc0)+bc0
sc0=tf.nn.sigmoid(sc0)

#Deuxième couche intermédiaire
wcint=tf.Variable(tf.truncated_normal(shape=(784, nbr_nint)), dtype=tf.float32)
bcint=tf.Variable(np.zeros(shape=int(nbr_nint)), dtype=tf.float32)
scint=tf.matmul(sc0, wcint)+bcint 
scint=tf.nn.sigmoid(scint)

#Couche de sortie
wcs=tf.Variable(tf.truncated_normal(shape=(nbr_n0, 10)), dtype=tf.float32)
bcs=tf.Variable(np.zeros(shape=(784)), dtype=tf.float32)
scs=tf.matmul(sc0, wcs)+bcs
scso=tf.nn.softmax(scs)


loss=tf.nn.softmax_cross_entropy_with_logits_v2(labels=ph_labels, logits=scs) #Definition de la fonction de perte à optimiser
train=tf.train.GradientDescentOptimizer(learning_rate).minimize(loss) #On utilise GradientDescentOptimizer comme méthode d'optimisation
accuracy=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(scso, 1), tf.argmax(ph_labels, 1)), dtype=tf.float32)) 


#Entraînement
with tf.Session() as s:
    
    # Initialisation des variables
    s.run(tf.global_variables_initializer())

    tab_acc_train=[]
    tab_acc_test=[]
    
    for id_entrainement in range(nbr_entrainement):
        print("ID entrainement", id_entrainement)
        for batch in range(0, len(mnist_train_images), taille_batch):
            # lancement de l'apprentissage en passant la commande "train". feed_dict est l'option désignant ce qui est
            # placé dans les placeholders
            s.run(train, feed_dict={
                ph_images: mnist_train_images[batch:batch+taille_batch],
                ph_labels: mnist_train_labels[batch:batch+taille_batch]
            })

        # Prédiction du modèle sur les batchs du dataset de training
        tab_acc=[]
        for batch in range(0, len(mnist_train_images),taille_batch):
            # lancement de la prédiction en passant la commande "accuracy". feed_dict est l'option désignant ce qui est
            # placé dans les placeholders
            acc=s.run(accuracy, feed_dict={
                ph_images: mnist_train_images[batch:batch+taille_batch],
                ph_labels: mnist_train_labels[batch:batch+taille_batch]
            })
            # création le tableau des accuracies
            tab_acc.append(acc)
        
        # calcul de la moyenne des accuracies 
        print("accuracy train:", np.mean(tab_acc))
        tab_acc_train.append(1-np.mean(tab_acc))
        
        # Prédiction du modèle sur les batchs du dataset de test
        tab_acc=[]
        for batch in range(0, len(mnist_test_images), taille_batch):
            acc=s.run(accuracy, feed_dict={
                ph_images: mnist_test_images[batch:batch+taille_batch],
                ph_labels: mnist_test_labels[batch:batch+taille_batch]
            })
            tab_acc.append(acc)
        print("accuracy test :", np.mean(tab_acc))
        tab_acc_test.append(1-np.mean(tab_acc))   
        resulat=s.run(scso, feed_dict={ph_images: mnist_test_images[0:taille_batch]})


#Affichage de la courbe d'erreur au cours de l'entraînement.
plot.ylim(0, 1)
plot.grid()
plot.plot(tab_acc_train, label="Train error")
plot.plot(tab_acc_test, label="Test error")
plot.legend(loc="upper right")
plot.show()

"""Voici la courbe de train error et test error au cours des entrainements avec la couche intermédiaire. On remarque une stabilisation autour d'une accuracy de environ 0.92 au bout de une centaine d'entrainements.


![courbeMLP2.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXQAAAD8CAYAAABn919SAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nO3de3hddZ3v8fd3X3O/9U5SoLSlUEppaSy9qLQgWuTWUVEQEEWnw8wgnhEHUI8O4+h5ZEZFUdSDM0zRg1xEgToiItLITegFsLSlpSktNC2lbZLmnuxLfuePtZMmadKkaZKVvft5Pc9+1n3luxfls9b67bV/25xziIhI+gv4XYCIiAwNBbqISIZQoIuIZAgFuohIhlCgi4hkCAW6iEiG6DfQzeweM9tnZhv7WG5mdqeZVZrZBjM7e+jLFBGR/gzkCn0lsOwIyy8EpqdeK4CfHHtZIiJytPoNdOfcM0DNEVa5DPi587wIFJnZpKEqUEREBiY0BPsoBXZ1ma5KzXun54pmtgLvKp7s7Ox5kydPHtQfbG9vJxBIz+b/dK4d0rt+1e4P1T603njjjQPOuXG9LRuKQB8w59zdwN0A5eXlbt26dYPaT0VFBUuWLBnCykZOOtcO6V2/aveHah9aZvZWX8uG4tSzG+h6qV2WmiciIiNoKAJ9FfCp1NMuC4A659xhzS0iIjK8+m1yMbP7gSXAWDOrAv4FCAM4534KPA58GKgEmoHPDFexIiLSt34D3Tl3ZT/LHfCPQ1aRiKSVeDxOVVUVra2tvS4vLCzk9ddfH+GqhoaftWdlZVFWVkY4HB7wNiP6oaiIZJ6qqiry8/M5+eSTMbPDljc0NJCfn+9DZcfOr9qdc1RXV1NVVcWUKVMGvN3oeh5HRNJOa2srY8aM6TXMZXDMjDFjxvR519MXBbqIHDOF+dAbzDFVoIuIZAgFuoikterqaubMmcOcOXOYOHEipaWlndOxWOyI265bt44bb7xxhCodfvpQVETS2pgxY3j11VcBuO2228jLy+NLX/pS5/JEIkEo1HvUlZeXU15ePuQ1JZNJgsFgn9MD3e5o6QpdRDLOpz/9aa6//nrOOeccbr75ZtasWcPChQuZO3cuixYtYuvWrYD31f6LL74Y8E4G1113HUuWLOGUU07hzjvv7HXfTz75JAsXLuTss8/m8ssvp7GxEYCTTz6ZW265hbPPPptf/epXh03ff//9nHnmmcyaNYtbbrmlc395eXncdNNNnHXWWfzlL385pvetK3QRGTL/+ttNbN5T323esV51zjyhgH+55Iyj3q6qqooXXniBYDBIfX09zz77LKFQiKeeeoqvfOUr/PrXvz5smy1btrB69WoaGhqYMWMGV199dbflBw4c4Jvf/CZPPfUUubm53H777Xzve9/j61//OuDdLbz88ssA3HrrrZ3Te/bsYcGCBaxfv57i4mI++MEP8uijj7J8+XKampo455xz+O53vzuIo9OdAl1EMtLll1/eeSKpq6vj2muvZdu2bZgZ8Xi8120uuugiotEo0WiU8ePHs2/fPkpKSjqXv/jii2zevJnFixcDEIvFWLhwYefyT3ziE9321zG9du1alixZwrhxXieJV111Fc888wzLly8nGAzy0Y9+dEjeswJdRIZMb1fSfn05Jzc3t3P8a1/7GkuXLuWRRx5h586dffagGI1GO8eDwSCJRKLbcuccF1xwAffff3+/f7O36d5kZWUd0x1MV2pDF5GMV1dXR2lpKQArV64c9H4WLFjA888/T2VlJQBNTU288cYb/W43f/58/vznP3PgwAGSyST3338/55577qDr6IsCXUQy3s0338yXv/xl5s6de9hV99EYN24cK1eu5Morr2T27NksXLiQLVu29LvdpEmT+Pa3v83SpUs566yzmDdvHpdddtmg6+iTc86X17x589xgrV69etDb+i2da3cuvetX7cNj8+bNR1xeX18/QpUMPb9r7+3YAutcH7mqK3QRkQyhQBcRyRAKdBGRDKFAFxHJEAp0EZEMoUAXEckQ+qaoiKS16upqzj//fAD27t1LMBjs/Ir9mjVriEQiR9y+oqKCSCTCokWLhr3W4aZAF5G01l/3uf2pqKggLy9v0IHes3veI3XXe6TthoKaXEQk46xfv55zzz2XefPm8aEPfYh33nkHgDvvvJOZM2cye/ZsrrjiCnbu3MlPf/pT7rjjDubMmcOzzz7bbT9NTU1cd911zJ8/n7lz5/LYY48BXvcBl156Keeddx7nn3/+YdM1NTUsX76c2bNns2DBAjZs2AB4J5xrrrmGxYsXc8011wz5+9YVuogMnd/fCntf6zYrO5mA4DFEzcQz4cJvD3h15xyf//zneeyxxxg3bhwPPvggX/3qV7nnnnv49re/zY4dO4hGoxw8eJCioiKuv/76Pq/qv/Od73Deeedxzz33cPDgQebPn88HPvABAF5++WU2bNhASUkJK1eu7Db9+c9/nrlz5/Loo4/y9NNP86lPfarzLmLz5s0899xzZGdnD/6Y9EGBLiIZpa2tjY0bN3LBBRcAXn/skyZNAmD27NlcddVVLF++nOXLl/e7r6effponnniC73znOwC0trby9ttvA3DBBRd061q36/Rzzz3X2d/6eeedR3V1NfX1Xj/xl1566bCEOSjQRWQo9XIl3TLC3ec65zjjjDN6/fWf3/3udzzzzDP89re/5Vvf+havvfZaL3vovq9f//rXzJgxo9v8l156aVBd5R7NeoOhNnQRySjRaJT9+/d3Bno8HmfTpk20t7eza9culi5dyu23305dXR2NjY3k5+fT0NDQ677OP/98fvjDH+L1iQWvvPLKgGp43/vex3333Qd4H7qOHTuWgoKCIXh3R6ZAF5GMEggEePjhh7nllls466yzmDNnDi+88ALJZJKrr76aM888k7lz53LjjTdSVFTEJZdcwiOPPNLrh6I333wz8Xic2bNnc8YZZ/C1r31tQDXcdtttrF+/ntmzZ3Prrbdy7733DsdbPVxf3TAO90vd56andK5ftQ8PdZ87fNR9rojIcUqBLiKSIRToInLMXOpDQxk6gzmmCnQROSZZWVlUV1cr1IeQc47q6mqysrKOajs9hy4ix6SsrIyqqir279/f6/LW1tajDqbRws/as7KyKCsrO6ptFOgickzC4TBTpkzpc3lFRQVz584dwYqGTrrVriYXEZEMMaBAN7NlZrbVzCrN7NZelp9oZqvN7BUz22BmHx76UkVE5Ej6DXQzCwJ3ARcCM4ErzWxmj9X+N/CQc24ucAXw46EuVEREjmwgV+jzgUrn3JvOuRjwAHBZj3Uc0NFRQSGwZ+hKFBGRgbD+HjUys48By5xzn0tNXwOc45y7ocs6k4AngWIgF/iAc259L/taAawAmDBhwrwHHnhgUEU3NjaSl5c3qG39ls61Q3rXr9r9odqH1tKlS9c758p7XdhXnwAdL+BjwH92mb4G+FGPdb4I3JQaXwhsBgJH2q/6cklP6Vy/aveHah9aHGNfLruByV2my1Lzuvos8FDqBPEXIAsYO4B9i4jIEBlIoK8FppvZFDOL4H3ouarH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)
"""