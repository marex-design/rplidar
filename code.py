from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt

PORT_NAME = '/dev/ttyUSB0'  
BAUDRATE = 115200  # pour RPLIDAR A1

lidar = RPLidar(PORT_NAME, baudrate=BAUDRATE)

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_title('Cartographie RPLIDAR A1')
ax.set_facecolor('black')

points_accum = []  # liste pour accumuler tous les points

sc = ax.scatter([], [], s=2, c='lime')  # taille et couleur des points

try:
    for scan in lidar.iter_scans(max_buf_meas=200):
        for (_, angle, distance) in scan:
            if distance > 0:
                rad = np.deg2rad(angle)
                x = distance * np.cos(rad)
                y = distance * np.sin(rad)
                points_accum.append([x, y])

        points_np = np.array(points_accum)
        sc.set_offsets(points_np)
        plt.draw()
        plt.pause(0.001)

except KeyboardInterrupt:
    print("Arrêt du scan...")

lidar.stop()
lidar.disconnect()
plt.ioff()
plt.show()

# Sauvegarder la carte
plt.figure(figsize=(6,6))
plt.scatter(points_np[:,0], points_np[:,1], s=2, c='black')
plt.axis('equal')
plt.savefig('carte_rplidar_A1.png')
print("Carte sauvegardée sous carte_rplidar_A1.png")