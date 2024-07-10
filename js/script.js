applyDarkTheme = () => {
    document.body.classList.add('dark-theme');
    document.body.style.backgroundColor = 'var(--background-color-dark)';
    document.body.style.color = 'var(--text-color-dark)';
}

removeDarkTheme = () => {
    document.body.classList.remove('dark-theme');
    document.body.style.backgroundColor = 'var(--background-color-light)';
    document.body.style.color = 'var(--text-color-light)';
}

document.addEventListener('DOMContentLoaded', function() {
    const hour = new Date().getHours();
    const isNight = hour < 6 || hour > 18;

    if (isNight) {
        applyDarkTheme();
    } else {
        removeDarkTheme();
    }
});

document.addEventListener("DOMContentLoaded", function() {
    var pres = document.querySelectorAll('pre code');
    pres.forEach(function(pre) {
        var lines = pre.innerText.split('\n').filter(line => line.length > 0); // Avoid empty lines
        var numberedHtml = '';
        lines.forEach(function(line, index) {
            numberedHtml += '<span class="line">' + line + '</span>\n';
        });
        pre.innerHTML = numberedHtml;
    });
});