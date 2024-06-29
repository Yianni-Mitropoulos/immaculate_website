document.addEventListener('DOMContentLoaded', function() {
    const hour = new Date().getHours();
    const isNight = hour < 6 || hour > 18;

    if (isNight) {
        document.body.classList.add('dark-theme');
        document.body.style.backgroundColor = 'var(--background-color-dark)';
        document.body.style.color = 'var(--text-color-dark)';
    } else {
        document.body.classList.remove('dark-theme');
        document.body.style.backgroundColor = 'var(--background-color-light)';
        document.body.style.color = 'var(--text-color-light)';
    }
});