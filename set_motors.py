from a_star import AStar
import time


# Instance of AStar
a_star = AStar()

def set_motors(left, right):
    a_star.motors(left, right)

if __name__ == '__main__':
    try:
        set_motors(100, 100)
        time.sleep(5) 
        set_motors(0, 0)
        time.sleep(1)
        set_motors(-100, -100)
        time.sleep(5) 
        set_motors(0, 0)
    except KeyboardInterrupt:
        print("Stopped by user")
