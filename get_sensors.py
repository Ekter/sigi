import time
import math
from IMU import LSM6
from a_star import AStar
from conversion import getPhysicalAccelerometer, getPhysicalGyrometer

# Gear ratios as provided
gearratio_motor = 86955 / 2912
gearratio_gearbox = 41 / 25

# Ticks per revolution of the wheel
ticks_per_wheel_revolution = 12 * gearratio_motor * gearratio_gearbox # Theoretical value
#ticks_per_wheel_revolution = 576 # Empirical value

# Initial previous values
previous_left_encoder = 0
previous_right_encoder = 0
previous_time = time.time()

# Instance of AStar and IMU
a_star = AStar()
imu = LSM6()

def get_accelerometer():
    imu.enable()

    imu.read()

    #print(f"Pre Conversion: ax={imu.a.z}, ay={imu.a.y}, az={-imu.a.x}")

    ax, ay, az = getPhysicalAccelerometer(imu.a.x, imu.a.y, imu.a.z)
    #print(f"Post Conversion: ax={az}, ay={ay}, az={-ax}")
    return az, ay, -ax # Flipped to compensate for gimbal lock

def get_gyrometer():
    imu = LSM6()
    imu.enable()

    imu.read()

    #print("Pre Conversion: gx=", imu.g.z, "gy=", imu.g.y, "gz=", -imu.g.x)
    gx, gy, gz = getPhysicalGyrometer(imu.g.x, imu.g.y, imu.g.z)
    #print("Post Conversion: gx=", int(gz), "gy=", int(gy), "gz=", int(-gx))
    return gz, gy, -gx # Flipped to compensate for gimbal lock


def get_encoders():
    global previous_left_encoder, previous_right_encoder, previous_time

    encoders = a_star.read_encoders()
    current_time = time.time()
    # print("Pre: Left=", encoders[0], "Right", encoders[1])
    # Convert encoder ticks to wheel angles
    leftWheelAngle = (encoders[0] * 2 * math.pi) / ticks_per_wheel_revolution
    rightWheelAngle = (encoders[1] * 2 * math.pi) / ticks_per_wheel_revolution
    #leftWheelAngle = encoders[0]
    #rightWheelAngle = encoders[1]
    #print("Post               : Left=", leftWheelAngle, "Right", rightWheelAngle)

    # Calculate time difference
    dt = current_time - previous_time

    if dt > 0:
        # Calculate the derivatives
        dLeft = ((encoders[0] - previous_left_encoder) * 2 * math.pi) / (ticks_per_wheel_revolution * dt)
        dRight = ((encoders[1] - previous_right_encoder) * 2 * math.pi) / (ticks_per_wheel_revolution * dt)
    else:
        dLeft = 0
        dRight = 0

    # Update previous values
    previous_left_encoder = encoders[0]
    previous_right_encoder = encoders[1]
    previous_time = current_time

    #print(f"Left Angle={leftWheelAngle}, Right Angle={rightWheelAngle}, dLeft={dLeft}, dRight={dRight}")
    return leftWheelAngle, rightWheelAngle, dLeft, dRight, dt


if __name__ == "__main__":
    import numpy as np
    def directions(right: float, left: float)-> str:
        # import math
        vec_right = right*np.array([0, 1]) + np.array([5, 0])
        vec_left = left*np.array([0, 1]) + np.array([-5, 0])
        vec = (vec_right * abs(right) + vec_left * abs(left))*np.array([1, -1])
        res = [["  " for _ in range(11)] for _ in range(11)]
        for co in np.linspace(np.array([0,0]), vec, 10):
            co = co/20+np.array([5, 5])
            x = round(min(10, max(0, co[1])))
            y = round(min(10, max(0, co[0])))
            res[x][y] = "██"
        res[x][y] = "❯❮"

        return "█ █"+"▀"*24+"█\n"+"\n".join(["█ █ "+"".join(line)+" █" for line in res])+"\n█ █"+"▄"*24+"█"

    def check_acc(*xyz, __previous=[]):
        norm = np.linalg.norm(np.array(xyz))
        __previous.append(norm)
        if len(__previous)>=5:
            __previous.pop(0)
        mean = sum(__previous)/len(__previous)
        if mean*0.8>norm or mean*1.25<norm:
            print("Warning! acc norm changed")

    while True:
        # time.sleep(0.1)
        print("█"*110 +"\n█")
        t1 = time.time()
        a = get_encoders()
        t2 = time.time()
        b = get_accelerometer()
        t3 = time.time()
        c = get_gyrometer()
        t4 = time.time()

        b = [round(bi, 4) for bi in b]
        check_acc(*b)
        c = [round(ci, 4) for ci in c]
        print(directions(a[2], a[3]))

        print(f"█   left: {a[0]},   right: {a[1]},   dt: {a[4]}\n█     ▶ time encoder: {t2-t1}\n█   acc:{b}\n█     ▶ time acc: {t3-t2}\n█   gyro:{c}\n█     ▶ time gyro: {t4-t3}\n█")
