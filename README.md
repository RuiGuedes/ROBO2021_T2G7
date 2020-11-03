# ROBO2021_T2G7

Project for the Intelligent Robotics (ROBO) class of the Master in Informatics and Computer Engineering (MIEIC) at the Faculty of Engineering of the University of Porto (FEUP). 

## Team Members 

Rui Jorge Leão Guedes
* Student Number: 201603854
* E-Mail: up201603854@fe.up.pt

João Fernando da Costa Meireles Barbosa
* Student Number: 201604156
* E-Mail: up201604156@fe.up.pt

César Alexandre da Costa Pinho <br>
* Student Number: 201604039
* E-Mail: up201604039@fe.up.pt 

## Getting Started

### Environment

* Ubuntu 20.04 LTS
* ROS: Noetic
* Python 3.9.0
* Gazebo 11.1.0

### Project Structure

```
../catkin_ws/src
    /ssr_description
        package.xml
        CMakeLists.txt
        / scripts
            control1.py
            control2.py
            control3.py
    /ssr_description
        package.xml
        CMakeLists.txt
        /urdf
            ssr.urdf
        /meshes
            mesh1.dae
            mesh2.dae
            ...
        /materials
        /cad
    /ssr_gazebo
        package.xml
        CMakeLists.txt
        /launch
            ssr.launch
        /worlds
            ssr.world
        /models
            world_object1.dae
            world_object2.stl
            world_object3.urdf
        /materials
        /plugins
```

### Setup

1. Install the packages
```bash
cd catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
```

2. Build the packages
```bash
cd catkin_ws 
catkin_make
```

### Running

```bash
cd catkin_ws 
devel/setup.bash
roslaunch srr_gazebo srr.launch
```