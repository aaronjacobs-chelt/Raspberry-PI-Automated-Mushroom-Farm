"""Web interface for MycoMonitor."""

from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import os

from ..metrics.collector import MetricsCollector
from ..diagnostics.hardware import HardwareDiagnostics
from ..utils.config import load_config

app = Flask(__name__)
metrics_collector = MetricsCollector()
config = load_config()
diagnostics = HardwareDiagnostics(config['gpio_pins'])

@app.route('/')
def index():
    """Render main dashboard."""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Get current system status."""
    latest = metrics_collector.get_latest_metrics()
    if latest:
        return jsonify({
            'timestamp': latest.timestamp,
            'humidity': latest.humidity_readings,
            'temperature': latest.temperature_readings,
            'humidifier_state': latest.humidifier_state,
            'runtime': latest.runtime,
            'cycle_count': latest.cycle_count,
            'errors': latest.errors
        })
    return jsonify({'error': 'No metrics available'})

@app.route('/api/metrics/<int:hours>')
def get_metrics(hours):
    """Get historical metrics."""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    metrics = metrics_collector.get_metrics_range(start_time, end_time)
    stats = metrics_collector.calculate_statistics(metrics)
    
    return jsonify({
        'metrics': [vars(m) for m in metrics],
        'statistics': stats
    })

@app.route('/api/diagnostics')
def get_diagnostics():
    """Run and return diagnostics."""
    results = diagnostics.run_full_diagnostic()
    return jsonify(results)

def create_app():
    """Create and configure the Flask app."""
    # Ensure the template directory exists
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # Create basic template if it doesn't exist
    index_template = os.path.join(template_dir, 'index.html')
    if not os.path.exists(index_template):
        with open(index_template, 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>MycoMonitor Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container mt-4">
        <h1>MycoMonitor Dashboard</h1>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Current Status
                    </div>
                    <div class="card-body" id="current-status">
                        Loading...
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        System Health
                    </div>
                    <div class="card-body" id="system-health">
                        Loading...
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        Humidity History
                    </div>
                    <div class="card-body">
                        <canvas id="humidityChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusDiv = document.getElementById('current-status');
                    statusDiv.innerHTML = `
                        <p>Last Update: ${new Date(data.timestamp * 1000).toLocaleString()}</p>
                        <p>Humidifier: ${data.humidifier_state ? 'ON' : 'OFF'}</p>
                        <p>Runtime: ${data.runtime.toFixed(1)} seconds</p>
                        <p>Cycles: ${data.cycle_count}</p>
                    `;
                });
        }

        function updateHealth() {
            fetch('/api/diagnostics')
                .then(response => response.json())
                .then(data => {
                    const healthDiv = document.getElementById('system-health');
                    healthDiv.innerHTML = `
                        <p>GPIO Status: ${data.gpio_tests.every(test => test[1]) ? 'OK' : 'Issues Found'}</p>
                        <p>Power Status: ${Object.values(data.power_states).every(state => state.powered) ? 'OK' : 'Issues Found'}</p>
                    `;
                });
        }

        // Update every 30 seconds
        setInterval(updateStatus, 30000);
        setInterval(updateHealth, 30000);
        
        // Initial updates
        updateStatus();
        updateHealth();
    </script>
</body>
</html>
            """)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
