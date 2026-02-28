from pymavlink import mavutil
import matplotlib.pyplot as plt

tlog_path = "2025-05-30 13-03-10.tlog"

log = mavutil.mavlink_connection(tlog_path)

roll_target_time, roll_target = [], []
roll_actual_time, roll_actual = [], []

print("PID verileri toplanıyor...")

while True:
    msg = log.recv_match(type=["ATTITUDE", "ATTITUDE_TARGET"], blocking=False)
    if msg is None:
        break

    # Zaman belirleme
    if hasattr(msg, "time_usec"):
        t = msg.time_usec / 1e6
    elif hasattr(msg, "time_boot_ms"):
        t = msg.time_boot_ms / 1000.0
    else:
        t = log.time_since('SYSTEM_BOOT')

    if msg.get_type() == "ATTITUDE":
        roll_actual_time.append(t)
        roll_actual.append(msg.roll)

    elif msg.get_type() == "ATTITUDE_TARGET":
        roll_target_time.append(t)
        roll_target.append(msg.body_roll_rate)

# Grafik çizimi
plt.figure(figsize=(12, 6))
plt.plot(roll_target_time, roll_target, label="Hedef Roll Hızı (rad/s)", linestyle="--")
plt.plot(roll_actual_time, roll_actual, label="Gerçek Roll Açısı (rad)", alpha=0.8)
plt.title("Roll PID Analizi")
plt.xlabel("Zaman (s)")
plt.ylabel("Değer (rad / rad/s)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
