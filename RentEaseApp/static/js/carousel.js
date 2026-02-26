document.addEventListener("DOMContentLoaded", function() {
    const carousels = document.querySelectorAll('.carousel-container');

    carousels.forEach(carousel => {
        let slideIndex = 1;
        const slides = carousel.querySelectorAll('.carousel-slide');
        const counter = carousel.querySelector('.carousel-counter');

        showSlides(slideIndex);

        carousel.querySelector('.carousel-prev').addEventListener('click', (event) => {
            event.stopPropagation();
            plusSlides(-1);
        });

        carousel.querySelector('.carousel-next').addEventListener('click', (event) => {
            event.stopPropagation();
            plusSlides(1);
        });

        function plusSlides(n) {
            showSlides(slideIndex += n);
        }

        function showSlides(n) {
            if (n > slides.length) {slideIndex = 1}
            if (n < 1) {slideIndex = slides.length}
            slides.forEach(slide => slide.style.display = "none");
            slides[slideIndex-1].style.display = "block";
            if (counter) {
                counter.innerHTML = slideIndex + ' / ' + slides.length;
            }
        }
    });
});
