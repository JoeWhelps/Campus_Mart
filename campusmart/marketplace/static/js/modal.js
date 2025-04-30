// static/js/modal.js

function showModal(listingId) {
    // Fetch listing details dynamically via an AJAX request
    fetch(`/marketplace/listings/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            const modalBody = document.querySelector('.modal-body');
            modalBody.innerHTML = `
                <h3>${data.title}</h3>
                <img src="${data.photo_url}" class="img-fluid mb-3" alt="Product Image">
                <p>${data.description}</p>
                <p>Price: $${data.price}</p>
                <p>Contact: ${data.contact}</p>
                <p>Seller: ${data.seller_username}</p>
                <p>Seller Email: ${data.seller_email}</p>
            `;
            // Populate all modal fields with the listing data
            document.getElementById('modalImage').src = data.photo_url;
            document.getElementById('modalImage').alt = data.title;
            document.getElementById('modalTitle').textContent = data.title;
            document.getElementById('modalDescription').textContent = data.description;
            document.getElementById('modalPrice').textContent = data.price;
            document.getElementById('modalCondition').textContent = data.condition || 'Not specified';
            document.getElementById('modalStatus').textContent = data.status || 'Available';
            document.getElementById('modalDate').textContent = data.created_at || 'Not specified';
            document.getElementById('modalUpdated').textContent = data.updated_at || 'Not specified';
            document.getElementById('modalSeller').textContent = data.seller_username;
            document.getElementById('modalEmail').textContent = data.seller_email || 'Not provided';
            
            // Set up the links
            document.getElementById('modalDetailLink').href = `/marketplace/listings/${listingId}/`;
            document.getElementById('modalMessageLink').href = `/messaging/new/${data.seller_id}/`;

            // Show the modal using Bootstrap 5
            const modalElement = document.getElementById('listingModal');
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching listing details:', error);
            alert('Error loading listing details. Please try again.');
        });
}

// The closeModal function is no longer needed as Bootstrap handles closing
// through the data-bs-dismiss attribute on the close button

