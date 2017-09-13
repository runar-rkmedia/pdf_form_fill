import { AddressInterface } from "./Common"
import { TSAppViewModel } from "./AppViewModel"

interface Modification {
  given_name: string
  family_name: string
  date: Date
}

interface Pagination {
  page: number
  pages: number
}

export interface Customers {
  id: number
  name: string
  address: AddressInterface
  created: Modification
  modified: Modification
}

interface CustomerPages extends Pagination {
  customers: Customers[]
}

export class Customers implements Customers {
  list: KnockoutObservableArray<Customers> = ko.observableArray()
  page: KnockoutObservable<number> = ko.observable()
  pages: KnockoutObservable<number> = ko.observable()
  parent: TSAppViewModel
  constructor(parent: TSAppViewModel) {
    parent = parent
    this.get_list()
  }
  get_list(page = 1) {
    page = Math.min(
      Math.max(page, 1),
      this.pages() || 1)
    if (page == this.page() || isNaN(page)) {
      return null
    }
    this.page(page)
    $.get('/json/v1/list/customers', {
      page: page,
      per_page: 10
    })
      .done((result: CustomerPages) => {
        console.log(result)
        this.list(result.customers)
        this.pages(result.pages)
        this.page(result.page)
      })
  }
}
