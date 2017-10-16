import { TSAppViewModel } from "./AppViewModel"
import { StrIndex } from "./Common"
import { HeatingCable } from "./HeatingCable"
import { Room } from "./Room"
import { Pagination, sortDist } from "./Pagination"
import { setCookie } from './helpers/cookie'
import * as data from '../data.json';

const static_data: StaticData = data;

export interface ProductInterface {
  effect: number;
  id: number;
  // These only exist on flatten products
  manufacturor?: string;
  type?: string;
  outside?: boolean;
  inside?: boolean;
  isMat?: boolean;
  per_meter?: boolean;
  self_limiting?: boolean;
  name?: string;
  mainSpec: number;
  secondarySpec?: number;
  restrictions?: ProductRestrictions
  specs?: ProductSpecs
  short_name?: string
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
  inside: boolean
  outside: boolean
  per_meter: boolean;
  self_limiting: boolean;
  isMat: boolean
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
  mustEqual?: any
  inList?: any
}
let compare_arrays = (a1: any[], a2: any[]) => {
  return a1.length == a2.length && a1.every((v: any, i: any) => a2.includes(v))
}
// Used to filter an arrayFilter.
let myArrayFilter = (list_to_filter: ArrayFylterInterface[]) => {
  for (let current_filter of list_to_filter) {
    let f = current_filter.value;
    if (current_filter.mustEqual) {
      let t = current_filter.mustEqual;
      if (t != undefined && f != t) {
        return false;
      }
    } else if (current_filter.inList) {
      let t = current_filter.inList;
      if (t.length == 0) {
        break
      }
      if (t.indexOf(f) == -1) {
        return false;
      }

    }

  }
  return true;
};

interface VKTypes {
  name: string
  observer: KnockoutObservable<boolean>
}



export class ProductFilter {
  target: HeatingCable
  room: Room
  product_model: TSProductModel
  effect: KnockoutObservable<number> = ko.observable();
  mainSpec: KnockoutObservable<number> = ko.observable();
  outside: KnockoutObservable<boolean> = ko.observable()
  manufacturor: KnockoutObservable<string> = ko.observable();
  cable: KnockoutObservable<boolean> = ko.observable(true)
  mat: KnockoutObservable<boolean> = ko.observable(false)
  single_leader: KnockoutObservable<boolean> = ko.observable(false)
  selected_manufacturors: KnockoutObservableArray<string> = ko.observableArray();
  vk_available_types: VKTypes[] = [
    {
      name: 'Kabel',
      observer: this.cable
    },
    {
      name: 'Matte',
      observer: this.mat
    },
    {
      name: 'Enleder',
      observer: this.single_leader
    },
  ]
  selected_vk_types: KnockoutObservableArray<string> = ko.observableArray();
  filtered_products_no_mainSpec: KnockoutComputed<ProductInterface[]>
  filtered_products: KnockoutComputed<ProductInterface[]>
  spec_groups: KnockoutComputed<ProductInterface[]>
  show_save_selected_manufacturors_button: KnockoutComputed<boolean>
  root: TSAppViewModel

  constructor(target: HeatingCable, room: Room, product_model: TSProductModel) {
    this.target = target
    this.room = room
    this.outside(room.outside())
    this.product_model = product_model
    this.root = room.parent.parent.parent
    this.selected_manufacturors(this.root.selected_manufacturors().slice())

    this.filtered_products_no_mainSpec = ko.computed(() => {
      return ko.utils.arrayFilter(this.product_model.flat_products(), (prod) => {

        if (this.outside() != prod.outside) { return false }
        if (this.mat() || this.cable() || this.single_leader()) {
          let matches_vk_type = false
          if (this.mat() && prod.isMat) { matches_vk_type = true }
          if (this.cable() && !prod.isMat && !prod.per_meter) { matches_vk_type = true }
          if (this.single_leader() && prod.per_meter) { matches_vk_type = true }

          if (!matches_vk_type) { return false }
        }

        let arrayFilterData: ArrayFylterInterface[] = [{
          value: prod.manufacturor,
          inList: this.selected_manufacturors()
        }
        ]

        return myArrayFilter(arrayFilterData);

      }).sort((a, b) => {
        return a.effect - b.effect;
      });
    });
    this.filtered_products = ko.computed(() => {
      if (!this.effect() && this.selected_manufacturors().length == 0 && !this.mainSpec() && this.selected_vk_types().length == 0) {
        return this.filtered_products_no_mainSpec()
      }
      return ko.utils.arrayFilter(this.filtered_products_no_mainSpec(), (prod) => {
        return myArrayFilter(
          [{
            value: prod.mainSpec,
            mustEqual: this.mainSpec()
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
    this.show_save_selected_manufacturors_button = ko.computed(() => {
      if (this.selected_manufacturors().length == 0) {
        return false
      }
      let a1 = this.root.selected_manufacturors()
      let a2 = this.selected_manufacturors()
      return !compare_arrays(a1, a2)
    })
  }


  by_id = (id: number) => {
    let f = this.product_model.flat_products();
    return f.find(myObj => {
      return myObj.id === Number(id)
    });
  }
  save_selected_manufacturors() {
    if (this.selected_manufacturors().length > 0) {
      setCookie('manufacturors', String(this.selected_manufacturors()))
      this.root.selected_manufacturors(this.selected_manufacturors().slice())
    }
  }
  toggle_selected_manufacturor = (product: ProductInterface, event: Event) => {
    let manufacturor = String(product.name)
    if (this.selected_manufacturors.indexOf(manufacturor) >= 0) {
      this.selected_manufacturors.remove(manufacturor)
      if (this.selected_manufacturors().length == 0)
        this.selected_vk_types(['Nexans', 'Thermofloor', 'Øglænd'])
    } else {
      this.selected_manufacturors.push(manufacturor)
    }
  }
  toggle_selected_vk_type = (vk_type: VKTypes, event: Event) => {
    vk_type.observer(!vk_type.observer())
    let all_false = true
    for (let vk of this.vk_available_types) {
      if (vk.observer()) {
        all_false = false
        break
      }
    }
    if (all_false) {
      for (let vk of this.vk_available_types) {
        vk.observer(true)
      }
    }

  }
}

export class TSProductModel {
  url = '/json/v1/static/'
  products: KnockoutObservableArray<ManufacturorInterface> = ko.observableArray(<ManufacturorInterface[]>[])
  room_type_info: KnockoutObservableArray<RoomTypeInfoServer> = ko.observableArray()

  constructor(private parentModel: TSAppViewModel) {
    this.products(static_data.products);
    this.room_type_info(static_data.room_type_info)
    this.parentModel.selected_vk(this.parentModel.forced_selected_vk());
  }
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
            p.isMat = d.isMat;
            p.outside = d.outside;
            p.inside = d.inside;
            p.self_limiting = d.self_limiting;
            p.name = d.name;
            p.short_name = d.name;
            p.per_meter = d.per_meter
            if (p.effect) {
              p.name += ` – ${p.effect}W`;
            }
            if (d.mainSpec) {
              p.name += ` – ${d.mainSpec}W/m`;
            }
            if (d.isMat) {
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
