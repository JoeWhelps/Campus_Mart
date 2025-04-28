// static/js/modal.js

function showModal(listingId) {
    fetch(`/listings/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            const modalBody = document.querySelector('.modal-body');
            modalBody.innerHTML = `
                <h3>${data.title}</h3>
                <img src="${data.photo_url}" class="img-fluid mb-3" alt="Product Image">
                <p>${data.description}</p>
                <p>Price: $${data.price}</p>
                <p>Contact: ${data.contact}</p>
            `;
            const modal = document.getElementById('listingModal');
            modal.style.display = 'block';
        });
}

function closeModal() {
    const modal = document.getElementById('listingModal');
    modal.style.display = 'none';
}


