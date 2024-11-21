function getRandomFact(topic) {
    fetch(`/get_fact/${topic}`)
        .then(response => {
            if (!response.ok) {  // Check if the response is not ok
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            const factArea = document.getElementById('factArea');
            const factContent = document.getElementById('factContent');
            factContent.textContent = data;  // Update fact content
            factArea.style.display = 'block';  // Make the fact area visible
        })
        .catch(error => {
            console.error("Error fetching fact:", error);  // Log the specific error
            const factArea = document.getElementById('factArea');
            const factContent = document.getElementById('factContent');
            factContent.textContent = "An error occurred while fetching the fact.";  // Display a more detailed error
            factArea.style.display = 'block';
        });
}
