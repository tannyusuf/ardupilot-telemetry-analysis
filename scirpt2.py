from pymavlink import mavutil
import matplotlib.pyplot as plt

tlog_path = "2025-05-30 14-55-59.tlog"  # kendi yolun

log = mavutil.mavlink_connection(tlog_path)

# Veriler
servo_times, s1, s2, s3, s4 = [], [], [], [], []
gyro_times, gx, gy, gz = [], [], [], []
acc_x, acc_y, acc_z = [], [], []
current_times, current_values = [], []
rc_times, rc1, rc2, rc3, rc4 = [], [], [], [], []
mode_times, modes = [], []

print("Veriler toplanıyor...")

while True:
    msg = log.recv_match(type=["SERVO_OUTPUT_RAW", "RAW_IMU", "SYS_STATUS", "RC_CHANNELS_RAW", "HEARTBEAT"], blocking=False)
    if msg is None:
        break

    # Zaman
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

    elif msg.get_type() == "SYS_STATUS":
        current_times.append(t)
        current_values.append(msg.current_battery / 100.0)

    elif msg.get_type() == "RC_CHANNELS_RAW":
        rc_times.append(t)
        rc1.append(msg.chan1_raw)
        rc2.append(msg.chan2_raw)
        rc3.append(msg.chan3_raw)
        rc4.append(msg.chan4_raw)

    elif msg.get_type() == "HEARTBEAT":
        mode_times.append(t)
        modes.append(msg.custom_mode)  # int değer, uçuş modu (örneğin: 0 = Stabilize, 3 = AltHold)

# Grafik
plt.figure(figsize=(16, 17))

# 1. Motor PWM
plt.subplot(6, 1, 1)
plt.plot(servo_times, s1, label="Motor 1")
plt.plot(servo_times, s2, label="Motor 2")
plt.plot(servo_times, s3, label="Motor 3")
plt.plot(servo_times, s4, label="Motor 4")
plt.ylabel("PWM")
plt.title("Motor PWM Çıkışları")
plt.grid()
plt.legend()

# 2. Gyro
plt.subplot(6, 1, 2)
plt.plot(gyro_times, gx, label="X Gyro")
plt.plot(gyro_times, gy, label="Y Gyro")
plt.plot(gyro_times, gz, label="Z Gyro")
plt.ylabel("°/s")
plt.title("Gyro Verileri")
plt.grid()
plt.legend()

# 3. Accel
plt.subplot(6, 1, 3)
plt.plot(gyro_times, acc_x, label="X Acc")
plt.plot(gyro_times, acc_y, label="Y Acc")
plt.plot(gyro_times, acc_z, label="Z Acc")
plt.ylabel("m/s² (scaled)")
plt.title("Accelerometer Verileri")
plt.grid()
plt.legend()

# 4. Akım
plt.subplot(6, 1, 4)
plt.plot(current_times, current_values, color="red", label="Çekilen Akım (A)")
plt.ylabel("Amper")
plt.title("APM Sistem Akımı")
plt.grid()
plt.legend()

# 5. RC
plt.subplot(6, 1, 5)
plt.plot(rc_times, rc1, label="RC1 (Roll)")
plt.plot(rc_times, rc2, label="RC2 (Pitch)")
plt.plot(rc_times, rc3, label="RC3 (Throttle)")
plt.plot(rc_times, rc4, label="RC4 (Yaw)")
plt.ylabel("RC PWM")
plt.title("RC Kumanda Girişleri")
plt.grid()
plt.legend()

# 6. Flight Mode
plt.subplot(6, 1, 6)
plt.step(mode_times, modes, where="post", label="Uçuş Modu (custom_mode)")
plt.xlabel("Zaman (s)")
plt.ylabel("Mode ID")
plt.title("Uçuş Modu Değişimleri (HEARTBEAT)")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
