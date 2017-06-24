$(function() {

  "use strict";

  function sortNumber(a, b) {
    return a - b;
  }

  function ProductModel(rootModel) {
    var self = this;
    self.products = ko.observableArray();
    self.flat_products = ko.computed(function() {
      return flatten_products(self.products());
    });

    function flatten_products(products) {
      var r = [];
      if (products) {
        for (var i = 0; i < products.length; i++) {
          var m = products[i];
          for (var j = 0; j < m.product_types.length; j++) {
            var d = m.product_types[j];
            for (var k = 0; k < d.products.length; k++) {
              var p = d.products[k];
              p.manufacturor = m.name;
              p.name = m.name + " " + d.name + " " + p.effect + "W";
              if ('watt_per_meter' in d) {
                p.watt_per_meter = d.watt_per_meter;
              }
              if ('watt_per_square_meter' in d) {
                p.watt_per_square_meter = d.watt_per_square_meter;
              }
              r.push(p);
            }
          }
        }
      }
      return r;
    }

    self.filtered_products = ko.computed(function() {
      return ko.utils.arrayFilter(self.flat_products(), function(prod) {
        var e = rootModel.effect();
        var w = rootModel.watt_per_meter();
        var m = rootModel.manufacturor();
        var f_e = false;
        var f_w = false;
        var f_m = false;
        if (!(w || e || m)) {
          return self.flat_products();
        }
        if (e) {
          f_e = true;
          if (prod.effect == e) {
            f_e = false;
          }
        }
        if (m) {
          f_m = true;
          if (prod.manufacturor == m) {
            f_m = false;
          }
        }
        if (w) {
          f_w = true;
          if (prod.watt_per_meter == w) {
            f_w = false;
          }
        }
        return !(f_e || f_m || f_w);
      }).sort(function(a, b) {
        return a.effect - b.effect;
      });
    });

    // self.filtered_products_effect = ko.computed(function() {
    //   var effects = [];
    //   var fp = self.flat_products();
    //   console.log('....');
    //   for (var i = 0; i < fp.length; i++) {
    //     var this_fp = fp[i].effect;
    //     effects.push(this_fp);
    //   }
    //   return ko.utils.arrayGetDistinctValues(effects).sort(function(a, b) {
    //     return a - b;
    //   });
    // });


    self.spec_groups = ko.computed(function() {
      var array = self.products();
      var w = [];
      var w_squared = [];
      for (var i = 0; i < array.length; i++) {
        if (!rootModel.manufacturor() || rootModel.manufacturor() === array[i].name) {
          var m = array[i].product_types;
          for (var j = 0; j < m.length; j++) {
            var p = m[j];
            if ('watt_per_meter' in p && w.indexOf(p.watt_per_meter) == -1) {
              w.push(p.watt_per_meter);
            }
            if ('watt_per_square_meter' in p && w.indexOf(p.watt_per_square_meter) == -1) {
              w_squared.push('watt_per_square_meter');
            }
          }
        }
      }
      return {
        'watt_per_meter': w.sort(sortNumber),
        'watt_per_square_meter': w_squared
      };
    });
    self.getProducts = function() {
      $.get("/products.json",
          $('#form').serialize())
        .done(function(result) {
          self.products(result);
          rootModel.selected_vk(rootModel.forced_selected_vk());
        })
        .fail(function(e) {
          console.log('Could not retrieve data = Error ' + e.status);
        });
    };
  }

  function AppViewModel() {

    var self = this;

    ko.validation.init({
      decorateInputElement: true,
      errorElementClass: 'has-error has-feedback',
      // successElementClass: 'has-feedback has-success',
      insertMessages: true,
      decorateElement: true,
      // errorElementClass: 'error',
      errorMessageClass: 'bg-danger'
    });

    // Add bootstrap-validation-css to parent of field
    var init = ko.bindingHandlers['validationCore'].init;
    ko.bindingHandlers['validationCore'].init = function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
      init(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);
      var config = ko.validation.utils.getConfigOptions(element);
      // if requested, add binding to decorate element
      if (config.decorateInputElement && ko.validation.utils.isValidatable(valueAccessor())) {
        var parent = $(element).parent();
        if (parent.length) {
          ko.applyBindingsToNode(parent[0], {
            validationElement: valueAccessor()
          });
        }
      }
    };



    self.anleggs_adresse = ko.observable().extend({
      required: true,
      minLength: 3,
    });
    self.anleggs_poststed = ko.observable().extend({
      required: true,
      minLength: 3,
    });
    self.anleggs_postnummer = ko.observable().extend({
      required: true,
      minLength: 4,
      number: true,
      min: 1000,
      max: 9999,
    });

    self.manufacturor = ko.observable();
    self.watt_per_meter = ko.observable();

    self.rom_navn = ko.observable().extend({
      required: true,
      minLength: 2,
    });
    self.areal = ko.observable().extend({
      number: true,
      min: 0.1
    });
    self.oppvarmet_areal = ko.observable().extend({
      required: true,
      number: true,
      min: 0.1
    });
    self.effect = ko.observable().extend({
      number: true,
    });

    self.ohm_a = ko.observable().extend({
      number: true,
      min: 0,
      max: 1000,
    });
    self.ohm_b = ko.observable().extend({
      number: true,
      min: 0,
      max: 1000,
    });
    self.ohm_c = ko.observable().extend({
      number: true,
      min: 0,
      max: 1000,
    });

    self.mohm_a = ko.observable();
    self.mohm_b = ko.observable();
    self.mohm_c = ko.observable();

    self.error_fields = ko.observableArray();
    self.error_message = ko.observable();

    self.file_download = ko.observable();

    self.last_sent_args = ko.observable();
    self.form_args = ko.observable($('#form').serialize());

    self.Products = ko.observable();
    self.selected_vk = ko.observable();
    self.forced_selected_vk = ko.observable();

    self.address_id = ko.observable();
    self.filled_form_modified_id = ko.observable();

    self.user_forms = ko.observableArray();
    self.company_forms = ko.observableArray();

    self.prefill = false;


    self.validation_errors = ko.validation.group(self);


    if (self.prefill) {
      self.anleggs_adresse('Kingsroad 1');
      self.anleggs_postnummer(4321);
      self.anleggs_poststed('Kings place');
      self.rom_navn('Kings room');
      self.areal(1000);
      self.oppvarmet_areal(900);
      self.forced_selected_vk(3);
      self.ohm_a(1);
      self.ohm_b(2);
      self.ohm_c(3);
      self.mohm_a(true);
      self.mohm_b(true);
      self.mohm_c(true);
    }

    self.init = function() {
      self.Products(new ProductModel(self));
      self.Products().getProducts();
    };




    $('body').on("change keyup paste click", 'input', function() {
      self.form_args($('#form').serialize());
    });
    self.form_changed = ko.computed(function() {
      return self.form_args() !== self.last_sent_args();
    }, this);


    ko.computed(function() {
      try {
        var f = self.Products().flat_products();
        if (f.length > 0) {
          get_user_forms();
          get_company_forms();
        }
      } catch (e) {

      } finally {

      }
    });

    function get_user_forms() {
      $.get("/forms.json", {}).done(function(result) {
        console.log(result);
        self.user_forms(result);
      });
    }

    function get_company_forms() {
      $.get("/forms.json", {
        type: 'company'
      }).done(function(result) {
        console.log(result);
        self.company_forms(result);
      });
    }
    self.get_product_by_id = function(id) {
      var f = self.Products().flat_products();
      for (var i = 0; i < f.length; i++) {
        if (f[i].id == id) {
          return f[i];
        }
      }
    };
    self.edit_form = function(e) {
      var f = e.request_form;
      self.filled_form_modified_id(e.id);
      self.anleggs_adresse(f.anleggs_adresse);
      self.anleggs_postnummer(f.anleggs_postnummer);
      self.anleggs_poststed(f.anleggs_poststed);
      self.rom_navn(f.rom_navn);
      self.areal(f.areal);
      self.oppvarmet_areal(f.oppvarmet_areal);
      self.selected_vk(f.product_id);
      self.address_id(e.address_id);
      self.filled_form_modified_id(e.id);
      self.ohm_a(f.ohm_a);
      self.ohm_b(f.ohm_b);
      self.ohm_c(f.ohm_c);
      self.mohm_a(f.mohm_a);
      self.mohm_b(f.ohm_b);
      self.mohm_c(f.ohm_c);
      self.last_sent_args($('#form').serialize());
      self.form_args($('#form').serialize());
      $('.nav-tabs a[href="#main_form"]').tab('show');
    };
    self.post_form = function(e, t) {
      self.form_args($('#form').serialize());
      if (self.validation_errors().length > 0) {
        self.validation_errors.showAllMessages();
        return false;
      }
      if (self.form_changed() || !self.filled_form_modified_id()) {
        // self.file_download(false);
        self.loading(true);
        $.post("/json/heating/", {
            'anleggs_adresse': self.anleggs_adresse(),
            'anleggs_poststed': self.anleggs_poststed(),
            'anleggs_postnummer': self.anleggs_postnummer(),
            'rom_navn': self.rom_navn(),
            'areal': self.areal(),
            'oppvarmet_areal': self.oppvarmet_areal(),
            'mohm_a': self.mohm_a(),
            'mohm_b': self.mohm_b(),
            'mohm_c': self.mohm_c(),
            'ohm_a': self.ohm_a(),
            'ohm_b': self.ohm_b(),
            'ohm_c': self.ohm_c(),
            'product_id': self.selected_vk(),
            'address_id': self.address_id(),
            'filled_form_modified_id': self.filled_form_modified_id()
          })
          .done(function(result) {
            parse_form_download(result);
          });
      } else {
        console.log(self.form_changed());
        self.loading(true);
        $.get("/json/heating/", {
          'filled_form_modified_id': self.filled_form_modified_id()
        }).done(function(result) {
          parse_form_download(result);
        });
      }
    };

    function parse_form_download(result) {
      console.log(result);
      self.loading(false);
      self.last_sent_args(self.form_args());
      if (result.error_fields) {
        self.error_fields(result.error_fields);
      }
      if (result.file_download) {
        self.file_download(result.file_download);
        if (result.address_id) {
          self.address_id(result.address_id);
        }
        if (result.filled_form_modified_id) {
          self.filled_form_modified_id(result.filled_form_modified_id);
        }
      }
      if (result.error_message) {
        self.error_message(result.error_message);
      }
    }

    self.loading = ko.observable(false); // true to show 'Loading...'
    self.suggestion = ko.observable(""); // the selected suggestion
    self.suggestions = ko.observableArray([]); // the selections available
    self.query = function(term) { // called to query for the data and to update the suggestions
      self.loading(true);
      service.query(term).then(function(data) {
        self.loading(false);
        self.suggestions(data);
      });
    };
  }

  // AppViewModel.suggestion.subscribe(function() { // called when an suggestion is selected to clear the suggestions
  //   AppViewModel.suggestions([]);
  // });
  var myApp = new AppViewModel();
  myApp.init();
  ko.applyBindings(myApp);
});

self.format_date = function(dateString) {
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
  return curr_date + '. ' + m_names[curr_month] + " " + curr_year + ' ' +
    pad(curr_hour, 2) + ':' + pad(curr_minute, 2)
}

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

$(function() {
  $('input[type=tel]').on('input', function(e) {
    this.value = this.value.replace(/\D/g, '');
  })
})
