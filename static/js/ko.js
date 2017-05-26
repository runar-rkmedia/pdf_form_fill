$(function() {

  "use strict";

  function sortNumber(a, b) {
    return a - b;
  }

  var service, model;
  // a dummy service used in the example
  service = (function() {

    var data = [
      new Item("One"),
      new Item("Two"),
      new Item("Three"),
      new Item("Four"),
      new Item("Five"),
      new Item("Six")
    ];

    $.get("/products.json",
        $('#form').serialize())
      .done(function(result) {
        data = flatten_products(result);
      })
      .fail(function(e) {
        console.log('Could not retrieve data = Error ' + e.status);
      });

    function Item(name) {
      this.name = name;
    }

    function flatten_products(products) {
      var r = [];
      for (var i = 0; i < products.length; i++) {
        var m = products[i];
        for (var j = 0; j < m.product_types.length; j++) {
          var d = m.product_types[j];
          for (var k = 0; k < d.products.length; k++) {
            var p = d.products[k];
            p.name = m.name + " " + d.name + " " + p.effect + "W";
            r.push(p);
          }
        }
      }
      return r;
    }

    function query(term) {
      return $.Deferred(function(deferred) {
        deferred.resolve(data.filter(function(item) {
          return !!~item.name.toLowerCase().indexOf(term.toLowerCase());
        }));
      });
    }

    return {
      query: query
    };
  })();

  function ProductModel(rootModel) {
    var self = this;
    self.products = ko.observableArray();

    self.filtered_products = ko.computed(function() {
      return ko.utils.arrayFilter(self.products(), function(prod) {
        return prod.name == rootModel.manufacturor();
      });


    });
    self.spec_groups = ko.computed(function() {
      var array = self.filtered_products();
      var w = [];
      var w_squared = [];
      for (var i = 0; i < array.length; i++) {
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
        })
        .fail(function(e) {
          console.log('Could not retrieve data = Error ' + e.status);
        });
    };
  }

  function AppViewModel() {

    var self = this;


    self.anleggs_adresse = ko.observable('sdfsd');
    self.anleggs_poststed = ko.observable();
    self.anleggs_postnummer = ko.observable();

    self.manufacturor = ko.observable('Nexans');
    self.watt_per_meter = ko.observable("17");

    self.rom_navn = ko.observable();
    self.areal = ko.observable();
    self.oppvarmet_areal = ko.observable(4);
    self.effect = ko.observable(500);

    self.ohm_a = ko.observable();
    self.ohm_b = ko.observable();
    self.ohm_c = ko.observable();

    self.mohm_a = ko.observable();
    self.mohm_b = ko.observable();
    self.mohm_c = ko.observable();

    self.error_fields = ko.observableArray();
    self.error_message = ko.observable();

    self.file_download = ko.observable();

    self.last_sent_args = ko.observable();
    self.form_args = ko.observable($('#form').serialize());

    self.Products = ko.observable();

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


    self.post_form = function(e, t) {
      self.form_args($('#form').serialize())
      if (self.form_changed()) {
        console.log('sending...');
        $.post("/json/heating/",
            self.form_args())
          .done(function(result) {
            console.log(result);
            self.last_sent_args(self.form_args());
            if (result.error_fields) {
              self.error_fields(result.error_fields);
            }
            if (result.file_download) {
              self.file_download(result.file_download);
            }
            if (result.error_message) {
              self.error_message(result.error_message);
            }


          });
      }
    };

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
