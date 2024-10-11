// script.js

document.getElementById('stock-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get form values
    const open = document.getElementById('open').value;
    const high = document.getElementById('high').value;
    const low = document.getElementById('low').value;
    const close = document.getElementById('close').value;
    const volume = document.getElementById('volume').value;

    // Validate inputs
    if (!open || !high || !low || !close || !volume) {
        alert('Please fill in all fields.');
        return;
    }

    // Prepare data
    const data = {
        Open: parseFloat(open),
        High: parseFloat(high),
        Low: parseFloat(low),
        Close: parseFloat(close),
        Volume: parseInt(volume)
    };

    // Send POST request to the backend
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if(result.error){
            alert(result.error);
            return;
        }
        document.getElementById('score').innerText = `Score: ${result.Recommendation_Score}`;
        document.getElementById('suggestion').innerText = `Suggestion: ${result.Suggestion}`;
        document.getElementById('result').classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching the recommendation.');
    });
});


