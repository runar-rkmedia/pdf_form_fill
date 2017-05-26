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

/**
 * almond 0.2.7 Copyright (c) 2011-2012, The Dojo Foundation All Rights Reserved.
 * Available via the MIT or new BSD license.
 * see: http://github.com/jrburke/almond for details
 */

(function(){var e,t,n;(function(r){function d(e,t){return h.call(e,t)}function v(e,t){var n,r,i,s,o,u,a,f,c,h,p=t&&t.split("/"),d=l.map,v=d&&d["*"]||{};if(e&&e.charAt(0)===".")if(t){p=p.slice(0,p.length-1),e=p.concat(e.split("/"));for(f=0;f<e.length;f+=1){h=e[f];if(h===".")e.splice(f,1),f-=1;else if(h===".."){if(f===1&&(e[2]===".."||e[0]===".."))break;f>0&&(e.splice(f-1,2),f-=2)}}e=e.join("/")}else e.indexOf("./")===0&&(e=e.substring(2));if((p||v)&&d){n=e.split("/");for(f=n.length;f>0;f-=1){r=n.slice(0,f).join("/");if(p)for(c=p.length;c>0;c-=1){i=d[p.slice(0,c).join("/")];if(i){i=i[r];if(i){s=i,o=f;break}}}if(s)break;!u&&v&&v[r]&&(u=v[r],a=f)}!s&&u&&(s=u,o=a),s&&(n.splice(0,o,s),e=n.join("/"))}return e}function m(e,t){return function(){return s.apply(r,p.call(arguments,0).concat([e,t]))}}function g(e){return function(t){return v(t,e)}}function y(e){return function(t){a[e]=t}}function b(e){if(d(f,e)){var t=f[e];delete f[e],c[e]=!0,i.apply(r,t)}if(!d(a,e)&&!d(c,e))throw new Error("No "+e);return a[e]}function w(e){var t,n=e?e.indexOf("!"):-1;return n>-1&&(t=e.substring(0,n),e=e.substring(n+1,e.length)),[t,e]}function E(e){return function(){return l&&l.config&&l.config[e]||{}}}var i,s,o,u,a={},f={},l={},c={},h=Object.prototype.hasOwnProperty,p=[].slice;o=function(e,t){var n,r=w(e),i=r[0];return e=r[1],i&&(i=v(i,t),n=b(i)),i?n&&n.normalize?e=n.normalize(e,g(t)):e=v(e,t):(e=v(e,t),r=w(e),i=r[0],e=r[1],i&&(n=b(i))),{f:i?i+"!"+e:e,n:e,pr:i,p:n}},u={require:function(e){return m(e)},exports:function(e){var t=a[e];return typeof t!="undefined"?t:a[e]={}},module:function(e){return{id:e,uri:"",exports:a[e],config:E(e)}}},i=function(e,t,n,i){var s,l,h,p,v,g=[],w=typeof n,E;i=i||e;if(w==="undefined"||w==="function"){t=!t.length&&n.length?["require","exports","module"]:t;for(v=0;v<t.length;v+=1){p=o(t[v],i),l=p.f;if(l==="require")g[v]=u.require(e);else if(l==="exports")g[v]=u.exports(e),E=!0;else if(l==="module")s=g[v]=u.module(e);else if(d(a,l)||d(f,l)||d(c,l))g[v]=b(l);else{if(!p.p)throw new Error(e+" missing "+l);p.p.load(p.n,m(i,!0),y(l),{}),g[v]=a[l]}}h=n?n.apply(a[e],g):undefined;if(e)if(s&&s.exports!==r&&s.exports!==a[e])a[e]=s.exports;else if(h!==r||!E)a[e]=h}else e&&(a[e]=n)},e=t=s=function(e,t,n,a,f){return typeof e=="string"?u[e]?u[e](t):b(o(e,t).f):(e.splice||(l=e,t.splice?(e=t,t=n,n=null):e=r),t=t||function(){},typeof n=="function"&&(n=a,a=f),a?i(r,e,t,n):setTimeout(function(){i(r,e,t,n)},4),s)},s.config=function(e){return l=e,l.deps&&s(l.deps,l.callback),s},e._defined=a,n=function(e,t,n){t.splice||(n=t,t=[]),!d(a,e)&&!d(f,e)&&(f[e]=[e,t,n])},n.amd={jQuery:!0}})(),n("../lib/almond",function(){}),n("closeHandler",[],function(){function e(t,n){return t===n?!0:n.parentNode==null?!1:e(t,n.parentNode)}function t(t,n){return function(r){e(t,r.srcElement)||n()}}function n(e,n,r){var r=t(n,r);return document.addEventListener(e,r,!0),function(){document.removeEventListener(e,r)}}return{create:function(e,t){var r=[],i;return i=function(){r.forEach(function(e){e()}),t()},r.push(n("click",e,i)),r.push(n("keypress",e,i)),i}}}),n("../lib/text",{load:function(e){throw new Error("Dynamic load not allowed: "+e)}}),n("../lib/text!../templates/dropdown.html",[],function(){return'<div class="dropdown" data-bind="if: loading">\r\n  <ul class="dropdown-menu" role="menu">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Loading...</a></li>\r\n  </ul>\r\n</div>\r\n<div class="dropdown" data-bind="if: (suggestions().length == 0 &amp;&amp; !loading())">\r\n  <ul class="dropdown-menu" role="menu">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">No matches found...</a></li>\r\n  </ul>\r\n</div>\r\n<div id="menu" class="dropdown" data-bind="if: suggestions().length">\r\n  <ul class="dropdown-menu" role="menu" data-bind="foreach: suggestions">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#" data-bind="text: name"></a></li>\r\n  </ul>\r\n</div>'}),n("constants",[],function(){var e;return e={Keys:{UP:38,DOWN:40,ENTER:13,ESC:27}}}),n("jquery",function(){return $}),n("ko",function(){return ko}),n("bindingHandler",["jquery","ko","closeHandler","../lib/text!../templates/dropdown.html","constants"],function(e,t,n,r,i){return t.bindingHandlers.dropdown={init:function(s,o,u,a,f){var l,c,h,p,d,v,m,g,y,b,w,E,S,x,T,N,C;return d=o(),T=!1,C=null,v=function(){},N=function(){var t;return T=!0,d.suggestion(""),t=e(".dropdown",h),t.addClass("open"),v=n.create(h.get(0),function(){return t.removeClass("open"),T=!1}),d.query(e(s).val())},b=function(){if(!T)return N()},g=function(){if(!T)return N()},p=function(e){return e.preventDefault(),e.stopPropagation()},E=function(e){switch(e.keyCode){case i.Keys.ENTER:return e.preventDefault()}},w=function(e){switch(e.keyCode){case i.Keys.ENTER:return e.preventDefault()}},S=function(n){var r,o;p(n);switch(n.keyCode){case i.Keys.UP:if(T)return r=e("li.selected",h),r.length?r.removeClass("selected").prev("li").addClass("selected"):e("li",h).last().addClass("selected");break;case i.Keys.DOWN:return T?(r=e("li.selected",h),r.length?r.removeClass("selected").next("li").addClass("selected"):e("li",h).first().addClass("selected")):N();case i.Keys.ENTER:if(T){r=e("li.selected > a",h);if(r.length)return o=t.dataFor(r.get(0)),d.suggestion(o),l.val(o.name),v()}break;case i.Keys.ESC:if(T)return v();break;default:return T||N(),clearTimeout(C),C=setTimeout(function(){return d.query(e(s).val())},200)}},y=function(e){var n;return p(e),n=t.dataFor(e.toElement),l.val(n.name),d.suggestion(n),v()},x=function(n){var r;p(n),r=t.dataFor(n.toElement);if(r!==f.$data)return e("li",h).removeClass("selected"),e(n.toElement).parent().addClass("selected")},m=function(e){var t;t=d.suggestion();if(!t)return d.suggestion(l.val())},l=e(s),h=l.parent(),h.append(e(r)),c=e("#menu",h),l.bind("focus",b),l.bind("click",g),l.bind("keyup",S),l.bind("keypress",E),l.bind("keydown",w),l.bind("change",m),c.bind("click",y),c.bind("mouseover",x),t.utils.domNodeDisposal.addDisposeCallback(s,function(){return l.unbind(b),l.unbind(g),l.unbind(S),l.unbind(E),l.unbind(w),l.unbind(m),c.unbind(y),c.unbind(x)})},update:function(e,t,n,r,i){}}}),t("bindingHandler")})();
$(function() {

      "use strict";

      function sortNumber(a, b) {
        return a - b;
      }

      function ProductModel(rootModel) {
        var self = this;
        self.products = ko.observableArray();
        self.flat_products = ko.computed(function () {
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
              });
            });


          self.spec_groups = ko.computed(function() {
            var array = self.products();
            var w = [];
            var w_squared = [];
            for (var i = 0; i < array.length; i++) {
              if (!rootModel.manufacturor() || rootModel.manufacturor() ===array[i].name) {
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
          }); self.getProducts = function() {
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


          self.anleggs_adresse = ko.observable();
          self.anleggs_poststed = ko.observable();
          self.anleggs_postnummer = ko.observable();

          self.manufacturor = ko.observable();
          self.watt_per_meter = ko.observable();

          self.rom_navn = ko.observable();
          self.areal = ko.observable();
          self.oppvarmet_areal = ko.observable();
          self.effect = ko.observable();

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
          self.selected_vk = ko.observable();

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
            self.form_args($('#form').serialize());
            if (self.form_changed()) {
              console.log('sending...');
              $.post("/json/heating/",
                  {
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
                    'product_id': self.selected_vk()

                  })
                .done(function(result) {
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
