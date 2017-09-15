import { ByID, } from "./Common"
import { Room, RoomInterface } from "./Room"
import { Customer } from "./Customer"
import { TSAppViewModel } from "./AppViewModel"

export class RoomList extends ByID {
  // list: KnockoutObservableArray<Room>
  parent: Customer
  root: TSAppViewModel

  constructor(root: TSAppViewModel, parent: Customer, list_of_rooms: RoomInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    if (list_of_rooms) {
      let list_of_rooms_obects = list_of_rooms.map((x) => {
        return new Room(this.root, this, x)
      })
      this.list(list_of_rooms_obects)

    }


  }
  add = () => {
    let new_room = this.by_id(-1)
    if (!new_room) {
      this.list.push(new Room(this.root, this))
    }
    let accordian = $('#accordion-room')
    let panel = accordian.find('#room-1')
    let room_form = panel.find('#room-form-1')
    let first_input = panel.find('input').first()
    room_form.addClass('in')
    panel.collapse('show')
    // Focus does not work becaus of an issue with using typeahead.Workaround
    // with using a setTimeOut doesnt seemt to work inside animated stuff, so
    // for now, I will leave it not working.
    first_input.focus()
    return new_room
  }
}
