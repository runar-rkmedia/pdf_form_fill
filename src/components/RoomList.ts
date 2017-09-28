import { ByID, } from "./Common"
import { Room, RoomInterface } from "./Room"
import { Customer } from "./Customer"
import { TSAppViewModel } from "./AppViewModel"
import { getCookie, setCookie } from "./helpers/cookie"

export class RoomList extends ByID {
  // list: KnockoutObservableArray<Room>
  parent: Customer
  root: TSAppViewModel
  selected: KnockoutObservable<number> = ko.observable()

  constructor(root: TSAppViewModel, parent: Customer, list_of_rooms: RoomInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    if (list_of_rooms) {
      let list_of_rooms_obects = list_of_rooms.map((x) => {
        return new Room(this.root, this, x)
      })
      this.list(list_of_rooms_obects)
      if (this.list().length > 0) {
        this.selected(Math.min(Number(getCookie('selected_room')), this.list().length - 1))
      }
    }
  }
  select = (index: number) => {
    if (index >= 0 && index < this.list().length) {
      this.selected(index)
      setCookie('selected_room', index)

    }
  }
  add = () => {
    let new_room = this.by_id(-1)
    if (!new_room) {
      this.list.push(new Room(this.root, this))
    }
    this.selected(this.list().length - 1)

    return new_room
  }
}
