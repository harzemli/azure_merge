This folder contains two Python scripts.

1. internal_communications_manager.py
This is the internal communications manager which handles communication between the Pi and Godot. Furthermore it will perform or at least delegate any processes or calculations that cannot or should not be performed on the Raspberry Pi (e.g. any AI training or velocity calculation).

2. udp_client.py
This script mocks an object detection script that is run on the Raspberry Pi and sends coordinates and other data through to the internal communications manager.

The communication is done via UDP. The internal communications manager acts as the server while the Pi and Godot act as clients.

To run it, perform the following steps:
1. Run internal_communications_manager.py
2. Press play in Godot
3. Run udp_client.py