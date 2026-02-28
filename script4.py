from pymavlink import mavutil
import matplotlib.pyplot as plt

tlog_path = "2025-05-24 05-48-33.tlog"
log = mavutil.mavlink_connection(tlog_path)

roll_target_time, roll_target = [], []
roll_actual_time, roll_actual = [], []
arm_time, arm_state = [], []

print("Veriler toplanıyor...")

while True:
    msg = log.recv_match(type=["ATTITUDE", "ATTITUDE_TARGET", "HEARTBEAT", "STATUSTEXT"], blocking=False)
    if msg is None:
        break

    # Zaman belirleme
    if hasattr(msg, "time_usec"):
        t = msg.time_usec / 1e6
    elif hasattr(msg, "time_boot_ms"):
        t = msg.time_boot_ms / 1000.0
    else:
        continue

    if msg.get_type() == "ATTITUDE":
        roll_actual_time.append(t)
        roll_actual.append(msg.roll)

    elif msg.get_type() == "ATTITUDE_TARGET":
        roll_target_time.append(t)
        roll_target.append(msg.body_roll_rate)

    elif msg.get_type() == "HEARTBEAT":
        base_mode = msg.base_mode
        is_armed = (base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED) != 0
        arm_time.append(t)
        arm_state.append(1 if is_armed else 0)

    elif msg.get_type() == "STATUSTEXT":
        if "PreArm" in msg.text:
            print(f"[{t:.1f}s] {msg.severity}: {msg.text}")

# Grafik çizimi
plt.figure(figsize=(12, 8))

# Roll PID
plt.subplot(2, 1, 1)
plt.plot(roll_target_time, roll_target, label="Hedef Roll Hızı (rad/s)", linestyle="--")
plt.plot(roll_actual_time, roll_actual, label="Gerçek Roll Açısı (rad)", alpha=0.8)
plt.title("Roll PID Analizi")
plt.xlabel("Zaman (s)")
plt.ylabel("Değer (rad / rad/s)")
plt.grid()
plt.legend()

# ARM durumu
plt.subplot(2, 1, 2)
plt.plot(arm_time, arm_state, label="ARM Durumu", color='green')
plt.yticks([0, 1], ['Disarmed', 'Armed'])
plt.xlabel("Zaman (s)")
plt.ylabel("ARM Durumu")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
