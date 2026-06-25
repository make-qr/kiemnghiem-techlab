(function () {
    var ADS_ID = 'AW-18270406607';
    var SEND_TO = {
        form: 'AW-18270406607/STV0CPOuncUcEM-PgYhE',
        thankYou: 'AW-18270406607/76T2CPvgm8UcEM-PgYhE',
        call: 'AW-18270406607/55kGCILim8UcEM-PgYhE',
        zalo: 'AW-18270406607/CkOzCO-wncUcEM-PgYhE'
    };

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

    function adsConversion(sendTo) {
        if (typeof gtag === 'function' && sendTo) {
            gtag('event', 'conversion', { send_to: sendTo });
        }
    }

    function trackConversion(eventName, label, sendTo) {
        adsConversion(sendTo);
        if (typeof gtag === 'function') {
            gtag('event', eventName, {
                event_category: 'conversion',
                event_label: label || ''
            });
        }
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            event: eventName,
            conversion_label: label || '',
            ads_send_to: sendTo || ''
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.body.classList.add('has-sticky-cta');
        prefillServiceSelects();

        if (/\/thank-you\.html$/i.test(window.location.pathname)) {
            trackConversion('thank_you_page', 'thank_you', SEND_TO.thankYou);
        }

        document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
            link.addEventListener('click', function () {
                trackConversion('click_call', link.getAttribute('href'), SEND_TO.call);
            });
        });

        document.querySelectorAll('a[href*="zalo.me"]').forEach(function (link) {
            link.addEventListener('click', function () {
                trackConversion('click_zalo', link.href, SEND_TO.zalo);
            });
        });

        document.querySelectorAll('.quote-form, .contact-form').forEach(function (form) {
            form.addEventListener('submit', function () {
                var label = form.classList.contains('quote-form') ? 'quote_form' : 'contact_form';
                trackConversion('form_submit', label, SEND_TO.form);
            });
        });
    });
})();
