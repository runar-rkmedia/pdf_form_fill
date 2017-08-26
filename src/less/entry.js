import './app.less'
$('div').on('shown.bs.collapse', function(e) {
  var target = $(e.target);
  if (target.hasClass('scrollto') || true) {
    var panelHeading = target.siblings('.panel-heading')
    var panelHeadingHeight = target.siblings('.panel-heading').height();
    var animationSpeed = 200; // animation speed in milliseconds
    var currentScrollbarPosition = $(document).scrollTop();
    var topOfPanelContent = target.offset().top;

    $("html, body").animate({
      scrollTop: topOfPanelContent - panelHeadingHeight -25
    }, animationSpeed);
  }
});
