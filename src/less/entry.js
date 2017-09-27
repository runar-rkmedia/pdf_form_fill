import './bs-callout.less';
import './bs-dropdown.less';
import './app.less';
$('div').on('shown.bs.collapse', function(e) {
  var target = $(e.target);
  var topOfPanelContent = target.offset().top;
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
$("#menu-toggle").click(function(e) {
  e.preventDefault();
  e.stopPropagation();
  $("#wrapper").toggleClass("toggled");
});

$('body,html').click(function(e) {
  $('#wrapper').removeClass('toggled');
});
$.ajaxPrefilter(function(options, originalOptions, jqXHR) {
  jqXHR.originalRequestOptions = originalOptions;
});
