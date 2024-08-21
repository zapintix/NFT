document.getElementById('nftForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('price', document.getElementById('price').value);
    formData.append('typePrice', document.getElementById('typePrice').value);
    formData.append('cat', document.getElementById('cat').value);
    formData.append('autor', document.getElementById('autor').value);

    let imageInput = document.getElementById('image');
    if (imageInput.files.length > 0) {
        formData.append('image', imageInput.files[0]);
    }

    // Получаем CSRF-токен из куки
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/v1/nfts/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(err => { throw err; });
        }
    })
    .then(data => {
        document.getElementById('result').innerText = 'NFT успешно добавлено: ' + JSON.stringify(data);
    })
    .catch(error => {
        document.getElementById('result').innerText = 'Ошибка: ' + JSON.stringify(error);
    });
});
