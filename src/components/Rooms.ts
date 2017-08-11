import { HTTPVerbs, ByID, Post, CsrfInterface}  from "./Common"
import { TSAppViewModel } from "./AppViewModel"
import { CustomerInterface, Customer } from './Customer'
import { HeatingCable, HeatingCables, HeatingCableInterface} from './HeatingCable'

export interface RoomInterface {
  room_name: string;
  id: number;
  area: number |null;
  heated_area: number |null;
  outside: boolean;
  customer_id?: number
  heating_cables?: HeatingCableInterface[]
}

export class Room extends Post {
  url = '/json/v1/room/'
  id: KnockoutObservable<number> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  outside: KnockoutObservable<boolean> = ko.observable()
  area: KnockoutObservable<number> = ko.observable()
  heated_area: KnockoutObservable<number> = ko.observable()
  heating_cables: KnockoutObservable<HeatingCables> = ko.observable()
  validationModel = ko.validatedObservable({
    name: this.name,
    outside: this.outside,
    area: this.area,
    heated_area: this.heated_area
  })
  parent: Rooms
  root: TSAppViewModel
  private last_sent_data: KnockoutObservable<RoomInterface> = ko.observable()

  constructor(root: TSAppViewModel, parent: Rooms, room: RoomInterface | undefined = undefined) {
    super()
    this.area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.heated_area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.name.extend(
      { required: true, minLength: 2, maxLength: 50 });
    this.parent = parent
    this.root = root
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
    let heating_cables: HeatingCable[] = []
    if (room.heating_cables) {
      let self = this
      let heating_cables = room.heating_cables.map(function(x) {
        // console.log(x)
        return new HeatingCable(self.root.Products(), self.heating_cables(), x)
      })
    }
    if (room.heating_cables) {
      // console.log(room.heating_cables)
      // console.log('room.heating_cables')
      // console.log(heating_cables)
    }
    this.heating_cables(new HeatingCables(this.root, this, heating_cables))
  }
  serialize(): RoomInterface & CsrfInterface {
    return {
      room_name: this.name(),
      id: this.id(),
      area: this.area(),
      heated_area: this.heated_area(),
      outside: this.outside(),
      customer_id: this.root.customer_id()
    }
  }
}

export class Rooms extends ByID {
  list: KnockoutObservableArray<Room>
  parent: Customer
  root: TSAppViewModel

  constructor(root: TSAppViewModel, parent: Customer, list_of_rooms: Room[] = []) {
    super(list_of_rooms)
    console.log(list_of_rooms)
    this.parent = parent
    this.root = root
  }
  add = () => {
    let new_room = this.by_id(-1)
    if (!new_room) {
      this.list.push(new Room(this.root, this))
    }
    let accordian = $('#accordion-room')
    let panel = accordian.find('#room-1')
    let first_input = panel.find('input:text').first()
    panel.removeClass('collapse')
    first_input.focus()
    return new_room
  }
  get = (id: number) => {
    $.get("/json/v1/customer/", { id })
      .done((result: CustomerInterface) => {
        this.parent.address1(result.address.address1)
        this.parent.address2(result.address.address2)
        this.parent.post_code(result.address.post_code)
        this.parent.post_area(result.address.post_area)
        this.root.customer_id(result.id)
        this.list([])
        this.list(result.rooms.map((x) => {
          return new Room(this.root, this, x)
        }))
      })
  }
}
