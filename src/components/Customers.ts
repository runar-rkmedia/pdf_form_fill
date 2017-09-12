import { AddressInterface } from "./Common"
import { TSAppViewModel } from "./AppViewModel"

interface Customers {
  id: number
  name: string
  address: AddressInterface
}

export class Customers implements Customers {
  list: KnockoutObservableArray<Customers> = ko.observableArray()
  parent: TSAppViewModel
  constructor(parent) {
    parent = TSAppViewModel
    this.get()
  }
  get() {
    $.get('/json/v1/list/customers')
      .done((result: Customers) => {
        this.list(result)
      })
  }
}
