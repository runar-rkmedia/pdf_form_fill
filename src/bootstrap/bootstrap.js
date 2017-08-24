import 'bootstrap/js/transition';
// import 'bootstrap/js/alert';
import 'bootstrap/js/button';
// import 'bootstrap/js/carousel';
import 'bootstrap/js/collapse';
// import 'bootstrap/js/dropdown';
// import 'bootstrap/js/modal';
// import 'bootstrap/js/tooltip';
// import 'bootstrap/js/popover';
// import 'bootstrap/js/scrollspy';
import 'bootstrap/js/tab';
// import 'bootstrap/js/affix';
import './bootstrap.less'
$('div').on('shown.bs.collapse', function(e) {
  var target = $(e.target);
    var panelHeadingHeight = target.siblings('.panel-heading').height();
    var animationSpeed = 200; // animation speed in milliseconds
    var currentScrollbarPosition = $(document).scrollTop();
    var topOfPanelContent = target.offset().top;

    $("html, body").animate({
      scrollTop: topOfPanelContent - panelHeadingHeight -25
    }, animationSpeed);
  }
});
