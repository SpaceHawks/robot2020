import motors
import tether


def receive_msg(msg, conn):
    # format is operator:arguments
    cmd, args = msg.split(':')
    if cmd == 'AD':
        throttle, turn = args.split(',')
        motors.arcade_drive(throttle, turn)
    elif cmd == 'TD':
        left, right = args.split(',')
        motors.tank_drive(left, right)
    elif cmd == 'STOP':
        motors.tank_drive(0,0)
    elif cmd == 'AI':
        motors.tank_drive(0,0)
        conn.send("MSG: TODO: autonomous")
        print('auto command received')
    else:
        motors.tank_drive(0,0)
        conn.send("WARN: invalid command")
        print('invalid command: ', msg)

tether.accept_connections(receive_msg)
