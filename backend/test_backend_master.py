"""
Podplay Sanctuary Backend Master Test
Covers REST endpoints, SocketIO events, Scrapybara, and error handling
"""
import os
import sys
import time
import requests
import socketio

API_BASE = os.getenv('VITE_API_BASE_URL', 'http://localhost:5000')
SIO = socketio.Client()

results = []

def log_result(test, passed, info=None):
    results.append({'test': test, 'passed': passed, 'info': info})
    print(f"{'[PASS]' if passed else '[FAIL]'} {test} - {info if info else ''}")

# 1. Health & Status
try:
    r = requests.get(f"{API_BASE}/")
    assert r.status_code == 200 and 'service' in r.json()
    log_result('GET /', True)
except Exception as e:
    log_result('GET /', False, str(e))

# 2. Monitoring
try:
    r = requests.get(f"{API_BASE}/monitoring")
    assert r.status_code == 200 and 'html' in r.headers.get('Content-Type','')
    log_result('GET /monitoring', True)
except Exception as e:
    log_result('GET /monitoring', False, str(e))

# 3. Error Handling (404)
try:
    r = requests.get(f"{API_BASE}/not_a_real_endpoint")
    assert r.status_code == 404 and 'error' in r.json()
    log_result('GET 404', True)
except Exception as e:
    log_result('GET 404', False, str(e))

# 4. SocketIO: Connect, Task Submit, Agent Status
socketio_events = {'progress': None, 'status': None}

@SIO.on('enhanced_task_progress')
def on_progress(data):
    socketio_events['progress'] = data

@SIO.on('agent_status')
def on_status(data):
    socketio_events['status'] = data

try:
    SIO.connect(API_BASE)
    # Submit a research task (simulate, may need adjustment for your backend)
    SIO.emit('submit_enhanced_task', {
        'task_description': 'Test research task',
        'task_type': 'research',
        'user_id': 'test_user',
        'priority': 1
    })
    time.sleep(2)
    log_result('SocketIO submit_enhanced_task', socketio_events['progress'] is not None)
    # Request agent status
    SIO.emit('get_agent_status', {'request': True})
    time.sleep(1)
    log_result('SocketIO get_agent_status', socketio_events['status'] is not None)
    SIO.disconnect()
except Exception as e:
    log_result('SocketIO events', False, str(e))

# 5. Scrapybara (if REST endpoints exposed)
# Add REST calls here if you expose workspace creation/status endpoints

# 6. Security: Check secrets not leaked
try:
    r = requests.get(f"{API_BASE}/")
    bad = any(x in r.text for x in ['API_KEY', 'SECRET', 'TOKEN'])
    log_result('No secrets in GET /', not bad)
except Exception as e:
    log_result('No secrets in GET /', False, str(e))

# 7. Print summary
print("\n=== TEST SUMMARY ===")
for res in results:
    print(f"{res['test']}: {'PASS' if res['passed'] else 'FAIL'}")

if not all(r['passed'] for r in results):
    sys.exit(1)
