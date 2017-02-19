import numpy as np
from keras.models import Sequential
from keras.layers import BatchNormalization, Convolution1D, Dropout, Flatten, Dense, Convolution2D
from preprocess import read_data

#Loading the data
filename = "driving_log.csv"

#Y_train is the angle of the camera
X_train, y_train = read_data(filename, pre_process=True, flip=True, dropSmallValuesWithRate=50)

#My model
model = Sequential()

print("The shape of the model is: " + str(X_train[0].shape))


def train_model(X_train, y_train):
    if len(X_train[0].shape) == 2:
        print("Using two dimensional network")
        model.add(BatchNormalization(input_shape=(X_train[0].shape[0], X_train[0].shape[1])))
        model.add(Convolution1D(5, 5))
        model.add(Convolution1D(5, 5))
        model.add(Convolution1D(3, 3))
        model.add(Convolution1D(3, 3))
    else:
        print("Using three dimensional network")
        model.add(Convolution2D(24, 5, 5, subsample=(2, 2), activation='relu',
                                input_shape=(X_train[0].shape[0], X_train[0].shape[1], X_train[0].shape[2])))
        model.add(Convolution2D(36, 5, 5, subsample=(2, 2), activation='relu'))
        model.add(Convolution2D(48, 5, 5, subsample=(2, 2), activation='relu'))
        model.add(Convolution2D(64, 3, 3, activation='relu'))

    model.add(Flatten())
    model.add(Dropout(0.25))
    model.add(Dense(100))
    model.add(Dense(50))
    model.add(Dense(10))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.summary()
    model.load_weights("model_with_color.h5")

    # Training
    model.fit(np.array(X_train), y_train, nb_epoch=13, validation_split=0.2, shuffle=True)

    model.save("model_with_color.h5")

train_model(X_train, y_train)