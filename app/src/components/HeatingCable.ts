import { Post, ObsMod } from "./Common"
import { HeatingCableList } from "./HeatingCableList"
import {
  TSProductModel,
  ProductInterface,
  ProductFilter,
} from "./ProductModel"

export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  c_date?: Date
  m_date?: Date
  mod_id?: number
  specs: HeatingCableSpecs
}

interface PostInterface {
  url: string
  post(): void;
  serialize(): {}
}

interface MeasurementsInterface {
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: number
  mohm_b: number
  mohm_c: number
}
interface CalculationsInterface {
  cc?: number
  area_output?: number
}
export interface HeatingCableSpecs {
  measurements?: MeasurementsInterface
  cc: InputReadOnlyToggleInterface
  area_output: InputReadOnlyToggleInterface
}

interface InputReadOnlyToggleInterface {
  v: any
  m: boolean
}

class InputReadOnlyToggle {
  override: ObsMod<boolean>
  calculated: KnockoutComputed<any>
  output: ObsMod<any>
  serialize: KnockoutObservable<InputReadOnlyToggleInterface>
  user_input = <KnockoutObservable<number>>ko.observable();

  constructor(calculateFunction: (() => number), modification_observable: any) {
    this.override = <ObsMod<boolean>>modification_observable(false);
    this.calculated = ko.computed(calculateFunction);
    this.output = modification_observable(() => {
      return Number(this.override() ? this.user_input() : this.calculated())
    }, ko.computed);
    // this.calculated = ko.computed(calculateFunction)
    this.serialize = ko.computed((): InputReadOnlyToggleInterface => {
      return {
        v: this.output() || 0,
        m: this.override(),
      }
    })
    ko.computed(() => {
      if (!this.override()) {
        this.user_input(this.calculated().toFixed(1))
      }
    })
  }
}


export class HeatingCable extends Post {
  measurements_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  product_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  other_modifications_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()

  measurements_observer = (value?: any, kind: any = ko.observable, ) => {
    return this.obs_mod([this.measurements_modifications_list], kind, value);
  }
  other_observer = (value?: any, kind: any = ko.observable) => {
    return this.obs_mod([this.other_modifications_list], kind, value);
  }
  product_observer = (value?: any, kind: any = ko.observable, ) => {
    return this.obs_mod([this.product_modifications_list], kind, value);
  }
  product_id = <ObsMod<number>>this.product_observer();
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  ohm_a = <ObsMod<number>>this.measurements_observer();
  ohm_b = <ObsMod<number>>this.measurements_observer();
  ohm_c = <ObsMod<number>>this.measurements_observer();
  mohm_a = <ObsMod<boolean>>this.measurements_observer(-1);
  mohm_b = <ObsMod<boolean>>this.measurements_observer(-1);
  mohm_c = <ObsMod<boolean>>this.measurements_observer(-1);
  area_output: KnockoutObservable<InputReadOnlyToggle>
  cc: KnockoutObservable<InputReadOnlyToggle>


  product_model: TSProductModel
  product_filter: KnockoutObservable<ProductFilter>
  suggested_effect: KnockoutComputed<number>;

