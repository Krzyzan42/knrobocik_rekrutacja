from select import select
import termios
import tty
import rclpy
import sys
import os
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

    

class PlayerController(Node):
    def __init__(self):
        super().__init__('player_controller')
        
        print('----------------------------------------------')
        print('Waiting for service')
        self.start_recording_srv = self.create_client(Trigger, 'start_recording')
        self.stop_recording_srv = self.create_client(Trigger, 'stop_recording')

        self.publisher_ = self.create_publisher(String, 'key_press', 10)
        self.timer = self.create_timer(0.16, self.readInput) 
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

        self.message = ''
        self.redraw_screen()

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        return ch
        
    def readInput(self):
        key = self.getKey()
        if key is not None and key != '':
            msg = String()
            msg.data = key
            self.publisher_.publish(msg)

        if key == 'q':
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            exit()
        if key == 'r':
            self.start_recording()
        if key == 't':
            self.end_recording()

        self.timer.cancel() # Prevent event queue from piling up
        self.timer = self.create_timer(0.16, self.readInput)

    def start_recording(self):
        if not self.start_recording_srv.wait_for_service(1.0):
            self.message = 'Failed to start recording: service not found'
            self.redraw_screen()
            return
        
        self.future = self.start_recording_srv.call_async(Trigger.Request())
        self.future.add_done_callback(self.handle_start_recording_response)

    def end_recording(self):
        if not self.stop_recording_srv.wait_for_service(1.0):
            self.message = 'Failed to end recording: service not found'
            self.redraw_screen()
            return
        
        self.future = self.stop_recording_srv.call_async(Trigger.Request())
        self.future.add_done_callback(self.handle_stop_recording_response)
    
    def handle_start_recording_response(self, future):
        try:
            response = future.result()
            self.message = str(response.success) + ": " + response.message
        except Exception as e:
            self.message = "Failed to start recording"
        self.redraw_screen()
        
    def handle_stop_recording_response(self, future):
        try:
            response = future.result()
            self.message = str(response.success) + ": " + response.message
        except Exception as e:
            self.message = "Failed to end recording"
        self.redraw_screen()

    def redraw_screen(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        os.system('clear')
        msg = '----------------------------------------------\n'
        msg += 'Reading from the keyboard\n'
        msg += 'WASD to move, Q to quit, R to start recording, T to terminate recording\n'
        msg += self.message +'\n'
        msg += '----------------------------------------------\n'
        print(msg)
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)


def main(args = None):
    rclpy.init(args=args)

    player_controller = PlayerController()

    rclpy.spin(player_controller)

    player_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()