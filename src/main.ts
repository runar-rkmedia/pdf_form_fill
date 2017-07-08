import $ = require("jquery");
import ko = require("knockout");
import ko_validation = require("knockout.validation");

interface ProductInterface {
    effect: number;
    id: number;
    // These only exist on flatten products
    manufacturor?: string;
    type?: string;
    name?: string;
    mainSpec?: number;
}

interface ProductTypeInterface {
    id: number;
    mainSpec: number;
    secondarySpec: number
    type: string
    products: ProductInterface[]
    name: string
}

interface ManufacturorInterface {
    id: number;
    name: string;
    product_types: ProductTypeInterface[]
}

interface ArrayFylterInterface {
    value: any,
    mustEqual: any
}


class TSProductModel {
    products: KnockoutObservableArray<ManufacturorInterface>

    constructor(private parentModel: any) {
        // this.products = ko.observable()
    }
    // Used to filter an arrayFilter.
    myArrayFilter = (list_to_filter: ArrayFylterInterface[]) => {
        for (var i = 0; i < list_to_filter.length; i++) {
            var f = list_to_filter[i]['value'];
            var t = list_to_filter[i]['mustEqual']();
            if (t && f != t) {
                return false;
            }
        }
        return true;
    };

    products = ko.observableArray();
    getProducts = () => {
        $.get("/products.json",
            $('#form').serialize())
            .done((result: ManufacturorInterface[]) => {
                this.products(result);
                this.parentModel.selected_vk(this.parentModel.forced_selected_vk());
            })
            .fail((e) => {
                console.log('Could not retrieve data = Error ' + e.status);
            });
    };
    flatten_products = (products_to_parse: ManufacturorInterface[]) => {
        var r = [];
        if (products_to_parse) {
            for (var i = 0; i < products_to_parse.length; i++) {
                var m = products_to_parse[i];
                for (var j = 0; j < m.product_types.length; j++) {
                    var d = m.product_types[j];
                    for (var k = 0; k < d.products.length; k++) {
                        var p = d.products[k];
                        p.manufacturor = m.name;
                        p.type = d.type;
                        p.name = m.name + " " + d.name;
                        if (p.effect) {
                            p.name += " " + p.effect + "W";
                        }
                        if (d.mainSpec) {
                            p.name += " " + d.mainSpec + "W/m";
                        }
                        if (d.type == 'mat') {
                            p.name += "²";
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
    };
    flat_products = ko.computed(() => {
        return this.flatten_products(this.products());
    });
    filtered_products_no_mainSpec = ko.computed(() => {
        if (!this.parentModel.effect() && !this.parentModel.manufacturor() && !this.parentModel.mainSpec() && !this.parentModel.vk_type()) {
        }
        return ko.utils.arrayFilter(this.flat_products(), (prod) => {
            return this.myArrayFilter(
                [{
                    value: prod.manufacturor,
                    mustEqual: this.parentModel.manufacturor
                },
                {
                    value: prod.type,
                    mustEqual: this.parentModel.vk_type
                }

                ]
            );

        }).sort(function(a, b) {
            return a.effect - b.effect;
        });
    });
    filtered_products = ko.computed(() => {
        if (!this.parentModel.effect() && !this.parentModel.manufacturor() && !this.parentModel.mainSpec() && !this.parentModel.vk_type()) {
            return this.filtered_products_no_mainSpec();
        }
        return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), (prod) => {
            return this.myArrayFilter(
                [{
                    value: prod.mainSpec,
                    mustEqual: this.parentModel.mainSpec
                },
                {
                    value: prod.effect,
                    mustEqual: this.parentModel.effect
                }
                ]
            );

        }).sort(function(a, b) {
            return a.effect - b.effect;
        });
    });


    spec_groups = ko.computed(() => {
        var filtered = this.filtered_products_no_mainSpec();
        var flags = {};
        return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), function(entry) {
            if (flags[entry.mainSpec]) {
                return false;
            }
            flags[entry.mainSpec] = true;
            return true;
        });
    });
};


class TSAppViewModel {
    anleggs_adresse: KnockoutObservable<{}>
    anleggs_poststed: KnockoutObservable<{}>
    anleggs_postnummer: KnockoutObservable<{}>
    manufacturor: KnockoutObservable<string>
    vk_type: KnockoutObservable<string>
    mainSpec: KnockoutObservable<string>
    rom_navn: KnockoutObservable<{}>
    areal: KnockoutObservable<{}>
    oppvarmet_areal: KnockoutObservable<{}>
    effect: KnockoutObservable<{}>
    ohm_a: KnockoutObservable<{}>
    ohm_b: KnockoutObservable<{}>
    ohm_c: KnockoutObservable<{}>
    mohm_a: KnockoutObservable<{}>
    mohm_b: KnockoutObservable<{}>
    mohm_c: KnockoutObservable<{}>
    error_fields: KnockoutObservableArray<string>
    error_message: KnockoutObservable<string>
    file_download: KnockoutObservable<string>
    last_sent_args: KnockoutObservable<string>
    form_args: KnockoutObservable<string>
    Products: KnockoutObservable<TSProductModel>
    selected_vk: KnockoutObservable<string>
    forced_selected_vk: KnockoutObservable<string>
    address_id: KnockoutObservable<string>
    filled_form_modified_id: KnockoutObservable<string>
    user_forms: KnockoutObservableArray<string>
    company_forms: KnockoutObservableArray<string>
    validation_errors: KnockoutValidationErrors
    loading: KnockoutObservableArray<string>

