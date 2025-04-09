from flask import Blueprint, request, jsonify
from app import db
from app.models.ota_settings import OTASettings, RateMapping, RoomMapping
from datetime import datetime

ota_settings_bp = Blueprint('ota_settings', __name__)

@ota_settings_bp.route('/', methods=['GET'])
def get_all_settings():
    """Get all OTA channel settings"""
    try:
        settings = OTASettings.query.all()
        return jsonify({
            'success': True,
            'data': [setting.to_dict() for setting in settings]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@ota_settings_bp.route('/<int:setting_id>', methods=['GET'])
def get_setting(setting_id):
    """Get specific OTA channel setting"""
    try:
        setting = OTASettings.query.get_or_404(setting_id)
        return jsonify({
            'success': True,
            'data': setting.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404

@ota_settings_bp.route('/', methods=['POST'])
def create_setting():
    """Create new OTA channel setting"""
    try:
        data = request.get_json()
        new_setting = OTASettings(
            channel_name=data['channel_name'],
            channel_type=data['channel_type'],
            api_key=data.get('api_key'),
            api_secret=data.get('api_secret'),
            hotel_id=data.get('hotel_id'),
            sync_rates=data.get('sync_rates', True),
            sync_inventory=data.get('sync_inventory', True),
            sync_bookings=data.get('sync_bookings', True),
            webhook_url=data.get('webhook_url')
        )
        db.session.add(new_setting)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'OTA setting created successfully',
            'data': new_setting.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@ota_settings_bp.route('/<int:setting_id>', methods=['PUT'])
def update_setting(setting_id):
    """Update existing OTA channel setting"""
    try:
        setting = OTASettings.query.get_or_404(setting_id)
        data = request.get_json()
        
        setting.channel_name = data.get('channel_name', setting.channel_name)
        setting.channel_type = data.get('channel_type', setting.channel_type)
        setting.api_key = data.get('api_key', setting.api_key)
        setting.api_secret = data.get('api_secret', setting.api_secret)
        setting.hotel_id = data.get('hotel_id', setting.hotel_id)
        setting.sync_rates = data.get('sync_rates', setting.sync_rates)
        setting.sync_inventory = data.get('sync_inventory', setting.sync_inventory)
        setting.sync_bookings = data.get('sync_bookings', setting.sync_bookings)
        setting.webhook_url = data.get('webhook_url', setting.webhook_url)
        setting.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'OTA setting updated successfully',
            'data': setting.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@ota_settings_bp.route('/<int:setting_id>', methods=['DELETE'])
def delete_setting(setting_id):
    """Delete OTA channel setting"""
    try:
        setting = OTASettings.query.get_or_404(setting_id)
        db.session.delete(setting)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'OTA setting deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# Rate Mapping Routes
@ota_settings_bp.route('/<int:setting_id>/rates', methods=['GET'])
def get_rate_mappings(setting_id):
    """Get all rate mappings for an OTA channel"""
    try:
        mappings = RateMapping.query.filter_by(ota_settings_id=setting_id).all()
        return jsonify({
            'success': True,
            'data': [mapping.to_dict() for mapping in mappings]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@ota_settings_bp.route('/<int:setting_id>/rates', methods=['POST'])
def create_rate_mapping(setting_id):
    """Create new rate mapping"""
    try:
        data = request.get_json()
        new_mapping = RateMapping(
            ota_settings_id=setting_id,
            hotel_rate_plan_id=data['hotel_rate_plan_id'],
            ota_rate_plan_id=data['ota_rate_plan_id'],
            markup_percentage=data.get('markup_percentage', 0)
        )
        db.session.add(new_mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Rate mapping created successfully',
            'data': new_mapping.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# Room Mapping Routes
@ota_settings_bp.route('/<int:setting_id>/rooms', methods=['GET'])
def get_room_mappings(setting_id):
    """Get all room mappings for an OTA channel"""
    try:
        mappings = RoomMapping.query.filter_by(ota_settings_id=setting_id).all()
        return jsonify({
            'success': True,
            'data': [mapping.to_dict() for mapping in mappings]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@ota_settings_bp.route('/<int:setting_id>/rooms', methods=['POST'])
def create_room_mapping(setting_id):
    """Create new room mapping"""
    try:
        data = request.get_json()
        new_mapping = RoomMapping(
            ota_settings_id=setting_id,
            hotel_room_id=data['hotel_room_id'],
            ota_room_id=data['ota_room_id']
        )
        db.session.add(new_mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Room mapping created successfully',
            'data': new_mapping.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
