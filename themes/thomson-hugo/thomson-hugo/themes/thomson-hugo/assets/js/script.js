// Preloader js    
$(window).on('load', function () {
  $('.preloader').fadeOut(100);
});

(function ($) {

  // carosel
  $('.owl-carousel').owlCarousel({
    items: 1,
    loop: true,
    autoplay: true,
    dots: false,
    autoplayTimeout: 8000
  });

  // Shuffle js filter and masonry
  var containerEl = document.querySelector('.shuffle-wrapper');
  if (containerEl) {
    var Shuffle = window.Shuffle;
    var myShuffle = new Shuffle(document.querySelector('.shuffle-wrapper'), {
      itemSelector: '.shuffle-item',
      buffer: 1
    });

    jQuery('input[name="shuffle-filter"]').on('change', function (evt) {
      var input = evt.currentTarget;
      if (input.checked) {
        myShuffle.filter(input.value);
      }
    });
  }

  // magnific popup
  $('.portfolio-gallery').each(function () {
    $(this).find('.popup-gallery').magnificPopup({
      type: 'image',
      gallery: {
        enabled: true
      }
    });
  });

})(jQuery);