    constructor() {
        ko_validation.init({
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
            var config = ko_validation.utils.getConfigOptions(element);
            // if requested, add binding to decorate element
            if (config.decorateInputElement && ko_validation.utils.isValidatable(valueAccessor())) {
                var parent = $(element).parent();
                if (parent.length) {
                    ko.applyBindingsToNode(parent[0], {
                        validationElement: valueAccessor()
                    });
                }
            }
        };
        this.anleggs_adresse = ko.observable().extend({
            required: true,
            minLength: 3,
        });
        this.anleggs_poststed = ko.observable().extend({
            required: true,
            minLength: 3,
        });
        this.anleggs_postnummer = ko.observable().extend({
            required: true,
            minLength: 4,
            number: true,
            min: 1000,
            max: 9999,
        });

        this.manufacturor = ko.observable();
        this.vk_type = ko.observable();
        this.mainSpec = ko.observable();

        this.rom_navn = ko.observable().extend({
            required: true,
            minLength: 2,
        });
        this.areal = ko.observable().extend({
            number: true,
            min: 0.1
        });
        this.oppvarmet_areal = ko.observable().extend({
            required: true,
            number: true,
            min: 0.1
        });
        this.effect = ko.observable().extend({
            number: true,
        });

        this.ohm_a = ko.observable().extend({
            number: true,
            min: 0,
            max: 1000,
        });
        this.ohm_b = ko.observable().extend({
            number: true,
            min: 0,
            max: 1000,
        });
        this.ohm_c = ko.observable().extend({
            number: true,
            min: 0,
            max: 1000,
        });

        this.mohm_a = ko.observable();
        this.mohm_b = ko.observable();
        this.mohm_c = ko.observable();

        this.error_fields = ko.observableArray();
        this.error_message = ko.observable();

        this.file_download = ko.observable();

        this.last_sent_args = ko.observable();
        this.form_args = ko.observable($('#form').serialize());

        this.Products = ko.observable();
        this.selected_vk = ko.observable();
        this.forced_selected_vk = ko.observable();

        this.address_id = ko.observable();
        this.filled_form_modified_id = ko.observable();

        this.user_forms = ko.observableArray();
        this.company_forms = ko.observableArray();

        this.validation_errors = ko_validation.group(self);
        this.loading = ko.observableArray();
        var dsfsd = this
        this.Products(new TSProductModel(dsfsd));
        // var myApsp = new TSProductModel(dsfsd);
        this.Products().getProducts();

    }

    post_form = function(e, t) {
        this.form_args($('#form').serialize());
        if (this.validation_errors().length > 0) {
            this.validation_errors.showAllMessages();
            return false;
        }
        if (this.form_changed() || !this.filled_form_modified_id()) {
            // this.file_download(false);
            this.loading.push('fill_form');
            $.post("/json/heating/", {
                'anleggs_adresse': this.anleggs_adresse(),
                'anleggs_poststed': this.anleggs_poststed(),
                'anleggs_postnummer': this.anleggs_postnummer(),
                'rom_navn': this.rom_navn(),
                'areal': this.areal(),
                'oppvarmet_areal': this.oppvarmet_areal(),
                'mohm_a': this.mohm_a(),
                'mohm_b': this.mohm_b(),
                'mohm_c': this.mohm_c(),
                'ohm_a': this.ohm_a(),
                'ohm_b': this.ohm_b(),
                'ohm_c': this.ohm_c(),
                'product_id': this.selected_vk(),
                'address_id': this.address_id(),
                'filled_form_modified_id': this.filled_form_modified_id()
            })
                .done(function(result) {
                    this.loading.remove('fill_form');
                    parse_form_download(result);
                });
        } else {
            this.loading.push('fill_form');
            $.get("/json/heating/", {
                'filled_form_modified_id': this.filled_form_modified_id()
            }).done(function(result) {
                this.loading.remove('fill_form');
                parse_form_download(result);
            });
        }
    };
}

$(function() {

    // ko_validation.locale('nb-NO');

    "use strict";

    function sortNumber(a: number, b: number): number {
        return a - b;
    }


    function AppViewModel() {





        $('body').on("change keyup paste click", 'input', function() {
            this.form_args($('#form').serialize());
        });
        this.form_changed = ko.computed(function() {
            return this.form_args() !== this.last_sent_args();
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
            if (this.mainSpec()) {
                try {
                    var f = this.Products().spec_groups();
                    if (findWithAttr(f, 'mainSpec', this.mainSpec()) < 0) {
                        this.mainSpec(undefined);
                    }
                } catch (e) {

                } finally {

                }
            }
        });


        ko.computed(function() {
            try {
                var f = this.Products().flat_products();
                if (f.length > 0) {
                    get_user_forms();
                    get_company_forms();
                }
            } catch (e) {

            } finally {

            }
        });

        function get_user_forms(loading) {
            this.loading.push('user_form')
            $.get("/forms.json", {})
                .done(function(result) {
                    result.user_forms.prefix = 'user_forms';
                    result.company_forms.prefix = 'company_forms';
                    this.user_forms(result.user_forms);
                    this.company_forms(result.company_forms);
                    this.loading.remove('user_form')
                });
        }


        function get_company_forms() {
            return false
            $.get("/forms.json", {
                type: 'company'
            }).done(function(result, d) {
                this.company_forms(result);
            });
        }


        this.get_product_by_id = function(id) {
            var f = this.Products().flat_products();
            for (var i = 0; i < f.length; i++) {
                if (f[i].id == id) {
                    return f[i];
                }
            }
        };
        this.expand_mods = function(e, d) {
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
        this.delete = ko.observable();

        this.confirmed_delete = function(e, d) {
            this.delete('');
            this.loading.push('delete');
            $.ajax({
                url: 'json/form_mod/' + e.id,
                type: 'DELETE',
                id: e.id
            })
                .done(function(result, d) {
                    this.loading.remove('delete');
                    get_user_forms();
                });
        };
        this.renamePrefix = function(e, d, f) { }
        this.edit_form = function(e) {
            var f = e.request_form;
            this.filled_form_modified_id(e.id);
            this.anleggs_adresse(f.anleggs_adresse);
            this.anleggs_postnummer(f.anleggs_postnummer);
            this.anleggs_poststed(f.anleggs_poststed);
            this.rom_navn(f.rom_navn);
            this.areal(f.areal);
            this.oppvarmet_areal(f.oppvarmet_areal);
            this.selected_vk(f.product_id);
            this.address_id(e.address_id);
            this.filled_form_modified_id(e.id);
            this.ohm_a(f.ohm_a);
            this.ohm_b(f.ohm_b);
            this.ohm_c(f.ohm_c);
            this.mohm_a(f.mohm_a);
            this.mohm_b(f.ohm_b);
            this.mohm_c(f.ohm_c);
            this.last_sent_args($('#form').serialize());
            this.form_args($('#form').serialize());
            $('.nav-tabs a[href="#main_form"]').tab('show');
        };


        function parse_form_download(result) {
            this.last_sent_args(this.form_args());
            if (result.error_fields) {
                this.error_fields(result.error_fields);
            }
            if (result.file_download) {
                this.file_download(result.file_download);
                if (result.address_id) {
                    this.address_id(result.address_id);
                }
                if (result.filled_form_modified_id) {
                    this.filled_form_modified_id(result.filled_form_modified_id);
                }
            }
            if (result.error_message) {
                console.log('sdfsd')
                this.error_message(result.error_message);
            }
        }

        this.loading = ko.observableArray();
    }

    // AppViewModel.suggestion.subscribe(function() { // called when an suggestion is selected to clear the suggestions
    //   AppViewModel.suggestions([]);
    // });
    var myApp = new TSAppViewModel();
    // myApp.init();
    ko.applyBindings(myApp);
});

this.format_date = function(dateString, type) {
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
