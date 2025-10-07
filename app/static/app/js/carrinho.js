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
    // Recalculate totals locally when user interacts (mirrors inline script from template)
    // Keeps the UI responsive while AJAX requests are processed.
    this.recalcTotalFromDOM();
    // Ensure minus buttons are correctly enabled/disabled on load
    this.updateAllDecreaseButtons();
    }

    getCsrfToken() {
        // Tenta pegar do input hidden primeiro (form)
        const inputToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (inputToken) return inputToken;
        
        // Fallback: pega do cookie (padrão Django)
        const cookieToken = document.cookie
            .split('; ')
            .find(cookie => cookie.startsWith('csrftoken='));
        return cookieToken ? cookieToken.split('=')[1] : '';
    }

    bindEvents() {
        // Quantity controls
        document.addEventListener('click', (e) => {
            // Use closest to ensure clicks on icons inside buttons are handled
            const plusBtn = e.target.closest('.quantity-btn-plus');
            const minusBtn = e.target.closest('.quantity-btn-minus');
            const removeBtn = e.target.closest('.remove-btn');
            const clearCartBtn = e.target.closest('.btn-clear-cart');
            const finalizeBtn = e.target.closest('#btn-finalize-order');

            if (plusBtn) {
                this.handleQuantityChange(plusBtn, 'plus');
            } else if (minusBtn) {
                this.handleQuantityChange(minusBtn, 'minus');
            } else if (removeBtn) {
                this.handleRemoveItem(removeBtn);
            } else if (clearCartBtn) {
                this.handleClearCart();
            } else if (finalizeBtn) {
                this.handleFinalizeOrder();
            }
        });

        // Quantity input direct change
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('quantity-input')) {
                const itemRow = e.target.closest('.cart-item');
                // Reflect decrease button state immediately while typing
                this.updateDecreaseButtonState(itemRow);
                this.handleQuantityInput(e.target);
            }
        });

        // Local total recalculation: keep cart total synchronized immediately on UI interactions
        document.addEventListener('click', (e) => {
            if (e.target.closest('.quantity-btn') || e.target.closest('.remove-btn')) {
                // wait a tick for DOM updates (animations/handlers) then recalc
                setTimeout(() => this.recalcTotalFromDOM(), 100);
            }
        });

        document.addEventListener('change', (e) => {
            if (e.target.classList && e.target.classList.contains('quantity-input')) {
                setTimeout(() => this.recalcTotalFromDOM(), 100);
            }
        });
    }

    // Recalculate cart total by summing visible .item-total elements (mirrors template logic)
    recalcTotalFromDOM() {
        let total = 0;
        document.querySelectorAll('.cart-item').forEach(function (item) {
            const el = item.querySelector('.item-total');
            if (!el) return;
            
            // Extrai o valor: "R$ 171.54" ou "R$ 171,54"
            let text = el.textContent.replace('R$', '').trim();
            
            // Remove espaços
            text = text.replace(/\s/g, '');
            
            // Normaliza para formato numérico JavaScript (ponto decimal)
            // Se tiver vírgula, assume formato brasileiro: 1.234,56 -> 1234.56
            // Se tiver só ponto, assume formato americano: 1,234.56 -> 1234.56
            if (text.includes(',')) {
                // Formato brasileiro: remove pontos (separador de milhar) e troca vírgula por ponto
                text = text.replace(/\./g, '').replace(',', '.');
            } else {
                // Formato americano: remove vírgulas (separador de milhar)
                text = text.replace(/,/g, '');
            }
            
            const price = parseFloat(text);
            if (!isNaN(price)) {
                total += price;
            }
        });

        const totalEl = document.getElementById('cart-total') || document.querySelector('.cart-total');
        if (totalEl) {
            // Formata em padrão americano (ponto decimal) para consistência
            totalEl.textContent = 'R$ ' + total.toFixed(2);
        }
    }

    handleQuantityChange(button, action) {
        const itemRow = button.closest('.cart-item');
        const itemId = itemRow.dataset.itemId;
        const input = itemRow.querySelector('.quantity-input');
        let currentQuantity = parseInt(input.value) || 1;

        // Guarda o valor anterior para rollback em caso de erro
        input.dataset.previousValue = currentQuantity;

        if (action === 'plus') {
            currentQuantity += 1;
        } else if (action === 'minus' && currentQuantity > 1) {
            currentQuantity -= 1;
        } else {
            return; // Don't allow quantity less than 1
        }

        // Validação máxima
        if (currentQuantity > 99) {
            this.showFeedback('Quantidade máxima é 99', 'error');
            return;
        }

        input.value = currentQuantity;
        // Update minus button state immediately so UI reflects allowed actions
        this.updateDecreaseButtonState(itemRow);
        this.updateQuantity(itemId, currentQuantity, itemRow);
    }

    handleQuantityInput(input) {
        clearTimeout(this.debounceTimeout);
        
        this.debounceTimeout = setTimeout(() => {
            const itemRow = input.closest('.cart-item');
            const itemId = itemRow.dataset.itemId;
            let quantity = parseInt(input.value) || 0;

            // Se quantidade for 0 ou menor, remover o item
            if (quantity <= 0) {
                const removeBtn = itemRow.querySelector('.remove-btn');
                if (removeBtn) {
                    this.handleRemoveItem(removeBtn);
                }
                return;
            }

            // Se quantidade for maior que 99, limitar a 99
            if (quantity > 99) {
                quantity = 99;
                input.value = quantity;
                this.showFeedback('Quantidade máxima é 99', 'error');
            }

            // Reflect the change in the minus button immediately
            this.updateDecreaseButtonState(itemRow);

            this.updateQuantity(itemId, quantity, itemRow);
        }, 500); // 500ms debounce
    }

    async updateQuantity(itemId, quantidade, itemRow) {
        try {
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

            // Verifica se a resposta HTTP foi bem-sucedida
            if (!response.ok) {
                // Tenta parsear erro do servidor
                let errorMessage = `Erro HTTP ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                    console.error('[CARRINHO] Erro do servidor:', errorData);
                } catch (e) {
                    // Se não conseguir parsear JSON, usa mensagem padrão
                    console.error('[CARRINHO] Erro ao parsear resposta de erro');
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            if (data.success) {
                // Update item total - usa formato simples com ponto decimal
                const itemTotal = itemRow.querySelector('.item-total');
                itemTotal.textContent = 'R$ ' + parseFloat(data.item_total).toFixed(2);

                // Ensure decrease button state matches the new quantity
                this.updateDecreaseButtonState(itemRow);

                // Update cart total
                this.updateCartTotal(data.pedido_total);

                // Show success feedback
                this.showFeedback('Quantidade atualizada!', 'success');
            } else {
                throw new Error(data.error || 'Erro ao atualizar quantidade');
            }
        } catch (error) {
            console.error('Erro ao atualizar quantidade:', error);
            
            // Mensagens de erro específicas
            let errorMsg = 'Erro ao atualizar quantidade';
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMsg = 'Erro de conexão. Verifique sua internet.';
            } else if (error.message) {
                errorMsg = error.message;
            }
            
            this.showFeedback(errorMsg, 'error');
            
            // Reverte a quantidade no input em caso de erro
            const input = itemRow.querySelector('.quantity-input');
            if (input && input.dataset.previousValue) {
                input.value = input.dataset.previousValue;
                this.updateDecreaseButtonState(itemRow);
            }
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

            // Verifica resposta HTTP
            if (!response.ok) {
                let errorMessage = `Erro HTTP ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            if (data.success) {
                // Remove item with animation
                itemRow.style.transition = 'all 0.3s ease';
                itemRow.style.opacity = '0';
                itemRow.style.transform = 'translateX(-100%)';

                setTimeout(() => {
                    itemRow.remove();
                    this.updateCartTotal(data.pedido_total);

                    // Update decrease buttons for any remaining items
                    this.updateAllDecreaseButtons();

                    // Check if cart is empty
                    if (data.items_count === 0) {
                        this.showEmptyCart();
                    }
                }, 300);

                this.showFeedback(data.message || 'Item removido do carrinho!', 'success');
            } else {
                throw new Error(data.error || 'Erro ao remover item');
            }
        } catch (error) {
            console.error('Erro ao remover item:', error);
            
            let errorMsg = 'Erro ao remover item';
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMsg = 'Erro de conexão. Verifique sua internet.';
            } else if (error.message) {
                errorMsg = error.message;
            }
            
            this.showFeedback(errorMsg, 'error');
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

            // Verifica resposta HTTP
            if (!response.ok) {
                let errorMessage = `Erro HTTP ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            if (data.success) {
                this.showEmptyCart();
                this.showFeedback(data.message, 'success');
            } else {
                throw new Error(data.error || 'Erro ao esvaziar carrinho');
            }
        } catch (error) {
            console.error('Erro ao esvaziar carrinho:', error);
            
            let errorMsg = 'Erro ao esvaziar carrinho';
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMsg = 'Erro de conexão. Verifique sua internet.';
            } else if (error.message) {
                errorMsg = error.message;
            }
            
            this.showFeedback(errorMsg, 'error');
        }
    }

    updateCartTotal(total) {
        const totalElement = document.querySelector('.cart-total');
        if (totalElement) {
            // Usa formato simples com ponto decimal para consistência
            totalElement.textContent = 'R$ ' + parseFloat(total).toFixed(2);
        }
    }

    // Enable/disable the minus button for a given item row based on quantity
    updateDecreaseButtonState(itemRow) {
        if (!itemRow) return;
        const input = itemRow.querySelector('.quantity-input');
        const minusBtn = itemRow.querySelector('.quantity-btn-minus');
        if (!input || !minusBtn) return;

        const qty = parseInt(input.value) || 1;
        if (qty <= 1) {
            minusBtn.setAttribute('disabled', '');
        } else {
            minusBtn.removeAttribute('disabled');
        }
    }

    // Update decrease buttons for all items on the page
    updateAllDecreaseButtons() {
        document.querySelectorAll('.cart-item').forEach((itemRow) => {
            this.updateDecreaseButtonState(itemRow);
        });
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

        // Hide cart actions (clear and finalize buttons)
        const cartActions = document.querySelector('.cart-actions');
        if (cartActions) {
            cartActions.style.display = 'none';
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

    async handleFinalizeOrder() {
        // Get cart total
        const totalElement = document.querySelector('.cart-total');
        const total = totalElement ? totalElement.textContent : 'R$ 0.00';

        // Show confirmation modal
        const confirmed = await this.showConfirmationModal(
            'Confirmar Pedido',
            `Tem certeza que deseja finalizar o pedido no valor de ${total}?<br><br>
            <strong>Após a confirmação, você receberá:</strong><br>
            • Um e-mail com os detalhes do pedido<br>
            • Instruções de pagamento via WhatsApp<br>
            • Atualizações sobre a compra coletiva`,
            'Confirmar Pedido',
            'btn-success'
        );

        if (confirmed) {
            // Redirect to finalize order endpoint
            window.location.href = this.baseUrl + '/finalizar-pedido/';
        }
    }
}

// Initialize cart manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CarrinhoManager();
});