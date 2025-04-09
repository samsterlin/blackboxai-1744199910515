import requests
from datetime import datetime

class MakeMyTripService:
    """Service class for MakeMyTrip API integration"""
    
    BASE_URL = "https://api.makemytrip.com/hotels/v1"
    
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Key': self.api_key,
            'X-API-Secret': self.api_secret
        })

    def _make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to MakeMyTrip API"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"MakeMyTrip API error: {str(e)}")

    def sync_rates(self, room_rates):
        """Sync room rates with MakeMyTrip"""
        try:
            formatted_rates = []
            for rate in room_rates:
                formatted_rates.append({
                    "roomTypeId": rate["ota_room_id"],
                    "ratePlanId": rate["ota_rate_plan_id"],
                    "dateRange": {
                        "startDate": rate["start_date"],
                        "endDate": rate["end_date"]
                    },
                    "pricing": {
                        "baseRate": rate["amount"],
                        "currencyCode": rate["currency"]
                    }
                })

            data = {
                "hotelRates": formatted_rates
            }

            return self._make_request('POST', 'rates/update', data=data)
        except Exception as e:
            raise Exception(f"Error syncing rates with MakeMyTrip: {str(e)}")

    def sync_inventory(self, room_inventory):
        """Sync room inventory with MakeMyTrip"""
        try:
            formatted_inventory = []
            for inventory in room_inventory:
                formatted_inventory.append({
                    "roomTypeId": inventory["ota_room_id"],
                    "dateRange": {
                        "startDate": inventory["start_date"],
                        "endDate": inventory["end_date"]
                    },
                    "inventory": {
                        "availableRooms": inventory["available_rooms"]
                    }
                })

            data = {
                "roomInventory": formatted_inventory
            }

            return self._make_request('POST', 'inventory/update', data=data)
        except Exception as e:
            raise Exception(f"Error syncing inventory with MakeMyTrip: {str(e)}")

    def get_bookings(self, start_date=None, end_date=None):
        """Get bookings from MakeMyTrip"""
        try:
            params = {}
            if start_date:
                params['fromDate'] = start_date
            if end_date:
                params['toDate'] = end_date

            response = self._make_request('GET', 'bookings', params=params)
            
            # Format bookings to standardized structure
            formatted_bookings = []
            for booking in response.get('bookings', []):
                formatted_bookings.append({
                    'booking_id': booking['bookingId'],
                    'channel': 'makemytrip',
                    'guest': {
                        'name': booking['guestDetails']['name'],
                        'email': booking['guestDetails']['email'],
                        'phone': booking['guestDetails'].get('phone', '')
                    },
                    'room': {
                        'room_id': booking['roomTypeId'],
                        'room_type': booking['roomTypeName']
                    },
                    'dates': {
                        'check_in': booking['checkInDate'],
                        'check_out': booking['checkOutDate']
                    },
                    'amount': {
                        'total': booking['totalAmount'],
                        'currency': booking['currencyCode']
                    },
                    'status': booking['bookingStatus'],
                    'created_at': booking['createdAt']
                })

            return formatted_bookings
        except Exception as e:
            raise Exception(f"Error getting bookings from MakeMyTrip: {str(e)}")

    def update_booking_status(self, booking_id, new_status):
        """Update booking status on MakeMyTrip"""
        try:
            data = {
                "bookingId": booking_id,
                "status": new_status
            }
            
            return self._make_request('PUT', f'bookings/{booking_id}/status', data=data)
        except Exception as e:
            raise Exception(f"Error updating booking status on MakeMyTrip: {str(e)}")

    def check_health(self):
        """Check API connectivity and authentication"""
        try:
            response = self._make_request('GET', 'health')
            return {
                'status': 'connected',
                'systemStatus': response.get('status'),
                'serverTime': response.get('timestamp')
            }
        except Exception as e:
            raise Exception(f"MakeMyTrip health check failed: {str(e)}")

    def _format_error_response(self, error_code, message):
        """Format error response"""
        return {
            'error': {
                'code': error_code,
                'message': message
            }
        }
