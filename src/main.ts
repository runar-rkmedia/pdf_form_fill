import $ = require("jquery");
import { TSAppViewModel } from "./components/AppViewModel"

export var myApp: TSAppViewModel;

let pad = (n: string, width: number, z: string = "0") => {
  // Pad a string(n), to a certain (width), and pad with (z)
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
// webpack doesn't like to litter the global-namespace, so to force this function to be available there, we need to add the function to global. then typescript compains, so we need to add to it.
(<any>window).format_date = (dateString: string, type: string) => {
  var d_names = new Array("Søndag", "Mandag", "Tirsdag",
    "Onsdag", "Torsdag", "Fredag", "Søndag");

  var m_names = new Array("januar", "februar", "mars",
    "april", "mai", "juni", "juli", "august", "september",
    "october", "november", "december");
  //
  // var d = new Date(dateString).toISOString()
  var d = new Date(dateString);
  var curr_day = d.getDay();
  var curr_date = d.getDate();
  var curr_month = d.getMonth();
  var curr_year = d.getFullYear();
  var curr_hour = d.getHours();
  var curr_minute = d.getMinutes();
  if (type === 'short') {
    return curr_date + '/' + curr_month + "-" + String(curr_year).slice(2) + ' ' +
      pad(String(curr_hour), 2) + ':' + pad(String(curr_minute), 2);
  }
  return curr_date + '. ' + m_names[curr_month] + " " + curr_year + ' ' +
    pad(String(curr_hour), 2) + ':' + pad(String(curr_minute), 2);
};

$(() => {
  myApp = new TSAppViewModel();
  ko.applyBindings(myApp);

  $('body').on("change keyup paste click", 'input', () => {
    myApp.form_args($('#form').serialize());
  });

  $('input[type=tel]').on('input', function(e) {
    let inputfield = (<HTMLInputElement>this);
    inputfield.value = inputfield.value.replace(/\D/g, '');
  })
});
var myObject = {};
var mySecondReference = myObject;
