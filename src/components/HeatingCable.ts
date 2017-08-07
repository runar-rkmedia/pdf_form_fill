import { Room } from "./Rooms"

export class HeatingCable {
  product_id: KnockoutObservable<number> = ko.observable();
  parent: HeatingCables
  constructor (parent: HeatingCables, product_id=-1){
    this.parent = parent
    this.product_id(product_id)
  }
}

export class HeatingCables {
  list: KnockoutObservableArray<HeatingCable> = ko.observableArray()
  parent: Room
  constructor (parent: Room, list=[]){
    this.parent = parent
    this.list(list)
  }
}
