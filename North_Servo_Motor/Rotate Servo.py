from machine import Pin, PWM
import sys

# Servo setup (GPIO 7, adjust as needed)
servo = PWM(Pin(7))
servo.freq(50)  # Standard servo PWM frequency

# Servo control function (0° offset = stop, higher offset = faster rotation)
def set_servo_speed(offset):
    """Sets the servo speed based on heading offset."""
    if offset > 0:  # Turn clockwise
        duty = int(1500 + (offset / 180) * 500)  # Scale from 1500µs to 2000µs
    elif offset < 0:  # Turn counterclockwise
        duty = int(1500 - (abs(offset) / 180) * 500)  # Scale from 1500µs to 1000µs
    else:
        duty = 1500  # Stop at neutral

    # Limit duty cycle to servo range (1000µs to 2000µs in Pico PWM)
    duty = max(1000, min(2000, duty))
    servo.duty_u16(int(duty / 20000 * 65535))  # Scale to 16-bit

    print(f"Offset: {offset}° -> Servo PWM: {duty}µs")

# Main loop: Read user input and adjust servo
while True:
    try:
        user_input = input("Enter degree offset from north (e.g., -30, 15, 0): ")
        offset = float(user_input)  # Convert input to float
        set_servo_speed(offset)  # Adjust servo speed
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nStopping servo and exiting...")
        set_servo_speed(0)  # Stop the servo
        break
