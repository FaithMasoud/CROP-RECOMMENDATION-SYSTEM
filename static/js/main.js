// ============================================
// CROPADVISOR — main.js
// ============================================

document.addEventListener('DOMContentLoaded', function () {

    // --- Smooth scrolling ---
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(
                this.getAttribute('href')
            );
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth', block: 'start'
                });
            }
        });
    });

    // --- Mobile menu toggle ---
    const mobileBtn  = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('open');
        });
    }

    // --- Animate confidence bar on result page ---
    const confBar = document.querySelector('.conf-bar-fill');
    if (confBar) {
        const targetWidth = confBar.style.width;
        confBar.style.width = '0%';
        setTimeout(() => {
            confBar.style.width = targetWidth;
        }, 300);
    }

    // --- Navbar active link highlight ---
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = 'rgba(255,255,255,0.15)';
            link.style.color = '#ffffff';
        }
    });

    console.log('CropAdvisor loaded successfully!');
});