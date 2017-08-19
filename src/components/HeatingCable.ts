import { ByID, Post, Base } from "./Common"
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
  specs?: HeatingCableSpecs
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
  cc: number
  w_per_m2: number
}
export interface HeatingCableSpecs {
  measurements?: MeasurementsInterface
  calculations?: CalculationsInterface
}

export class HeatingCable extends Post {
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  product_id: KnockoutObservable<number> = ko.observable();
  ohm_a: KnockoutObservable<number> = ko.observable();
  ohm_b: KnockoutObservable<number> = ko.observable();
  ohm_c: KnockoutObservable<number> = ko.observable();
  mohm_a: KnockoutObservable<number> = ko.observable();
  mohm_b: KnockoutObservable<number> = ko.observable();
  mohm_c: KnockoutObservable<number> = ko.observable();
  cc: KnockoutObservable<number> = ko.observable();
  w_per_m2: KnockoutObservable<number> = ko.observable();
  cc_calculated: KnockoutComputed<number | undefined>
  w_per_m2_calculated: KnockoutComputed<number | undefined>

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
    heating_cable: HeatingCableInterface = { id: -1, product_id: -1 }
  ) {
    super()
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.product_filter = ko.observable(new ProductFilter(this, this.product_model))
    this.parent = parent
    this.cc_calculated = ko.computed(() => {
      if (this.product()) {
        let effect = this.product()!.effect
        if (effect) {
          return effect
        }
      }
    })
    this.w_per_m2_calculated = ko.computed(() => {
      if (this.product()) {
        let effect = this.product()!.effect
        let heated_area = this.parent.parent.heated_area()
        if (effect) {
          return effect / heated_area
        }
      }
    })

    this.serialize = ko.computed(() => {
      let obj = {
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
          calculations: {
            cc: Number(this.cc()),
            w_per_m2: Number(this.w_per_m2()),
          }
        }
      }

      return obj
    })
    this.init()
    this.set(heating_cable)
  }
  product = ko.computed((): ProductInterface | undefined => {
    if (this.product_id() >= 0 && this.product_model) {
      return this.product_model.by_id(this.product_id())
    }
  })
  product_restrictions = ko.computed(() => {
    let product = this.product()
    let boundary: ProductResctrictionsCalculated = { top: 0, bottom: 0 }
    let restrictions_from_nominal = (
      boundary: ProductResctrictionsCalculated, value: number
    ) => {
      boundary.top = value * 1.05
      boundary.bottom = value * 0.95
      return boundary
    }
    if (product) {
      let restrictions = product!.restrictions
      if (restrictions) {
        if (restrictions.R_max) {
          boundary.top = restrictions.R_max
        }
        if (restrictions.R_min) {
          boundary.bottom = restrictions.R_min
        }
        if (!restrictions.R_min && !restrictions.R_max) {
          if (restrictions.R_nom) {
            boundary = restrictions_from_nominal(boundary, restrictions.R_nom)
          } else {
            console.log('We need to calculate this:', product)
          }
        }
      }

      if ((boundary.top <= 0 || boundary.bottom <= 0) && product!.effect) {

        console.log('lazily calculating restrictions for: ', product)
        // Calculate the resistance based on effect
        let voltage = product!.secondarySpec || 230
        let resistance = voltage ^ 2 / product!.effect
        boundary = restrictions_from_nominal(boundary, resistance)

      }
    }
    return boundary
  })

  set(heating_cable: HeatingCableInterface) {
    this.id(heating_cable.id)
    this.product_id(Number(heating_cable.product_id))
    if (heating_cable.specs) {

      if (heating_cable.specs.measurements) {
        this.ohm_a(heating_cable.specs.measurements.ohm_a)
        this.ohm_b(heating_cable.specs.measurements.ohm_b)
        this.ohm_c(heating_cable.specs.measurements.ohm_c)
        this.mohm_a(heating_cable.specs.measurements.mohm_a)
        this.mohm_b(heating_cable.specs.measurements.mohm_b)
        this.mohm_c(heating_cable.specs.measurements.mohm_c)
      }
      if (heating_cable.specs.calculations) {
        this.cc(heating_cable.specs.calculations.cc)
        this.w_per_m2(heating_cable.specs.calculations.w_per_m2)
      }
    }
    this.save()
  }

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
      let pane = panel.find('#pane_select_cable-1')
      let navpill = panel.find('a[href="#pane_select_cable-1"]')
      console.log(btn, accordian, panel, pane, navpill)
      console.log(btn.length, accordian.length, panel.length, pane.length, navpill.length)
      // pane.addClass('active')
      navpill.tab('show')
      panel.collapse('show')
    }, 20)

  }
}
