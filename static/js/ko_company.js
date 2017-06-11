$(function() {

  "use strict";


  function AppControlCompany() {
    var self = this;

    self.invites = ko.observableArray();
    self.base_url = ko.observable();

    $.get("/invite.json")
      .done(function(result) {
        self.invites(result.invites);
        self.base_url(result.base_url);
        console.log(result);
      });

    self.createInvite = function() {
      $.post("/invite.json")
        .done(function(result) {
          self.invites(result.invites);
          self.base_url(result.base_url);
        })
        .fail(function(result, t, d) {
          console.log(result.responseText);
          $('.flash').append('<li class="error">'+ result.responseText + '</li>')
          // alert(result.reposneText);
        })
    };
  }
  var myAppControlCompany = new AppControlCompany();
  ko.applyBindings(myAppControlCompany);
  console.log('sdf');
});
