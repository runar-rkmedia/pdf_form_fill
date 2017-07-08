import $ = require("jquery");
import ko = require("knockout");
import ko_validation = require("knockout.validation");

var pad = (n:string, width:number, z:string = "0") => {
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
// webpack doesn't like to litter the global-namespace, so to force this function to be available there, we need to add the function to global. then typescript compains, so we need to add to it.
(<any>window).format_date = (dateString:string, type:string) => {
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

interface ProductInterface {
    effect: number;
    id: number;
    // These only exist on flatten products
    manufacturor?: string;
    type?: string;
    name?: string;
    mainSpec: number;
    secondarySpec?: number;
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

interface UserFormInterface {
    date: string;
    id: number;
    request_form: RequestFormInterface
}

interface RequestFormInterface {
    anleggs_adresse: string
    anleggs_postnummer: number
    anleggs_poststed: string
    rom_navn: string
    areal: number
    oppvarmet_areal: number
    selected_vk: number
    product_id: number
    address_id: number
    ohm_a: number
    ohm_b: number
    ohm_c: number
    mohm_a: boolean
    mohm_b: boolean
    mohm_c: boolean
}

interface FileDownloadInterface {
    address_id: number
    file_download: string
    filled_form_modified_id: number
    error_fields?: Array<string>
    error_message?: string
}


class TSProductModel {
    products: KnockoutObservableArray<ManufacturorInterface> = ko.observableArray(<ManufacturorInterface[]>[])

    constructor(private parentModel: TSAppViewModel) {
        // this.products = ko.observableArray(<ManufacturorInterface[]>[])
    }
    // Used to filter an arrayFilter.
    myArrayFilter = (list_to_filter: ArrayFylterInterface[]) => {
        for (let current_filter of list_to_filter) {
            let f = current_filter['value'];
            let t = current_filter['mustEqual']();
            if (t && f != t) {
                return false;
            }
        }
        return true;
    };

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

        }).sort((a, b)=> {
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

        }).sort((a, b)=> {
            return a.effect - b.effect;
        });
    });


    spec_groups = ko.computed(() => {
        let filtered = this.filtered_products_no_mainSpec();
        let flags:StrIndex<boolean> = {};
        return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), (entry: ProductInterface)=> {
            if (flags[entry.mainSpec]) {
                return false;
            }
            flags[entry.mainSpec] = true;
            return true;
        });
    });
};

interface StrIndex<TValue> {
    [key: string]: TValue
}


class TSAppViewModel {
    anleggs_adresse: KnockoutObservable<{}> = ko.observable().extend({
        required: true,
        minLength: 3,
        maxLength: 50
    })
    anleggs_poststed: KnockoutObservable<{}> = ko.observable().extend({
        required: true,
        minLength: 3,
        maxLength: 50
    });
    anleggs_postnummer: KnockoutObservable<{}> = ko.observable().extend({
        required: true,
        minLength: 4,
        number: true,
        min: 1000,
        max: 9999,
    });
    manufacturor: KnockoutObservable<string> = ko.observable();
    vk_type: KnockoutObservable<string> = ko.observable();
    mainSpec: KnockoutObservable<string> = ko.observable();
    rom_navn: KnockoutObservable<{}> = ko.observable().extend({
        required: true,
        minLength: 2,
        maxLength: 50
    });
    areal: KnockoutObservable<{}> = ko.observable().extend({
        number: true,
        min: 0.1
    });
    oppvarmet_areal: KnockoutObservable<{}> = ko.observable().extend({
        required: true,
        number: true,
        min: 0.1
    });
    effect: KnockoutObservable<{}> = ko.observable().extend({
        number: true,
    });
    ohm_a: KnockoutObservable<{}> = ko.observable().extend({
        number: true,
        min: 0,
        max: 1000,
    });
    ohm_b: KnockoutObservable<{}> = ko.observable().extend({
        number: true,
        min: 0,
        max: 1000,
    });
    ohm_c: KnockoutObservable<{}> = ko.observable().extend({
        number: true,
        min: 0,
        max: 1000,
    });
    mohm_a: KnockoutObservable<{}> = ko.observable();
    mohm_b: KnockoutObservable<{}> = ko.observable();
    mohm_c: KnockoutObservable<{}> = ko.observable();
    error_fields: KnockoutObservableArray<string> = ko.observableArray();
    error_message: KnockoutObservable<string> = ko.observable();
    file_download: KnockoutObservable<string> = ko.observable();
    last_sent_args: KnockoutObservable<string> = ko.observable();
    form_args: KnockoutObservable<string> = ko.observable($('#form').serialize());
    Products: KnockoutObservable<TSProductModel> = ko.observable();
    selected_vk: KnockoutObservable<number> = ko.observable();
    forced_selected_vk: KnockoutObservable<number> = ko.observable();
    address_id: KnockoutObservable<number> = ko.observable();
    filled_form_modified_id: KnockoutObservable<number> = ko.observable();
    user_forms: KnockoutObservableArray<string> = ko.observableArray();
    company_forms: KnockoutObservableArray<string> = ko.observableArray();
    validation_errors: KnockoutValidationErrors = ko_validation.group(self);
    loading: KnockoutObservableArray<string> = ko.observableArray();

