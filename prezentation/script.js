 let currentSlide = 1;
        const totalSlides = 8;

        function showSlide(slideNumber) {
            // Скрываем все слайды
            const slides = document.querySelectorAll('.slide');
            slides.forEach(slide => {
                slide.style.display = 'none';
            });
            
            // Показываем нужный слайд
            const targetSlide = document.getElementById('slide' + slideNumber);
            if (targetSlide) {
                targetSlide.style.display = 'flex';
            }
            
            // Обновляем URL
            window.location.hash = 'slide' + slideNumber;
            
            // Обновляем состояние кнопок
            updateButtons();
        }

        function nextSlide() {
            if (currentSlide < totalSlides) {
                currentSlide++;
                showSlide(currentSlide);
            }
        }

        function previousSlide() {
            if (currentSlide > 1) {
                currentSlide--;
                showSlide(currentSlide);
            }
        }

        function updateButtons() {
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            
            // Обновляем состояние кнопки "Назад"
            if (currentSlide === 1) {
                prevBtn.disabled = true;
                prevBtn.style.opacity = '0.5';
            } else {
                prevBtn.disabled = false;
                prevBtn.style.opacity = '1';
            }
            
            // Обновляем состояние кнопки "Вперед"
            if (currentSlide === totalSlides) {
                nextBtn.disabled = true;
                nextBtn.style.opacity = '0.5';
            } else {
                nextBtn.disabled = false;
                nextBtn.style.opacity = '1';
            }
        }

        // Навигация клавиатурой
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                e.preventDefault();
                nextSlide();
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                previousSlide();
            }
        });

        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            // Проверяем URL на наличие хеша
            const hash = window.location.hash;
            if (hash) {
                const slideNum = parseInt(hash.replace('#slide', ''));
                if (slideNum >= 1 && slideNum <= totalSlides) {
                    currentSlide = slideNum;
                }
            }
            
            showSlide(currentSlide);
        });

        // Добавляем обработку колесика мыши
        let scrollTimeout;
        document.addEventListener('wheel', function(e) {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                if (e.deltaY > 0) {
                    nextSlide();
                } else if (e.deltaY < 0) {
                    previousSlide();
                }
            }, 100);
        });