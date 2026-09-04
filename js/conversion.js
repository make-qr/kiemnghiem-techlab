(function () {
    var SEND_TO = {
        thankYou: 'AW-18270406607/76T2CPvgm8UcEM-PgYhE',
        call: 'AW-18270406607/55kGCILim8UcEM-PgYhE',
        zalo: 'AW-18270406607/CkOzCO-wncUcEM-PgYhE',
        // Primary lead — thiếu key này khiến gtag không gửi conversion form
        form: 'AW-18270406607/STV0CPOuncUcEM-PgYhE'
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
    var cachedIp = '';

    function getQueryParam(name) {
        var params = new URLSearchParams(window.location.search);
        return params.get(name);
    }

    function field(form, key) {
        return form.querySelector('[data-field="' + key + '"]');
    }

    function fetchClientIp() {
        if (cachedIp) {
            return Promise.resolve(cachedIp);
        }
        if (clientIpPromise) return clientIpPromise;

        function fromIpify(url) {
            return fetch(url, { cache: 'no-store' }).then(function (res) {
                if (!res.ok) throw new Error('ip lookup failed');
                return res.json();
            }).then(function (data) {
                return (data && data.ip) || '';
            });
        }

        clientIpPromise = Promise.race([
            fromIpify('https://api.ipify.org?format=json').catch(function () {
                return fromIpify('https://api64.ipify.org?format=json');
            }),
            new Promise(function (resolve) {
                setTimeout(function () {
                    resolve('');
                }, 3000);
            })
        ]).then(function (ip) {
            cachedIp = ip || '';
            return cachedIp;
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

    function nowVietnam() {
        return new Date().toLocaleString('vi-VN', {
            timeZone: 'Asia/Ho_Chi_Minh',
            hour12: false
        });
    }

    function fillSubmissionMeta(form, ip) {
        var ipValue = ip || cachedIp || '(không lấy được)';
        var uaValue = navigator.userAgent || '(không lấy được)';
        var urlValue = window.location.href;
        var timeValue = nowVietnam();

        var ipInput = field(form, 'client_ip');
        var uaInput = field(form, 'user_agent');
        var urlInput = field(form, 'page_url');
        var timeInput = field(form, 'submitted_at');

        if (ipInput) ipInput.value = ipValue;
        if (uaInput) uaInput.value = uaValue;
        if (urlInput) urlInput.value = urlValue;
        if (timeInput) timeInput.value = timeValue;

        return {
            'Địa_chỉ_IP': ipValue,
            'Trình_duyệt': uaValue,
            'Trang_gửi_form': urlValue,
            'Thời_điểm_gửi': timeValue
        };
    }

    function getAjaxEndpoint(form) {
        var action = form.getAttribute('action') || '';
        if (action.indexOf('/ajax/') !== -1) return action;
        return action.replace('https://formsubmit.co/', 'https://formsubmit.co/ajax/');
    }

    function getNextUrl(form) {
        var next = form.querySelector('input[name="_next"]');
        return (next && next.value) || 'https://kiemnghiem.techlabglobal.com.vn/thank-you.html';
    }

    function buildPayload(form, ip) {
        var meta = fillSubmissionMeta(form, ip);
        var payload = {};
        var formData = new FormData(form);

        formData.forEach(function (value, key) {
            if (key === '_honey') return;
            if (value === null || value === undefined) return;
            var text = String(value).trim();
            if (!text && (key === 'Địa_chỉ_IP' || key === 'Trình_duyệt' || key === 'Trang_gửi_form' || key === 'Thời_điểm_gửi')) {
                return;
            }
            payload[key] = text;
        });

        payload['Địa_chỉ_IP'] = meta['Địa_chỉ_IP'];
        payload['Trình_duyệt'] = meta['Trình_duyệt'];
        payload['Trang_gửi_form'] = meta['Trang_gửi_form'];
        payload['Thời_điểm_gửi'] = meta['Thời_điểm_gửi'];
        payload._template = payload._template || 'table';
        payload._captcha = 'false';

        return payload;
    }

    function setSubmitting(form, isSubmitting) {
        var btn = form.querySelector('button[type="submit"]');
        if (!btn) return;
        if (isSubmitting) {
            btn.disabled = true;
            if (!btn.dataset.originalText) {
                btn.dataset.originalText = btn.textContent;
            }
            btn.textContent = 'Đang gửi...';
        } else {
            btn.disabled = false;
            if (btn.dataset.originalText) {
                btn.textContent = btn.dataset.originalText;
            }
        }
    }

    function trackFormSubmit(form) {
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
    }

    function setupQuoteFormSubmit(form) {
        setupOtherDetailFields(form);
        fillSubmissionMeta(form, cachedIp);

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (form.getAttribute('data-sending') === '1') return;
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            form.setAttribute('data-sending', '1');
            setSubmitting(form, true);

            fetchClientIp().then(function (ip) {
                var payload = buildPayload(form, ip);
                var endpoint = getAjaxEndpoint(form);

                return fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(payload)
                }).then(function (res) {
                    if (!res.ok) {
                        throw new Error('FormSubmit HTTP ' + res.status);
                    }
                    return res.json().catch(function () {
                        return {};
                    });
                });
            }).then(function () {
                trackFormSubmit(form);
                window.location.href = getNextUrl(form);
            }).catch(function () {
                // Fallback: native POST với meta đã điền
                fillSubmissionMeta(form, cachedIp);
                form.removeAttribute('data-sending');
                setSubmitting(form, false);
                trackFormSubmit(form);
                HTMLFormElement.prototype.submit.call(form);
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
        forms.forEach(function (form) {
            fillSubmissionMeta(form, '');
            setupQuoteFormSubmit(form);
        });

        if (forms.length) {
            fetchClientIp().then(function (ip) {
                forms.forEach(function (form) {
                    fillSubmissionMeta(form, ip);
                });
            });
        }
    });
})();
