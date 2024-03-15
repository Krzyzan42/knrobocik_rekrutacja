from typing import List
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

class Board(Node):
    width = 30
    height = 15
    recording = False
    obstacles = []

    def __init__(self):
        super().__init__('board')
        self.setup_obstacles()
        self.subscription = self.create_subscription(
            String,
            'key_press',
            self.key_press_callback, 
            10
        )
        self.start_recording_srv = self.create_service(Trigger, 'start_recording', self.start_recording)
        self.stop_recording_srv = self.create_service(Trigger, 'stop_recording', self.stop_recording)

        self.x = self.width // 2
        self.y = self.height // 2

        self.print_board()

    def setup_obstacles(self):
        self.declare_parameter('xs', value=[0])
        self.declare_parameter('ys', value=[0])
        self.declare_parameter('width', value=30)
        self.declare_parameter('height', value=15)
        self.declare_parameter('health', value=15)

        ys = self.get_parameter('ys').get_parameter_value().integer_array_value
        xs = self.get_parameter('xs').get_parameter_value().integer_array_value
        self.width = self.get_parameter('width').get_parameter_value().integer_value
        self.height = self.get_parameter('height').get_parameter_value().integer_value
        self.health = self.get_parameter('health').get_parameter_value().integer_value

        self.obstacles = []
        for i in range(len(ys)):
            self.obstacles.append((xs[i], ys[i]))

    def print_board(self):
        
        print('\n'*30)

        for y in range(self.height):
            row_str = ''
            for x in range(self.width):
                row_str += self.get_board_character(x, y)
            print(row_str)
        if self.health > 0:
            print(f'Health: {self.health}')
        else:
            print('You lost')

    def get_board_character(self, x, y):
        if self.x == x and self.y == y:
            return 'O'
        elif (x, y) in self.obstacles:
            return 'X'
        else:
            return '.'


    def key_press_callback(self, key):
        if self.health <= 0:
            return
        key = key.data
        if key == 'w':
            self.y -= 1
        elif key == 's':
            self.y += 1
        elif key == 'a':
            self.x -= 1
        elif key == 'd':
            self.x += 1
        self.x = self.x % self.width
        self.y = self.y % self.height
        if (self.x, self.y) in self.obstacles:
            self.obstacles.remove((self.x, self.y))
            self.health -= 1

        self.print_board()

        if self.recording:
            print('recording')
            self.record_move()

    def start_recording(self, request, response):
        if self.recording:
            response.success = False
            response.message = 'Already recording'
            return response

        try:
            with open('movement.log', 'w') as f:
                f.write('LOG START--------------\n')
            self.recording = True
            response.success = True
            response.message = 'Started recording movement'
            return response
        except Exception:
            response.success = False
            response.message = 'Failed to create log file'
            return response
        
    def record_move(self):
        with open('movement.log', 'a') as f:
            f.write(f'[{self.x}, {self.y}]\n')

    def stop_recording(self, request, response):
        if self.recording is not True:
            response.success = False
            response.message = 'Nothing to stop'
            return response

        self.recording = False
        response.success = True
        response.message = 'Stopped recording'
        return response

def main(args = None):
    rclpy.init(args=args)

    board = Board()
    
    rclpy.spin(board)

    board.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    