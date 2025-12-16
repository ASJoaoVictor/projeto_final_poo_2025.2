function openTransactionModal(id) {
    const modal = document.getElementById(`transactionModal_${id}`);
    const content = document.getElementById(`transactionModalContent_${id}`);

    modal.classList.remove("hidden");
    modal.classList.add("flex", "items-center", "justify-center");

    setTimeout(() => {
        modal.classList.add("opacity-100");
        content.classList.add("opacity-100", "scale-100");
        content.classList.remove("scale-95");
    }, 10);

    // fechar clicando no fundo
    modal.onclick = (e) => {
        if (e.target === modal) closeTransactionModal(id);
    };
}

function closeTransactionModal(id) {
    const modal = document.getElementById(`transactionModal_${id}`);
    const content = document.getElementById(`transactionModalContent_${id}`);

    modal.classList.remove("opacity-100");
    content.classList.remove("opacity-100", "scale-100");
    content.classList.add("scale-95");

    setTimeout(() => {
        modal.classList.add("hidden");
        modal.classList.remove("flex", "items-center", "justify-center");
    }, 250);
}

// --- Lógica do Modal Genérico de Confirmação ---

function openConfirmModal(actionUrl, title, message) {
    // 1. Pega os elementos do modal genérico
    const modal = document.getElementById('modal-confirm');
    const backdrop = document.getElementById('modal-confirm-backdrop');
    const panel = document.getElementById('modal-confirm-panel');
    
    // 2. Atualiza os textos e o destino do formulário
    document.getElementById('confirm-form').action = actionUrl;
    if(title) document.getElementById('confirm-title').innerText = title;
    if(message) document.getElementById('confirm-message').innerHTML = message;

    // 3. Abre o modal
    modal.classList.remove('hidden');
    
    // Animação de entrada
    setTimeout(() => {
        backdrop.classList.remove('opacity-0');
        panel.classList.remove('opacity-0', 'scale-95');
        panel.classList.add('opacity-100', 'scale-100');
    }, 10);
}

function closeConfirmModal() {
    const modal = document.getElementById('modal-confirm');
    const backdrop = document.getElementById('modal-confirm-backdrop');
    const panel = document.getElementById('modal-confirm-panel');

    // Animação de saída
    backdrop.classList.add('opacity-0');
    panel.classList.remove('opacity-100', 'scale-100');
    panel.classList.add('opacity-0', 'scale-95');

    setTimeout(() => {
        modal.classList.add('hidden');
    }, 300);
}

// Fechar ao clicar no fundo escuro
document.getElementById('modal-confirm-backdrop').onclick = closeConfirmModal;