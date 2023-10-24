import serial
import datetime
import getpass

# Get the current Windows user
current_user = getpass.getuser()
if current_user == '320027279':
    current_user = 'Afshin Ashrafy'
else:
    current_user = getpass.getuser()
# Define the serial port and baud rate
ser = serial.Serial('COM4', 19200)

# Define a list of tuples where each tuple contains a command and its expected response for C5 ParameterRange_MaxValues
commands = [(bytes([0x84, 0x04, 0x01, 0x06, 0x52, 0x1F]), bytes([0x84, 0x04, 0x01, 0x06, 0x52, 0x1F])),
            (bytes([0x84, 0x06, 0x0B, 0x4F, 0x02, 0x00, 0x00, 0x1A]), bytes([0x84, 0x06, 0x0B, 0x4F, 0x02, 0x00, 0x00, 0x1A])),
            (bytes([0x84, 0x04, 0x04, 0x03, 0x74, 0x7D]), bytes([0x84, 0x04, 0x04, 0x03, 0x74, 0x7D])),
            (bytes([0x84, 0x03, 0x09, 0x01, 0x6F]), bytes([0x84, 0x03, 0x09, 0x01, 0x6F])),
            (bytes([0x88, 0x05, 0x55, 0x1E, 0x07, 0x7F, 0x7A]), bytes([0x88, 0x04, 0x1E, 0x07, 0x7F, 0x50])),
            (bytes([0x88, 0x05, 0x55, 0x1F, 0x07, 0x7F, 0x79]), bytes([0x88, 0x04, 0x1F, 0x07, 0x7F, 0x4F])),
            (bytes([0x88, 0x05, 0x55, 0x20, 0x07, 0x7F, 0x78]), bytes([0x88, 0x04, 0x20, 0x07, 0x7F, 0x4E]))]

# Initialize an empty list to store responses
responses = []

# Get the current date and time
current_datetime = datetime.datetime.now()

# Create a fixed output file name
output_file_name = 'Param_MaxLimitCommands_Results.txt'

# Record the start time
start_time = datetime.datetime.now()

# Open the output file for writing
with open(output_file_name, 'w') as file:
    # Adding header to text file
    file.write(f"{'*' * 50} Executed by: {current_user} {'*' * 76}\n")
    # Add the date and time of the run in the middle of the file
    file.write(f"{'*' * 50} Date and Time of Run: {current_datetime.strftime('%B %d, %Y %H:%M:%S')} {'*' * 51}\n\n")
    # Send commands and receive responses
    for cmd, expected_response in commands:
        ser.write(cmd)  # Send the command
        response = ser.read(len(expected_response))  # Read the expected number of bytes
        responses.append(response)

        # Verify responses using assert and write to the output file
        verification_message = (
            f"Verifying command {' '.join([f'{byte:02X}' for byte in cmd])}, "
            f"Received response {' '.join([f'{byte:02X}' for byte in response])} "
            f"against expected response {' '.join([f'{byte:02X}' for byte in expected_response])}")

        if response == expected_response:
            verification_message += " --> PASS" + "\n"
        else:
            verification_message += " --> FAIL" + "\n"
        file.write(verification_message + '\n')

# Record the end time
end_time = datetime.datetime.now()

# Calculate and write the time it took to run the code
execution_time = end_time - start_time
with open(output_file_name, 'a') as file:
    # Update the execution time in the header
    file.write(f"{'*' * 50} Execution Time: {execution_time} {'*' * 68}\n\n")

# Close the serial port
ser.close()
