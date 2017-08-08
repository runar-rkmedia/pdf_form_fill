import { TSProductModel } from './ProductModel'
import { RoomSuggestionInterface, RoomSuggestionList} from './InterfaceRoom'
import nb_NO = require('./../../node_modules/knockout.validation/localization/nb-NO.js')
import kv = require("knockout.validation");
import { StrIndex, AddressInterface, HTTPVerbs } from "./Common"
import { CustomerInterface, Customer} from "./Customer"
import { Rooms, RoomInterface  } from "./Rooms"
import ko = require("knockout");
import $ = require("jquery");
var titleCase = require('title-case')

require("knockout.typeahead");
require("knockout-template-loader?name=suggestion-template!html-loader?-minimize!./suggestion.html");

// Switch locale for knockout.validation
kv.defineLocale('no-NO', nb_NO);
kv.locale('nb-NO')

interface FileDownloadInterface {
  address_id: number
  file_download: string
  filled_form_modified_id: number
  error_fields?: Array<string>
  error_message?: string
}



export class TSAppViewModel {
  manufacturor: KnockoutObservable<string> = ko.observable();
  vk_type: KnockoutObservable<string> = ko.observable();
  mainSpec: KnockoutObservable<number> = ko.observable();
  effect: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
  });
  ohm_a: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  ohm_b: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  ohm_c: KnockoutObservable<{}> = ko.observable().extend({
    number: true,
    min: 0,
    max: 1000,
  });
  mohm_a: KnockoutObservable<{}> = ko.observable();
  mohm_b: KnockoutObservable<{}> = ko.observable();
  mohm_c: KnockoutObservable<{}> = ko.observable();
  error_fields: KnockoutObservableArray<string> = ko.observableArray();
  error_message: KnockoutObservable<string> = ko.observable();
  file_download: KnockoutObservable<string> = ko.observable();
  last_sent_args: KnockoutObservable<string> = ko.observable();
  form_args: KnockoutObservable<string> = ko.observable($('#form').serialize());
  Products: KnockoutObservable<TSProductModel> = ko.observable();
  selected_vk: KnockoutObservable<number> = ko.observable();
  forced_selected_vk: KnockoutObservable<number> = ko.observable();
  address_id: KnockoutObservable<number> = ko.observable();
  editing_heating_cable_id: KnockoutObservable<number> = ko.observable();
  customer_id: KnockoutObservable<number> = ko.observable();
  customer: KnockoutObservable<Customer> = ko.observable(new Customer(this))
  filled_form_modified_id: KnockoutObservable<number> = ko.observable();
  user_forms: KnockoutObservableArray<string> = ko.observableArray();
  company_forms: KnockoutObservableArray<string> = ko.observableArray();
  validation_errors: KnockoutValidationErrors = kv.group(self);
  loading: KnockoutObservableArray<string> = ko.observableArray();
  autocompleteAddress: KnockoutComputed<string>;

  delete: KnockoutObservable<string> = ko.observable();


  noname: any

  constructor() {
    kv.init({
      decorateInputElement: true,
      errorElementClass: 'has-error has-feedback',
      // successElementClass: 'has-feedback has-success',
      insertMessages: true,
      // decorateElement: true,
      // errorElementClass: 'error',
      errorMessageClass: 'bg-danger'
    });

    // Add bootstrap-validation-css to parent of field
    let init = ko.bindingHandlers['validationCore'].init!;
    ko.bindingHandlers['validationCore'].init = (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) => {
      init(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);
      let config = kv.utils.getConfigOptions(element);
      // if requested, add binding to decorate element
      if (config.decorateInputElement && kv.utils.isValidatable(valueAccessor())) {
        let parent = $(element).parent();
        if (parent.length) {
          ko.applyBindingsToNode(parent[0], {
            validationElement: valueAccessor()
          });
        }
      }
    };
    this.Products(new TSProductModel(this));
    this.Products().getProducts();

    this.noname = ko.computed(() => {
      try {
        var f = this.Products().flat_products();
        if (f.length > 0) {
          this.get_user_forms();
        }
      } catch (e) {

      } finally {

      }
    });

    this.autocompleteAddress = ko.computed(() => {
      let url: string = '/address/?q=%QUERY'
      if (this.customer().address1()) {
        url += '&p=' + this.customer().address1()
      }
      return url
      // We need a rateLimiter here so that the url doesn't change too early
      // when a user clicks a selection.
    }).extend({ rateLimit: 50 })


    ko.computed(() => {
      if (this.mainSpec()) {
        try {
          let f = this.Products().spec_groups();
          if (f.find(item => item.mainSpec === this.mainSpec())) {

          }
          if (this.findWithAttr(f, 'mainSpec', this.mainSpec()) < 0) {
            this.mainSpec(null);
          }
        } catch (e) {

        } finally {

        }
      }
    });
    this.customer().get(52)
  }

  suggestRoom = () => {
    let listOfRooms: RoomSuggestionInterface[] = []
    RoomSuggestionList.forEach((room, index) => {
      listOfRooms.push({
        name: room.name,
        id: index
      })
      if (room.aliases) {
        for (let alias of room.aliases) {
          listOfRooms.push({
            name: alias,
            id: index
          })
        }
      }
    })
    return listOfRooms
  };

  roomSuggestionOnSelect = (
    value: KnockoutObservable<string>,
    roomSuggestion: RoomInterface,
    event: Event
  ) => {
    let room_data = RoomSuggestionList[roomSuggestion.id]
    let form = $(event.target).closest('form').serializeArray()
    let id = form[this.findWithAttr(form, 'name', 'id')].value
    let room = this.customer().rooms().by_id(Number(id))
    if (room) {
      room.outside(Boolean(room_data.outside))
    }
  }

  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    address: AddressInterface,
    event: any,
    element: any) => {
    value(titleCase(address.street_name))
    this.customer().post_code((address.post_code))
    this.customer().post_area(address.post_area.toUpperCase())
  }

  parse_form_download = (result: FileDownloadInterface) => {
    this.last_sent_args(this.form_args());
    if (result.error_fields) {
      this.error_fields(result.error_fields);
    }
    if (result.file_download) {
      this.file_download(result.file_download);
      if (result.address_id) {
        this.address_id(result.address_id);
      }
      if (result.filled_form_modified_id) {
        this.filled_form_modified_id(result.filled_form_modified_id);
      }
    }
    if (result.error_message) {
      this.error_message(result.error_message);
    }
  }
  post_customer_form = (e: any, event: any) => {
    let button = $(event.target)
    button.button('loading')
    let type = 'POST'
    let data = $('#customer_form').serializeArray()
    if (this.customer_id()) {
      data.push({ name: 'id', value: String(this.customer_id()) })
    }
    if (this.customer_id()) {
      type = 'PUT'
    }
    $.ajax({
      url: '/json/v1/customer/',
      type: type,
      data: data
    }).done((result) => {
      this.customer_id(result.customer_id)
      setTimeout(() => {
        button.text('Endre')
      }, 20)
    }).always(() => {
      button.button('reset')
    })
  }
  findWithAttr = (array: Array<any>, attr: string, value: any) => {
    for (var i = 0; i < array.length; i += 1) {
      if (array[i][attr] === value) {
        return i;
      }
    }
    return -1;
  }

  get_user_forms = () => {
    this.loading.push('user_form')
    $.get("/forms.json", {})
      .done((result) => {
        result.user_forms.prefix = 'user_forms';
        result.company_forms.prefix = 'company_forms';
        this.user_forms(result.user_forms);
        this.company_forms(result.company_forms);
        this.loading.remove('user_form')
      });
  }
}
// Inject our CSRF token into our AJAX request.
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(String(settings.type)) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
    }
  }
})
