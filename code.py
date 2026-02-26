from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt

PORT_NAME = '/dev/ttyUSB0' 
lidar = RPLidar(PORT_NAME)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
sc = ax.scatter([], [])
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_title('Cartographie RPLIDAR')

points = []

try:
    for scan in lidar.iter_scans(max_buf_meas=200):
        points = []
        for (_, angle, distance) in scan:
            if distance > 0:
                rad = np.deg2rad(angle)
                x = distance * np.cos(rad)
                y = distance * np.sin(rad)
                points.append([x, y])

        points = np.array(points)
        sc.set_offsets(points)
        plt.draw()
        plt.pause(0.001)

except KeyboardInterrupt:
    print("Arrêt du scan...")

lidar.stop()
lidar.disconnect()
plt.ioff()
plt.show()