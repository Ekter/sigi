import ftprci as fci

# Create an instance of the LSM6 sensor
sensor = fci.LSM6(0x6B)

estimator = fci.ComplementaryFilter()

pid = fci.PIDController(10, 0, 3, fci.DiscreteIntegral.Tustin())

actuators = fci.PololuAstar()

th = fci.RunnerThread(frequency=100)

th.callback | sensor.read | estimator.estimate | pid.steer | actuators.command

while True:
    pid.set_order(0.1)
    fci.sleep(0.5)
    pid.set_order(-0.1)
    fci.sleep(0.5)
