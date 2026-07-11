(function () {
    var lightbox = document.getElementById('hs-lightbox');
    if (!lightbox) return;

    var lightboxImg = lightbox.querySelector('.hs-lightbox-img');
    var images = [];
    var currentIndex = 0;

    function openLightbox(src, group) {
        images = Array.from(document.querySelectorAll('[data-lightbox="' + group + '"]'))
            .map(function (el) { return el.getAttribute('href') || el.querySelector('img').src; });
        currentIndex = images.indexOf(src);
        if (currentIndex < 0) {
            images = [src];
            currentIndex = 0;
        }
        showImage(currentIndex);
        lightbox.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function showImage(index) {
        if (!images.length) return;
        currentIndex = (index + images.length) % images.length;
        lightboxImg.src = images[currentIndex];
        lightboxImg.alt = 'Xem phóng to';
    }

    function closeLightbox() {
        lightbox.classList.remove('is-open');
        document.body.style.overflow = '';
        lightboxImg.src = '';
    }

    document.querySelectorAll('[data-lightbox]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var src = el.getAttribute('href') || (el.querySelector('img') && el.querySelector('img').src);
            var group = el.getAttribute('data-lightbox') || 'default';
            if (src) openLightbox(src, group);
        });
    });

    lightbox.querySelector('.hs-lightbox-close').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) {
        if (e.target === lightbox) closeLightbox();
    });

    var prevBtn = lightbox.querySelector('.hs-lightbox-prev');
    var nextBtn = lightbox.querySelector('.hs-lightbox-next');
    if (prevBtn) prevBtn.addEventListener('click', function () { showImage(currentIndex - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { showImage(currentIndex + 1); });

    document.addEventListener('keydown', function (e) {
        if (!lightbox.classList.contains('is-open')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showImage(currentIndex - 1);
        if (e.key === 'ArrowRight') showImage(currentIndex + 1);
    });

    /* Gallery tabs */
    document.querySelectorAll('.hs-gallery-tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
            var target = tab.getAttribute('data-tab');
            document.querySelectorAll('.hs-gallery-tab').forEach(function (t) {
                t.classList.toggle('is-active', t === tab);
            });
            document.querySelectorAll('.hs-gallery-grid').forEach(function (grid) {
                grid.classList.toggle('is-hidden', grid.getAttribute('data-panel') !== target);
            });
        });
    });

    /* Side nav active on scroll */
    var sections = document.querySelectorAll('.hs-main section[id]');
    var navLinks = document.querySelectorAll('.hs-side-nav a');

    function updateNav() {
        var scrollPos = window.scrollY + 120;
        var current = '';
        sections.forEach(function (section) {
            if (section.offsetTop <= scrollPos) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(function (link) {
            link.classList.toggle('is-active', link.getAttribute('href') === '#' + current);
        });
    }

    window.addEventListener('scroll', updateNav);
    updateNav();
})();
