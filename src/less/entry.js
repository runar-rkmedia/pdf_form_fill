import './bs-callout.less';
import './bs-dropdown.less';
import './app.less';
$('div').on('shown.bs.collapse', function(e) {
  var target = $(e.target);
  var topOfPanelContent = target.offset().top;
  console.log(target);
  if (target.hasClass('scrollto')) {
    var panelHeadingHeight = 30;
    if (target.hasClass('panel')) {
      var panelHeading = target.siblings('.panel-heading');
      panelHeadingHeight = panelHeading.height();

    }
    $("html, body").animate({
      scrollTop: -70 + topOfPanelContent - panelHeadingHeight - 25
    }, 200);
  }
});
