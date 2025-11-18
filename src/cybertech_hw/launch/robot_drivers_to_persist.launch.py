# Copyright 2025 PickNik Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the PickNik Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, LifecycleNode
from moveit_studio_utils_py.system_config import SystemConfigParser


def generate_launch_description():
    # Get MoveIt Pro system configuration
    system_config_parser = SystemConfigParser()
    hardware_config = system_config_parser.get_hardware_config()
    robot_description = system_config_parser.get_processed_urdf()

    # Extract and parse URDF parameters from MoveIt Pro config
    urdf_params = hardware_config.robot_description.urdf_params

    # Parse urdf_params into a dictionary (matches MoveIt Pro's parsing logic)
    urdf_params_dict = {}
    for param in urdf_params:
        if isinstance(param, dict):
            urdf_params_dict.update(param)
        elif isinstance(param, str) and ": " in param:
            key, value = param.split(": ", 1)
            urdf_params_dict[key] = value

    # Extract configuration values from MoveIt Pro config
    # driver_version = urdf_params_dict.get("driver_version", "rsi_only")
    robot_model = urdf_params_dict.get("robot_model", "kr16_r2010_2")
    use_gpio = urdf_params_dict.get("use_gpio", "false").lower() == "true"

    # Load controller configuration
    # TODO: RSI-only for now; extend to EKI+RSI later via driver_version
    controller_config = (
        get_package_share_directory("cybertech_hw")
        + "/config/control/ros2_control.yaml"
    )

    # Load driver-specific configuration
    driver_config = (
        get_package_share_directory("kuka_rsi_driver") + "/config/driver_config.yaml"
    )

    # The control node (Kuka's controller manager)
    # This will automatically read robot_description from the parameter server
    control_node = Node(
        namespace="",
        package="kuka_drivers_core",
        executable="control_node",
        parameters=[
            controller_config,
            {
                "robot_description": robot_description,
                "hardware_components_initial_state": {"unconfigured": [robot_model]},
            },
        ],
        output="both",
    )

    # The robot manager node (Kuka-specific driver)
    robot_manager_node = LifecycleNode(
        namespace="",
        name="robot_manager",
        package="kuka_rsi_driver",
        executable="robot_manager_node_rsi_only",
        parameters=[
            driver_config,
            {
                "robot_model": robot_model,
                "use_gpio": use_gpio,
            },
        ],
        output="both",
    )

    nodes_to_start = [
        control_node,
        robot_manager_node,
    ]

    return LaunchDescription(nodes_to_start)
