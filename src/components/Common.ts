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
export interface CsrfInterface {
  csrf_token?: string
}
export abstract class Post {
  abstract id: KnockoutObservable<number>;
  abstract serialize(): CsrfInterface
  abstract save(): void
  abstract set(result: any): void
  abstract url: string
  send_data(): void {

  }
  post = (h: any, event: Event) => {
    // Abstract class for posting data. Will use PUT if id > 0
    // Also handles buttons
    // Needs a csrf_token to be placed in HTML above button
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let csrf_field = btn.prev('#csrf_token')
    if (csrf_field.length == 0) {
      throw "Could not find the csrf_token, aborting"
    }
    let csrf_token = String(csrf_field.val())
    let data = this.serialize()
    data.csrf_token = csrf_token
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      method = HTTPVerbs.post
    }
    $.ajax({
      url: this.url,
      type: method,
      data: data
    }).done((result: any) => {
      this.save()
      if (method == HTTPVerbs.post) {
        this.set(result)
      } else if (method == HTTPVerbs.put) {
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).always(() => {
      btn.button('reset')
    })
  }
  constructor() { }
}
