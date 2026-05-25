import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro

def generate_launch_description():

    # Lấy giá trị tham số xem có sử dụng thời gian mô phỏng hay không
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Đường dẫn đến file robot.urdf.xacro
    pkg_path = os.path.join(get_package_share_directory('xetuhanh1'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    
    # Chuyển đổi file xacro thành định dạng xml để robot_state_publisher có thể hiểu
    robot_description_config = xacro.process_file(xacro_file).toxml()
    
    # Thiết lập tham số cho node robot_state_publisher
    params = {
        'robot_description': robot_description_config,  
        'use_sim_time': use_sim_time
    }
    
    # Tạo node robot_state_publisher (node này giúp công bố trạng thái các khớp của robot)
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Node này sẽ tạo ra các khớp giả lập để RSP có thể tính toán TF
    node_joint_state_publisher = Node(
        package='joint_state_publisher_gui', # Dùng bản GUI để bạn có thể vặn khớp
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )

    # Trả về danh sách các tác vụ cần chạy khi launch
    return LaunchDescription([
        # Khai báo đối số (argument) có thể truyền vào khi chạy lệnh ros2 launch
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Sử dụng thời gian mô phỏng nếu là true'),

        # Thêm node vào tiến trình khởi chạy
        node_robot_state_publisher
    ])