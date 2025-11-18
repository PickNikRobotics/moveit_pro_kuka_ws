# KUKA CYBERTECH Hardware

A MoveIt Pro mock configuration for a real KUKA CYBERTECH robot.

This config is for running Moveit Pro with real hardware.

For detailed documentation see: [MoveIt Pro Documentation](https://docs.picknik.ai/)

## Build

- `colcon build --packages-up-to cybertech_hw --packages-ignore kuka_gazebo`

## Run

Launch MoveIt Pro as usual, then execute the following commands to enable control of the robot:

- `ros2 lifecycle set robot_manager configure`
- `ros2 lifecycle set robot_manager activate`
