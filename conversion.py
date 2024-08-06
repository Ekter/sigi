
def getPhysicalAccelerometer(x, y, z):
    conversionFactor = 9.80665/16384

    x = x*conversionFactor
    y = y*conversionFactor
    z = z*conversionFactor
    return x,y,z

def getPhysicalGyrometer(x, y, z):
    conversionFactor = 35/1000

    x = x*conversionFactor
    y = y*conversionFactor
    z = z*conversionFactor
    return x,y,z

def getPhysicalYaw(encoder_r,encoder_l):
    R = 0.040 #m
    W = 0.100 #m
    yaw = R/W(encoder_r,encoder_l)
    return yaw

def getPhysicalTravel(encoder_r,encoder_l):
    R = 0.040 #m
    x_l = R*encoder_r
    x_r = R*encoder_l
    x = (x_l+x_r)/2
    return x

def getPhysicalSpeed(encoder_r_dot,encoder_l_dot):
    R = 0.040 #m
    x_l_dot = R*encoder_r_dot
    x_r_dot = R*encoder_l_dot
    x_dot = (x_l_dot+x_r_dot)/2
    return x_dot
