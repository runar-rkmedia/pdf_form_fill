import { HTTPVerbs, ByID, Post, compareDicts, Base } from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import {
  TSProductModel,
  ProductInterface,
  ProductFilter,
  ProductResctrictionsCalculated
} from "./ProductModel"

interface MeasurementsInterface {
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: boolean
  mohm_b: boolean
  mohm_c: boolean
}
interface HeatingCableSpecs {
  measurements: MeasurementsInterface
}
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

class Measurements extends Base {
  ohm_a: KnockoutObservable<number> = ko.observable();
  ohm_b: KnockoutObservable<number> = ko.observable();
  ohm_c: KnockoutObservable<number> = ko.observable();
  mohm_a: KnockoutObservable<boolean> = ko.observable();
  mohm_b: KnockoutObservable<boolean> = ko.observable();
  mohm_c: KnockoutObservable<boolean> = ko.observable();
  // modified: KnockoutObservable<boolean>
  last_sent_data: KnockoutObservable<MeasurementsInterface> = ko.observable()

  constructor() {
    super()
    this.init()
  }
  set(measurements?: MeasurementsInterface) {
    if (measurements) {
      this.ohm_a(measurements.ohm_a)
      this.ohm_b(measurements.ohm_b)
      this.ohm_c(measurements.ohm_c)

      this.mohm_a(measurements.mohm_a)
      this.mohm_b(measurements.mohm_b)
      this.mohm_c(measurements.mohm_c)
    }
  }
  serialize = ko.computed(() => {
    return {
      ohm_a: this.ohm_a(),
      ohm_b: this.ohm_b(),
      ohm_c: this.ohm_c(),
      mohm_a: this.mohm_a(),
      mohm_b: this.mohm_b(),
      mohm_c: this.mohm_c()
    }
  })
}

export class HeatingCable extends Post {
  product_id: KnockoutObservable<number> = ko.observable();
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  measurements: KnockoutObservable<Measurements> = ko.observable(new Measurements())
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
    console.log(heating_cable)
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.product_filter = ko.observable(new ProductFilter(this, this.product_model))
    this.parent = parent
    this.serialize = ko.computed(() => {
      let obj = {
        id: this.id(),
        room_id: this.parent.parent.id(),
        product_id: Number(this.product_id()),
        specs: { measurements: this.measurements().serialize() }
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
      let restrictions = product.restrictions
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

      if ((boundary.top <= 0 || boundary.bottom <= 0) && product.effect) {

        console.log('lazily calculating restrictions for: ', product)
        // Calculate the resistance based on effect
        let voltage = product.secondarySpec || 230
        let resistance = voltage ^ 2 / product.effect
        boundary = restrictions_from_nominal(boundary, resistance)

      }
    }
    return boundary
  })

  set(heating_cable: HeatingCableInterface) {
    console.log(heating_cable)
    this.id(heating_cable.id)
    this.product_id(Number(heating_cable.product_id))
    if (heating_cable.specs && heating_cable.specs.measurements) {
      this.measurements().set(heating_cable.specs.measurements)
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
