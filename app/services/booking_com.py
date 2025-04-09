import requests
from datetime import datetime

class BookingComService:
    """Service class for Booking.com API integration"""
    
    BASE_URL = "https://distribution-xml.booking.com/2.0"
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.auth = (self.api_key, self.api_secret)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to Booking.com API"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Booking.com API error: {str(e)}")

    def sync_rates(self, room_rates):
        """Sync room rates with Booking.com"""
        try:
            formatted_rates = []
            for rate in room_rates:
                formatted_rates.append({
                    "room_id": rate["ota_room_id"],
                    "rate_plan_id": rate["ota_rate_plan_id"],
                    "date_range": {
                        "start_date": rate["start_date"],
                        "end_date": rate["end_date"]
                    },
                    "price": {
                        "amount": rate["amount"],
                        "currency": rate["currency"]
                    }
                })

            data = {
                "rates": formatted_rates
            }

            return self._make_request('POST', 'rates/update', data=data)
        except Exception as e:
            raise Exception(f"Error syncing rates with Booking.com: {str(e)}")

    def sync_inventory(self, room_inventory):
        """Sync room inventory with Booking.com"""
        try:
            formatted_inventory = []
            for inventory in room_inventory:
                formatted_inventory.append({
                    "room_id": inventory["ota_room_id"],
                    "date_range": {
                        "start_date": inventory["start_date"],
                        "end_date": inventory["end_date"]
                    },
                    "available_rooms": inventory["available_rooms"]
                })

            data = {
                "rooms": formatted_inventory
            }

            return self._make_request('POST', 'rooms/availability', data=data)
        except Exception as e:
            raise Exception(f"Error syncing inventory with Booking.com: {str(e)}")

    def get_bookings(self, start_date=None, end_date=None):
        """Get bookings from Booking.com"""
        try:
            params = {}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date

            response = self._make_request('GET', 'reservations', params=params)
            
            # Format bookings to standardized structure
            formatted_bookings = []
            for booking in response.get('reservations', []):
                formatted_bookings.append({
                    'booking_id': booking['id'],
                    'channel': 'booking.com',
                    'guest': {
                        'name': f"{booking['guest']['first_name']} {booking['guest']['last_name']}",
                        'email': booking['guest']['email'],
                        'phone': booking['guest'].get('phone', '')
                    },
                    'room': {
                        'room_id': booking['room_id'],
                        'room_type': booking['room_type']
                    },
                    'dates': {
                        'check_in': booking['check_in'],
                        'check_out': booking['check_out']
                    },
                    'amount': {
                        'total': booking['total_amount'],
                        'currency': booking['currency']
                    },
                    'status': booking['status'],
                    'created_at': booking['created_at']
                })

            return formatted_bookings
        except Exception as e:
            raise Exception(f"Error getting bookings from Booking.com: {str(e)}")

    def update_booking_status(self, booking_id, new_status):
        """Update booking status on Booking.com"""
        try:
            data = {
                "status": new_status
            }
            
            return self._make_request('PUT', f'reservations/{booking_id}/status', data=data)
        except Exception as e:
            raise Exception(f"Error updating booking status on Booking.com: {str(e)}")

    def check_health(self):
        """Check API connectivity and authentication"""
        try:
            response = self._make_request('GET', 'health-check')
            return {
                'status': 'connected',
                'api_version': response.get('api_version'),
                'server_time': response.get('server_time')
            }
        except Exception as e:
            raise Exception(f"Booking.com health check failed: {str(e)}")
