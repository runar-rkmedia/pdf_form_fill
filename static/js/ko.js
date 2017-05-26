$(function() {

  "use strict";

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
        data = flatten_products(result)
      })
      .fail(function(e) {
        console.log('Could not retrieve data: Error ' + e.status);
      });

    function Item(name) {
      this.name = name;
    }

    function flatten_products(products) {
      var r = [];
      for (var i = 0; i < products.length; i++) {
        var m = products[i]
        for (var j = 0; j < m['product_types'].length; j++) {
          var d = m['product_types'][j]
          for (var k = 0; k < d['products'].length; k++) {
            var p = d['products'][k]
            p['name'] = m.name + " " + d.name + " " + p.effect + "W"
            r.push(p)
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

  model = {


    anleggs_adresse: ko.observable(),
    anleggs_poststed: ko.observable(),
    anleggs_postnummer: ko.observable(),

    manufacturor: ko.observable(),
    watt_per_meter: ko.observable(),

    rom_navn: ko.observable(),
    areal: ko.observable(),
    oppvarmet_areal: ko.observable(),
    effect: ko.observable(),

    ohm_a: ko.observable(),
    ohm_b: ko.observable(),
    ohm_c: ko.observable(),

    mohm_a: ko.observable(),
    mohm_b: ko.observable(),
    mohm_c: ko.observable(),

    error_fields: ko.observableArray(),
    error_message: ko.observable(),

    file_download: ko.observable(),

    post_form: function() {
      $.post("/json/heating/",
          $('#form').serialize())
        .done(function(result) {
          var form = $('#form');
          console.log(result)
          if (result.error_fields) {
            model.error_fields(result.error_fields)
          }
          if (result.file_download) {
            model.file_download(result.file_download)
          }
          if (result.error_message) {
            model.error_message(result.error_message)
          }


        })
    },

    loading: ko.observable(false), // true to show 'Loading...'
    suggestion: ko.observable(""), // the selected suggestion
    suggestions: ko.observableArray([]), // the selections available
    query: function(term) { // called to query for the data and to update the suggestions
      model.loading(true);
      service.query(term).then(function(data) {
        model.loading(false);
        model.suggestions(data);
      });
    }
  };

  model.suggestion.subscribe(function() { // called when an suggestion is selected to clear the suggestions
    model.suggestions([]);
  });

  ko.applyBindings(model);
});
