import ftprci as fci

# Create an instance of the LSM6 sensor
sensor = fci.LSM6()

# Create an instance of the PIDController


th = fci.RunnerThread()

th.callback | sensor.read

th.run()
