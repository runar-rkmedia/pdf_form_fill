import { TSAppViewModel } from "./AppViewModel"
import { StrIndex } from "./Common"
import { HeatingCable } from "./HeatingCable"
import { Room } from "./Rooms"
import ko = require("knockout");

export interface ProductInterface {
  effect: number;
  id: number;
  // These only exist on flatten products
  manufacturor?: string;
  type?: string;
  outside?: boolean;
  name?: string;
  mainSpec: number;
  secondarySpec?: number;
  restrictions?: ProductRestrictions
  specs?: ProductSpecs
}


interface ProductSpecs {
  Area?: number
  Length?: number
  width?: number
}

interface ProductRestrictions {
  R_max: number
  R_min: number
  R_nom: number
}
export interface ProductResctrictionsCalculated {
  top: number
  bottom: number
}

interface ProductTypeInterface {
  id: number;
  mainSpec: number;
  secondarySpec: number
  type: string
  inside: string
  products: ProductInterface[]
  name: string
}


interface ManufacturorInterface {
  id: number;
  name: string;
  product_types: ProductTypeInterface[]
}

interface StaticData {
  products: ManufacturorInterface[]
  room_type_info: RoomTypeInfoServer[]
}

interface RoomTypeInfo {
  id: number
  maxEffect: number
  normalEffect: number
}

interface RoomTypeInfoServer extends RoomTypeInfo {
  names: string[]
  outside?: boolean
}


export interface RoomTypesInfoFlat extends RoomTypeInfo {
  name: string
  outside: boolean
}

interface ArrayFylterInterface {
  value: any,
  mustEqual: any
}

// Used to filter an arrayFilter.
let myArrayFilter = (list_to_filter: ArrayFylterInterface[]) => {
  for (let current_filter of list_to_filter) {
    let f = current_filter['value'];
    let t = current_filter['mustEqual']();
    if (t != undefined && f != t) {
      return false;
    }
  }
  return true;
};

export class ProductFilter {
  target: HeatingCable
  room: Room
  product_model: TSProductModel
  effect: KnockoutObservable<number> = ko.observable();
  mainSpec: KnockoutObservable<number> = ko.observable();
  manufacturor: KnockoutObservable<string> = ko.observable();
  vk_type: KnockoutObservable<string> = ko.observable();
  filtered_products_no_mainSpec: KnockoutComputed<ProductInterface[]>
  filtered_products: KnockoutComputed<ProductInterface[]>
  spec_groups: KnockoutComputed<ProductInterface[]>

  constructor(target: HeatingCable, room: Room, product_model: TSProductModel) {
    this.target = target
    this.room = room
    this.product_model = product_model
    this.filtered_products_no_mainSpec = ko.computed(() => {
      if (!this.effect() && !this.manufacturor() && !this.mainSpec() && !this.vk_type() && !this.room.outside()) {
        // return this.product_model.flat_products();
      }
      return ko.utils.arrayFilter(this.product_model.flat_products(), (prod) => {
        return myArrayFilter(
          [{
            value: prod.manufacturor,
            mustEqual: this.manufacturor
          },
          {
            value: prod.type,
            mustEqual: this.vk_type
          },
          {
            value: prod.outside,
            mustEqual: this.room.outside
          }

          ]
        );

      }).sort((a, b) => {
        return a.effect - b.effect;
      });
    });
    this.filtered_products = ko.computed(() => {
      if (!this.effect() && !this.manufacturor() && !this.mainSpec() && !this.vk_type()) {
        return this.filtered_products_no_mainSpec()
      }
      return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), (prod) => {
        return myArrayFilter(
          [{
            value: prod.mainSpec,
            mustEqual: this.mainSpec
          }
          ]
        );

      })
    });
    this.spec_groups = ko.computed(() => {
      let filtered = this.filtered_products_no_mainSpec();
      let flags: StrIndex<boolean> = {};
      return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), (entry: ProductInterface) => {
        if (flags[entry.mainSpec]) {
          return false;
        }
        flags[entry.mainSpec] = true;
        return true;
      })
    });
  }
  // Sort any list of object by its distance to a setpoint to a certain key.
  // For instance, sort all towns with distance closest to 800m:
  // kings road: 760m
  // queens road: 850m
  // princes road: 750m
  sortDist = (list: any[], setPoint: number, key = 'effect') => {
    return list.sort((a, b) => {
      if (setPoint) {
        let diffA = Math.abs(setPoint - a[key])
        let diffB = Math.abs(setPoint - b[key])
        return diffA - diffB
      } else {
        return (a[key]) - (b[key]);
      }
    });
  }


  by_id = (id: number) => {
    let f = this.product_model.flat_products();
    return f.find(myObj => {
      return myObj.id === Number(id)
    });
  }
}

export class TSProductModel {
  url = '/json/v1/static/'
  products: KnockoutObservableArray<ManufacturorInterface> = ko.observableArray(<ManufacturorInterface[]>[])
  room_type_info: KnockoutObservableArray<RoomTypeInfoServer> = ko.observableArray()

  constructor(private parentModel: TSAppViewModel) {
    // this.products = ko.observableArray(<ManufacturorInterface[]>[])
  }


  getProducts = () => {
    $.get(this.url)
      .done((result: StaticData) => {
        this.products(result.products);
        this.room_type_info(result.room_type_info)
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
            p.outside = !d.inside;
            p.name = m.name + " " + d.name;
            if (p.effect) {
              p.name += " " + p.effect + "W";
            } if (p.effect) {
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
  flat_room_type_info = ko.computed((): RoomTypesInfoFlat[] => {
    let flattened: RoomTypesInfoFlat[] = []
    if (this.room_type_info()) {
      for (let room_type_info of this.room_type_info()) {
        for (let name of room_type_info.names) {
          flattened.push({
            name: name,
            id: room_type_info.id,
            maxEffect: room_type_info.maxEffect,
            normalEffect: room_type_info.normalEffect,
            outside: room_type_info.outside || false
          })
        }

      }
    }
    return flattened
  })
  by_id = (id: number) => {
    let f = this.flat_products();
    return f.find(myObj => {
      return myObj.id === Number(id)
    });
  }
};
