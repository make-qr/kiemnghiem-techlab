(function () {
  window.dataLayer = window.dataLayer || [];
  window.TLG_TRACKING = window.TLG_TRACKING || {
    gtmId: 'GTM-MRHPPTJ7',
    ga4Id: 'G-4YE334L4TV',
    adsId: 'AW-18270406607',
    metaPixelId: '4620520364845904',
    siteHost: 'kiemnghiem.techlabglobal.com.vn'
  };

  window.gtag =
    window.gtag ||
    function () {
      window.dataLayer.push(arguments);
    };
  window.gtag('js', new Date());
  window.gtag('config', window.TLG_TRACKING.ga4Id);
  window.gtag('config', window.TLG_TRACKING.adsId);
})();
