# Vision Code Documentation

## Library Description
The code in `vision.py` provides classes and namespaces for utilizing hardware for robot vision. Anything that is used to gain information
on the environment around the robot will be a part of this library

## Classes
The following are the classes defined in `vision.py`.

### SpacehawksHokuyoLXWrapper
In `vision.py`, the `SpacehawksHokuyoLXWrapper` class is defined. This is a low level wrapper 
of the HokuyoLX class with functionalities that are both (A) shared by the two subclasses and (B)
interacting with the lower level `HokuyoLX` library to encapsulate functions and limit knowledge needed
to work on this file to just the Spacehawks code and not the `HokuyoLX`. __I do not recommend using this in
other parts of the project other than to serve as superclass to `SpacehawksHokuyoLXDetecter` and `SpacehawksHokuyoLXLocater`.__

#### Constructors
##### `SpacehawksHokuyoLXLocater()`
Initializes connection to the sensor at its default configuration.

#### Methods
##### `get_dists()`
Gives a two-dimensional Python list. Each internal value is an ordered pair, with each index holding values as follows:
* 0 - *the value of the sensor's rotational value at this datapoint*
* 1 - *the value of the distance this datapoint's beam reached before reflecting back*

##### `get_intens`
Gives a two-dimensional Python list. Each internal value is an ordered triple, with each index holding values as follows:
* 0 - *the value of the sensor's rotational value at this datapoint*
* 1 - *the value of the distance this datapoint's beam reached before reflecting back*
* 2 - *the arbitrary value of the intensity of the reflected beam as produced by the HokuyoLX's internal hardware*

### SpacehawksHokuyoLXDetecter
The `SpacehawksHokuyoLXLocater` class defines an object with the functionalities desired of the front-facing diagonal LIDAR used for detecting
obstacles in the robot's path. It derives from `SpacehawksHokuyoLXWrapper`. 

#### Constructors
##### `SpacehawksHokuyoLXDetecter()`
Initializes connection to the sensor at its default configuration and ?????????????

#### Constants

#### Functions
##### `get_danger_coords()`
Gives a two-dimensional Python list. Each internal value is an ordered pair of the  

### SpacehawksHokuyoLXLocater
The `SpacehawksHokuyoLXLocater` class defines an object with functionalities needed for the back-facing horizontally mounted LIDAR used
for tracking the reflective target to track robot location. It inherits from `SpacehawksHokuyoLXWrapper`.

#### Constructors
##### `SpacehawksHokuyoLXLocater()`
Initiates connection to the sensor and sets default coordinate to (0.0, 0.0) @ 0.0 rad.

#### Constants

#### Functions
