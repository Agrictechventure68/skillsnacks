// frontend/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.addEventListener('click', function () {
            alert('SkillSnacks AI Bot is launching…');
        });
    }
});

> Link it in index.html:



<script src="scripts.js"></script>
