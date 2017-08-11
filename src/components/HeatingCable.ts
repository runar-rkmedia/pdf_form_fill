import { HTTPVerbs, ByID, Post }  from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import { TSProductModel, ProductInterface } from "./ProductModel"

export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  csrf_token?: string
  c_date?: Date
  m_date?: Date
  mod_id?: number
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

}

export class HeatingCables extends ByID {
  list: KnockoutObservableArray<HeatingCable>
  parent: Room
  root: TSAppViewModel
  constructor(root: TSAppViewModel, parent: Room, list: HeatingCable[] = []) {
    super(list)
    this.parent = parent
    this.root = root
  }
  add = () => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this.root.Products(), this))
    }
    this.root.editing_heating_cable_id(-1)
  }
}
