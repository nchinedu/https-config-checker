function calculate() {
    const username = document.getElementById('username').value;
    const microscope_size = document.getElementById('microscope_size').value;
    const magnification = document.getElementById('magnification').value;

    if (!username || !microscope_size || !magnification) {
alert('Please fill in all fields');
return;
    }

    fetch('/calculate', {
method: 'POST',
headers: {
    'Content-Type': 'application/json',
},
body: JSON.stringify({
    username: username,
    microscope_size: microscope_size,
    magnification: magnification
})
    })
    .then(response => response.json())
    .then(data => {
if (data.success) {
    document.getElementById('result').innerHTML = 
`Original size of specimen: ${data.result} µm`;
    loadRecentMeasurements();
} else {
    alert('Error: ' + data.error);
}
    });
}

function loadRecentMeasurements() {
    fetch('/recent-measurements')
    .then(response => response.json())
    .then(data => {
const tbody = document.getElementById('measurements');
tbody.innerHTML = '';
data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
<td>${row[0]}</td>
<td>${row[1]}</td>
<td>${row[2]}</td>
<td>${row[3]}</td>
    `;
    tbody.appendChild(tr);
});
    });
}

// Load measurements when page loads
loadRecentMeasurements();