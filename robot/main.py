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
        motors.Trenchdigger.set_TD_speed(0)

    # emergency stop
    elif cmd == 'DIE':
        motors.DriveTrain.stop()
        sys.exit(1)

    # switch to autonomous mode
    elif cmd == 'AI':
        motors.DriveTrain.tank_drive(0, 0)
        conn.send("MSG: TODO: autonomous")
        print('auto command received')

    # read trench digger encoder
    elif cmd == 'ENC':
        motors.Trenchdigger.get_encoder()

    # activate hopper servo
    elif cmd == 'SER':
        motors.Trenchdigger.servo(90)

    # read potentiometer
    elif cmd == 'POT':
        motors.Trenchdigger.get_pot();

    #start trench digger
    elif cmd == 'DIG':
        motors.Trenchdigger.set_TD_speed(0.75)
        print('trench digger active')

    else:
        motors.DriveTrain.tank_drive(0,0)
        conn.send("WARN: invalid command")
        print('invalid command: ', msg)

# begin accepting connections
t = tether.accept_connections(receive_msg)
t.join()
