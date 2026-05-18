// ============================================
// CROP RECOMMENDATION SYSTEM
// static/js/main.js
// ============================================

// This runs when the entire page has loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('CropAdvisor app loaded successfully!');

    // Smooth scrolling for anchor links (e.g. href="#predict")
    // When user clicks "Get Recommendation →" it scrolls smoothly
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();     // stop instant jump

            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                // Smooth scroll to the section
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});