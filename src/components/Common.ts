import { AddressInterface } from "./Common"
import { TSAppViewModel } from './AppViewModel'
var diff = require('recursive-diff');
import bootbox = require("bootbox")
export interface StrIndex<TValue> {
  [key: string]: TValue
}
export interface AddressInterface {
  post_area: string;
  post_code: number | null;
  street_name?: string;
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
    return this.list().find(myObj => {
      return myObj.id === Number(id)
    });
  }
}
export abstract class Base {
  abstract serialize: KnockoutObservable<{}>
  modification_tracking_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  save(): void {
    for (let observable of this.modification_tracking_list()) {
      if (observable) {
        observable.save()
      }
    }
  }

  constructor() {
  }
  modification_check(list: ObsMod<any>[]) {
    for (let observable of list) {
      if (observable.modified()) {
        return true
      }
    }
    return false
  }
  obs_mod = (group: KnockoutObservableArray<any>[] = [], kind: any = ko.observable, value?: any) => {
    let list = [this.modification_tracking_list].concat(group)
    return kind(value).extend({ modification: list });
  }
  modified = ko.computed(() => {
    return this.modification_check(this.modification_tracking_list())
  })
}

export interface FileDownloadInterface {
  file_download: string
}
export abstract class Post extends Base {
  abstract id: KnockoutObservable<number>;
  abstract serialize: KnockoutObservable<{}>
  abstract set(result: any): void
  abstract url: string
  parent: any
  file_download: KnockoutObservable<string> = ko.observable()
  public delete() {
    return $.ajax({
      url: this.url,
      type: HTTPVerbs.delete,
      data: JSON.stringify({ id: this.id() })
    }).done((result: any) => {
      this.parent.list.remove(this)
    })
  }
  public post(h: any, event: Event, data_object?: any, url?: string) {
    // Abstract class for posting data. Will use PUT if id > 0
    // Also handles buttons
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let data = data_object || this.serialize()
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      delete data['id']
      method = HTTPVerbs.post
    }
    return $.ajax({
      url: url || this.url,
      type: method,
      data: JSON.stringify(data),
    }).done((result: any) => {
      this.save()
      if (method == HTTPVerbs.post) {
        this.set(result)
      } else if (method == HTTPVerbs.put) {
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).fail((result, a, c) => {
      console.log(result.responseJSON.errors)
    }).always(function(result) {
      btn.button('reset')
    })
  }
  comfirm_delete_dialog(title: string, message: string, warning?: string) {
    let message_warning = message
    message_warning += warning ? `<div class="bs-callout bs-callout-warning"><h4>ADVARSEL!</h4><p>${warning}</p></div>` : ''
    console.log(warning)
    bootbox.confirm({
      title: title,
      message: message_warning,
      buttons: {
        cancel: {
          label: 'Nei, ikke slett',
        },
        confirm: {
          label: '<span class="glyphicon glyphicon-trash" aria-hidden="true"></span> SLETT',
          className: 'btn-danger'
        }
      },
      callback: (result) => {
        if (result) {
          console.log(this.delete())
        }
      }
    });
  }
  get_form_and_open(target: string = 'VarmeDokPDF') {
    let importantStuff = window.open('', target);
    importantStuff.document.write('Henter skjema...');
    return this.get_form().done((result: FileDownloadInterface) => {
      importantStuff.location.href = result.file_download;
    })
  }
  get_form() {
    return $.get(this.url, { id: this.id() })
      .done((result: FileDownloadInterface) => {
        this.file_download(result.file_download)
      })
  }
  constructor(parent: ByID | TSAppViewModel) {
    super()
    this.parent = parent
  }
}

declare global {
  interface KnockoutExtenders {
    modification<T>(target: T, track: any): ObsMod<T>;
  }
}

export interface ObsMod<T> extends KnockoutObservable<T> {
  // last_data(any: any): any
  reset(): void
  save(): void
  modified(): boolean
}
ko.extenders.modification = (target: any, option: KnockoutObservableArray<any>[]) => {
  target.last_data = ko.observable()
  target.modified = ko.computed(() => {
    if (target() != target.last_data()) {
      let div = target() / target.last_data()
      // for calculated values that are almost the same.
      if (div > 0.99999 && div < 1.00001) {
        return false
      }
    }
    return target() != target.last_data()
  })
  target.reset = () => {
    target(target.last_data())
  }
  target.save = () => {
    target.last_data(target())
  }
  for (let list of option) {
    list.push(target)
  }
  return target;
};
