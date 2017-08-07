import { AddressInterface } from "./Common"

export interface StrIndex<TValue> {
  [key: string]: TValue
}
export interface AddressInterface {
  post_area: string;
  post_code: number;
  street_name: string;
}

export interface AddressFullInterface extends AddressInterface {
  address1: string;
  address2: string;
}

export const enum HTTPVerbs {
  post = 'POST',
  get = 'GET',
  put = 'PUT',
  delete = 'DELETE',
  patch = 'PATCH'
}

export class ByID {
  list: KnockoutObservableArray<any>
  constructor(list: any[]) {
    this.list = ko.observableArray(list)
  }
  by_id(id: number) {
    for (let item of this.list()) {
      if (item.id() == id) {
        return item
      }
    }
  }
}
