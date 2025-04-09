// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// Fetch all OTA settings
async function fetchOTASettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/settings/`);
        const data = await response.json();
        if (data.success) {
            renderOTASettings(data.data);
        } else {
            showError('Failed to fetch OTA settings');
        }
    } catch (error) {
        showError('Error connecting to the server');
        console.error('Error:', error);
    }
}

// Render OTA settings cards
function renderOTASettings(settings) {
    const container = document.getElementById('ota-channels');
    container.innerHTML = '';

    settings.forEach(setting => {
        const card = createChannelCard(setting);
        container.appendChild(card);
    });
}

// Create channel card
function createChannelCard(setting) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-sm p-6';
    
    const statusClass = setting.is_active ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800';
    const statusText = setting.is_active ? 'Active' : 'Inactive';
    
    card.innerHTML = `
        <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
                <img src="${getChannelLogo(setting.channel_type)}" alt="${setting.channel_name}" class="w-8 h-8 mr-3">
                <h3 class="text-lg font-semibold">${setting.channel_name}</h3>
            </div>
            <span class="px-2 py-1 ${statusClass} rounded text-sm">${statusText}</span>
        </div>
        <div class="space-y-3 mb-4">
            <div>
                <label class="text-sm text-gray-600">Hotel ID</label>
                <p class="font-medium">${setting.hotel_id}</p>
            </div>
            <div>
                <label class="text-sm text-gray-600">Last Sync</label>
                <p class="font-medium">${formatDate(setting.updated_at)}</p>
            </div>
            <div>
                <label class="text-sm text-gray-600">Sync Status</label>
                <div class="flex items-center mt-1">
                    ${getSyncStatusIcons(setting)}
                </div>
            </div>
        </div>
        <div class="flex space-x-2">
            <button onclick="editChannel('${setting.id}')" class="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded hover:bg-gray-200 transition duration-300">
                <i class="fas fa-edit mr-2"></i>Edit
            </button>
            <button onclick="syncChannel('${setting.id}')" class="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded hover:bg-gray-200 transition duration-300">
                <i class="fas fa-sync-alt mr-2"></i>Sync Now
            </button>
        </div>
    `;
    
    return card;
}

// Get channel logo URL
function getChannelLogo(channelType) {
    const logos = {
        'booking.com': 'https://cf.bstatic.com/static/img/favicon/favicon-32x32.png',
        'makemytrip': 'https://imgak.mmtcdn.com/pwa_v3/pwa_hotel_assets/header/logo@2x.png',
        'expedia': 'https://www.expedia.com/_dms/header/logo.svg?locale=en_US&siteid=1&2'
    };
    return logos[channelType] || 'default-logo.png';
}

// Get sync status icons
function getSyncStatusIcons(setting) {
    return `
        <span class="mr-3">
            <i class="fas fa-${setting.sync_rates ? 'check' : 'times'}-circle text-${setting.sync_rates ? 'green' : 'red'}-500"></i>
            Rates
        </span>
        <span class="mr-3">
            <i class="fas fa-${setting.sync_inventory ? 'check' : 'times'}-circle text-${setting.sync_inventory ? 'green' : 'red'}-500"></i>
            Inventory
        </span>
        <span>
            <i class="fas fa-${setting.sync_bookings ? 'check' : 'times'}-circle text-${setting.sync_bookings ? 'green' : 'red'}-500"></i>
            Bookings
        </span>
    `;
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleString();
}

// Add new channel
async function addChannel(formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/settings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        if (data.success) {
            closeAddModal();
            fetchOTASettings();
            showSuccess('Channel added successfully');
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Error adding channel');
        console.error('Error:', error);
    }
}

// Edit channel
async function editChannel(channelId) {
    try {
        const response = await fetch(`${API_BASE_URL}/settings/${channelId}`);
        const data = await response.json();
        if (data.success) {
            openEditModal(data.data);
        } else {
            showError('Failed to fetch channel details');
        }
    } catch (error) {
        showError('Error fetching channel details');
        console.error('Error:', error);
    }
}

// Update channel
async function updateChannel(channelId, formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/settings/${channelId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        if (data.success) {
            closeEditModal();
            fetchOTASettings();
            showSuccess('Channel updated successfully');
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Error updating channel');
        console.error('Error:', error);
    }
}

// Sync channel
async function syncChannel(channelId) {
    try {
        const response = await fetch(`${API_BASE_URL}/channels/sync/rates`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ channel_id: channelId })
        });
        
        const data = await response.json();
        if (data.success) {
            showSuccess('Channel sync initiated');
            fetchOTASettings();
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Error syncing channel');
        console.error('Error:', error);
    }
}

// Show success message
function showSuccess(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Show error message
function showError(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Modal functions
function openAddModal() {
    document.getElementById('addModal').classList.remove('hidden');
}

function closeAddModal() {
    document.getElementById('addModal').classList.add('hidden');
    document.getElementById('addChannelForm').reset();
}

function openEditModal(channelData) {
    const modal = document.getElementById('editModal');
    const form = document.getElementById('editChannelForm');
    
    // Populate form with channel data
    form.elements['channel_name'].value = channelData.channel_name;
    form.elements['channel_type'].value = channelData.channel_type;
    form.elements['hotel_id'].value = channelData.hotel_id;
    form.elements['sync_rates'].checked = channelData.sync_rates;
    form.elements['sync_inventory'].checked = channelData.sync_inventory;
    form.elements['sync_bookings'].checked = channelData.sync_bookings;
    
    form.dataset.channelId = channelData.id;
    modal.classList.remove('hidden');
}

function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchOTASettings();
    
    // Add channel form submission
    document.getElementById('addChannelForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            channel_name: formData.get('channel_name'),
            channel_type: formData.get('channel_type'),
            hotel_id: formData.get('hotel_id'),
            api_key: formData.get('api_key'),
            api_secret: formData.get('api_secret'),
            sync_rates: formData.get('sync_rates') === 'on',
            sync_inventory: formData.get('sync_inventory') === 'on',
            sync_bookings: formData.get('sync_bookings') === 'on'
        };
        addChannel(data);
    });
    
    // Edit channel form submission
    document.getElementById('editChannelForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const channelId = e.target.dataset.channelId;
        const data = {
            channel_name: formData.get('channel_name'),
            channel_type: formData.get('channel_type'),
            hotel_id: formData.get('hotel_id'),
            sync_rates: formData.get('sync_rates') === 'on',
            sync_inventory: formData.get('sync_inventory') === 'on',
            sync_bookings: formData.get('sync_bookings') === 'on'
        };
        updateChannel(channelId, data);
    });
});
