
from vex import *

# Robot Configuration 
brain = Brain()

# Sensors
distance_sensor = Distance(Ports.PORT5) 
inertial_sensor = Inertial(Ports.PORT6)

# Drivetrain
# Left Motor, Right Motor, Wheel Travel (mm), Track Width (mm), Wheelbase (mm), Units
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = SmartDrive(left_motor, right_motor, 319.19, 295, 40, MM, 1)

# Movement Functions 
def move_forward(distance_mm, speed_percent):
    drivetrain.set_drive_velocity(speed_percent, PERCENT)
    drivetrain.drive_for(FORWARD, distance_mm, MM)  

def turn_left(angle_degrees):
    drivetrain.set_turn_velocity(50, PERCENT)
    drivetrain.turn_for(LEFT, angle_degrees, DEGREES) 

def turn_right(angle_degrees):
    drivetrain.set_turn_velocity(50, PERCENT)
    drivetrain.turn_for(RIGHT, angle_degrees, DEGREES) 

def stop_motors():
    drivetrain.stop() 

def main():
    # --- Task A.1: SENSOR CALIBRATION ---
    brain.screen.clear_screen()
    brain.screen.print("Calibrating Gyro...")
    inertial_sensor.calibrate()
    
    while inertial_sensor.is_calibrating():
        wait(50, MSEC)
    
    brain.screen.clear_screen()
    brain.screen.print("Check Sensors (5s)")
    
    # Run a loop for 5 seconds to let you verify sensor readings 
    # We use a timer to break the loop so code proceeds to movement
    timer = 0
    while timer < 5000: # 5000 milliseconds = 5 seconds
        brain.screen.set_cursor(2, 1)
        
        # Display Distance
        dist = distance_sensor.object_distance(MM)
        brain.screen.print("Dist: " + str(dist) + " mm   ") # Spaces to clear old text
        
        brain.screen.new_line()
        
        # Display Heading
        heading = inertial_sensor.heading(DEGREES)
        brain.screen.print("Ang: " + str(heading) + " deg   ")
        
        # Increment timer
        wait(200, MSEC)
        timer = timer + 200

    # --- Task A.2 MOVEMENT TEST ---
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Starting Motion Test...")
    wait(1, SECONDS)

    # 1. Move Forward 500mm
    brain.screen.print("Moving Fwd...")
    move_forward(500, 50) # [cite: 31]
    wait(0.5, SECONDS)

    # 2. Turn Left 90 degrees
    brain.screen.print("Turning Left...")
    turn_left(90)
    wait(0.5, SECONDS)

    # 3. Turn Right 90 degrees
    brain.screen.print("Turning Right...")
    turn_right(90)
    wait(0.5, SECONDS)

    # 4. Stop
    stop_motors()
    brain.screen.print("Test Complete.")

# Run the program
main()