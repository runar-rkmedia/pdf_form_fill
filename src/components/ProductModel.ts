import { TSAppViewModel } from "./AppViewModel"
import {StrIndex}  from "./Common"
import ko = require("knockout");

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

export class TSProductModel {
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
                }
                ]
            );

        }).sort((a, b)=> {
          let effect = this.parentModel.effect();
          if (effect) {
              let diffA = Math.abs(effect - a.effect)
              let diffB = Math.abs(effect - b.effect)
              return diffA-diffB
          } else {
            return (a.effect) - (b.effect);
          }
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
