(function ($) {
  'use strict';

  // Preloader js    
  $(window).on('load', function () {
    $('.preloader').fadeOut(100);
  });

  // Count Down JS
  var Year = $('#simple-timer').attr('data-year');
  var Month = $('#simple-timer').attr('data-month');
  var Day = $('#simple-timer').attr('data-day');
  var Hour = $('#simple-timer').attr('data-hour');
  $('#simple-timer').syotimer({
    year: Year,
    month: Month,
    day: Day,
    hour: Hour,
    minute: 0
  });

})(jQuery);