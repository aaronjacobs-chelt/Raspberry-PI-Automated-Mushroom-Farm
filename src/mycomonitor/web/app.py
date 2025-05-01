"""Web interface for MycoMonitor."""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from flask import Flask, jsonify, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from ..diagnostics.hardware import HardwareDiagnostics
from ..metrics.collector import MetricsCollector
from ..utils.config import SystemConfig, load_config

class MycoMonitorWeb:
    """Web interface handler for MycoMonitor."""

    def __init__(self, config: Optional[SystemConfig] = None) -> None:
        """
        Initialize web interface.
        
        Args:
            config: Optional system configuration
        """
        self.config = config or load_config()
        self.metrics_collector = MetricsCollector()
        self.diagnostics = HardwareDiagnostics(self.config.gpio_pins)
        self.app = self._create_app()

    def _create_app(self) -> Flask:
        """
        Create and configure Flask application.
        
        Returns:
            Configured Flask application
        """
        app = Flask(__name__)
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

        # Ensure template directory exists
        template_dir = Path(__file__).parent / 'templates'
        template_dir.mkdir(exist_ok=True)
        
        # Create basic template if it doesn't exist
        self._ensure_template_exists(template_dir)

        # Register routes
        app.route('/')(self.index)
        app.route('/api/status')(self.status)
        app.route('/api/metrics/<int:hours>')(self.get_metrics)
        app.route('/api/diagnostics')(self.get_diagnostics)

        return app

    def _ensure_template_exists(self, template_dir: Path) -> None:
        """
        Ensure the basic template exists.
        
        Args:
            template_dir: Path to template directory
        """
        index_template = template_dir / 'index.html'
        if not index_template.exists():
            with index_template.open('w') as f:
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
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    const statusDiv = document.getElementById('current-status');
                    statusDiv.innerHTML = `
                        <p>Last Update: ${new Date(data.timestamp * 1000).toLocaleString()}</p>
                        <p>Humidifier: ${data.humidifier_state ? 'ON' : 'OFF'}</p>
                        <p>Runtime: ${data.runtime.toFixed(1)} seconds</p>
                        <p>Cycles: ${data.cycle_count}</p>
                    `;
                })
                .catch(error => console.error('Error:', error));
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
                })
                .catch(error => console.error('Error:', error));
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

    def index(self) -> str:
        """Render main dashboard."""
        return render_template('index.html')

    def status(self) -> Dict[str, Any]:
        """Get current system status."""
        latest = self.metrics_collector.get_latest_metrics()
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

    def get_metrics(self, hours: int) -> Dict[str, Any]:
        """
        Get historical metrics.
        
        Args:
            hours: Number of hours of history to retrieve
            
        Returns:
            Dictionary containing metrics and statistics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        metrics = self.metrics_collector.get_metrics_range(start_time, end_time)
        stats = self.metrics_collector.calculate_statistics(metrics)
        
        return jsonify({
            'metrics': [vars(m) for m in metrics],
            'statistics': stats
        })

    def get_diagnostics(self) -> Dict[str, Any]:
        """
        Run and return diagnostics.
        
        Returns:
            Dictionary containing diagnostic results
        """
        results = self.diagnostics
        return jsonify(results.run_full_diagnostic())

def create_app(config: Optional[SystemConfig] = None) -> Flask:
    """
    Create the Flask application.
    
    Args:
        config: Optional system configuration
        
    Returns:
        Configured Flask application
    """
    monitor = MycoMonitorWeb(config)
    return monitor.app
