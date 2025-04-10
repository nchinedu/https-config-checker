function calculate() {
    const username = document.getElementById('username').value;
    const microscope_size = parseFloat(document.getElementById('microscope_size').value);
    const magnification = parseInt(document.getElementById('magnification').value);

    if (!username || !microscope_size || !magnification) {
        alert('Please fill in all fields');
        return;
    }

    const actual_size = (microscope_size / magnification) * 1000;
    
    // Save to localStorage
    const measurement = {
        username,
        microscope_size,
        actual_size,
        date_added: new Date().toISOString()
    };

    let measurements = JSON.parse(localStorage.getItem('measurements') || '[]');
    measurements.unshift(measurement);
    measurements = measurements.slice(0, 5); // Keep only last 5
    localStorage.setItem('measurements', JSON.stringify(measurements));

    // Display result
    document.getElementById('result').textContent = 
        `Original size of specimen: ${actual_size.toFixed(2)} µm`;

    updateMeasurementTable();
}

function updateMeasurementTable() {
    const measurements = JSON.parse(localStorage.getItem('measurements') || '[]');
    const tbody = document.getElementById('measurements');
    tbody.innerHTML = '';

    measurements.forEach(m => {
        const row = tbody.insertRow();
        row.insertCell().textContent = m.username;
        row.insertCell().textContent = m.microscope_size;
        row.insertCell().textContent = `${m.actual_size.toFixed(2)}`;
        row.insertCell().textContent = new Date(m.date_added).toLocaleString();
    });
}

// Load measurements on page load
document.addEventListener('DOMContentLoaded', updateMeasurementTable);