"""
Cost Tracking and Token Usage Monitoring

Provides comprehensive tracking of API usage, costs, and performance metrics
for budget management and optimization insights.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path


class TokenTracker:
    """
    Tracks API usage, costs, and provides budget management capabilities.
    
    Monitors OpenAI API calls for embeddings and completions with real-time
    cost calculation and budget alerts.
    """
    
    def __init__(self, storage_path: str = "storage/token_usage.json"):
        """
        Initialize the token tracker.
        
        Args:
            storage_path: Path to store usage data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        
        # Current pricing (as of 2025)
        self.pricing = {
            'text-embedding-3-small': {'input': 0.00002},  # per 1K tokens
            'gpt-4o-mini': {
                'input': 0.00015,   # per 1K tokens
                'output': 0.0006    # per 1K tokens
            }
        }
        
        self.usage_data = self._load_usage_data()
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'embedding_tokens': 0,
            'completion_input_tokens': 0,
            'completion_output_tokens': 0,
            'total_requests': 0,
            'total_cost': 0.0
        }
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """
        Load existing usage data from storage.
        
        Returns:
            Usage data dictionary
        """
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_empty_usage_data()
        else:
            return self._create_empty_usage_data()
    
    def _create_empty_usage_data(self) -> Dict[str, Any]:
        """
        Create empty usage data structure.
        
        Returns:
            Empty usage data dictionary
        """
        return {
            'total_cost': 0.0,
            'total_tokens': 0,
            'sessions': [],
            'daily_usage': {},
            'monthly_usage': {},
            'model_usage': {
                'text-embedding-3-small': {'tokens': 0, 'cost': 0.0, 'requests': 0},
                'gpt-4o-mini': {'input_tokens': 0, 'output_tokens': 0, 'cost': 0.0, 'requests': 0}
            }
        }
    
    def track_embedding_usage(self, input_tokens: int, model: str = 'text-embedding-3-small') -> float:
        """
        Track embedding API usage.
        
        Args:
            input_tokens: Number of input tokens
            model: Model used for embeddings
            
        Returns:
            Cost of the request
        """
        cost = (input_tokens / 1000) * self.pricing[model]['input']
        
        # Update current session
        self.current_session['embedding_tokens'] += input_tokens
        self.current_session['total_requests'] += 1
        self.current_session['total_cost'] += cost
        
        # Update total usage
        self.usage_data['total_cost'] += cost
        self.usage_data['total_tokens'] += input_tokens
        self.usage_data['model_usage'][model]['tokens'] += input_tokens
        self.usage_data['model_usage'][model]['cost'] += cost
        self.usage_data['model_usage'][model]['requests'] += 1
        
        # Update daily usage
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.usage_data['daily_usage']:
            self.usage_data['daily_usage'][today] = {'tokens': 0, 'cost': 0.0, 'requests': 0}
        
        self.usage_data['daily_usage'][today]['tokens'] += input_tokens
        self.usage_data['daily_usage'][today]['cost'] += cost
        self.usage_data['daily_usage'][today]['requests'] += 1
        
        return cost
    
    def track_completion_usage(self, input_tokens: int, output_tokens: int, 
                              model: str = 'gpt-4o-mini') -> float:
        """
        Track completion API usage.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model used for completion
            
        Returns:
            Cost of the request
        """
        input_cost = (input_tokens / 1000) * self.pricing[model]['input']
        output_cost = (output_tokens / 1000) * self.pricing[model]['output']
        total_cost = input_cost + output_cost
        
        # Update current session
        self.current_session['completion_input_tokens'] += input_tokens
        self.current_session['completion_output_tokens'] += output_tokens
        self.current_session['total_requests'] += 1
        self.current_session['total_cost'] += total_cost
        
        # Update total usage
        total_tokens = input_tokens + output_tokens
        self.usage_data['total_cost'] += total_cost
        self.usage_data['total_tokens'] += total_tokens
        self.usage_data['model_usage'][model]['input_tokens'] += input_tokens
        self.usage_data['model_usage'][model]['output_tokens'] += output_tokens
        self.usage_data['model_usage'][model]['cost'] += total_cost
        self.usage_data['model_usage'][model]['requests'] += 1
        
        # Update daily usage
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.usage_data['daily_usage']:
            self.usage_data['daily_usage'][today] = {'tokens': 0, 'cost': 0.0, 'requests': 0}
        
        self.usage_data['daily_usage'][today]['tokens'] += total_tokens
        self.usage_data['daily_usage'][today]['cost'] += total_cost
        self.usage_data['daily_usage'][today]['requests'] += 1
        
        return total_cost
    
    def get_usage_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get usage summary for the specified period.
        
        Args:
            days: Number of days to include in summary
            
        Returns:
            Usage summary dictionary
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        period_cost = 0.0
        period_tokens = 0
        period_requests = 0
        
        # Calculate period usage
        for date_str, usage in self.usage_data['daily_usage'].items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if start_date <= date <= end_date:
                period_cost += usage['cost']
                period_tokens += usage['tokens']
                period_requests += usage['requests']
        
        return {
            'period_days': days,
            'total_cost': self.usage_data['total_cost'],
            'period_cost': period_cost,
            'period_tokens': period_tokens,
            'period_requests': period_requests,
            'current_session_cost': self.current_session['total_cost'],
            'daily_average_cost': period_cost / max(days, 1),
            'cost_per_token': period_cost / max(period_tokens, 1),
            'model_breakdown': self.usage_data['model_usage']
        }
    
    def set_budget_limit(self, monthly_limit: float) -> None:
        """
        Set monthly budget limit with alert thresholds.
        
        Args:
            monthly_limit: Monthly budget limit in USD
        """
        self.usage_data['budget_limit'] = monthly_limit
        self.usage_data['alert_thresholds'] = {
            'warning': monthly_limit * 0.8,  # 80% warning
            'critical': monthly_limit * 0.9   # 90% critical
        }
        self._save_usage_data()
    
    def check_budget_status(self) -> Dict[str, Any]:
        """
        Check current budget status and alerts.
        
        Returns:
            Budget status information
        """
        if 'budget_limit' not in self.usage_data:
            return {'status': 'no_budget_set'}
        
        # Calculate current month usage
        current_month = datetime.now().strftime('%Y-%m')
        monthly_cost = 0.0
        
        for date_str, usage in self.usage_data['daily_usage'].items():
            if date_str.startswith(current_month):
                monthly_cost += usage['cost']
        
        budget_limit = self.usage_data['budget_limit']
        usage_percentage = (monthly_cost / budget_limit) * 100
        
        # Determine alert level
        alert_level = 'normal'
        if monthly_cost >= self.usage_data['alert_thresholds']['critical']:
            alert_level = 'critical'
        elif monthly_cost >= self.usage_data['alert_thresholds']['warning']:
            alert_level = 'warning'
        
        return {
            'status': 'active',
            'monthly_budget': budget_limit,
            'monthly_spent': monthly_cost,
            'remaining_budget': budget_limit - monthly_cost,
            'usage_percentage': usage_percentage,
            'alert_level': alert_level,
            'days_remaining': (datetime.now().replace(month=datetime.now().month+1, day=1) - timedelta(days=1) - datetime.now()).days
        }
    
    def get_optimization_suggestions(self) -> List[str]:
        """
        Get suggestions for optimizing API usage and costs.
        
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        usage_summary = self.get_usage_summary()
        
        # Analyze usage patterns
        if usage_summary['cost_per_token'] > 0.0001:
            suggestions.append("Consider using smaller models for simple queries to reduce costs")
        
        if usage_summary['period_requests'] > 1000:
            suggestions.append("Implement caching to reduce redundant API calls")
        
        embedding_usage = self.usage_data['model_usage']['text-embedding-3-small']
        completion_usage = self.usage_data['model_usage']['gpt-4o-mini']
        
        if embedding_usage['cost'] > completion_usage['cost']:
            suggestions.append("Embedding costs are high - consider batch processing or caching embeddings")
        
        if completion_usage['requests'] > 500:
            suggestions.append("High number of completion requests - consider longer context windows to reduce calls")
        
        return suggestions
    
    def _save_usage_data(self) -> None:
        """
        Save current usage data to storage.
        """
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except IOError as e:
            print(f"Error saving usage data: {e}")
    
    def end_session(self) -> Dict[str, Any]:
        """
        End current session and save data.
        
        Returns:
            Session summary
        """
        self.current_session['end_time'] = datetime.now().isoformat()
        
        # Add session to history
        self.usage_data['sessions'].append(self.current_session.copy())
        
        # Save data
        self._save_usage_data()
        
        session_summary = self.current_session.copy()
        
        # Reset current session
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'embedding_tokens': 0,
            'completion_input_tokens': 0,
            'completion_output_tokens': 0,
            'total_requests': 0,
            'total_cost': 0.0
        }
        
        return session_summary