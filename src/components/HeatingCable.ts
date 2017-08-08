import { HTTPVerbs, ByID }  from "./Common"
import { Room } from "./Rooms"
import { TSAppViewModel } from "./AppViewModel"
import { TSProductModel, ProductInterface } from "./ProductModel"

export interface HeatingCableInterface {
  id: number
  product_id: number
  room_id?: number
  csrf_token?: string
}

export class HeatingCable {
  product_id: KnockoutObservable<number> = ko.observable();
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
  save = () => {
    console.log('not implemented yet (heatingcable.save)')
  }
  set = (heating_cable: HeatingCableInterface) => {
    console.log('not implemented yet (heatingcable.set)')
  }
  serialize = (): HeatingCableInterface => {
    return {
      id: this.id(),
      room_id: this.parent.parent.id(),
      product_id: this.product_id()
    }
  }
  post = (h: HeatingCable, event: Event) => {
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let csrf_field = btn.prev('#csrf_token')
    let csrf_token
    if (csrf_field.length) {
      let csrf_token = String(csrf_field.val())
    } else {
      throw "Could not find the csrf_token, aborting"
    }
    let data = this.serialize()
    data.csrf_token = csrf_token
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      method = HTTPVerbs.post
    }
    $.ajax({
      url: '/json/v1/heat/',
      type: method,
      data: data
    }).done((result: HeatingCableInterface) => {
      this.save()
      if (method == 'POST') {
        this.set(result)
      } else if (method == 'PUT') {
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).always(() => {
      btn.button('reset')
    })
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
