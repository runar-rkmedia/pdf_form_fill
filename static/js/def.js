$(function () {
  $("input[name='manufacturor']").change(set_manufacturor);
  // lazy set visible-checkboxes based on manufacturor.
  function set_manufacturor() {
    radioValue = $('input:radio[name=manufacturor]:checked').val();
    var $wattRadios = $('input:radio[name=meterEffekt]');
    var wattRadioChecked = $wattRadios.filter(':checked').val();

    switch (radioValue) {
      case 'Nexans':
        $('#meterEffekt8').hide();
        $('#meterEffekt10').show();
        $('#meterEffekt10').css('margin-left',0);
        $('#meterEffekt16').hide();
        $('#meterEffekt17').show();
        if (['10','17'].indexOf(wattRadioChecked) === -1) {
          $wattRadios.filter('[value='+ wattRadioChecked +  ']').prop('checked', false);
        }
        break;
      case 'Øglænd':
        $('#meterEffekt8').show();
        $('#meterEffekt10').show();
        $('#meterEffekt10').css('margin-left',$('#meterEffekt16').css('margin-left'));
        $('#meterEffekt16').show();
        $('#meterEffekt17').hide();
        if (['8', '10', '16'].indexOf(wattRadioChecked) === -1) {
          $wattRadios.filter('[value='+ wattRadioChecked +  ']').prop('checked', false);
        }
        break;
      default:
    }
  }
  set_manufacturor();
});
