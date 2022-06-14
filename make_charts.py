
import ast

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from get_bms_data import get_values
import traceback

avg_cell_voltages = []
_avg_cell_temperatures = []
_soc_ = []
pack_voltages = []
pack_currents = []
pack_powers = []
avg_ambient_temperatures = []

def update_data(i):
    data = get_values()

    print("Raw Data: ", data)
    
    avg_cell_temperatures = data[3]
    soc = data[2]
    pack_voltage = data[1]
    pack_current = data[0]

    try:

        if avg_cell_temperatures != []:
            ax1.cla()
            ax1.set_title("Pack Temperature (Average)")
            ax1.set_xlabel("Time(sec)")
            ax1.set_ylabel("Avg Temperture (deg C)")
            ax1.set_ylim([-20, 80])
            
            _avg_cell_temperatures.append(avg_cell_temperatures[-1])
            ax1.plot(_avg_cell_temperatures)
            ax1.scatter(len(_avg_cell_temperatures)-1, _avg_cell_temperatures[-1])
            ax1.text(len(_avg_cell_temperatures)-1, _avg_cell_temperatures[-1]+2, "{} C".format(_avg_cell_temperatures[-1]))

        if soc != []:
            ax2.cla()
            ax2.set_title("Pack SoC")
            ax2.set_xlabel("Time (sec)")
            ax2.set_ylabel("SoC (%)")
            ax2.set_ylim([0, 100])
            
            _soc_.append(soc[-1])
            print("SoC: ", soc)
            ax2.plot(_soc_)
            ax2.scatter(len(_soc_)-1, _soc_[-1])
            ax2.text(len(_soc_)-1, _soc_[-1]+2, "{}%".format(_soc_[-1]))

        if pack_voltage != []:
            ax4.cla()
            ax4.set_title("Pack Voltage")
            ax4.set_xlabel("Time(sec)")
            ax4.set_ylabel("Battery Voltage (V)")
            ax4.set_ylim([48,96])
            
            pack_voltages.append(pack_voltage[-1])
            print("Pack V: ", pack_voltage)
            ax4.plot(pack_voltages)
            ax4.scatter(len(pack_voltages)-1, pack_voltages[-1])
            ax4.text(len(pack_voltages)-1, pack_voltages[-1]+2, "{} V".format(pack_voltages[-1]))

        if pack_current != []:
            ax5.cla()
            ax5.set_title("Pack Current")
            ax5.set_xlabel("Time(sec)")
            ax5.set_ylabel("Battery Current (Amp)")
            ax5.set_ylim([-250, 250])
            
            print("Pack Current", pack_current, " ")
            
            if isinstance(pack_current[0], float) and pack_current[0] < 100:
                pack_currents.append(pack_current[0])
                ax5.plot(pack_currents)
                print(1)
                ax5.scatter(len(pack_currents)-1, pack_currents[-1])
                ax5.text(len(pack_currents)-1, pack_currents[-1]+2, "{} A".format(pack_currents[-1]))
            else:
                ax5.plot(pack_currents)
                print(2)
                ax5.scatter(len(pack_currents)-1, pack_currents[-1])
                ax5.text(len(pack_currents)-1, pack_currents[-1]+2, "{} A".format(pack_currents[-1])) 

        
    except Exception as exc:
        traceback.print_tb(exc)
        print(exc)


fig = plt.figure(figsize=(5, 5), facecolor="#DEDEDE")

ax1 = plt.subplot(2, 2, 1)
# ax1.set_facecolor("black")
ax1.set_title("Pack Temp(Avg)")
ax1.set_xlabel("Time(sec)")
ax1.set_ylabel("Pack Temp(Avg)")
ax1.set_ylim([-1, 5000])

ax2 = plt.subplot(2, 2, 2)
# ax2.set_facecolor("black")
ax2.set_title("Pack SoC")
ax2.set_xlabel("Time(sec)")
ax2.set_ylabel("Pack SoC")
ax2.set_ylim([-1, 20])

ax4 = plt.subplot(2, 2, 3)
# ax4.set_facecolor("black")
ax4.set_title("Pack Voltage")
ax4.set_xlabel("Time(sec)")
ax4.set_ylabel("Pack Voltage")
ax4.set_ylim([-1000, 180])

ax5 = plt.subplot(2, 2, 4)
# ax5.set_facecolor("black")
ax5.set_title("Pack Current")
ax5.set_xlabel("Time(sec)")
ax5.set_ylabel("Pack Current")
ax5.set_ylim([-10000000, 18000])


ani = FuncAnimation(fig, update_data, interval=20 )
#ani.save('abc.png')
#ani.show()
plt.tight_layout()
plt.subplots_adjust(top=0.9, bottom= 0.1)
plt.show()
# plt.savefig('abc.png')
