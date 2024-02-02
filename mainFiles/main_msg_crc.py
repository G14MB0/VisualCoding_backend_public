from app.routers.pythonBus import utils
import cantools
import can


DBC = cantools.database.load_file("D:\\users\\s005859\\Downloads\\520MY24_C1-CAN_E(2A)_R1_plusCR18658.dbc")
# Find the message in the DBC file
message = DBC.get_message_by_frame_id(257)

# Create a dictionary to hold signal values
signal_values = {}
# Assign arbitrary values to the signals
for signal in message.signals:
    # You might want to check signal.size or other properties to determine a valid value
    # For simplicity, we're assigning an arbitrary value of 1 or True, depending on the signal type
    value = 0
    # if signal.is_multiplexer:
    #     value = 0  # Typically multiplexer signals are set to a specific case, here it's set to 0
    # # elif signal.choices:
    # #     value = next(iter(signal.choices))  # Choose an arbitrary value from defined choices
    # else:
    #     value = 0 if signal.length > 1 else True  # Assign a simple number or boolean
    
    signal_values[signal.name] = value
signal_values["ABSActive"] = 1

print(signal_values)
# Encode the signal values into a data byte array
data = message.encode(signal_values)


new_can_message = can.Message(arbitration_id=257, data=data, is_extended_id=False)
new_can_message_with_crc = can.Message(arbitration_id=257, data=utils.calculateNewCrc(new_can_message), is_extended_id=False)
print(data)
print(utils.calculateNewCrc(new_can_message))
print(new_can_message)
print(new_can_message_with_crc)