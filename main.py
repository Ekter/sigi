import ftprci as fci

# Create an instance of the LSM6 sensor
sensor = fci.LSM6(0x6B)

estimator = fci.ComplementaryFilter()

pid = fci.PIDController(10, 0, 3, fci.DiscreteIntegral.Tustin())

motors = fci.PololuAstar()

th = fci.RunnerThread()

th.callback | sensor.read | estimator.estimate | pid.steer | motors.command

th.run()
