# KUKA CYBERTECH Mock Hardware

A MoveIt Pro mock configuration for a KUKA CYBERTECH robot.

This config is for running Moveit Pro with ROS2 control mock hardware.

For detailed documentation see: [MoveIt Pro Documentation](https://docs.picknik.ai/)

## Build

- `colcon build --packages-up-to cybertech_mock --packages-ignore kuka_gazebo`
