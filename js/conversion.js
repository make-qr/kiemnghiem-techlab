(function () {
    var SERVICE_MAP = {
        'banh-trung-thu': 'banh-trung-thu',
        'banh-keo': 'banh-trung-thu',
        'nuoc-uong': 'nuoc-uong',
        'nuoc': 'nuoc-uong',
        'thuc-pham': 'thuc-pham',
        'my-pham': 'my-pham',
        'duoc-pham': 'duoc-pham',
        'kiem-nghiem': 'kiem-nghiem',
        'chung-nhan': 'chung-nhan',
        'tu-van': 'tu-van',
        'khac': 'khac'
    };

    function getQueryParam(name) {
        var params = new URLSearchParams(window.location.search);
        return params.get(name);
    }

    function prefillServiceSelects() {
        var service = getQueryParam('dich-vu') || getQueryParam('service');
        if (!service || !SERVICE_MAP[service]) return;

        var value = SERVICE_MAP[service];
        document.querySelectorAll('select[name="service"], select[name="product_type"]').forEach(function (select) {
            var option = select.querySelector('option[value="' + value + '"]');
            if (option) {
                select.value = value;
            }
        });
    }

    function trackConversion(eventName, label) {
        if (typeof gtag === 'function') {
            gtag('event', eventName, {
                event_category: 'conversion',
                event_label: label || ''
            });
        }
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: eventName,
            conversion_label: label || ''
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.body.classList.add('has-sticky-cta');
        prefillServiceSelects();

        document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
            link.addEventListener('click', function () {
                trackConversion('click_call', link.getAttribute('href'));
            });
        });

        document.querySelectorAll('a[href*="zalo.me"]').forEach(function (link) {
            link.addEventListener('click', function () {
                trackConversion('click_zalo', link.href);
            });
        });

        document.querySelectorAll('.quote-form, .contact-form').forEach(function (form) {
            form.addEventListener('submit', function () {
                trackConversion('form_submit', form.classList.contains('quote-form') ? 'quote_form' : 'contact_form');
            });
        });
    });
})();
