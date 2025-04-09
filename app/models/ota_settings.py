from app import db
from datetime import datetime

class OTASettings(db.Model):
    """Model for storing OTA channel settings"""
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(100), nullable=False)
    channel_type = db.Column(db.String(50), nullable=False)  # booking.com, makemytrip, expedia
    api_key = db.Column(db.String(255))
    api_secret = db.Column(db.String(255))
    hotel_id = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    sync_rates = db.Column(db.Boolean, default=True)
    sync_inventory = db.Column(db.Boolean, default=True)
    sync_bookings = db.Column(db.Boolean, default=True)
    webhook_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'channel_name': self.channel_name,
            'channel_type': self.channel_type,
            'hotel_id': self.hotel_id,
            'is_active': self.is_active,
            'sync_rates': self.sync_rates,
            'sync_inventory': self.sync_inventory,
            'sync_bookings': self.sync_bookings,
            'webhook_url': self.webhook_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RateMapping(db.Model):
    """Model for mapping hotel room rates to OTA rates"""
    id = db.Column(db.Integer, primary_key=True)
    ota_settings_id = db.Column(db.Integer, db.ForeignKey('ota_settings.id'), nullable=False)
    hotel_rate_plan_id = db.Column(db.String(100), nullable=False)
    ota_rate_plan_id = db.Column(db.String(100), nullable=False)
    markup_percentage = db.Column(db.Float, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'ota_settings_id': self.ota_settings_id,
            'hotel_rate_plan_id': self.hotel_rate_plan_id,
            'ota_rate_plan_id': self.ota_rate_plan_id,
            'markup_percentage': self.markup_percentage,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RoomMapping(db.Model):
    """Model for mapping hotel rooms to OTA rooms"""
    id = db.Column(db.Integer, primary_key=True)
    ota_settings_id = db.Column(db.Integer, db.ForeignKey('ota_settings.id'), nullable=False)
    hotel_room_id = db.Column(db.String(100), nullable=False)
    ota_room_id = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'ota_settings_id': self.ota_settings_id,
            'hotel_room_id': self.hotel_room_id,
            'ota_room_id': self.ota_room_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
