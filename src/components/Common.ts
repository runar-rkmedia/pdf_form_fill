import { TSAppViewModel } from './AppViewModel'

var GetFormTemplate = require('./get_form_.tpl.html');


export interface StrIndex<TValue> {
  [key: string]: TValue
}
export interface AddressInterface {
  post_area: string;
  post_code: string | null;
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
      return myObj.id() === Number(id)
    });
  }
}
export abstract class Base {
  abstract serialize: KnockoutObservable<{}>
  modification_tracking_list: KnockoutObservableArray<ObsMod<any>> = ko.observableArray()
  public save(): void {
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
  abstract count_cables(): number
  form_url = '/form/'
  parent: any
  file_download: KnockoutObservable<string> = ko.observable()
  remove_instance() {
    this.parent.list.remove(this)
  }
  delete = (data: any = { id: this.id() }) => {
    return $.ajax({
      url: this.url,
      type: HTTPVerbs.delete,
      data: JSON.stringify(data)
    }).done((result: any) => {
      if (result.status == 'OK') {
        this.remove_instance()
      }
    })
  }
  public _delete = this.delete
  public post(h: any, event: Event, data_object?: any, url?: string): any {
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
      if (method == HTTPVerbs.post) {
        this.set(result)
      } else if (method == HTTPVerbs.put) {
        this.save()
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).always(function(result) {
      btn.button('reset')
    })
  }
  comfirm_delete_dialog(title: string, message: string, warning = '') {
    this.comfirm_dialog(title, message, warning, this.delete)
  }
  comfirm_dialog(title: string, message: string, warning = '', callback: any) {
    let message_warning = message
    message_warning += warning ? `<div class="bs-callout bs-callout-warning"><h4>ADVARSEL!</h4><p>${warning}</p></div>` : ''
    bootbox.confirm({
      title: title,
      message: message_warning,
      buttons: {
        cancel: {
          label: 'Avbryt',
        },
        confirm: {
          label: '<span class="glyphicon glyphicon-trash" aria-hidden="true"></span> SLETT',
          className: 'btn-danger'
        }
      },
      callback: (result) => {
        if (result) {
          callback()
        }
      }
    });
  }
  comfirm_unsaved_dialog(title: string, message: string, callback: any) {
    let message_warning = message
    message_warning += `<div class="bs-callout bs-callout-warning"><h4>ADVARSEL!</h4><p>Du har ulagrede elementer. Om du går videre nå, uten å lagre, vil du miste dine endringer.</p></div>`
    bootbox.confirm({
      title: title,
      message: message_warning,
      buttons: {
        cancel: {
          label: 'Avbryt',
        },
        confirm: {
          label: `<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Ja, jeg er sikker`,
          className: 'btn-danger'
        }
      },
      callback: (result) => {
        if (result) {
          callback()
        }
      }
    });
  }
  get_form_and_open(target: string = 'VarmeDokPDF') {
    let importantStuff = window.open('', target);
    // importantStuff.location.href = 'www.gogo.com';
    importantStuff.document.write(GetFormTemplate.replace('${count}', this.count_cables()));
    return this.get_form().done((result: FileDownloadInterface) => {
      importantStuff.location.href = result.file_download;
    })
  }
  get_form() {
    return $.get(this.form_url + this.id())
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
    if (target() == null) {
      return false
    }
    if (target.last_data() == null) {
      return true
    }
    if (typeof target().getMonth === 'function') {
      return target().getTime() != target.last_data().getTime()
    }
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
