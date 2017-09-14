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

export interface CustomerListInterface {
  id: number
  name: string
  address: AddressInterface
  created: Modification
  modified: Modification
}

interface CustomerPages extends Pagination {
  customers: CustomerListInterface[]
}

export class CustomerList {
  list: KnockoutObservableArray<CustomerListInterface> = ko.observableArray()
  page: KnockoutObservable<number> = ko.observable()
  loading: KnockoutObservable<boolean> = ko.observable(false)
  pages: KnockoutObservable<number> = ko.observable(1)
  root: TSAppViewModel
  constructor(root: TSAppViewModel) {
    root = root
    $("a[href='#customer-list-pane']").on('show.bs.tab', (e) => {
      if (this.list().length == 0) {
        this.get_list()
      }
    })
  }
  get_list = (page = 1) => {
    page = Math.min(
      Math.max(page, 1),
      this.pages() || 1)
    if (page == this.page() || isNaN(page)) {
      return null
    }
    this.page(page)
    this.loading(true)
    $.get('/json/v1/list/customers', {
      page: page,
      per_page: 10
    })
      .done((result: CustomerPages) => {
        this.list(result.customers)
        this.pages(result.pages)
        this.page(result.page)
      })
      .always(() => {
        this.loading(false)
      })
  }

}
