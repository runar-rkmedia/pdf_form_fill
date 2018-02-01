import { ByID, } from "./Common"
import { HeatingCable, HeatingCableInterface } from "./HeatingCable"
import { Room } from "./Room"
import { TSAppViewModel } from "./AppViewModel"



export class HeatingCableList extends ByID {
  list: KnockoutObservableArray<HeatingCable>
  parent: Room
  root: TSAppViewModel
  constructor(root: TSAppViewModel, parent: Room, heating_cables: HeatingCableInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    let heating_cables_objects: HeatingCable[] = []
    if (heating_cables_objects) {
      heating_cables_objects = heating_cables.map((x) => {
        return new HeatingCable(this.root.Products(), this, x)
      })
    }
    this.list(heating_cables_objects)
  }
  has_key = (key: string, value: any[]): boolean => {
    for (let heating_cable of this.list()) {
      if (heating_cable.product()) {
        if (value.indexOf((<any>heating_cable.product()!)[key]) >= 0) {
          return true
        }
      }
    }
    return false
  }
  has_manufacturor = (manufacturor: string[] | string): boolean => {
    if (manufacturor instanceof String) {
      manufacturor = [manufacturor]
    }
    return this.has_key('manufacturor', manufacturor)
  }
  add = (event: Event) => {
    let new_heating_cable = this.by_id(-1)
    if (!new_heating_cable) {
      new_heating_cable = new HeatingCable(this.root.Products(), this)
      this.list.push(new_heating_cable)
    }
    new_heating_cable.product_filter().effect(new_heating_cable.suggested_effect())
    this.root.editing_heating_cable_id(-1)
    setTimeout(() => {    // Expand the panel
      let btn = $(event.target)
      let accordian = btn.closest('.panel-body')
      let panel = accordian.find('#heat-1')
      let panel_vk = panel.find('#panel_select_cable-1')
      panel.collapse('show')
      panel_vk.collapse('show')
      new_heating_cable.validationModel.errors.showAllMessages(false)

    }, 50)

  }
}
