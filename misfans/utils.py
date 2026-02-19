import os


def read_cpu_temp_c():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            m = int(f.read().strip())
            return m / 1000.0
    except Exception:
        # fallback: try vcgencmd if available
        try:
            import subprocess
            out = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
            # e.g. temp=48.0'C
            return float(out.split('=')[1].split("'"[0])[0])
        except Exception:
            return None
