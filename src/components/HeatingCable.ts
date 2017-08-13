import { HTTPVerbs, ByID, Post, compareDicts, Base } from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import { TSProductModel, ProductInterface, ProductFilterInterface } from "./ProductModel"

interface MeasurementsInterface {
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: boolean
  mohm_b: boolean
  mohm_c: boolean
}

export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  c_date?: Date
  m_date?: Date
  mod_id?: number
  measurements?: MeasurementsInterface
}


interface PostInterface {
  url: string
  post(): void;
  serialize(): {}
}


export interface HeatingInterfaceFull extends MeasurementsInterface, HeatingCableInterface {
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
  effect: KnockoutObservable<number> = ko.observable();
  mainSpec: KnockoutObservable<number> = ko.observable();
  manufacturor: KnockoutObservable<string> = ko.observable();
  vk_type: KnockoutObservable<string> = ko.observable();
  product_filter: KnockoutObservable<ProductInterface[]>;
  validationModel = ko.validatedObservable({
    product_id: this.product_id,
  })
  last_sent_data: KnockoutObservable<HeatingCableInterface> = ko.observable()
  serialize: KnockoutObservable<HeatingInterfaceFull>
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
    this.product_filter = ko.computed(() => {
      return this.product_model.filter_products({
        effect: this.effect() || this.parent.parent.bestFitEffect(),
        manufacturor: this.manufacturor(),
        mainSpec: this.mainSpec(),
        vk_type: this.vk_type()
      })
    })
    this.serialize = ko.computed(() => {
      let obj = Object.assign(
        {
          id: this.id(),
          room_id: this.parent.parent.id(),
          product_id: Number(this.product_id())
        },
        this.measurements().serialize()
      )
      return obj
    })
    this.init()
    console.log(heating_cable)
    this.set(heating_cable)
  }
  product = ko.computed((): ProductInterface | undefined => {
    if (this.product_id() >= 0 && this.product_model) {
      return this.product_model.by_id(this.product_id())
    }
  })

  set(heating_cable: HeatingCableInterface) {
    this.product_id(heating_cable.product_id)
    this.id(heating_cable.id)
    this.product_id(heating_cable.product_id)
    if (heating_cable.measurements) {
      this.measurements().set(heating_cable.measurements)
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
  add = () => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this.root.Products(), this))
    }
    this.root.editing_heating_cable_id(-1)
  }
}
