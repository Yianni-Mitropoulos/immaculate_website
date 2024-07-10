document.querySelectorAll('.animation').forEach(function (container) {

    // Get the content in the HTML
    const contents = Array.from(container.children);

    // Initialize variables
    let currentIndex = 0;
    let intervalId = null;
    let isPlaying = false;

    // Create a sidebar
    let sidebar = document.createElement('div');
    sidebar.className = 'sidebar';
    container.insertBefore(sidebar, container.firstChild);

    // Iterate over content items
    contents.forEach((content, index) => {

        // Give non-sidebar children mainContent class
        content.classList.add('mainContent');
        content.style.display = 'none';  // Hide all content initially

        // Create button
        let btn = document.createElement('button');
        btn.className = 'content-button';
        btn.textContent = content.getAttribute('name');
        btn.onclick = () => changeContent(index);
        sidebar.appendChild(btn);

    });

    // Special style for the last content button
    sidebar.firstElementChild.classList.add('first-content-button');
    sidebar.lastElementChild.classList.add('last-content-button');

    // Create control panel
    let controlPanel = document.createElement('div');
    controlPanel.className = 'control-panel';
    sidebar.appendChild(controlPanel);

    const buttons = [
        {icon: 'fa-fast-backward', action: 'first'},
        {icon: 'fa-step-backward', action: 'previous'},
        {icon: 'fa-play', action: 'play-pause'},
        {icon: 'fa-step-forward', action: 'next'},
        {icon: 'fa-fast-forward', action: 'last'}
    ];
    buttons.forEach(({icon, action}) => {
        let btn = document.createElement('button');
        btn.className = 'button';
        btn.innerHTML = `<i class="fas ${icon}"></i>`;
        btn.onclick = () => controlClick(action);
        controlPanel.appendChild(btn);
    });

    // Slider for animation speed
    let sliderContainer = document.createElement('div');
    sliderContainer.className = 'slider-container';
    sliderContainer.innerHTML = `<div class="slider-label">Animation Speed:</div>
    <input type="range" min="1" max="100" value="50" class="slider" title="Animation Speed">`;
    sidebar.appendChild(sliderContainer);

    function changeContent(index, endByPausing=true) {
        contents.forEach((div, idx) => {
            div.style.display = (idx === index) ? 'block' : 'none';
        });
        currentIndex = index;
        updateActiveButton();
        if (endByPausing) pause();
    }

    function updateActiveButton() {
        sidebar.querySelectorAll('.content-button').forEach((btn, idx) => {
            btn.classList.toggle('active', idx === currentIndex);
        });
    }

    function controlClick(action) {
        switch (action) {
            case 'first':
                changeContent(0);
                break;
            case 'previous':
                if (currentIndex > 0) changeContent(currentIndex - 1);
                break;
            case 'play-pause':
                toggleAnimation();
                break;
            case 'next':
                if (currentIndex < contents.length - 1) changeContent(currentIndex + 1)
                break;
            case 'last':
                changeContent(contents.length - 1);
                break;
        }
    }

    function play() {
        const playPauseIcon = controlPanel.querySelector('.fa-play, .fa-pause');
        intervalId = setInterval(() => {
            if (currentIndex < contents.length - 1) {
                changeContent(currentIndex + 1, false);
            } else {
                autoPause();
            }
        }, 2000 - document.querySelector('.slider').value * 19);
        playPauseIcon.classList.remove('fa-play');
        playPauseIcon.classList.add('fa-pause');
        isPlaying = true;
    }

    function pause() {
        const playPauseIcon = controlPanel.querySelector('.fa-play, .fa-pause');
        clearInterval(intervalId);
        playPauseIcon.classList.add('fa-play');
        playPauseIcon.classList.remove('fa-pause');
        isPlaying = false;
    }
    function toggleAnimation() {
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    }

    // Initialize active state
    changeContent(0);
});
