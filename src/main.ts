import { TSAppViewModel } from "./components/AppViewModel"
import './bootstrap/bootstrap'
import './less/entry'
import './components/bootstrap-slider-knockout-binding/bootstrap-slider-knockout-binding.js';
export var myApp: TSAppViewModel;



WebFont.load({
  google: {
    families: ['Lato:400,700,400i']
  }
});
// webpack doesn't like to litter the global-namespace, so to force this function to be available there, we need to add the function to global. then typescript compains, so we need to add to it.
(<any>window).format_date = (dateString: string, type: string) => {
  let d = new Date(dateString);
  return moment(d).calendar()
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
let myObject = {};
let mySecondReference = myObject;
