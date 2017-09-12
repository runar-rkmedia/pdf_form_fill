import './bs-callout.less';
import './bs-dropdown.less';
import './app.less';
$('div').on('shown.bs.collapse', function(e) {
  var target = $(e.target);
  var topOfPanelContent = target.offset().top;
  if (target.hasClass('scrollto') || true) {
    var panelHeadingHeight = 30;
    if (target.hasClass('panel')) {
      var panelHeading = target.siblings('.panel-heading');
      panelHeadingHeight = target.siblings('.panel-heading').height();

    }

    $("html, body").animate({
      scrollTop: topOfPanelContent - panelHeadingHeight -25
    }, 200);
  }
});
