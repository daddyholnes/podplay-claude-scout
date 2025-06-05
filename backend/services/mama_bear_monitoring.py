# backend/services/mama_bear_monitoring.py
"""
🐻 Mama Bear Monitoring & Health System
Real-time monitoring, health checks, and performance tracking
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import json
import os

logger = logging.getLogger(__name__)

class MamaBearMonitoring:
    """
    Comprehensive monitoring system for Mama Bear infrastructure
    """
    
    def __init__(self, model_manager, orchestrator):
        self.model_manager = model_manager
        self.orchestrator = orchestrator
        
        # Metrics storage
        self.metrics = {
            'requests_per_minute': deque(maxlen=60),
            'response_times': deque(maxlen=1000),
            'success_rates': deque(maxlen=100),
            'model_usage': defaultdict(int),
            'agent_usage': defaultdict(int),
            'error_counts': defaultdict(int),
            'user_activity': defaultdict(int)
        }
        
        # Health status
        self.system_health = {
            'overall_status': 'healthy',
            'last_check': datetime.now(),
            'components': {
                'model_manager': 'unknown',
                'memory_system': 'unknown',
                'orchestrator': 'unknown',
                'agents': 'unknown'
            },
            'alerts': []
        }
        
        # Performance baselines
        self.baselines = {
            'avg_response_time': 2.0,  # seconds
            'success_rate_threshold': 0.95,
            'max_error_rate': 0.05,
            'max_queue_length': 100
        }
        
        # Alert history
        self.alert_history = deque(maxlen=1000)
        
        # Start monitoring loops
        asyncio.create_task(self._monitoring_loop())
        asyncio.create_task(self._health_check_loop())
        asyncio.create_task(self._metrics_persistence_loop())
    
    async def log_interaction(self, user_id: str, agent: str, message: str, response: Dict[str, Any]):
        """Log an interaction for monitoring"""
        
        timestamp = datetime.now()
        
        # Update metrics
        self.metrics['requests_per_minute'].append(timestamp)
        self.metrics['agent_usage'][agent] += 1
        self.metrics['user_activity'][user_id] += 1
        
        if response.get('success', False):
            response_time = response.get('response_time', 0)
            self.metrics['response_times'].append(response_time)
            
            model_used = response.get('model_used', 'unknown')
            self.metrics['model_usage'][model_used] += 1
        else:
            error_type = response.get('error', 'unknown_error')
            self.metrics['error_counts'][error_type] += 1
        
        # Update success rate
        success = 1 if response.get('success', False) else 0
        self.metrics['success_rates'].append(success)
        
        # Check for anomalies
        await self._check_anomalies()
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        
        while True:
            try:
                await asyncio.sleep(60)  # Run every minute
                
                # Calculate current metrics
                current_metrics = await self._calculate_current_metrics()
                
                # Check thresholds
                await self._check_thresholds(current_metrics)
                
                # Log metrics
                logger.info(f"📊 Metrics: {json.dumps(current_metrics, indent=2)}")
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
    
    async def _health_check_loop(self):
        """Health check loop"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                
                # Check component health
                health_status = await self._perform_health_checks()
                
                # Update system health
                self.system_health.update(health_status)
                self.system_health['last_check'] = datetime.now()
                
                # Determine overall status
                component_statuses = list(health_status['components'].values())
                if all(status == 'healthy' for status in component_statuses):
                    self.system_health['overall_status'] = 'healthy'
                elif any(status == 'critical' for status in component_statuses):
                    self.system_health['overall_status'] = 'critical'
                else:
                    self.system_health['overall_status'] = 'degraded'
                
                logger.info(f"🏥 Health Check: {self.system_health['overall_status']}")
                
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
    
    async def _metrics_persistence_loop(self):
        """Persist metrics to storage"""
        
        while True:
            try:
                await asyncio.sleep(900)  # Run every 15 minutes
                
                # Save metrics to file
                metrics_data = {
                    'timestamp': datetime.now().isoformat(),
                    'metrics': await self._calculate_current_metrics(),
                    'health': self.system_health,
                    'recent_alerts': list(self.alert_history)[-10:]  # Last 10 alerts
                }
                
                os.makedirs('monitoring_data', exist_ok=True)
                with open('monitoring_data/metrics_snapshot.json', 'w') as f:
                    json.dump(metrics_data, f, indent=2, default=str)
                
            except Exception as e:
                logger.error(f"Metrics persistence error: {e}")
    
    async def _calculate_current_metrics(self) -> Dict[str, Any]:
        """Calculate current system metrics"""
        
        now = datetime.now()
        
        # Requests per minute
        recent_requests = [
            req for req in self.metrics['requests_per_minute']
            if (now - req).seconds < 60
        ]
        requests_per_minute = len(recent_requests)
        
        # Average response time
        avg_response_time = (
            sum(self.metrics['response_times']) / len(self.metrics['response_times'])
            if self.metrics['response_times'] else 0
        )
        
        # Success rate
        success_rate = (
            sum(self.metrics['success_rates']) / len(self.metrics['success_rates'])
            if self.metrics['success_rates'] else 1.0
        )
        
        # Error rate
        total_errors = sum(self.metrics['error_counts'].values())
        total_requests = len(self.metrics['response_times']) + total_errors
        error_rate = total_errors / max(total_requests, 1)
        
        # Top models and agents
        top_models = dict(sorted(
            self.metrics['model_usage'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])
        
        top_agents = dict(sorted(
            self.metrics['agent_usage'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])
        
        return {
            'requests_per_minute': requests_per_minute,
            'avg_response_time': avg_response_time,
            'success_rate': success_rate,
            'error_rate': error_rate,
            'top_models': top_models,
            'top_agents': top_agents,
            'active_users': len(self.metrics['user_activity']),
            'total_requests': total_requests
        }
    
    async def _check_thresholds(self, metrics: Dict[str, Any]):
        """Check if metrics exceed thresholds"""
        
        alerts = []
        
        # Response time check
        if metrics['avg_response_time'] > self.baselines['avg_response_time'] * 2:
            alerts.append({
                'type': 'high_response_time',
                'severity': 'warning',
                'message': f"High response time: {metrics['avg_response_time']:.2f}s",
                'timestamp': datetime.now().isoformat()
            })
        
        # Success rate check
        if metrics['success_rate'] < self.baselines['success_rate_threshold']:
            alerts.append({
                'type': 'low_success_rate',
                'severity': 'critical',
                'message': f"Low success rate: {metrics['success_rate']:.2%}",
                'timestamp': datetime.now().isoformat()
            })
        
        # Error rate check
        if metrics['error_rate'] > self.baselines['max_error_rate']:
            alerts.append({
                'type': 'high_error_rate',
                'severity': 'warning',
                'message': f"High error rate: {metrics['error_rate']:.2%}",
                'timestamp': datetime.now().isoformat()
            })
        
        # Add alerts to history and system health
        for alert in alerts:
            self.alert_history.append(alert)
            self.system_health['alerts'].append(alert)
            logger.warning(f"🚨 ALERT: {alert['message']}")
        
        # Keep only recent alerts in system health
        self.system_health['alerts'] = [
            alert for alert in self.system_health['alerts']
            if datetime.fromisoformat(alert['timestamp']) > datetime.now() - timedelta(hours=1)
        ]
    
    async def _check_anomalies(self):
        """Check for anomalies in recent data"""
        
        # Check for sudden spikes in errors
        recent_errors = list(self.metrics['error_counts'].values())[-10:]
        if recent_errors and max(recent_errors) > 10:  # More than 10 errors of same type
            await self._create_alert(
                'error_spike',
                'warning',
                f"Error spike detected: {max(recent_errors)} errors of same type"
            )
    
    async def _perform_health_checks(self) -> Dict[str, Any]:
        """Perform comprehensive health checks"""
        
        health = {
            'components': {},
            'details': {}
        }
        
        # Model Manager health
        try:
            model_status = await self.model_manager.get_status()
            available_models = sum(1 for model in model_status['models'] if model['status'] == 'available')
            
            if available_models > 0:
                health['components']['model_manager'] = 'healthy'
            else:
                health['components']['model_manager'] = 'critical'
            
            health['details']['model_manager'] = {
                'available_models': available_models,
                'total_models': len(model_status['models'])
            }
            
        except Exception as e:
            health['components']['model_manager'] = 'critical'
            health['details']['model_manager'] = {'error': str(e)}
        
        # Orchestrator health
        try:
            orchestrator_status = await self.orchestrator.get_orchestration_status()
            
            if orchestrator_status.get('system_health') == 'healthy':
                health['components']['orchestrator'] = 'healthy'
            else:
                health['components']['orchestrator'] = 'degraded'
            
            health['details']['orchestrator'] = orchestrator_status
            
        except Exception as e:
            health['components']['orchestrator'] = 'critical'
            health['details']['orchestrator'] = {'error': str(e)}
        
        # Agent health
        try:
            registered_agents = len(self.orchestrator.agent_registry)
            
            if registered_agents > 5:  # We expect 7 agents
                health['components']['agents'] = 'healthy'
            elif registered_agents > 3:
                health['components']['agents'] = 'degraded'
            else:
                health['components']['agents'] = 'critical'
            
            health['details']['agents'] = {
                'registered_agents': registered_agents,
                'expected_agents': 7
            }
            
        except Exception as e:
            health['components']['agents'] = 'critical'
            health['details']['agents'] = {'error': str(e)}
        
        # Memory system health (simplified)
        health['components']['memory_system'] = 'healthy'
        health['details']['memory_system'] = {'status': 'operational'}
        
        return health
    
    async def _create_alert(self, alert_type: str, severity: str, message: str):
        """Create and log an alert"""
        
        alert = {
            'type': alert_type,
            'severity': severity,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        self.alert_history.append(alert)
        self.system_health['alerts'].append(alert)
        
        logger.warning(f"🚨 ALERT [{severity.upper()}]: {message}")
    
    async def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive monitoring dashboard data"""
        
        current_metrics = await self._calculate_current_metrics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_health': self.system_health,
            'metrics': current_metrics,
            'recent_alerts': list(self.alert_history)[-20:],
            'baselines': self.baselines,
            'uptime': self._calculate_uptime(),
            'performance_trends': await self._calculate_trends()
        }
    
    def _calculate_uptime(self) -> Dict[str, Any]:
        """Calculate system uptime"""
        
        # This is simplified - in a real system, you'd track actual start time
        return {
            'since': datetime.now().isoformat(),
            'duration': '0:00:00',  # Placeholder
            'availability': '99.9%'  # Placeholder
        }
    
    async def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate performance trends"""
        
        # This is simplified - would calculate actual trends over time
        return {
            'response_time_trend': 'stable',
            'success_rate_trend': 'improving',
            'error_rate_trend': 'decreasing',
            'usage_trend': 'increasing'
        }
    
    async def shutdown(self):
        """Gracefully shutdown monitoring"""
        logger.info("🐻 Shutting down Mama Bear Monitoring...")
        
        # Save final metrics
        try:
            final_metrics = {
                'shutdown_time': datetime.now().isoformat(),
                'final_metrics': await self._calculate_current_metrics(),
                'final_health': self.system_health
            }
            
            os.makedirs('monitoring_data', exist_ok=True)
            with open('monitoring_data/shutdown_metrics.json', 'w') as f:
                json.dump(final_metrics, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save shutdown metrics: {e}")
        
        logger.info("✅ Monitoring shutdown complete")