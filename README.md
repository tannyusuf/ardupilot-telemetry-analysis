# ArduPilot Telemetry Analysis

A lightweight Python toolkit for parsing and visualizing MAVLink telemetry logs (`.tlog`) recorded by an **APM 2.8** flight controller.

## Background

This project was developed during my student years while working with the APM 2.8 flight controller board. Because the APM 2.8 is an older and limited piece of hardware, the standard ground-station tools (e.g. Mission Planner's log-analysis views) often failed to parse or display its telemetry logs correctly. To work around this limitation I wrote these scripts to directly read the raw `.tlog` files using `pymavlink` and produce clear matplotlib plots for post-flight analysis.

## Features

| Script | What it analyses |
|---|---|
| `script.py` | Roll PID tracking — compares the roll target rate (`ATTITUDE_TARGET`) against the actual roll angle (`ATTITUDE`) |
| `scirpt2.py` *(filename typo is intentional — matches the file on disk)* | Full-session dashboard — motor PWM outputs, raw gyroscope & accelerometer data, battery current, RC channel inputs, and flight-mode transitions |
| `script3.py` | Extended dashboard — adds attitude (roll/pitch/yaw), vibration levels, and altitude/airspeed (VFR HUD) on top of the data in `scirpt2.py` |
| `script4.py` | Roll PID analysis with ARM-state tracking and automatic detection of pre-arm warning messages (`STATUSTEXT`) |

## Requirements

- Python 3.x
- [pymavlink](https://github.com/ArduPilot/pymavlink)
- [matplotlib](https://matplotlib.org/)

Install dependencies with pip:

```bash
pip install pymavlink matplotlib
```

## Usage

1. Copy your `.tlog` file into the project directory (or note its full path).
2. Open the script you want to run and update the `tlog_path` variable at the top of the file to point to your log file.
3. Run the script:

```bash
python script3.py
```

A matplotlib window will open showing the plotted telemetry data.

## MAVLink Message Types Used

| Message | Data extracted |
|---|---|
| `ATTITUDE` | Roll, pitch, yaw angles (rad) |
| `ATTITUDE_TARGET` | Target roll rate (rad/s) |
| `SERVO_OUTPUT_RAW` | Motor PWM outputs |
| `RAW_IMU` | Gyroscope (°/s) and accelerometer (m/s²) |
| `SYS_STATUS` | Battery current (A) |
| `RC_CHANNELS_RAW` | RC input channels (PWM) |
| `HEARTBEAT` | Flight mode ID and ARM state |
| `VFR_HUD` | Altitude and airspeed |
| `VIBRATION` | Vibration levels (g) |
| `STATUSTEXT` | Pre-arm warning messages |

## License

This project is open source. Feel free to use or adapt the scripts for your own flight-log analysis.
