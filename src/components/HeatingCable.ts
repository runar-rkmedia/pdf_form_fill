import {
  ByID,
  Post,
  Base,
  ObservableWithModification,
  observable_modification
} from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import {
  TSProductModel,
  ProductInterface,
  ProductFilter,
  ProductResctrictionsCalculated
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
  override = <ObservableWithModification<boolean>>observable_modification(false);
  calculated: ObservableWithModification<any>
  serialize: KnockoutObservable<InputReadOnlyToggleInterface>
  user_input = <ObservableWithModification<number>>observable_modification();

  constructor(calculateFunction: (() => any)) {
    this.calculated = observable_modification(calculateFunction, ko.computed);
    // this.calculated = ko.computed(calculateFunction)
    this.serialize = ko.computed((): InputReadOnlyToggleInterface => {
      return {
        v: (this.override() ? this.user_input() : this.calculated()) || 0,
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
  product_id = <ObservableWithModification<number>>observable_modification();
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  ohm_a = <ObservableWithModification<number>>observable_modification();
  ohm_b = <ObservableWithModification<number>>observable_modification();
  ohm_c = <ObservableWithModification<number>>observable_modification();
  mohm_a = <ObservableWithModification<boolean>>observable_modification(-1);
  mohm_b = <ObservableWithModification<boolean>>observable_modification(-1);
  mohm_c = <ObservableWithModification<boolean>>observable_modification(-1);
  area_output: KnockoutObservable<InputReadOnlyToggle>
  cc: KnockoutObservable<InputReadOnlyToggle>
  measurements_modifications_list: ObservableWithModification<any>[] = [
    this.ohm_a,
    this.ohm_b,
    this.ohm_c,
    this.mohm_a,
    this.mohm_b,
    this.mohm_c,
  ]
  product_modifications_list: ObservableWithModification<any>[] = [
    this.product_id,
  ]
  other_modifications_list: KnockoutObservableArray<ObservableWithModification<any>> = ko.observableArray()


  parent: HeatingCables
  product_model: TSProductModel
  product_filter: KnockoutObservable<ProductFilter>

  validationModel = ko.validatedObservable({
    product_id: this.product_id,
  })
  last_sent_data: KnockoutObservable<HeatingCableInterface> = ko.observable()
  serialize: KnockoutObservable<HeatingCableInterface>
  constructor(
    product_model: TSProductModel,
    parent: HeatingCables,
    heating_cable_?: HeatingCableInterface
  ) {
    super()
    let default_data: HeatingCableInterface = {
      id: -1,
      product_id: -1,
      specs: {
        measurements: {
          ohm_a: -1,
          ohm_b: -1,
          ohm_c: -1,
          mohm_a: -1,
          mohm_b: -1,
          mohm_c: -1
        },
        cc: {
          v: -1,
          m: false
        },
        area_output: {
          v: -1,
          m: false
        },
      }
    }
    let heating_cable = Object.assign(default_data, heating_cable_)
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.product_filter = ko.observable(new ProductFilter(this, this.product_model))
    this.parent = parent

    this.area_output = ko.observable(new InputReadOnlyToggle(() => {
      if (this.product()) {
        if (this.product()!.type == 'mat') {
          return this.product()!.mainSpec
        }
      }
      let heated_area = this.parent.parent.heated_area()
      let room_effect = this.parent.parent.room_effect()
      if (room_effect && heated_area) {
        return room_effect / heated_area
      }
      return Number(heating_cable!.specs.area_output.v) || 0
    }))
    this.other_modifications_list.push(this.area_output().user_input)
    this.other_modifications_list.push(this.area_output().calculated)
    this.other_modifications_list.push(this.area_output().override)
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
            return value
          }
        }
      }
      // Set an initial value, to keep the modified-flag from raising
      return Number(heating_cable!.specs.cc.v) || 0
    }))
    this.other_modifications_list.push(this.cc().user_input)
    this.other_modifications_list.push(this.cc().calculated)
    this.other_modifications_list.push(this.cc().override)

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
    // this.modification_tracking_list(this.measurements_modifications_list.concat(
    //   this.product_modifications_list,
    //   this.other_modifications_list()
    // ))
    this.set(heating_cable)
    this.init()

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
    return this.modification_check(this.product_modifications_list)
  })
  measurements_modifications = ko.computed(() => {
    return this.modification_check(this.measurements_modifications_list)
  })



}

export class HeatingCables extends ByID {
  list: KnockoutObservableArray<HeatingCable>
  parent: Room
  root: TSAppViewModel
  constructor(root: TSAppViewModel, parent: Room, heating_cables: HeatingCableInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    let heating_cables_objects: HeatingCable[] = []
    if (heating_cables_objects) {
      let self = this
      heating_cables_objects = heating_cables.map(function(x) {
        return new HeatingCable(self.root.Products(), self, x)
      })
    }
    this.list(heating_cables_objects)
  }
  add = (event: Event) => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this.root.Products(), this))
    }
    this.root.editing_heating_cable_id(-1)
    setTimeout(() => {    // Expand the panel
      let btn = $(event.target)
      let accordian = $('#accordion-heat')
      let panel = accordian.find('#heat-1')
      let panel_vk = panel.find('#panel_select_cable-1')
      panel.collapse('show')
      panel_vk.addClass('in')
    }, 20)

  }
}
