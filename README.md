# Hotel OTA Channel Manager API

A comprehensive API for managing multiple Online Travel Agency (OTA) channels like Booking.com, MakeMyTrip, and Expedia in a single interface.

## Features

- Unified API for multiple OTA channels
- Real-time rate and inventory synchronization
- Booking management across channels
- Channel-specific settings management
- Health monitoring for OTA connections

## Supported OTA Channels

- Booking.com
- MakeMyTrip
- Expedia

## API Endpoints

### OTA Settings

- `GET /api/settings/` - Get all OTA channel settings
- `GET /api/settings/<id>` - Get specific OTA channel setting
- `POST /api/settings/` - Create new OTA channel setting
- `PUT /api/settings/<id>` - Update OTA channel setting
- `DELETE /api/settings/<id>` - Delete OTA channel setting

### Rate Mapping

- `GET /api/settings/<id>/rates` - Get rate mappings for an OTA channel
- `POST /api/settings/<id>/rates` - Create new rate mapping

### Room Mapping

- `GET /api/settings/<id>/rooms` - Get room mappings for an OTA channel
- `POST /api/settings/<id>/rooms` - Create new room mapping

### Channel Management

- `POST /api/channels/sync/rates` - Sync rates with all active channels
- `POST /api/channels/sync/inventory` - Sync inventory with all active channels
- `GET /api/channels/bookings` - Get bookings from all channels
- `PUT /api/channels/bookings/<id>/status` - Update booking status
- `GET /api/channels/health-check` - Check health of all channel connections

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## API Usage Examples

### Create OTA Channel Setting

```bash
curl -X POST http://localhost:5000/api/settings/ \
  -H "Content-Type: application/json" \
  -d '{
    "channel_name": "Booking.com Main",
    "channel_type": "booking.com",
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "hotel_id": "your_hotel_id",
    "sync_rates": true,
    "sync_inventory": true,
    "sync_bookings": true
  }'
```

### Sync Rates

```bash
curl -X POST http://localhost:5000/api/channels/sync/rates \
  -H "Content-Type: application/json" \
  -d '{
    "room_rates": [
      {
        "ota_room_id": "room123",
        "ota_rate_plan_id": "rate456",
        "start_date": "2024-01-01",
        "end_date": "2024-01-07",
        "amount": 100.00,
        "currency": "USD"
      }
    ]
  }'
```

### Get Bookings

```bash
curl -X GET "http://localhost:5000/api/channels/bookings?start_date=2024-01-01&end_date=2024-01-31"
```

## Database Schema

### OTASettings
- id (Primary Key)
- channel_name
- channel_type
- api_key
- api_secret
- hotel_id
- is_active
- sync_rates
- sync_inventory
- sync_bookings
- webhook_url
- created_at
- updated_at

### RateMapping
- id (Primary Key)
- ota_settings_id (Foreign Key)
- hotel_rate_plan_id
- ota_rate_plan_id
- markup_percentage
- is_active
- created_at
- updated_at

### RoomMapping
- id (Primary Key)
- ota_settings_id (Foreign Key)
- hotel_room_id
- ota_room_id
- is_active
- created_at
- updated_at

## Error Handling

The API returns standard HTTP status codes and JSON responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Security

- API authentication required for all endpoints
- Sensitive data (API keys, secrets) are never returned in responses
- CORS enabled for frontend integration
- Rate limiting implemented to prevent abuse

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License
