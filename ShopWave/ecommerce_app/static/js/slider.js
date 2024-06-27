function initializeSlider() {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slider-images img');
    const totalSlides = slides.length;

    for (let i = 1; i < totalSlides; i++) {
        slides[i].style.display = 'none';
    }

    function nextSlide() {
        slides[currentSlide].style.display = 'none';
        currentSlide = (currentSlide + 1) % totalSlides;
        slides[currentSlide].style.display = 'block';
    }

    setInterval(nextSlide, 3000);
}

window.addEventListener('load', function() {
    initializeSlider();
});
