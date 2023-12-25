from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Port, Stop
from pybricks.tools import wait

# CONSTANTS
SPEED_ACCELERATE = 5
SPEED_DECELERATE = 2
SPEED_STEERING   = 500

hub = TechnicHub()
hub.light.on(Color.ORANGE)

motor_steering = Motor(Port.D)
motor_front    = Motor(Port.B)
motor_rear     = Motor(Port.A)

remote_control = Remote()

# steering calibration sequence
def calibrate_steering(hub):
    hub.light.on(Color.YELLOW)
    motor_steering.run_until_stalled(+500)
    steering_angle_max = motor_steering.angle()
    motor_steering.run_until_stalled(-500)
    steering_angle_min = motor_steering.angle()
    steering_angle_neutral = (steering_angle_max + steering_angle_min) / 2
    motor_steering.run_target(SPEED_STEERING, steering_angle_neutral)
    return steering_angle_neutral, steering_angle_max, steering_angle_min

steering_angle_neutral, steering_angle_max, steering_angle_min = calibrate_steering(hub)
speed = 0

while True:
    hub.light.on(Color.GREEN)
    buttons = remote_control.buttons.pressed()

    # Acceleration:
    if Button.LEFT in buttons:
        speed = 0
    elif Button.LEFT_PLUS in buttons:
        speed = min(100, speed + SPEED_ACCELERATE)
    elif Button.LEFT_MINUS in buttons:
        speed = max(-100, speed - SPEED_ACCELERATE)
    elif speed > 0:
        speed = max(0, speed - SPEED_DECELERATE)
    else:
        speed = min(0, speed + SPEED_DECELERATE)
    motor_front.dc(speed)
    motor_rear.dc(speed)

    if Button.RIGHT in buttons:
        # re-calibrate
        steering_angle_neutral, steering_angle_max, steering_angle_min = calibrate_steering(hub)
    elif Button.RIGHT_PLUS in buttons:
        motor_steering.run_target(SPEED_STEERING, steering_angle_max, then=Stop.HOLD, wait=False)
    elif Button.RIGHT_MINUS in buttons:
        motor_steering.run_target(SPEED_STEERING, steering_angle_min, then=Stop.HOLD, wait=False)
    else:
        motor_steering.run_target(SPEED_STEERING, steering_angle_neutral, Stop.HOLD, False)

    # Turn off using green Remote Control button:
    if Button.CENTER in buttons:
        hub.light.on(Color.RED)
        hub.system.shutdown()

    wait(20)
