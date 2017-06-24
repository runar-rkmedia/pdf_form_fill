(function(){var e,t,n;(function(r){function d(e,t){return h.call(e,t)}function v(e,t){var n,r,i,s,o,u,a,f,c,h,p=t&&t.split("/"),d=l.map,v=d&&d["*"]||{};if(e&&e.charAt(0)===".")if(t){p=p.slice(0,p.length-1),e=p.concat(e.split("/"));for(f=0;f<e.length;f+=1){h=e[f];if(h===".")e.splice(f,1),f-=1;else if(h===".."){if(f===1&&(e[2]===".."||e[0]===".."))break;f>0&&(e.splice(f-1,2),f-=2)}}e=e.join("/")}else e.indexOf("./")===0&&(e=e.substring(2));if((p||v)&&d){n=e.split("/");for(f=n.length;f>0;f-=1){r=n.slice(0,f).join("/");if(p)for(c=p.length;c>0;c-=1){i=d[p.slice(0,c).join("/")];if(i){i=i[r];if(i){s=i,o=f;break}}}if(s)break;!u&&v&&v[r]&&(u=v[r],a=f)}!s&&u&&(s=u,o=a),s&&(n.splice(0,o,s),e=n.join("/"))}return e}function m(e,t){return function(){return s.apply(r,p.call(arguments,0).concat([e,t]))}}function g(e){return function(t){return v(t,e)}}function y(e){return function(t){a[e]=t}}function b(e){if(d(f,e)){var t=f[e];delete f[e],c[e]=!0,i.apply(r,t)}if(!d(a,e)&&!d(c,e))throw new Error("No "+e);return a[e]}function w(e){var t,n=e?e.indexOf("!"):-1;return n>-1&&(t=e.substring(0,n),e=e.substring(n+1,e.length)),[t,e]}function E(e){return function(){return l&&l.config&&l.config[e]||{}}}var i,s,o,u,a={},f={},l={},c={},h=Object.prototype.hasOwnProperty,p=[].slice;o=function(e,t){var n,r=w(e),i=r[0];return e=r[1],i&&(i=v(i,t),n=b(i)),i?n&&n.normalize?e=n.normalize(e,g(t)):e=v(e,t):(e=v(e,t),r=w(e),i=r[0],e=r[1],i&&(n=b(i))),{f:i?i+"!"+e:e,n:e,pr:i,p:n}},u={require:function(e){return m(e)},exports:function(e){var t=a[e];return typeof t!="undefined"?t:a[e]={}},module:function(e){return{id:e,uri:"",exports:a[e],config:E(e)}}},i=function(e,t,n,i){var s,l,h,p,v,g=[],w=typeof n,E;i=i||e;if(w==="undefined"||w==="function"){t=!t.length&&n.length?["require","exports","module"]:t;for(v=0;v<t.length;v+=1){p=o(t[v],i),l=p.f;if(l==="require")g[v]=u.require(e);else if(l==="exports")g[v]=u.exports(e),E=!0;else if(l==="module")s=g[v]=u.module(e);else if(d(a,l)||d(f,l)||d(c,l))g[v]=b(l);else{if(!p.p)throw new Error(e+" missing "+l);p.p.load(p.n,m(i,!0),y(l),{}),g[v]=a[l]}}h=n?n.apply(a[e],g):undefined;if(e)if(s&&s.exports!==r&&s.exports!==a[e])a[e]=s.exports;else if(h!==r||!E)a[e]=h}else e&&(a[e]=n)},e=t=s=function(e,t,n,a,f){return typeof e=="string"?u[e]?u[e](t):b(o(e,t).f):(e.splice||(l=e,t.splice?(e=t,t=n,n=null):e=r),t=t||function(){},typeof n=="function"&&(n=a,a=f),a?i(r,e,t,n):setTimeout(function(){i(r,e,t,n)},4),s)},s.config=function(e){return l=e,l.deps&&s(l.deps,l.callback),s},e._defined=a,n=function(e,t,n){t.splice||(n=t,t=[]),!d(a,e)&&!d(f,e)&&(f[e]=[e,t,n])},n.amd={jQuery:!0}})(),n("../lib/almond",function(){}),n("closeHandler",[],function(){function e(t,n){return t===n?!0:n.parentNode==null?!1:e(t,n.parentNode)}function t(t,n){return function(r){e(t,r.srcElement)||n()}}function n(e,n,r){var r=t(n,r);return document.addEventListener(e,r,!0),function(){document.removeEventListener(e,r)}}return{create:function(e,t){var r=[],i;return i=function(){r.forEach(function(e){e()}),t()},r.push(n("click",e,i)),r.push(n("keypress",e,i)),i}}}),n("../lib/text",{load:function(e){throw new Error("Dynamic load not allowed: "+e)}}),n("../lib/text!../templates/dropdown.html",[],function(){return'<div class="dropdown" data-bind="if: loading">\r\n  <ul class="dropdown-menu" role="menu">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Loading...</a></li>\r\n  </ul>\r\n</div>\r\n<div class="dropdown" data-bind="if: (suggestions().length == 0 &amp;&amp; !loading())">\r\n  <ul class="dropdown-menu" role="menu">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">No matches found...</a></li>\r\n  </ul>\r\n</div>\r\n<div id="menu" class="dropdown" data-bind="if: suggestions().length">\r\n  <ul class="dropdown-menu" role="menu" data-bind="foreach: suggestions">\r\n    <li role="presentation"><a role="menuitem" tabindex="-1" href="#" data-bind="text: name"></a></li>\r\n  </ul>\r\n</div>'}),n("constants",[],function(){var e;return e={Keys:{UP:38,DOWN:40,ENTER:13,ESC:27}}}),n("jquery",function(){return $}),n("ko",function(){return ko}),n("bindingHandler",["jquery","ko","closeHandler","../lib/text!../templates/dropdown.html","constants"],function(e,t,n,r,i){return t.bindingHandlers.dropdown={init:function(s,o,u,a,f){var l,c,h,p,d,v,m,g,y,b,w,E,S,x,T,N,C;return d=o(),T=!1,C=null,v=function(){},N=function(){var t;return T=!0,d.suggestion(""),t=e(".dropdown",h),t.addClass("open"),v=n.create(h.get(0),function(){return t.removeClass("open"),T=!1}),d.query(e(s).val())},b=function(){if(!T)return N()},g=function(){if(!T)return N()},p=function(e){return e.preventDefault(),e.stopPropagation()},E=function(e){switch(e.keyCode){case i.Keys.ENTER:return e.preventDefault()}},w=function(e){switch(e.keyCode){case i.Keys.ENTER:return e.preventDefault()}},S=function(n){var r,o;p(n);switch(n.keyCode){case i.Keys.UP:if(T)return r=e("li.selected",h),r.length?r.removeClass("selected").prev("li").addClass("selected"):e("li",h).last().addClass("selected");break;case i.Keys.DOWN:return T?(r=e("li.selected",h),r.length?r.removeClass("selected").next("li").addClass("selected"):e("li",h).first().addClass("selected")):N();case i.Keys.ENTER:if(T){r=e("li.selected > a",h);if(r.length)return o=t.dataFor(r.get(0)),d.suggestion(o),l.val(o.name),v()}break;case i.Keys.ESC:if(T)return v();break;default:return T||N(),clearTimeout(C),C=setTimeout(function(){return d.query(e(s).val())},200)}},y=function(e){var n;return p(e),n=t.dataFor(e.toElement),l.val(n.name),d.suggestion(n),v()},x=function(n){var r;p(n),r=t.dataFor(n.toElement);if(r!==f.$data)return e("li",h).removeClass("selected"),e(n.toElement).parent().addClass("selected")},m=function(e){var t;t=d.suggestion();if(!t)return d.suggestion(l.val())},l=e(s),h=l.parent(),h.append(e(r)),c=e("#menu",h),l.bind("focus",b),l.bind("click",g),l.bind("keyup",S),l.bind("keypress",E),l.bind("keydown",w),l.bind("change",m),c.bind("click",y),c.bind("mouseover",x),t.utils.domNodeDisposal.addDisposeCallback(s,function(){return l.unbind(b),l.unbind(g),l.unbind(S),l.unbind(E),l.unbind(w),l.unbind(m),c.unbind(y),c.unbind(x)})},update:function(e,t,n,r,i){}}}),t("bindingHandler")})();$(function(){"use strict";function sortNumber(a,b){return a-b;}
function ProductModel(rootModel){var self=this;self.products=ko.observableArray();self.flat_products=ko.computed(function(){return flatten_products(self.products());});function flatten_products(products){var r=[];if(products){for(var i=0;i<products.length;i++){var m=products[i];for(var j=0;j<m.product_types.length;j++){var d=m.product_types[j];for(var k=0;k<d.products.length;k++){var p=d.products[k];p.manufacturor=m.name;p.name=m.name+" "+d.name+" "+p.effect+"W";if('watt_per_meter'in d){p.watt_per_meter=d.watt_per_meter;}
if('watt_per_square_meter'in d){p.watt_per_square_meter=d.watt_per_square_meter;}
r.push(p);}}}}
console.log(r);return r;}
self.filtered_products=ko.computed(function(){return ko.utils.arrayFilter(self.flat_products(),function(prod){var e=rootModel.effect();var w=rootModel.watt_per_meter();var m=rootModel.manufacturor();var f_e=false;var f_w=false;var f_m=false;if(!(w||e||m)){return self.flat_products();}
if(e){f_e=true;if(prod.effect==e){f_e=false;}}
if(m){f_m=true;if(prod.manufacturor==m){f_m=false;}}
if(w){f_w=true;if(prod.watt_per_meter==w){f_w=false;}}
return!(f_e||f_m||f_w);}).sort(function(a,b){return a.effect-b.effect;});});self.spec_groups=ko.computed(function(){var array=self.products();var w=[];var w_squared=[];for(var i=0;i<array.length;i++){if(!rootModel.manufacturor()||rootModel.manufacturor()===array[i].name){var m=array[i].product_types;for(var j=0;j<m.length;j++){var p=m[j];if('watt_per_meter'in p&&w.indexOf(p.watt_per_meter)==-1){w.push(p.watt_per_meter);}
if('watt_per_square_meter'in p&&w.indexOf(p.watt_per_square_meter)==-1){w_squared.push('watt_per_square_meter');}}}}
return{'watt_per_meter':w.sort(sortNumber),'watt_per_square_meter':w_squared};});self.getProducts=function(){$.get("/products.json",$('#form').serialize()).done(function(result){self.products(result);rootModel.selected_vk(rootModel.forced_selected_vk());}).fail(function(e){console.log('Could not retrieve data = Error '+e.status);});};}
function AppViewModel(){var self=this;self.anleggs_adresse=ko.observable();self.anleggs_poststed=ko.observable();self.anleggs_postnummer=ko.observable();self.manufacturor=ko.observable();self.watt_per_meter=ko.observable();self.rom_navn=ko.observable();self.areal=ko.observable();self.oppvarmet_areal=ko.observable();self.effect=ko.observable();self.ohm_a=ko.observable();self.ohm_b=ko.observable();self.ohm_c=ko.observable();self.mohm_a=ko.observable();self.mohm_b=ko.observable();self.mohm_c=ko.observable();self.error_fields=ko.observableArray();self.error_message=ko.observable();self.file_download=ko.observable();self.last_sent_args=ko.observable();self.form_args=ko.observable($('#form').serialize());self.Products=ko.observable();self.selected_vk=ko.observable();self.forced_selected_vk=ko.observable();self.address_id=ko.observable();self.filled_form_id=ko.observable();self.user_forms=ko.observableArray();self.prefill=false;if(self.prefill){self.anleggs_adresse('Kingsroad 1');self.anleggs_postnummer(4321);self.anleggs_poststed('Kings place');self.rom_navn('Kings room');self.areal(1000);self.oppvarmet_areal(900);self.forced_selected_vk(3);self.ohm_a(1);self.ohm_b(2);self.ohm_c(3);self.mohm_a(true);self.mohm_b(true);self.mohm_c(true);}
self.init=function(){self.Products(new ProductModel(self));self.Products().getProducts();};$('body').on("change keyup paste click",'input',function(){self.form_args($('#form').serialize());});self.form_changed=ko.computed(function(){return self.form_args()!==self.last_sent_args();},this);ko.computed(function(){try{var f=self.Products().flat_products();if(f.length>0){get_user_forms();}}catch(e){}finally{}});function get_user_forms(){$.get("/forms.json",{}).done(function(result){console.log(result);self.user_forms(result);});}
self.get_product_by_id=function(id){var f=self.Products().flat_products();for(var i=0;i<f.length;i++){if(f[i].id==id){return f[i];}}};self.edit_form=function(e){var f=e.request_form;self.filled_form_id(e.id);self.anleggs_adresse(f.anleggs_adresse);self.anleggs_postnummer(f.anleggs_postnummer);self.anleggs_poststed(f.anleggs_poststed);self.rom_navn(f.rom_navn);self.areal(f.areal);self.oppvarmet_areal(f.oppvarmet_areal);self.selected_vk(f.product_id);self.address_id(e.address_id);self.filled_form_id(e.id);self.ohm_a(f.ohm_a);self.ohm_b(f.ohm_b);self.ohm_c(f.ohm_c);self.mohm_a(f.mohm_a);self.mohm_b(f.ohm_b);self.mohm_c(f.ohm_c);$('.nav-tabs a[href="#main_form"]').tab('show');console.log('adress'+e.address_id)
console.log('filled_form_id'+e.id)
console.log(f);};self.post_form=function(e,t){self.form_args($('#form').serialize());if(self.form_changed()){self.loading(true);$.post("/json/heating/",{'anleggs_adresse':self.anleggs_adresse(),'anleggs_poststed':self.anleggs_poststed(),'anleggs_postnummer':self.anleggs_postnummer(),'rom_navn':self.rom_navn(),'areal':self.areal(),'oppvarmet_areal':self.oppvarmet_areal(),'mohm_a':self.mohm_a(),'mohm_b':self.mohm_b(),'mohm_c':self.mohm_c(),'ohm_a':self.ohm_a(),'ohm_b':self.ohm_b(),'ohm_c':self.ohm_c(),'product_id':self.selected_vk(),'address_id':self.address_id(),'filled_form_id':self.filled_form_id()}).done(function(result){self.loading(false);self.last_sent_args(self.form_args());if(result.error_fields){self.error_fields(result.error_fields);}
if(result.file_download){self.file_download(result.file_download);self.address_id(result.address_id);self.filled_form_id(result.filled_form_id);}
if(result.error_message){self.error_message(result.error_message);}});}};self.loading=ko.observable(false);self.suggestion=ko.observable("");self.suggestions=ko.observableArray([]);self.query=function(term){self.loading(true);service.query(term).then(function(data){self.loading(false);self.suggestions(data);});};}
var myApp=new AppViewModel();myApp.init();ko.applyBindings(myApp);});self.format_date=function(dateString){var d_names=new Array("Søndag","Mandag","Tirsdag","Onsdag","Torsdag","Fredag","Søndag");var m_names=new Array("januar","februar","mars","april","mai","juni","juli","august","september","october","november","december");var d=new Date(dateString);var curr_day=d.getDay();var curr_date=d.getDate();var curr_month=d.getMonth();var curr_year=d.getFullYear();var curr_hour=d.getHours();var curr_minute=d.getMinutes();return curr_date+'. '+m_names[curr_month]+" "+curr_year+' '+
pad(curr_hour,2)+':'+pad(curr_minute,2)}
function pad(n,width,z){z=z||'0';n=n+'';return n.length>=width?n:new Array(width-n.length+1).join(z)+n;}