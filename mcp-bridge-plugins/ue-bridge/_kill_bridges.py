import psutil

killed = 0
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
    try:
        if p.info['name'] != 'node.exe':
            continue
        cmdline = p.info.get('cmdline') or []
        cmd_str = ' '.join(cmdline)
        if 'dist/index.js' not in cmd_str:
            continue
        cwd = p.info.get('cwd', '')
        print(f"Killing PID={p.info['pid']} CWD={cwd}")
        p.terminate()
        killed += 1
    except Exception as e:
        print(f"Error: {e}")

print(f"\nKilled {killed} bridge processes")
