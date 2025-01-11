document.addEventListener('DOMContentLoaded', function () {
    console.log('JavaScript Loaded Successfully!');

    const form = document.querySelector('#recommend-form');
    const recommendations = document.querySelector('#recommendations');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const userId = document.querySelector('#user_id').value;

            fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    recommendations.innerHTML = '';
                    data.forEach((movie) => {
                        const li = document.createElement('li');
                        li.textContent = movie;
                        recommendations.appendChild(li);
                    });
                })
                .catch((error) => console.error('Error:', error));
        });
    }
});
