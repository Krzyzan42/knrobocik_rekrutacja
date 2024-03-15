# Recruitment task for KN Robocik
It's a simple game written in python and ROS2 (humble) made of a board and a controller. <br>

Board: <br>
![Screenshot from 2024-03-15 10-25-54](https://github.com/Krzyzan42/knrobocik_rekrutacja/assets/100627976/34248872-8d9b-4166-92e1-9e8b1c1eb509)


Controller: <br>
![Screenshot from 2024-03-15 10-26-06](https://github.com/Krzyzan42/knrobocik_rekrutacja/assets/100627976/89172b12-559d-480a-8270-9e8b66fa9da0)

You can move around and if you step on an 'X' tile, you lose health. If your health is 0, then you lose. You can also record your moves to a 'movement.log' file

## Description
Project consists of two nodes - Board and Controller.

Controller:
- Captures the keys and publishes them for the board to capture.
- If recording key is pressed ('R' or 'T'), controller tries to call a board recording service

Board:
- Contains game and recording logic
- Reads parameters from `game/src/params/standard.yaml`
- Subscribes to the 'key_press' topic, responds to events published there
- Has two services: 'start_recording' and 'stop_recording'. Records to a 'movement.log' file

## Running
Before running anything, you need to build and source ROS2 workspace. Remember to build and source in seperate terminals. You need to source ROS2 workspace in each terminal you want to run a node. <br>
Building: `colcon build` <br>
Sourcing: `source install/setup.sh`

In order to launch board, type in terminal: <br>
`ros2 run game board --ros-args --params-file src/game/params/standard.yaml`

You can also launch with default parameters: <br>
`ros2 run game board`

Then run controller in another terminal: <br>
`ros2 run game controller`

It should all work now.
