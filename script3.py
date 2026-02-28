from pymavlink import mavutil
import matplotlib.pyplot as plt

tlog_path = "2025-05-30 13-03-10.tlog"  # Change this to your log path

log = mavutil.mavlink_connection(tlog_path)

# Data containers
servo_times, s1, s2, s3, s4 = [], [], [], [], []
gyro_times, gx, gy, gz = [], [], [], []
acc_x, acc_y, acc_z = [], [], []

att_times, roll, pitch, yaw = [], [], [], []
vfr_times, altitudes, airspeeds = [], [], []
rc_times, rc1, rc2, rc3, rc4 = [], [], [], [], []
current_times, current_values = [], []
vibe_times, vibe_x, vibe_y, vibe_z = [], [], [], []
mode_times, modes = [], []

print("Collecting data...")

while True:
    msg = log.recv_match(type=[
        "SERVO_OUTPUT_RAW", "RAW_IMU", "SYS_STATUS", "RC_CHANNELS_RAW",
        "HEARTBEAT", "ATTITUDE", "VFR_HUD", "VIBRATION"
    ], blocking=False)

    if msg is None:
        break

    if hasattr(msg, "time_usec"):
        t = msg.time_usec / 1e6
    elif hasattr(msg, "time_boot_ms"):
        t = msg.time_boot_ms / 1000.0
    else:
        t = log.time_since('SYSTEM_BOOT')

    if msg.get_type() == "SERVO_OUTPUT_RAW":
        servo_times.append(t)
        s1.append(msg.servo1_raw)
        s2.append(msg.servo2_raw)
        s3.append(msg.servo3_raw)
        s4.append(msg.servo4_raw)

    elif msg.get_type() == "RAW_IMU":
        gyro_times.append(t)
        gx.append(msg.xgyro)
        gy.append(msg.ygyro)
        gz.append(msg.zgyro)
        acc_x.append(msg.xacc)
        acc_y.append(msg.yacc)
        acc_z.append(msg.zacc)

    elif msg.get_type() == "ATTITUDE":
        att_times.append(t)
        roll.append(msg.roll)
        pitch.append(msg.pitch)
        yaw.append(msg.yaw)

    elif msg.get_type() == "VFR_HUD":
        vfr_times.append(t)
        altitudes.append(msg.alt)
        airspeeds.append(msg.airspeed)

    elif msg.get_type() == "RC_CHANNELS_RAW":
        rc_times.append(t)
        rc1.append(msg.chan1_raw)
        rc2.append(msg.chan2_raw)
        rc3.append(msg.chan3_raw)
        rc4.append(msg.chan4_raw)

    elif msg.get_type() == "SYS_STATUS":
        current_times.append(t)
        current_values.append(msg.current_battery / 100.0)

    elif msg.get_type() == "VIBRATION":
        vibe_times.append(t)
        vibe_x.append(msg.vibration_x)
        vibe_y.append(msg.vibration_y)
        vibe_z.append(msg.vibration_z)

    elif msg.get_type() == "HEARTBEAT":
        mode_times.append(t)
        modes.append(msg.custom_mode)

# Plotting
plt.figure(figsize=(16, 22))

# 1. Motor PWM
plt.subplot(7, 1, 1)
plt.plot(servo_times, s1, label="Motor 1")
plt.plot(servo_times, s2, label="Motor 2")
plt.plot(servo_times, s3, label="Motor 3")
plt.plot(servo_times, s4, label="Motor 4")
plt.ylabel("PWM")
plt.title("Motor PWM Outputs")
plt.grid()
plt.legend()

# 2. Gyroscope Data
plt.subplot(7, 1, 2)
plt.plot(gyro_times, gx, label="Gyro X")
plt.plot(gyro_times, gy, label="Gyro Y")
plt.plot(gyro_times, gz, label="Gyro Z")
plt.ylabel("°/s")
plt.title("Gyroscope Readings")
plt.grid()
plt.legend()

# 3. Accelerometer Data
plt.subplot(7, 1, 3)
plt.plot(gyro_times, acc_x, label="Accel X")
plt.plot(gyro_times, acc_y, label="Accel Y")
plt.plot(gyro_times, acc_z, label="Accel Z")
plt.ylabel("m/s²")
plt.title("Accelerometer Readings")
plt.grid()
plt.legend()

# 4. Attitude (Roll, Pitch, Yaw)
plt.subplot(7, 1, 4)
plt.plot(att_times, roll, label="Roll")
plt.plot(att_times, pitch, label="Pitch")
plt.plot(att_times, yaw, label="Yaw")
plt.ylabel("Radians")
plt.title("Attitude (Roll, Pitch, Yaw)")
plt.grid()
plt.legend()

# 5. Vibration Levels
plt.subplot(7, 1, 5)
plt.plot(vibe_times, vibe_x, label="Vibe X")
plt.plot(vibe_times, vibe_y, label="Vibe Y")
plt.plot(vibe_times, vibe_z, label="Vibe Z")
plt.ylabel("Vibration (g)")
plt.title("Vibration Levels")
plt.grid()
plt.legend()

# 6. RC Input Channels
plt.subplot(7, 1, 6)
plt.plot(rc_times, rc1, label="RC1 (Roll)")
plt.plot(rc_times, rc2, label="RC2 (Pitch)")
plt.plot(rc_times, rc3, label="RC3 (Throttle)")
plt.plot(rc_times, rc4, label="RC4 (Yaw)")
plt.ylabel("PWM")
plt.title("RC Input Channels")
plt.grid()
plt.legend()

# 7. Flight Mode Changes
plt.subplot(7, 1, 7)
plt.step(mode_times, modes, where="post", label="Flight Mode (ID)")
plt.xlabel("Time (s)")
plt.ylabel("Mode ID")
plt.title("Flight Mode Transitions")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
