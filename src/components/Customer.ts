import { TSAppViewModel } from "./AppViewModel"
import {StrIndex}  from "./Common"
import ko = require("knockout");

export interface RoomInterface {
  room_name: string;
  id: number;
  area: number |null;
  heated_area: number |null;
  outside: boolean;
  customer_id?: number
}
export interface CustomerInterface {
  id: number;
  name: string;
  address: AddressFullInterface;
  rooms: RoomInterface[];
}

export class Room {
  id: KnockoutObservable<number> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  outside: KnockoutObservable<boolean> = ko.observable()
  area: KnockoutObservable<number> = ko.observable()
  heated_area: KnockoutObservable<number> = ko.observable()
  parent: Rooms
  private last_sent_data: KnockoutObservable<RoomInterface> = ko.observable()

  constructor(
    parent: Rooms,
    room: RoomInterface | undefined = undefined) {
    this.parent = parent
    this.set(room)
  }
  modified = ko.computed(() => {
    if (!this.last_sent_data()) {
      return true
    }
    if (
      this.name() != this.last_sent_data().room_name ||
      this.outside() != this.last_sent_data().outside ||
      this.area() != this.last_sent_data().area ||
      this.heated_area() != this.last_sent_data().heated_area
    ) {
      return true
    }
    return false
  })
  save() {
    this.last_sent_data({
      room_name: this.name(),
      id: this.id(),
      area: this.area(),
      heated_area: this.heated_area(),
      outside: this.outside()
    })
  }
  set(room: RoomInterface = {
    room_name: '',
    id: -1,
    area: null,
    heated_area: null,
    outside: false
  }) {
    this.name(room.room_name)
    this.id(room.id)
    this.area(room.area)
    this.heated_area(room.heated_area)
    this.outside(room.outside)
    this.save()
  }
  serialize(): RoomInterface {
    // TODO: Can be removed
    return {
      room_name: this.name(),
      id: this.id(),
      area: this.area(),
      heated_area: this.heated_area(),
      outside: this.outside(),
      customer_id: this.parent.parent.customer_id()
    }
  }
  post = (r: Rooms,event: Event) => {
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let form = btn.closest('form')
    let data = form.serializeArray()
    data.push({name: 'customer_id', value: String(this.parent.parent.customer_id())})
    data.push({name: 'id', value: String(this.id())})
    console.log(data)
    if (this.id() >= 0) {
      method = HTTPVerbs.put
    } else {
      method = HTTPVerbs.post
    }
    $.ajax({
      url: '/json/v1/room/',
      type: method,
      data: data
    }).done((result: RoomInterface) => {
      this.save()
      if (method == 'POST') {
        this.set(result)
      } else if (method == 'PUT') {
      }
      setTimeout(() => {
        btn.text('Endre')
      }, 20)
    }).always(() => {
      btn.button('reset')
    })
  }
}

export class Rooms {
  list: KnockoutObservableArray<Room>
  parent: TSAppViewModel

  constructor(parent: TSAppViewModel, list_of_rooms: Room[] = []) {
    this.list = ko.observableArray(list_of_rooms)
    this.parent = parent
  }
  by_id(id: number) {
    for (let room of this.list()) {
      if (room.id() == id) {
        return room
      }
    }
  }
  add = () => {
    let new_room = this.by_id(-1)
    if (!new_room) {
      this.list.push(new Room(this))
    }
    let accordian = $('#accordion-room')
    let panel = accordian.find('#room-1')
    let first_input = panel.find('input:text').first()
    panel.removeClass('collapse')
    first_input.focus()
    return new_room
  }
  get = () => {
    $.get("/json/v1/customer/", { id: 51 })
      .done((result: CustomerInterface) => {
        this.parent.anleggs_adresse(result.address.address1)
        this.parent.anleggs_adresse2(result.address.address2)
        this.parent.anleggs_postnummer(result.address.post_code)
        this.parent.anleggs_poststed(result.address.post_area)
        this.parent.customer_id(result.id)
        this.list([])
        let self = this
        this.list(result.rooms.map(function(x) {
          return new Room(self, x)
        }))
      })
  }
}
