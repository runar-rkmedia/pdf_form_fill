import { TSProductModel } from './ProductModel'
import nb_NO = require('./../../node_modules/knockout.validation/localization/nb-NO.js')
import kv = require("knockout.validation");
import { StrIndex, AddressInterface, HTTPVerbs } from "./Common"
import { CustomerInterface, Customer } from "./Customer"
import { Rooms, RoomInterface } from "./Rooms"
import ko = require("knockout");
import $ = require("jquery");


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
  customer: KnockoutObservable<Customer> = ko.observable(new Customer(this))
  filled_form_modified_id: KnockoutObservable<number> = ko.observable();
  user_forms: KnockoutObservableArray<string> = ko.observableArray();
  company_forms: KnockoutObservableArray<string> = ko.observableArray();
  // validation_errors: KnockoutValidationErrors = kv.group(self);
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
    this.customer().get(1)
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

  findWithAttr = (array: Array<any>, attr: string, value: any) => {
    for (var i = 0; i < array.length; i += 1) {
      if (array[i][attr] === value) {
        return i;
      }
    }
    return -1;
  }

  get_user_forms = () => {
    $.get("/forms.json", {})
      .done((result) => {
        result.user_forms.prefix = 'user_forms';
        result.company_forms.prefix = 'company_forms';
        this.user_forms(result.user_forms);
        this.company_forms(result.company_forms);
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
