$(function() {

    ko.validation.locale('nb-NO');

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
                            p.type = d.type;
                            p.name = m.name + " " + d.name;
                            if (p.effect) {
                                p.name +=  " " + p.effect + "W";
                            }
                            if (d.mainSpec) {
                                p.name +=  " " + d.mainSpec + "W/m";
                            }
                            if (d.type == 'mat') {
                                p.name +=  "²";
                            }
                            if ('mainSpec' in d) {
                                p.mainSpec = d.mainSpec;
                            }
                            if ('secondarySpec' in d) {
                                p.secondarySpec = d.secondarySpec;
                            }
                            r.push(p);
                        }
                    }
                }
            }
            return r;
        }
        // Used to filter an arrayFilter.
        myArrayFilter = function(list_to_filter) {
            for (var i = 0; i < list_to_filter.length; i++) {
                f = list_to_filter[i][0];
                t = list_to_filter[i][1]();
                if (t && f != t) {
                    return false;
                }
            }
            return true;
        };

        self.filtered_products_no_mainSpec = ko.computed(function() {
            if (!rootModel.effect() && !rootModel.manufacturor() && !rootModel.mainSpec() && !rootModel.vk_type()) {
                return self.flat_products();
            }
            return ko.utils.arrayFilter(self.flat_products(), function(prod) {
                return myArrayFilter([
                    [prod.manufacturor, rootModel.manufacturor],
                    [prod.type, rootModel.vk_type]
                ]);

            }).sort(function(a, b) {
                return a.effect - b.effect;
            });
        });

        self.spec_groups = ko.computed(function() {
            filtered = self.filtered_products_no_mainSpec();
            var flags = {};
            return ko.utils.arrayFilter(self.filtered_products_no_mainSpec(), function(entry) {
                if (flags[entry.mainSpec]) {
                    return false;
                }
                flags[entry.mainSpec] = true;
                return true;
            });
        });



        self.filtered_products = ko.computed(function() {
            if (!rootModel.effect() && !rootModel.manufacturor() && !rootModel.mainSpec() && !rootModel.vk_type()) {
                return self.filtered_products_no_mainSpec();
            }
            return ko.utils.arrayFilter(self.filtered_products_no_mainSpec(), function(prod) {
                return myArrayFilter([
                    [prod.mainSpec, rootModel.mainSpec],
                    [prod.effect, rootModel.effect]
                ]);

            }).sort(function(a, b) {
                return a.effect - b.effect;
            });
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
        self.vk_type = ko.observable();
        self.mainSpec = ko.observable();

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

        function findWithAttr(array, attr, value) {
            for (var i = 0; i < array.length; i += 1) {
                if (array[i][attr] === value) {
                    return i;
                }
            }
            return -1;
        }

        ko.computed(function() {
            if (self.mainSpec()) {
                try {
                    var f = self.Products().spec_groups();
                    if (findWithAttr(f, 'mainSpec', self.mainSpec()) < 0) {
                        self.mainSpec(undefined);
                    }
                } catch (e) {

                } finally {

                }
            }
        });


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

        function get_user_forms(loading) {
            self.loading.push('user_form')
            $.get("/forms.json", {})
                .done(function(result) {
                    result.user_forms.prefix = 'user_forms';
                    result.company_forms.prefix = 'company_forms';
                    self.user_forms(result.user_forms);
                    self.company_forms(result.company_forms);
                    self.loading.remove('user_form')
                });
        }


        function get_company_forms() {
            return false
            $.get("/forms.json", {
                type: 'company'
            }).done(function(result, d) {
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
        self.expand_mods = function(e, d) {
            var t = $(d.target);
            var m = t.siblings('.modifications-table');
            var up = 'glyphicon-menu-up';
            var down = 'glyphicon-menu-down';
            m.toggleClass('hidden');
            if (m.hasClass('hidden')) {
                t.removeClass(up);
                t.addClass(down);
            } else {
                t.removeClass(down);
                t.addClass(up);
            }

        };
        self.delete = ko.observable();

        self.confirmed_delete = function(e, d) {
            self.delete('');
            self.loading.push('delete');
            $.ajax({
                    url: 'json/form_mod/' + e.id,
                    type: 'DELETE',
                    id: e.id
                })
                .done(function(result, d) {
                    self.loading.remove('delete');
                    get_user_forms();
                });
        };
        self.renamePrefix = function(e, d, f) {}
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
                self.loading.push('fill_form');
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
                        self.loading.remove('fill_form');
                        parse_form_download(result);
                    });
            } else {
                self.loading.push('fill_form');
                $.get("/json/heating/", {
                    'filled_form_modified_id': self.filled_form_modified_id()
                }).done(function(result) {
                    self.loading.remove('fill_form');
                    parse_form_download(result);
                });
            }
        };

        function parse_form_download(result) {
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

        self.loading = ko.observableArray();
    }

    // AppViewModel.suggestion.subscribe(function() { // called when an suggestion is selected to clear the suggestions
    //   AppViewModel.suggestions([]);
    // });
    var myApp = new AppViewModel();
    myApp.init();
    ko.applyBindings(myApp);
});

self.format_date = function(dateString, type) {
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
            pad(curr_hour, 2) + ':' + pad(curr_minute, 2);
    }
    return curr_date + '. ' + m_names[curr_month] + " " + curr_year + ' ' +
        pad(curr_hour, 2) + ':' + pad(curr_minute, 2);
};

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
