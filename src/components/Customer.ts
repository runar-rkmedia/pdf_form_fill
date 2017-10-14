import { TSAppViewModel } from "./AppViewModel"
import { RoomInterface, Room } from "./Room"
import { RoomList } from "./RoomList"
import { CustomerData, CustomerDataInterface } from "./CustomerData"
import { HeatingCableInterface } from "./HeatingCable"

import { StrIndex, AddressFullInterface, Base, Post, AddressInterface, ObsMod } from "./Common"


export interface CustomerInterface {
  customer_id: number;
  datas: CustomerDataInterface[]
  rooms?: RoomInterface[];
  construction_voltage: number
  construction_new: boolean
}

interface MultiSave {
  rooms: RoomInterface[]
  heating_cables: HeatingCableInterface[]
  customer?: CustomerInterface
}

interface MultiSaveID {
  room?: RoomInterface
  heating_cable?: HeatingCableInterface
  customer?: CustomerInterface
}

export class Customer extends Post {
  url = '/json/v1/customer/'
  construction = new CustomerData('construction', true)
  owner = new CustomerData('owner', false)
  root: TSAppViewModel
  construction_voltage: KnockoutObservable<number> = this.obs_mod(undefined, undefined, 230)
  construction_new: KnockoutObservable<boolean> = this.obs_mod(undefined, undefined, false)
  loading: KnockoutObservable<boolean> = ko.observable(false)
  rooms: KnockoutObservable<RoomList> = ko.observable(new RoomList(this.root, this))
  id: KnockoutObservable<number> = ko.observable()
  serialize: KnockoutObservable<CustomerInterface>
  constructor(parent: TSAppViewModel, id: number = -1000, root: TSAppViewModel = parent) {
    super(parent)
    this.root = parent
    this.id(id)

    this.serialize = ko.computed((): CustomerInterface => {
      let t: CustomerInterface = {
        customer_id: this.id(),
        datas: [this.construction.serialize()],
        construction_new: this.construction_new(),
        construction_voltage: this.construction_voltage()
      }
      if (this.owner.address1()) {
        t.datas.push(this.owner.serialize())
      }
      return t
    })
  }
  isValid = ko.computed(() => {
    return this.owner.validationModel.isValid() && this.construction.validationModel.isValid()
  })

  sub_isValid = ko.computed(() => {
    for (let room of this.rooms().list()) {
      if (!room.validationModel.isValid()) {
        return false
      }
      for (let heating_cable of room.heating_cables().list()) {
        if (!heating_cable.validationModel.isValid()) {
          return false
        }
      }
    }
    return true
  })

  modified = ko.computed(() => {
    if (this.construction.modified() || this.owner.modified()) {
      return true
    }
    return this.modification_check(this.modification_tracking_list())
  })
  sub_modified = ko.computed(() => {
    if (this.rooms()) {
      for (let room of this.rooms().list()) {
        if (room.modified() || room.sub_modified()) {
          return true
        }
      }
    }
    return false
  })
  can_fill_form = ko.computed(() => {
    if (this.modified() || this.sub_modified()) {
      return false
    }
    if (this.rooms().list().length == 0) {
      return false
    }
    for (let room of this.rooms().list()) {
      if (room.heating_cables().list().length > 0) {
        return true
      }
    }
    return false
  })
  save() {
    this.owner.save()
    this.construction.save()
    super.save()
    $('#customer_form_collapse').collapse('hide')
  }
  post(h: any, event: Event) {
    if (!this.modified() || !this.isValid()) {
      return $.Deferred()
    }
    return super.post(h, event)
  }
  post_all(h: any, event: Event) {
    let data = this.serialize_all()
    if (
      data.rooms.length > 0 ||
      data.heating_cables.length > 0 ||
      data.customer
    ) {
      return super.post(h, event, data, '/json/v1/multi_save').done(this.save_all)

    }
  }
  serialize_all(): MultiSave {
    let data: MultiSave = {
      customer: this.modified() ? this.serialize() : undefined,
      rooms: [],
      heating_cables: []
    }
    for (let room of this.rooms().list()) {
      if (room.modified()) {
        data.rooms.push(room.serialize())
      }
      for (let heating_cable of room.heating_cables().list()) {
        if (heating_cable.modified()) {
          data.heating_cables.push(heating_cable.serialize())
        }
      }
    }
    return data
  }
  save_all = (result: MultiSaveID) => {
    if (result.customer) {
      this.set(result.customer)
    }
    for (let room of this.rooms().list()) {
      if (room.id() == -1 && result.room) {
        room.set(result.room)
      } else {
        room.save()
        for (let heating_cable of room.heating_cables().list()) {
          if (heating_cable.id() == -1 && result.heating_cable) {
            heating_cable.set(result.heating_cable)
          } else {
            heating_cable.save()
          }
        }
      }
    }
  }

  set(result: CustomerInterface) {
    if (result.customer_id) {
      this.id(result.customer_id)
    }
    if (result.datas) {
      for (let data of result.datas) {
        if (data.data_type == 'construction') {
          this.construction.set(data)
        } else if (data.data_type == 'owner') {
          this.owner.set(data)
        }
      }
    }
    if (result.construction_new) {
      this.construction_new(result.construction_new)
    }
    if (result.construction_voltage) {
      this.construction_voltage(result.construction_voltage)
    }
    if (result.rooms) {
      this.rooms(new RoomList(this.root, this, result.rooms))
    }
    this.save()
  }
  remove_instance() {
    this.parent.customer(new Customer(this.parent))
  }
  confirm_create_new = () => {
    if (this.modified() || this.sub_modified()) {
      this.comfirm_unsaved_dialog('Opprette ny kunde', 'Er du sikker på at du vil opprette en ny kunde?', this.create_new)
    } else {
      this.create_new()
    }
  }
  create_new = () => {
    this.set({
      customer_id: -1,
      construction_new: false,
      construction_voltage: 230,
      datas:
      [
        {
          orgnumber: null,
          phone: null,
          mobile: null,
          contact_name: '',
          data_type: 'owner',
          customer_name: '',
          address: {
            address1: '',
            address2: '',
            post_code: null,
            post_area: ''
          }
        },
        {
          orgnumber: null,
          phone: null,
          mobile: null,
          contact_name: '',
          data_type: 'construction',
          customer_name: '',
          address: {
            address1: '',
            address2: '',
            post_code: null,
            post_area: ''
          }
        }
      ],
      rooms: []
    })
    this.construction.validationModel.errors.showAllMessages(false)
    $('#customer_form_collapse').collapse('show')
  }
  get = (id?: number) => {
    this.loading(true)
    $.get("/json/v1/customer/", { id })
      .done((result: CustomerInterface) => {
        this.set(result)
      })
      .always(() => {
        this.loading(false)
      })
  }
  public delete = (data = { customer_id: this.id() }) => {
    return this._delete(data)
  }
}
