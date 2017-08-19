
20th August 2017

## Data

As of today, we have two datasets that are not small.

- turn_right - 7831 images on right turn only
- first_big_dataset - 15353 images on full track

We are driving on white.

should make git repo on these 2 to avoid data loss.


## Model
We are using variation of Nvidia-proposed architecture.

    Conv2D(24, (5, 5), strides=(2, 2), padding='valid')
    ELU()

    Conv2D(36, (5, 5), strides=(2, 2), padding='valid')
    ELU()

    Conv2D(48, (5, 5), strides=(2, 2), padding='valid')
    ELU()

    Conv2D(64, (3, 3), strides=(1, 1), padding='valid')
    ELU()

    Conv2D(64, (3, 3), strides=(1, 1), padding='same')
    ELU()

    Conv2D(64, (3, 3), strides=(1, 1), padding='same')
    model.add(ELU())

    Conv2D(64, (3, 3), strides=(1, 1), padding='same')
    model.add(ELU())

    Flatten()

    Dense(100)
    ELU()

    Dense(50)
    ELU()

    Dense(10)
    ELU()
    Dropout(0.5)

    Dense(3, activation='softmax')


Task: classification
loss: categorical cross entropy
optimizer: Adam
Infra/lib: keras



## Ideas, work in progress

Prepared data viewer. If needed, can try to minimize conflicting inputs
by hand.

Need to add richer model save name handling to minimize risk of
overwriting good results with new runs.



## Experiments

Right turn only, 100 epochs,
We are using regularization: random flip, random translation up to 10 pix.

Val acc stabilies at around 85% which is record so far.
Can even be theoretical maximum (when we gather data, we sometimes give
different steering for same inputs.)

Killed optimization after 63rd epoch.

Max acc history
epoch acc
0 65
2 80
4 82
8 84
20 84
36 85


Output file called third.json

Checking OOS by hand...

Shows reasonable traces of working :)
Needs more through testing in real world, but batteries are down.

In particular spots on real right turn, turns wheels to the right.

Next thing to do: Test more, next perhaps work on dataset augmentation.


