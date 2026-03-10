screen_precision = 0
console_precision = 0
ai_vision_7_objects = []
ai_vision_7_index = 0
myVariable = 0
Object_picked = False
Signal_pickup = False
Signal_drop = False

def when_started1():
    global myVariable, my_event, Object_picked, Signal_pickup, Signal_drop, screen_precision, console_precision, ai_vision_7_objects, ai_vision_7_index
    # Task A
    Signal_drop = False
    Signal_pickup = False
    drivetrain.set_turn_velocity(50, PERCENT)
    drivetrain.drive(FORWARD)
    while True:
        ai_vision_7_objects = ai_vision_7.take_snapshot(AiVision.ALL_AIOBJS)
        if ai_vision_7_objects[ai_vision_7_index].id == ClassroomElements.BLUE_RING and distance_2.object_distance(MM) < 200:
            drivetrain.stop()
            brain.screen.print("Obstacle detected")
            drivetrain.turn_for(RIGHT, 45, DEGREES)
            drivetrain.drive(FORWARD)
        else:
            ai_vision_7_objects = ai_vision_7.take_snapshot(AiVision.ALL_AIOBJS)
            if ai_vision_7_objects[ai_vision_7_index].id == ClassroomElements.BLUE_BALL and distance_2.object_distance(MM) < 400:
                drivetrain.stop()
                drivetrain.drive_for(FORWARD, 600, MM)
                Signal_pickup = True
                while not Object_picked:
                    wait(5, MSEC)
                drivetrain.turn_for(RIGHT, 110, DEGREES)
                drivetrain.drive_for(FORWARD, 1000, MM)
                while not drivetrain.is_done():
                    wait(5, MSEC)
                Signal_drop = True
        wait(5, MSEC)

def when_started2():
    global myVariable, my_event, Object_picked, Signal_pickup, Signal_drop, screen_precision, console_precision, ai_vision_7_objects, ai_vision_7_index
    # Task B
    Object_picked = False
    brain.screen.clear_screen()
    brain.screen.print("Calibrating arm and claw motors")
    print("Start time of arm movement ", end="")
    ArmMotor.spin_for(REVERSE, 10, DEGREES)
    print("End time of arm movement ", end="")
    print("Start time of claw movement ", end="")
    ClawMotor.spin_for(REVERSE, 10, DEGREES)
    print("End time of claw movement", end="")
    while not Signal_pickup:
        wait(5, MSEC)
    ArmMotor.set_max_torque(50, PERCENT)
    if ArmMotor.position(DEGREES) > 180:
        ArmMotor.stop()
        brain.screen.print("Torque limit reached! stopping arm motor")
    brain.screen.print("Adjusting gear ratio for safer torque")
    brain.screen.clear_screen()
    brain.screen.print("Picking up")
    ClawMotor.set_stopping(HOLD)
    ClawMotor.spin_for(REVERSE, 40, DEGREES)
    while not ClawMotor.is_done():
        wait(5, MSEC)
    drivetrain.drive_for(FORWARD, 190, MM)
    while not drivetrain.is_done():
        wait(5, MSEC)
    ClawMotor.spin_for(FORWARD, 45, DEGREES)
    while not ClawMotor.is_done():
        wait(5, MSEC)
    ClawMotor.set_stopping(HOLD)
    ArmMotor.spin_for(FORWARD, 180, DEGREES)
    while not ArmMotor.is_done():
        wait(5, MSEC)
    while not Object_picked:
        if distance_2.object_distance(MM) < 80:
            Object_picked = True
        else:
            brain.screen.print("Pick-up failed.. retrying")
            ClawMotor.set_stopping(HOLD)
            ClawMotor.spin_for(REVERSE, 40, DEGREES)
            while not ClawMotor.is_done():
                wait(5, MSEC)
            drivetrain.drive_for(FORWARD, 30, MM)
            while not drivetrain.is_done():
                wait(5, MSEC)
            ClawMotor.spin_for(FORWARD, 45, DEGREES)
            while not ClawMotor.is_done():
                wait(5, MSEC)
            ClawMotor.set_stopping(HOLD)
            ArmMotor.spin_for(FORWARD, 180, DEGREES)
            while not ArmMotor.is_done():
                wait(5, MSEC)
        wait(5, MSEC)
    brain.screen.clear_screen()
    brain.screen.print("Object secured")
    while not Signal_drop:
        wait(5, MSEC)
    brain.screen.clear_screen()
    brain.screen.print("Dropping object")
    ArmMotor.spin_for(REVERSE, 180, DEGREES)
    while not ArmMotor.is_done():
        wait(5, MSEC)
    ClawMotor.spin_for(REVERSE, 45, DEGREES)
    while not ClawMotor.is_done():
        wait(5, MSEC)
    drivetrain.drive_for(REVERSE, 500, MM)
    brain.screen.clear_screen()
    if distance_2.object_distance(MM) < 80:
        brain.screen.print("Drop failed")
    else:
        brain.screen.print("Object dropped successfully")
    print(console_format(drivetrain.power()), end="")
    print(console_format(ClawMotor.efficiency(PERCENT)), end="")
    print(console_format(ArmMotor.efficiency(PERCENT)), end="")

ws2 = Thread( when_started2 )
when_started1()
