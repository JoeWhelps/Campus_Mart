function showModal(listingId) {
    // Fetch listing details dynamically via an AJAX request
    fetch(`/api/listings/${listingId}/`)
        .then(response => response.json())
        .then(data => {
            const modalBody = document.querySelector('.modal-body');
            modalBody.innerHTML = `
                <div class="modal-header">
                    <h3 class="text-secondary">${data.title}</h3>
                </div>
                <div class="modal-content-grid">
                    <div class="modal-image">
                        <img src="${data.photo_url}" class="img-fluid rounded" alt="${data.title}">
                    </div>
                    <div class="modal-details">
                        <div class="price-section">
                            <h4 class="text-primary">$${data.price}</h4>
                            <span class="badge ${data.status === 'Available' ? 'badge-success' : 'badge-secondary'}">${data.status}</span>
                        </div>
                        <div class="details-section">
                            <p><strong>Condition:</strong> ${data.condition}</p>
                            <p class="description">${data.description}</p>
                        </div>
                        <div class="seller-section">
                            <h5>Seller Information</h5>
                            <p><strong>Name:</strong> ${data.seller_username}</p>
                            <p><strong>Email:</strong> ${data.seller_email}</p>
                        </div>
                        <div class="dates-section text-muted">
                            <small>Posted: ${data.created_at}</small>
                            ${data.updated_at ? `<br><small>Last Updated: ${data.updated_at}</small>` : ''}
                        </div>
                    </div>
                </div>
            `;

            // Add styles dynamically
            const style = document.createElement('style');
            style.textContent = `
                .modal-content-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 2rem;
                    margin-top: 1rem;
                }
                
                .modal-image img {
                    width: 100%;
                    height: auto;
                    max-height: 400px;
                    object-fit: contain;
                }
                
                .modal-details {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }
                
                .price-section {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }
                
                .badge {
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    font-size: 0.875rem;
                }
                
                .badge-success {
                    background-color: #28a745;
                    color: white;
                }
                
                .badge-secondary {
                    background-color: #6c757d;
                    color: white;
                }
                
                .description {
                    line-height: 1.6;
                }
                
                @media (max-width: 768px) {
                    .modal-content-grid {
                        grid-template-columns: 1fr;
                    }
                }
            `;
            modalBody.appendChild(style);

            const modal = document.getElementById('listingModal');
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            const modalBody = document.querySelector('.modal-body');
            modalBody.innerHTML = `
                <div class="error-message">
                    <h4>Error</h4>
                    <p>Failed to load listing details. Please try again later.</p>
                </div>
            `;
            const modal = document.getElementById('listingModal');
            modal.style.display = 'block';
        });
}

function closeModal() {
    const modal = document.getElementById('listingModal');
    modal.style.display = 'none';
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('listingModal');
    if (event.target == modal) {
        closeModal();
    }
} 