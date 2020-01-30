import motors
import tether

import sys

def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, args = msg.split(':')

    # arcade drive
    if cmd == 'AD':
        throttle, turn = map(int, args.split(','))
        motors.DriveTrain.arcade_drive(throttle, turn)

    # tank drive
    elif cmd == 'TD':
        left, right = map(int, args.split(','))
        motors.DriveTrain.tank_drive(left, right)

    # stop all movement
    elif cmd == 'STOP':
        motors.DriveTrain.stop()

    # emergency stop
    elif cmd == 'DIE':
        motors.DriveTrain.stop()
        sys.exit(1)

    # switch to autonomous mode
    elif cmd == 'AI':
        motors.DriveTrain.tank_drive(0, 0)
        conn.send("MSG: TODO: autonomous")
        print('auto command received')

    else:
        motors.DriveTrain.tank_drive(0,0)
        conn.send("WARN: invalid command")
        print('invalid command: ', msg)

# begin accepting connections
t = tether.accept_connections(receive_msg)
t.join()
