
import can
import time
from testing_module import write_to_can, connect_to_can


for i in range(5000):
    CAN_INPUT_ID = 0x238
    INPUT_MSG = [0xB8, 0x0B, 0x14, 0x01, 0x00, 0x00, 0x00, 0x00]

    can_msg = can.Message(
            arbitration_id=CAN_INPUT_ID,
            data=INPUT_MSG,
            is_extended_id=False,
        )

    can_bus = connect_to_can()
    print(INPUT_MSG)
    write_to_can(can_bus, can_msg)
    print(2)
    time.sleep(4)