# Modules

## Connect the pin

- A pin module can only have 3-6 pins
- Only two correct pin have to be connected together
- Pin ordering goes from left -> right, top -> bottom

### Colors

- yellow
- red 
- blue
- purple 
- cyan

### 3 pin

- If there are no red pins connect second and third pin
- Otherwise, if the last pin is cyan connect first and third pin
- Otherwise, if there is more than one blue pin, connect first blue pin and last blue pin
- Otherwise, connect first and second pin

### 4 pin 
- If there is more than one red wire and the last digit of the serial number is odd, connect first pin and last red pin. 
- Otherwise, if the last pin is yellow and there are no red pins, connect second pin and last pin
- Otherwise, if there is exactly one blue pin, connect second pin and third pin
- Otherwise, if there is more than one yellow pin, connect third pin and last pin
- Otherwise, connect first pin and third pin

### 5 pin
- If the last pin is purple and the last digit of the serial number is odd, connect the third and fourth pin
- Otherwise, if there is exactly one red pin and there is more than one yellow pin, connect first pin and second pin
- Otherwise, if there are no purple pins, connect second pin and fifth pin
- Otherwise, connect fourth pin and fifth pin

### 6 pin 
- If there are no yellow pin and the last digit of the serial number is odd, connect third pin and sixth pin
- Otherwise, if there is exactly one yellow pin and there is more than one cyan pin, connect fourth pin and sixth pin
- Otherwise, if there are no red wires, connect first pin and second pin
- Otherwise, connect second pin and fifth pin
