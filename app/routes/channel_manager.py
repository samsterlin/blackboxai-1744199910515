from flask import Blueprint, request, jsonify
from app import db
from app.models.ota_settings import OTASettings
from app.services.booking_com import BookingComService
from app.services.makemytrip import MakeMyTripService
from app.services.expedia import ExpediaService

channel_manager_bp = Blueprint('channel_manager', __name__)

def get_channel_service(channel_type, api_key, api_secret):
    """Factory method to get appropriate channel service"""
    if channel_type == 'booking.com':
        return BookingComService(api_key, api_secret)
    elif channel_type == 'makemytrip':
        return MakeMyTripService(api_key, api_secret)
    elif channel_type == 'expedia':
        return ExpediaService(api_key, api_secret)
    else:
        raise ValueError(f"Unsupported channel type: {channel_type}")

@channel_manager_bp.route('/sync/rates', methods=['POST'])
def sync_rates():
    """Sync rates with all active OTA channels"""
    try:
        data = request.get_json()
        room_rates = data.get('room_rates', [])
        
        # Get all active OTA settings
        active_settings = OTASettings.query.filter_by(
            is_active=True,
            sync_rates=True
        ).all()
        
        results = []
        for setting in active_settings:
            try:
                # Get appropriate channel service
                service = get_channel_service(
                    setting.channel_type,
                    setting.api_key,
                    setting.api_secret
                )
                
                # Sync rates for this channel
                sync_result = service.sync_rates(room_rates)
                results.append({
                    'channel': setting.channel_name,
                    'status': 'success',
                    'message': sync_result
                })
            except Exception as e:
                results.append({
                    'channel': setting.channel_name,
                    'status': 'error',
                    'message': str(e)
                })
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@channel_manager_bp.route('/sync/inventory', methods=['POST'])
def sync_inventory():
    """Sync inventory with all active OTA channels"""
    try:
        data = request.get_json()
        room_inventory = data.get('room_inventory', [])
        
        # Get all active OTA settings
        active_settings = OTASettings.query.filter_by(
            is_active=True,
            sync_inventory=True
        ).all()
        
        results = []
        for setting in active_settings:
            try:
                # Get appropriate channel service
                service = get_channel_service(
                    setting.channel_type,
                    setting.api_key,
                    setting.api_secret
                )
                
                # Sync inventory for this channel
                sync_result = service.sync_inventory(room_inventory)
                results.append({
                    'channel': setting.channel_name,
                    'status': 'success',
                    'message': sync_result
                })
            except Exception as e:
                results.append({
                    'channel': setting.channel_name,
                    'status': 'error',
                    'message': str(e)
                })
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@channel_manager_bp.route('/bookings', methods=['GET'])
def get_bookings():
    """Get bookings from all active OTA channels"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Get all active OTA settings
        active_settings = OTASettings.query.filter_by(
            is_active=True,
            sync_bookings=True
        ).all()
        
        all_bookings = []
        for setting in active_settings:
            try:
                # Get appropriate channel service
                service = get_channel_service(
                    setting.channel_type,
                    setting.api_key,
                    setting.api_secret
                )
                
                # Get bookings from this channel
                channel_bookings = service.get_bookings(start_date, end_date)
                all_bookings.extend(channel_bookings)
            except Exception as e:
                # Log the error but continue with other channels
                print(f"Error getting bookings from {setting.channel_name}: {str(e)}")
        
        return jsonify({
            'success': True,
            'data': all_bookings
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@channel_manager_bp.route('/bookings/<string:booking_id>/status', methods=['PUT'])
def update_booking_status(booking_id):
    """Update booking status on the respective OTA channel"""
    try:
        data = request.get_json()
        channel_type = data.get('channel_type')
        new_status = data.get('status')
        
        # Get the OTA setting
        setting = OTASettings.query.filter_by(
            channel_type=channel_type,
            is_active=True
        ).first()
        
        if not setting:
            return jsonify({
                'success': False,
                'message': f'No active setting found for channel: {channel_type}'
            }), 404
        
        # Get appropriate channel service
        service = get_channel_service(
            setting.channel_type,
            setting.api_key,
            setting.api_secret
        )
        
        # Update booking status
        result = service.update_booking_status(booking_id, new_status)
        
        return jsonify({
            'success': True,
            'message': 'Booking status updated successfully',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@channel_manager_bp.route('/health-check', methods=['GET'])
def check_channel_health():
    """Check health/connectivity of all active OTA channels"""
    try:
        # Get all active OTA settings
        active_settings = OTASettings.query.filter_by(is_active=True).all()
        
        results = []
        for setting in active_settings:
            try:
                # Get appropriate channel service
                service = get_channel_service(
                    setting.channel_type,
                    setting.api_key,
                    setting.api_secret
                )
                
                # Check channel health
                health_status = service.check_health()
                results.append({
                    'channel': setting.channel_name,
                    'status': 'online',
                    'details': health_status
                })
            except Exception as e:
                results.append({
                    'channel': setting.channel_name,
                    'status': 'offline',
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
