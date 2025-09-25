/**
 * Carrinho de Compras - JavaScript
 * Funcionalidades AJAX para atualização em tempo real
 */

class CarrinhoManager {
    constructor() {
        this.baseUrl = window.location.origin;
        this.csrfToken = this.getCsrfToken();
        this.debounceTimeout = null;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    bindEvents() {
        // Quantity controls
        document.addEventListener('click', (e) => {
            // Use closest to ensure clicks on icons inside buttons are handled
            const plusBtn = e.target.closest('.quantity-btn-plus');
            const minusBtn = e.target.closest('.quantity-btn-minus');
            const removeBtn = e.target.closest('.remove-btn');
            const clearCartBtn = e.target.closest('.btn-clear-cart');

            if (plusBtn) {
                this.handleQuantityChange(plusBtn, 'plus');
            } else if (minusBtn) {
                this.handleQuantityChange(minusBtn, 'minus');
            } else if (removeBtn) {
                this.handleRemoveItem(removeBtn);
            } else if (clearCartBtn) {
                this.handleClearCart();
            }
        });

        // Quantity input direct change
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('quantity-input')) {
                this.handleQuantityInput(e.target);
            }
        });
    }

    handleQuantityChange(button, action) {
        const itemRow = button.closest('.cart-item');
        const itemId = itemRow.dataset.itemId;
        const input = itemRow.querySelector('.quantity-input');
        let currentQuantity = parseInt(input.value) || 1;

        if (action === 'plus') {
            currentQuantity += 1;
        } else if (action === 'minus' && currentQuantity > 1) {
            currentQuantity -= 1;
        } else {
            return; // Don't allow quantity less than 1
        }

        input.value = currentQuantity;
        this.updateQuantity(itemId, currentQuantity, itemRow);
    }

    handleQuantityInput(input) {
        clearTimeout(this.debounceTimeout);
        
        this.debounceTimeout = setTimeout(() => {
            const itemRow = input.closest('.cart-item');
            const itemId = itemRow.dataset.itemId;
            let quantity = parseInt(input.value) || 1;

            if (quantity < 1) {
                quantity = 1;
                input.value = quantity;
            }

            this.updateQuantity(itemId, quantity, itemRow);
        }, 500); // 500ms debounce
    }

    async updateQuantity(itemId, quantidade, itemRow) {
        try {
            this.setLoading(itemRow, true);

            const response = await fetch(`${this.baseUrl}/ajax/atualizar-quantidade/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                },
                body: JSON.stringify({
                    item_id: itemId,
                    quantidade: quantidade
                })
            });

            const data = await response.json();

            if (data.success) {
                // Update item total
                const itemTotal = itemRow.querySelector('.item-total');
                itemTotal.textContent = this.formatCurrency(data.item_total);

                // Update cart total
                this.updateCartTotal(data.pedido_total);

                // Show success feedback
                this.showFeedback('Quantidade atualizada!', 'success');
            } else {
                throw new Error(data.error || 'Erro ao atualizar quantidade');
            }
        } catch (error) {
            console.error('Erro:', error);
            this.showFeedback('Erro ao atualizar quantidade', 'error');
        } finally {
            this.setLoading(itemRow, false);
        }
    }

    async handleRemoveItem(button) {
        const itemRow = button.closest('.cart-item');
        const itemId = itemRow.dataset.itemId;
        const productName = itemRow.querySelector('.product-name').textContent;

        // Show confirmation modal
        if (!await this.showConfirmationModal(
            'Remover Item',
            `Tem certeza que deseja remover "${productName}" do carrinho?`,
            'Remover',
            'btn-danger'
        )) {
            return;
        }

        try {
            this.setLoading(itemRow, true);

            const response = await fetch(`${this.baseUrl}/ajax/remover-item/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                },
                body: JSON.stringify({
                    item_id: itemId
                })
            });

            const data = await response.json();

            if (data.success) {
                // Remove item with animation
                itemRow.style.transition = 'all 0.3s ease';
                itemRow.style.opacity = '0';
                itemRow.style.transform = 'translateX(-100%)';

                setTimeout(() => {
                    itemRow.remove();
                    this.updateCartTotal(data.pedido_total);

                    // Check if cart is empty
                    if (data.items_count === 0) {
                        this.showEmptyCart();
                    }
                }, 300);

                this.showFeedback('Item removido do carrinho!', 'success');
            } else {
                throw new Error(data.error || 'Erro ao remover item');
            }
        } catch (error) {
            this.setLoading(itemRow, false);
            console.error('Erro:', error);
            this.showFeedback('Erro ao remover item', 'error');
        }
    }

    async handleClearCart() {
        // Show confirmation modal
        if (!await this.showConfirmationModal(
            'Esvaziar Carrinho',
            'Tem certeza que deseja remover todos os itens do carrinho? Esta ação não pode ser desfeita.',
            'Esvaziar Carrinho',
            'btn-danger'
        )) {
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/ajax/esvaziar-carrinho/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showEmptyCart();
                this.showFeedback(data.message, 'success');
            } else {
                throw new Error(data.error || 'Erro ao esvaziar carrinho');
            }
        } catch (error) {
            console.error('Erro:', error);
            this.showFeedback('Erro ao esvaziar carrinho', 'error');
        }
    }

    updateCartTotal(total) {
        const totalElement = document.querySelector('.cart-total');
        if (totalElement) {
            totalElement.textContent = this.formatCurrency(total);
        }
    }

    showEmptyCart() {
        const cartBody = document.querySelector('.cart-body');
        if (cartBody) {
            cartBody.innerHTML = `
                <div class="empty-cart">
                    <div class="empty-cart-icon">
                        <i class="fas fa-shopping-cart"></i>
                    </div>
                    <h3>Seu carrinho está vazio</h3>
                    <p>Adicione produtos do nosso catálogo para começar suas compras!</p>
                    <a href="/catalogo/" class="btn btn-primary btn-lg mt-3">
                        <i class="fas fa-leaf me-2"></i>Ver Catálogo
                    </a>
                </div>
            `;
        }

        // Hide cart summary
        const cartSummary = document.querySelector('.cart-summary');
        if (cartSummary) {
            cartSummary.style.display = 'none';
        }
    }

    setLoading(itemRow, isLoading) {
        if (isLoading) {
            itemRow.classList.add('loading');
        } else {
            itemRow.classList.remove('loading');
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }

    showFeedback(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert-cart');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
        
        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-cart d-flex align-items-center`;
        alert.innerHTML = `
            <i class="${icon} me-2"></i>
            <span>${message}</span>
        `;

        // Insert at top of cart
        const container = document.querySelector('.cart-container .container');
        if (container) {
            container.insertBefore(alert, container.firstChild);
        }

        // Auto-remove after 3 seconds
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    }

    showConfirmationModal(title, message, confirmText, confirmClass) {
        return new Promise((resolve) => {
            // Create modal
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn ${confirmClass} confirm-action">${confirmText}</button>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            // Show modal
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();

            // Handle buttons
            modal.querySelector('.confirm-action').addEventListener('click', () => {
                bsModal.hide();
                resolve(true);
            });

            modal.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
                btn.addEventListener('click', () => {
                    bsModal.hide();
                    resolve(false);
                });
            });

            // Clean up when modal is hidden
            modal.addEventListener('hidden.bs.modal', () => {
                modal.remove();
            });
        });
    }
}

// Initialize cart manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CarrinhoManager();
});