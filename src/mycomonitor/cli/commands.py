"""Command-line interface for MycoMonitor."""

import click
import json
import sys
from datetime import datetime, timedelta
from typing import Optional

from ..core.controller import HumidifierController
from ..diagnostics.hardware import HardwareDiagnostics
from ..metrics.collector import MetricsCollector
from ..utils.config import load_config

@click.group()
def cli():
    """MycoMonitor CLI - Manage your mushroom growing environment."""
    pass

@cli.command()
@click.option('--config', '-c', type=str, help='Path to configuration file')
def start(config: Optional[str]):
    """Start the MycoMonitor system."""
    try:
        controller = HumidifierController(config_path=config)
        click.echo("Starting MycoMonitor...")
        controller.run()
    except Exception as e:
        click.echo(f"Error starting system: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--pin', '-p', type=int, help='Test specific GPIO pin')
def test_gpio(pin: Optional[int]):
    """Test GPIO pins."""
    config = load_config()
    diagnostics = HardwareDiagnostics(config['gpio_pins'])
    
    if pin:
        success, message = diagnostics.test_gpio_output(pin)
        click.echo(f"Pin {pin}: {message}")
        sys.exit(0 if success else 1)
    else:
        results = diagnostics.test_all_pins()
        for pin, success, message in results:
            click.echo(f"Pin {pin}: {message}")
        if not all(success for _, success, _ in results):
            sys.exit(1)

@cli.command()
def diagnose():
    """Run full system diagnostics."""
    config = load_config()
    diagnostics = HardwareDiagnostics(config['gpio_pins'])
    
    click.echo("Running system diagnostics...")
    results = diagnostics.run_full_diagnostic()
    
    click.echo("\nGPIO Tests:")
    for pin, success, message in results['gpio_tests']:
        click.echo(f"  {message}")
    
    click.echo("\nPower States:")
    for name, state in results['power_states'].items():
        click.echo(f"  {name}: {'Powered' if state['powered'] else 'Unpowered'} ({state['voltage']}V)")
    
    if not all(state['powered'] for state in results['power_states'].values()):
        sys.exit(1)

@cli.command()
@click.option('--hours', '-h', type=int, default=24, help='Hours of metrics to show')
def metrics(hours: int):
    """Show system metrics."""
    collector = MetricsCollector()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    metrics = collector.get_metrics_range(start_time, end_time)
    stats = collector.calculate_statistics(metrics)
    
    click.echo(f"\nMetrics for the last {hours} hours:")
    click.echo("\nHumidity:")
    click.echo(f"  Min: {stats['humidity']['min']:.1f}%")
    click.echo(f"  Max: {stats['humidity']['max']:.1f}%")
    click.echo(f"  Avg: {stats['humidity']['avg']:.1f}%")
    
    click.echo("\nTemperature:")
    click.echo(f"  Min: {stats['temperature']['min']:.1f}°C")
    click.echo(f"  Max: {stats['temperature']['max']:.1f}°C")
    click.echo(f"  Avg: {stats['temperature']['avg']:.1f}°C")
    
    click.echo(f"\nTotal Runtime: {stats['runtime']['total'] / 3600:.1f} hours")
    click.echo(f"Cycles: {stats['cycles']}")
    click.echo(f"Errors: {stats['errors']}")

@cli.command()
def status():
    """Show current system status."""
    try:
        collector = MetricsCollector()
        latest = collector.get_latest_metrics()
        
        if latest:
            click.echo("\nCurrent Status:")
            click.echo("\nHumidity Readings:")
            for sensor, value in latest.humidity_readings.items():
                click.echo(f"  {sensor}: {value:.1f}%")
            
            click.echo("\nTemperature Readings:")
            for sensor, value in latest.temperature_readings.items():
                click.echo(f"  {sensor}: {value:.1f}°C")
            
            click.echo(f"\nHumidifier: {'ON' if latest.humidifier_state else 'OFF'}")
            click.echo(f"Current Runtime: {latest.runtime:.1f} seconds")
            click.echo(f"Cycle Count: {latest.cycle_count}")
            
            if latest.errors:
                click.echo("\nErrors:")
                for error in latest.errors:
                    click.echo(f"  - {error}")
        else:
            click.echo("No current metrics available")
    except Exception as e:
        click.echo(f"Error getting status: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
