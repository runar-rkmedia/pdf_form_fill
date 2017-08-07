import { HTTPVerbs, ByID }  from "./Common"
import { Room } from "./Rooms"

export interface HeatingCableInterface {
  id: number
  product_id: number
}

export class HeatingCable {
  product_id: KnockoutObservable<number> = ko.observable();
  id: KnockoutObservable<number> = ko.observable();
  parent: HeatingCables
  private last_sent_data: KnockoutObservable<HeatingCableInterface> = ko.observable()
  constructor(
    parent: HeatingCables,
    heating_cable: HeatingCableInterface = { id: -1, product_id: 123 }
  ) {
    this.parent = parent
    this.product_id(heating_cable.product_id)
    this.id(heating_cable.id)
  }
}

export class HeatingCables extends ByID {
  list: KnockoutObservableArray<HeatingCable>
  parent: Room
  constructor(parent: Room, list: HeatingCable[] = []) {
    super(list)
    this.parent = parent
  }
  add = () => {
    let new_heating_cable = this.by_id(-1)
    console.log(new_heating_cable)
    if (!new_heating_cable) {
      this.list.push(new HeatingCable(this))
    }
    this.parent.parent.parent.parent.editing_heating_cable_id(-1)
    return new_heating_cable
  }
}
