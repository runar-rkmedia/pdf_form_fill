import { HTTPVerbs, ByID, Post } from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import { TSProductModel, ProductInterface } from "./ProductModel"

export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  c_date?: Date
  m_date?: Date
  mod_id?: number
}

interface MeasurementsInterface {
  id: number
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: boolean
  mohm_b: boolean
  mohm_c: boolean
}

interface PostInterface {
  url: string
  post(): void;
  serialize(): {}
}



export class HeatingCable extends Post {
  product_id: KnockoutObservable<number> = ko.observable();
  url = '/json/v1/heat/'
  id: KnockoutObservable<number> = ko.observable();
  parent: HeatingCables
  product_model: TSProductModel
  ohm_a: KnockoutObservable<number> = ko.observable();
  ohm_b: KnockoutObservable<number> = ko.observable();
  ohm_c: KnockoutObservable<number> = ko.observable();
  mohm_a: KnockoutObservable<boolean> = ko.observable();
  mohm_b: KnockoutObservable<boolean> = ko.observable();
  mohm_c: KnockoutObservable<boolean> = ko.observable();
  validationModel = ko.validatedObservable({
    product_id: this.product_id,
  })
  private last_sent_data: KnockoutObservable<HeatingCableInterface> = ko.observable()
  constructor(
    product_model: TSProductModel,
    parent: HeatingCables,
    heating_cable: HeatingCableInterface = { id: -1, product_id: -1 }
  ) {
    super()
    this.product_id.extend(
      { required: true, number: true, min: 1000000, max: 9999999 })
    this.product_model = product_model
    this.parent = parent
    this.product_id(heating_cable.product_id)
    this.id(heating_cable.id)
    this.product_id(heating_cable.product_id)
  }
  product = ko.computed((): ProductInterface | undefined => {
    if (this.product_id() >= 0 && this.product_model) {
      return this.product_model.by_id(this.product_id())
    }
  })
  modified = ko.computed(() => {
    if (!this.last_sent_data()) {
      return true
    }
    if (this.product_id() != this.last_sent_data().product_id) {
      return true
    }
    return false
  })
  save() {
    console.log('not implemented yet (heatingcable.save)')
  }
  set(heating_cable: HeatingCableInterface) {
    console.log('not implemented yet (heatingcable.set)')
  }
  serialize(): HeatingCableInterface {
    return {
      id: this.id(),
      room_id: this.parent.parent.id(),
      product_id: this.product_id()
    }
  }
  public post_measurements(h: any, event: Event): void {
    this.post(
      h,
      event,
      this.serializeMeasurements(),
      '/json/v1/measurements')
  }
  serializeMeasurements(): MeasurementsInterface {
    return {
      id: this.id(),
      ohm_a: this.ohm_a(),
      ohm_b: this.ohm_b(),
      ohm_c: this.ohm_c(),
      mohm_a: this.mohm_a(),
      mohm_b: this.mohm_b(),
      mohm_c: this.mohm_c(),
    }
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
  add = () => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this.root.Products(), this))
    }
    this.root.editing_heating_cable_id(-1)
  }
}