  validationModel = ko.validatedObservable({
    product_id: this.product_id,
  })
  serialize: KnockoutObservable<HeatingCableInterface>
  constructor(
    product_model: TSProductModel,
    parent: HeatingCableList,
    heating_cable_?: HeatingCableInterface
  ) {
    super(parent)
    let room = parent.parent
    let customer = room.parent.parent
    this.form_url = `${this.form_url}${customer.id()}/${room.id()}/`

    let default_data: HeatingCableInterface = {
      id: -1,
      product_id: -1,
      specs: {
        measurements: {
          ohm_a: 0,
          ohm_b: 0,
          ohm_c: 0,
          mohm_a: -1,
          mohm_b: -1,
          mohm_c: -1
        },
        cc: {
          v: 0,
          m: false
        },
        area_output: {
          v: 0,
          m: false
        },
      }
    }
    let heating_cable = Object.assign(default_data, heating_cable_)
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.product_filter = ko.observable(new ProductFilter(this, this.parent.parent, this.product_model))

    this.area_output = ko.observable(new InputReadOnlyToggle(() => {
      if (this.product()) {
        if (this.product()!.type == 'mat') {
          return this.product()!.mainSpec
        }
      }
      let heated_area = this.parent.parent.heated_area()
      let room_effect = this.parent.parent.room_effect()
      if (room_effect && heated_area) {
        return parseFloat((room_effect / heated_area).toFixed(1))
      }
      return Number(heating_cable!.specs.area_output.v) || 0
    }, this.other_observer))
    this.cc = ko.observable(new InputReadOnlyToggle(() => {
      if (this.product() && this.product()!.type != 'mat') {
        // For rooms with multiple cables, we need to do some guesswork to
        // calculate the area that this cable is covering.
        let room_effect = this.parent.parent.room_effect()
        let this_effect = this.product()!.effect
        if (room_effect && this_effect) {
          let coverage_fraction = this_effect / room_effect
          let heated_area = this.parent.parent.heated_area()
          let heated_area_of_this_cable = heated_area * coverage_fraction
          let length = this.product()!.specs!.Length
          if (length && heated_area_of_this_cable) {
            let value = heated_area_of_this_cable / length * 100
            return parseFloat(value.toFixed(1))
          }
        }
      }
      // Set an initial value, to keep the modified-flag from raising
      return Number(heating_cable!.specs.cc.v) || 0
    }, this.other_observer))

    this.serialize = ko.computed(() => {
      let obj: HeatingCableInterface = {
        id: this.id(),
        room_id: this.parent.parent.id(),
        product_id: Number(this.product_id()),
        specs: {
          measurements: {
            ohm_a: Number(this.ohm_a()),
            ohm_b: Number(this.ohm_b()),
            ohm_c: Number(this.ohm_c()),
            mohm_a: (this.mohm_a() ? 999 : -1),
            mohm_b: (this.mohm_b() ? 999 : -1),
            mohm_c: (this.mohm_c() ? 999 : -1),
          },
          cc: this.cc().serialize(),
          area_output: this.area_output().serialize()
        },
      }
      return obj
    })
    this.suggested_effect = ko.computed(() => {
      let this_effect = 0
      if (this.product()) {
        this_effect = this.product()!.effect
      }
      return this.parent.parent.bestFitEffect() - (this.parent.parent.room_effect() - this_effect)
    })
    this.set(heating_cable)
  }
  product = ko.computed((): ProductInterface | undefined => {
    if (this.product_id() >= 0 && this.product_model) {
      return this.product_model.by_id(this.product_id())

    }
  })


  set(heating_cable: HeatingCableInterface) {
    this.id(heating_cable.id)
    this.product_id(Number(heating_cable.product_id))
    if (heating_cable.specs && heating_cable.specs.measurements) {
      // this.measurements().set(heating_cable.specs.measurements)
      this.ohm_a(heating_cable.specs.measurements.ohm_a)
      this.ohm_b(heating_cable.specs.measurements.ohm_b)
      this.ohm_c(heating_cable.specs.measurements.ohm_c)
      this.mohm_a(heating_cable.specs.measurements.mohm_a >= 0)
      this.mohm_b(heating_cable.specs.measurements.mohm_b >= 0)
      this.mohm_c(heating_cable.specs.measurements.mohm_c >= 0)
      this.area_output().override(Boolean(heating_cable.specs.area_output!.m))
      this.area_output().user_input(Number(heating_cable.specs.area_output!.v))
      this.cc().override(Boolean(heating_cable.specs.cc!.m))
      this.cc().user_input(Number(heating_cable.specs.cc!.v))
    }
    if (this.serialize) {
      this.save()
    }
  }
  modifications_other = ko.computed(() => {
    return this.modification_check(this.other_modifications_list())
  })
  product_modifications = ko.computed(() => {
    return this.modification_check(this.product_modifications_list())
  })
  measurements_modifications = ko.computed(() => {
    return this.modification_check(this.measurements_modifications_list())
  })



}
