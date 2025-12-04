/**
 * Основной JavaScript файл для веб-приложения книжного клуба
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Book Club Web App loaded');

    // Инициализация tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Обработка форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Валидация перед отправкой
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля (помечены *).');
            }
        });
    });

    // Автоматическое обновление данных каждые 30 секунд
    setInterval(() => {
        if (window.location.pathname === '/') {
            updateBookList();
        }
    }, 30000);
});

/**
 * Обновляет список книг через AJAX
 */
function updateBookList() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            console.log('Book list updated');
            // Здесь можно обновить таблицу без перезагрузки страницы
        })
        .catch(error => console.error('Error updating book list:', error));
}

/**
 * Показывает уведомление
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.querySelector('.container').prepend(alertDiv);

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }
    }, 5000);
}

/**
 * Форматирует дату
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}