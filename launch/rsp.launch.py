import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro

def generate_launch_description():

    # Lấy giá trị tham số xem có sử dụng thời gian mô phỏng hay không
    su_dung_thoi_gian_mo_phong = LaunchConfiguration('use_sim_time')

    # Đường dẫn đến file robot.urdf.xacro
    duong_dan_goi_goi_goi = os.path.join(get_package_share_directory('xetuhanh1'))
    tep_xacro = os.path.join(duong_dan_goi_goi_goi, 'description', 'robot.urdf.xacro')
    
    # Chuyển đổi file xacro thành định dạng xml để robot_state_publisher có thể hiểu
    cau_hinh_mo_ta_robot = xacro.process_file(tep_xacro).toxml()
    
    # Thiết lập tham số cho node robot_state_publisher
    tham_so = {
        'robot_description': cau_hinh_mo_ta_robot,  
        'use_sim_time': su_dung_thoi_gian_mo_phong
    }
    
    # Tạo node robot_state_publisher (node này giúp công bố trạng thái các khớp của robot)
    node_cong_bo_trang_thai_robot = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[tham_so]
    )

    # Node này sẽ tạo ra các khớp giả lập để RSP có thể tính toán TF
    node_cong_bo_trang_thai_khop = Node(
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
        node_cong_bo_trang_thai_robot
    ])