import requests
import hmac
import hashlib
import time
from datetime import datetime

class ExpediaService:
    """Service class for Expedia API integration"""
    
    BASE_URL = "https://api.expediapartnersolutions.com/v3"
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def _generate_signature(self, timestamp, method, endpoint):
        """Generate signature for Expedia API authentication"""
        string_to_sign = f"{method}\n{endpoint}\n{self.api_key}\n{timestamp}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to Expedia API"""
        url = f"{self.BASE_URL}/{endpoint}"
        timestamp = str(int(time.time()))
        signature = self._generate_signature(timestamp, method, endpoint)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Key': self.api_key,
            'X-Signature': signature,
            'X-Timestamp': timestamp
        }

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Expedia API error: {str(e)}")

    def sync_rates(self, room_rates):
        """Sync room rates with Expedia"""
        try:
            formatted_rates = []
            for rate in room_rates:
                formatted_rates.append({
                    "roomTypeId": rate["ota_room_id"],
                    "ratePlanId": rate["ota_rate_plan_id"],
                    "dates": {
                        "start": rate["start_date"],
                        "end": rate["end_date"]
                    },
                    "rates": {
                        "perNight": rate["amount"],
                        "currencyCode": rate["currency"]
                    }
                })

            data = {
                "propertyRates": formatted_rates
            }

            return self._make_request('POST', 'properties/rates', data=data)
        except Exception as e:
            raise Exception(f"Error syncing rates with Expedia: {str(e)}")

    def sync_inventory(self, room_inventory):
        """Sync room inventory with Expedia"""
        try:
            formatted_inventory = []
            for inventory in room_inventory:
                formatted_inventory.append({
                    "roomTypeId": inventory["ota_room_id"],
                    "dates": {
                        "start": inventory["start_date"],
                        "end": inventory["end_date"]
                    },
                    "availability": {
                        "roomsAvailable": inventory["available_rooms"]
                    }
                })

            data = {
                "propertyAvailability": formatted_inventory
            }

            return self._make_request('POST', 'properties/availability', data=data)
        except Exception as e:
            raise Exception(f"Error syncing inventory with Expedia: {str(e)}")

    def get_bookings(self, start_date=None, end_date=None):
        """Get bookings from Expedia"""
        try:
            params = {}
            if start_date:
                params['startDate'] = start_date
            if end_date:
                params['endDate'] = end_date

            response = self._make_request('GET', 'bookings', params=params)
            
            formatted_bookings = []
            for booking in response.get('bookings', []):
                formatted_bookings.append({
                    'booking_id': booking['itineraryId'],
                    'channel': 'expedia',
                    'guest': {
                        'name': f"{booking['guest']['firstName']} {booking['guest']['lastName']}",
                        'email': booking['guest']['email'],
                        'phone': booking['guest'].get('phone', '')
                    },
                    'room': {
                        'room_id': booking['roomTypeId'],
                        'room_type': booking['roomTypeDescription']
                    },
                    'dates': {
                        'check_in': booking['checkIn'],
                        'check_out': booking['checkOut']
                    },
                    'amount': {
                        'total': booking['totalCharge'],
                        'currency': booking['currencyCode']
                    },
                    'status': booking['status'],
                    'created_at': booking['createDateTime']
                })

            return formatted_bookings
        except Exception as e:
            raise Exception(f"Error getting bookings from Expedia: {str(e)}")

    def update_booking_status(self, booking_id, new_status):
        """Update booking status on Expedia"""
        try:
            data = {
                "status": new_status
            }
            
            return self._make_request('PUT', f'bookings/{booking_id}/status', data=data)
        except Exception as e:
            raise Exception(f"Error updating booking status on Expedia: {str(e)}")

    def check_health(self):
        """Check API connectivity and authentication"""
        try:
            response = self._make_request('GET', 'ping')
            return {
                'status': 'connected',
                'apiVersion': response.get('version'),
                'environment': response.get('environment'),
                'timestamp': response.get('timestamp')
            }
        except Exception as e:
            raise Exception(f"Expedia health check failed: {str(e)}")

    def get_room_types(self):
        """Get available room types from Expedia"""
        try:
            return self._make_request('GET', 'properties/roomTypes')
        except Exception as e:
            raise Exception(f"Error getting room types from Expedia: {str(e)}")

    def get_rate_plans(self):
        """Get available rate plans from Expedia"""
        try:
            return self._make_request('GET', 'properties/ratePlans')
        except Exception as e:
            raise Exception(f"Error getting rate plans from Expedia: {str(e)}")
