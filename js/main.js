function getHeaderOffset() {
    var header = document.querySelector('header');
    return header ? header.offsetHeight + 8 : 70;
}

// Smooth scrolling for in-page anchor links
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href');
        if (!targetId || targetId === '#') return;

        var targetElement = document.querySelector(targetId);
        if (!targetElement) return;

        e.preventDefault();
        closeMobileNav();

        window.scrollTo({
            top: targetElement.offsetTop - getHeaderOffset(),
            behavior: 'smooth'
        });
    });
});

function closeMobileNav() {
    var nav = document.querySelector('header nav');
    var toggle = document.querySelector('.nav-toggle');
    if (nav) nav.classList.remove('is-open');
    if (toggle) toggle.classList.remove('is-active');
    document.body.classList.remove('menu-open');
}

function setupMobileHeader() {
    var container = document.querySelector('header .container');
    if (!container) return;

    var nav = container.querySelector('nav');
    if (!nav) return;

    if (!container.querySelector('.header-actions')) {
        var actions = document.createElement('div');
        actions.className = 'header-actions';

        var callBtn = document.createElement('a');
        callBtn.href = 'tel:0899551228';
        callBtn.className = 'header-call-btn';
        callBtn.setAttribute('aria-label', 'Gọi 0899.551.228');
        callBtn.innerHTML = '<i class="fas fa-phone"></i>';

        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'nav-toggle';
        toggle.setAttribute('aria-label', 'Mở menu');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<span></span><span></span><span></span>';

        actions.appendChild(callBtn);
        actions.appendChild(toggle);
        container.appendChild(actions);
    }

    var toggleBtn = container.querySelector('.nav-toggle');
    if (!toggleBtn || toggleBtn.dataset.bound) return;
    toggleBtn.dataset.bound = '1';

    toggleBtn.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('is-open');
        toggleBtn.classList.toggle('is-active', isOpen);
        document.body.classList.toggle('menu-open', isOpen);
        toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    nav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeMobileNav);
    });
}

// Header scroll effect
var header = document.querySelector('header');
if (header) {
    window.addEventListener('scroll', function () {
        if (window.scrollY > 100) {
            header.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = '';
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    setupMobileHeader();

    document.addEventListener('click', function (e) {
        if (!document.body.classList.contains('menu-open')) return;
        if (e.target.closest('header')) return;
        closeMobileNav();
    });

    var faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(function (question) {
        question.addEventListener('click', function () {
            var faqItem = this.parentNode;
            document.querySelectorAll('.faq-item.active').forEach(function (item) {
                if (item !== faqItem) item.classList.remove('active');
            });
            faqItem.classList.toggle('active');
        });
    });
});
