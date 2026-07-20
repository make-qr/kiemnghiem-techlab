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

    var clientIpPromise = null;

    function getQueryParam(name) {
        var params = new URLSearchParams(window.location.search);
        return params.get(name);
    }

    function field(form, key) {
        return form.querySelector('[data-field="' + key + '"]');
    }

    function fetchClientIp() {
        if (clientIpPromise) return clientIpPromise;

        clientIpPromise = fetch('https://api.ipify.org?format=json')
            .then(function (res) {
                if (!res.ok) throw new Error('ipify failed');
                return res.json();
            })
            .then(function (data) {
                return (data && data.ip) || '';
            })
            .catch(function () {
                return fetch('https://api64.ipify.org?format=json')
                    .then(function (res) {
                        if (!res.ok) throw new Error('ipify64 failed');
                        return res.json();
                    })
                    .then(function (data) {
                        return (data && data.ip) || '';
                    })
                    .catch(function () {
                        return '';
                    });
            });

        return clientIpPromise;
    }

    function prefillServiceSelects() {
        var service = getQueryParam('dich-vu') || getQueryParam('service');
        if (!service || !SERVICE_MAP[service]) return;

        var slug = SERVICE_MAP[service];
        document.querySelectorAll('select[data-field="product_type"], select[name="service"]').forEach(function (select) {
            var option = select.querySelector('option[data-slug="' + slug + '"]');
            if (option) {
                select.value = option.value;
            }
        });
    }

    function isOtherSelected(select) {
        var opt = select.options[select.selectedIndex];
        return !!(opt && opt.getAttribute('data-other') === '1');
    }

    function syncOtherDetailField(select, otherGroup, otherInput) {
        var isOther = isOtherSelected(select);
        otherGroup.hidden = !isOther;
        if (isOther) {
            otherInput.setAttribute('required', 'required');
            otherInput.disabled = false;
        } else {
            otherInput.removeAttribute('required');
            otherInput.value = '';
            otherInput.disabled = true;
        }
    }

    function setupOtherDetailFields(form) {
        [
            { selectKey: 'city', otherKey: 'city_other' },
            { selectKey: 'product_type', otherKey: 'product_type_other' }
        ].forEach(function (cfg) {
            var select = field(form, cfg.selectKey);
            var otherGroup = form.querySelector('[data-other-for="' + cfg.selectKey + '"]');
            var otherInput = field(form, cfg.otherKey);
            if (!select || !otherGroup || !otherInput) return;

            select.addEventListener('change', function () {
                syncOtherDetailField(select, otherGroup, otherInput);
            });
            syncOtherDetailField(select, otherGroup, otherInput);
        });
    }

    function fillSubmissionMeta(form, ip) {
        var ipInput = field(form, 'client_ip');
        var uaInput = field(form, 'user_agent');
        var urlInput = field(form, 'page_url');
        var timeInput = field(form, 'submitted_at');

        if (ipInput) {
            ipInput.value = ip || '(không lấy được)';
        }
        if (uaInput) {
            uaInput.value = navigator.userAgent || '(không lấy được)';
        }
        if (urlInput) {
            urlInput.value = window.location.href;
        }
        if (timeInput) {
            timeInput.value = new Date().toLocaleString('vi-VN', {
                timeZone: 'Asia/Ho_Chi_Minh',
                hour12: false
            });
        }
    }

    function setupQuoteFormSubmit(form) {
        setupOtherDetailFields(form);

        form.addEventListener('submit', function (event) {
            if (form.getAttribute('data-meta-ready') === '1') {
                markFormConversionPending();
                trackConversion('quote_form_submit', 'quote_form', SEND_TO.form);

                if (typeof gtag === 'function') {
                    gtag('event', 'form_submit', {
                        event_category: 'conversion',
                        event_label: form.classList.contains('quote-form') ? 'quote_form' : 'contact_form'
                    });
                }
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: 'form_submit',
                    conversion_label: form.classList.contains('quote-form') ? 'quote_form' : 'contact_form'
                });
                return;
            }

            event.preventDefault();

            var btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.dataset.originalText = btn.textContent;
                btn.textContent = 'Đang gửi...';
            }

            fetchClientIp().then(function (ip) {
                fillSubmissionMeta(form, ip);
                form.setAttribute('data-meta-ready', '1');
                if (typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                } else {
                    markFormConversionPending();
                    trackConversion('quote_form_submit', 'quote_form', SEND_TO.form);
                    form.submit();
                }
            }).catch(function () {
                fillSubmissionMeta(form, '');
                form.setAttribute('data-meta-ready', '1');
                if (typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                } else {
                    markFormConversionPending();
                    trackConversion('quote_form_submit', 'quote_form', SEND_TO.form);
                    form.submit();
                }
            });
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

    function markFormConversionPending() {
        try {
            sessionStorage.setItem('tlg_form_ads_sent', '1');
        } catch (e) {}
    }

    function consumeFormConversionPending() {
        try {
            var sent = sessionStorage.getItem('tlg_form_ads_sent') === '1';
            sessionStorage.removeItem('tlg_form_ads_sent');
            return sent;
        } catch (e) {
            return false;
        }
    }

    function initThankYouConversions() {
        if (!/\/thank-you\.html$/i.test(window.location.pathname)) {
            return;
        }

        trackConversion('thank_you_page', 'thank_you', SEND_TO.thankYou);

        if (!consumeFormConversionPending()) {
            trackConversion('quote_form_complete', 'quote_form', SEND_TO.form);
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.body.classList.add('has-sticky-cta');
        prefillServiceSelects();

        window.addEventListener('load', initThankYouConversions);

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

        var forms = document.querySelectorAll('.quote-form, .contact-form');
        forms.forEach(setupQuoteFormSubmit);

        if (forms.length) {
            fetchClientIp().then(function (ip) {
                forms.forEach(function (form) {
                    var ipInput = field(form, 'client_ip');
                    if (ipInput && !ipInput.value) {
                        ipInput.value = ip || '(không lấy được)';
                    }
                    fillSubmissionMeta(form, ip || ipInput && ipInput.value);
                });
            });
        }
    });
})();
