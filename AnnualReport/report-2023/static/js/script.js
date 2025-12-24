document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('.slider');
    let currentPage = 1;

    // Handle touch or swipe events for sliding pages
    let startX, startY, endX, endY;

    document.addEventListener('touchstart', function (e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });

    document.addEventListener('touchend', function (e) {
        endX = e.changedTouches[0].clientX;
        endY = e.changedTouches[0].clientY;

        handleSwipe();
    });

    function handleSwipe() {
        const deltaX = endX - startX;
        const deltaY = endY - startY;

        // Adjust sensitivity based on your needs
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            // Check if swipe is horizontally significant
            if (deltaX > 0 && currentPage > 1) {
                // Swipe to the right
                currentPage--;
            } else if (deltaX < 0 && currentPage < document.querySelectorAll('.page').length) {
                // Swipe to the left
                currentPage++;
            }

            updateSlider();
        }
    }

    // Listen for changes in the URL to handle browser back/forward navigation
    window.addEventListener('popstate', function (event) {
        const pageIndex = parseInt(window.location.hash.substring(1));
        if (!isNaN(pageIndex) && pageIndex >= 1 && pageIndex <= document.querySelectorAll('.page').length) {
            currentPage = pageIndex;
            updateSlider();
        }
    });

    // Update the slider position based on the current page
    function updateSlider() {
        const translateValue = `translateX(-${(currentPage - 1) * 100}%)`;
        slider.style.transform = translateValue;

        // Update the URL hash for back/forward navigation
        window.history.pushState({}, '', `#${currentPage}`);
    }
});