    delete: KnockoutObservable<string> = ko.observable();

    noname: any

    constructor() {
        ko_validation.init({
            decorateInputElement: true,
            errorElementClass: 'has-error has-feedback',
            // successElementClass: 'has-feedback has-success',
            insertMessages: true,
            // decorateElement: true,
            // errorElementClass: 'error',
            errorMessageClass: 'bg-danger'
        });

        // Add bootstrap-validation-css to parent of field
        let init = ko.bindingHandlers['validationCore'].init! ;
        ko.bindingHandlers['validationCore'].init = (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext)=> {
            init(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);
            let config = ko_validation.utils.getConfigOptions(element);
            // if requested, add binding to decorate element
            if (config.decorateInputElement && ko_validation.utils.isValidatable(valueAccessor())) {
                let parent = $(element).parent();
                if (parent.length) {
                    ko.applyBindingsToNode(parent[0], {
                        validationElement: valueAccessor()
                    });
                }
            }
        };
        this.Products(new TSProductModel(this));
        this.Products().getProducts();

        this.noname = ko.computed(() => {
            try {
                var f = this.Products().flat_products();
                if (f.length > 0) {
                    this.get_user_forms();
                    // this.get_company_forms();
                }
            } catch (e) {

            } finally {

            }
        });

        ko.computed(() => {
            if (this.mainSpec()) {
                try {
                    var f = this.Products().spec_groups();
                    if (this.findWithAttr(f, 'mainSpec', this.mainSpec()) < 0) {
                        this.mainSpec(null);
                    }
                } catch (e) {

                } finally {

                }
            }
        });
    }



    form_changed = ko.computed(() => {
        return this.form_args() !== this.last_sent_args();
    }, this);

    parse_form_download = (result: FileDownloadInterface) => {
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
            this.error_message(result.error_message);
        }
    }

    post_form = () => {
        this.form_args($('#form').serialize());
        if (this.validation_errors().length > 0) {
            this.validation_errors.showAllMessages();
            return false;
        }
        if (this.form_changed() || !this.filled_form_modified_id()) {
            this.file_download(null);
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
                .done((result: FileDownloadInterface) => {
                    this.loading.remove('fill_form');
                    this.parse_form_download(result);
                });
        } else {
            this.loading.push('fill_form');
            $.get("/json/heating/", {
                'filled_form_modified_id': this.filled_form_modified_id()
            }).done((result: FileDownloadInterface) => {
                this.loading.remove('fill_form');
                this.parse_form_download(result);
            });
        }
    };
    findWithAttr = (array: Array<any>, attr: string, value: any) => {
        for (var i = 0; i < array.length; i += 1) {
            if (array[i][attr] === value) {
                return i;
            }
        }
        return -1;
    }

    get_user_forms = () => {
        this.loading.push('user_form')
        $.get("/forms.json", {})
            .done((result) => {
                result.user_forms.prefix = 'user_forms';
                result.company_forms.prefix = 'company_forms';
                this.user_forms(result.user_forms);
                this.company_forms(result.company_forms);
                this.loading.remove('user_form')
            });
    }

    get_product_by_id = (id: number) => {
        var f = this.Products().flat_products();
        for (var i = 0; i < f.length; i++) {
            if (f[i].id == id) {
                return f[i];
            }
        }
    };

    confirmed_delete = (e: UserFormInterface) => {
        this.delete('');
        this.loading.push('delete');
        $.ajax({
            url: 'json/form_mod/' + e.id,
            type: 'DELETE',
            data: {
                id: e.id
            }
        })
            .done((result) => {
                this.loading.remove('delete');
                this.get_user_forms();
            });
    };

    edit_form = (e: UserFormInterface) => {
        console.log(e)
        var f = e.request_form;
        this.filled_form_modified_id(e.id);
        this.anleggs_adresse(f.anleggs_adresse);
        this.anleggs_postnummer(f.anleggs_postnummer);
        this.anleggs_poststed(f.anleggs_poststed);
        this.rom_navn(f.rom_navn);
        this.areal(f.areal);
        this.oppvarmet_areal(f.oppvarmet_areal);
        this.selected_vk(f.product_id);
        // this.address_id(e.address_id);
        // TODO: fix address_id
        this.ohm_a(f.ohm_a);
        this.ohm_b(f.ohm_b);
        this.ohm_c(f.ohm_c);
        this.mohm_a(f.mohm_a);
        this.mohm_b(f.ohm_b);
        this.mohm_c(f.ohm_c);
        this.last_sent_args($('#form').serialize());
        this.form_args($('#form').serialize());
        ($('.nav-tabs a[href="#main_form"]') as any).tab('show');
    };

}

$(function() {
    var myApp = new TSAppViewModel();
    ko.applyBindings(myApp);

    $('body').on("change keyup paste click", 'input', () => {
        myApp.form_args($('#form').serialize());
    });
});

$(function() {
    $('input[type=tel]').on('input', function(e) {
        let inputfield = (<HTMLInputElement>this);
        inputfield.value = inputfield.value.replace(/\D/g, '');
    })
})
