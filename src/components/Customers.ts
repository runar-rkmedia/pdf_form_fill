import { AddressInterface } from "./Common"
import { TSAppViewModel } from "./AppViewModel"

interface Modification {
  given_name: string
  family_name: string
  date: Date
}

export interface Customers {
  id: number
  name: string
  address: AddressInterface
  created: Modification
  modified: Modification
}

export class Customers implements Customers {
  list: KnockoutObservableArray<Customers> = ko.observableArray()
  parent: TSAppViewModel
  constructor(parent: TSAppViewModel) {
    parent = parent
    this.get_list()
  }
  get_list() {
    $.get('/json/v1/list/customers')
      .done((result: Customers[]) => {
        console.log(result)
        this.list(result)
      })
  }
}
