import { HTTPVerbs, ByID }  from "./Common"
import { TSAppViewModel } from "./AppViewModel"
import { CustomerInterface, Customer } from './Customer'

export interface RoomInterface {
  room_name: string;
  id: number;
  area: number |null;
  heated_area: number |null;
  outside: boolean;
  customer_id?: number
}

export class Room {
  id: KnockoutObservable<number> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  outside: KnockoutObservable<boolean> = ko.observable()
  area: KnockoutObservable<number> = ko.observable()
  heated_area: KnockoutObservable<number> = ko.observable()
  validationModel = ko.validatedObservable({
    name: this.name,
    outside: this.outside,
    area: this.area,
    heated_area: this.heated_area
  })
  parent: Rooms
  private last_sent_data: KnockoutObservable<RoomInterface> = ko.observable()

  constructor(parent: Rooms, room: RoomInterface | undefined = undefined) {
    this.area.extend(
      {required: true, number: true, min: 0.1, max: 1000});
    this.heated_area.extend(
      {required: true, number: true, min: 0.1, max: 1000});
    this.name.extend(
      {required: true, minLength: 2, maxLength: 50});
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
      customer_id: this.parent.parent.parent.customer_id()
    }
  }
  post = (r: Rooms, event: Event) => {
    let method: HTTPVerbs
    let btn = $(event.target)
    btn.button('loading')
    let form = btn.closest('form')
    let data = form.serializeArray()
    data.push({ name: 'customer_id', value: String(this.parent.parent.parent.customer_id()) })
    data.push({ name: 'id', value: String(this.id()) })
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

export class Rooms extends ByID {
  list: KnockoutObservableArray<Room>
  parent: Customer

  constructor(parent: Customer, list_of_rooms: Room[] = []) {
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
}
