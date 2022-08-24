methods['NOVA_POSHTA'] = {
        "select_handler": handle_select,
        "document_generate": generate
}
var area_options = ""
// AreaID, Options
var city_options = {}
// WarehouseID, Options
var warehouse_options = {}

function handle_select() {
    addAreas()
}

function generate() {
    var value = $("#Warehouse-options>select option:selected").val()
    return  value !== "undefined" ? value : ""
}

async function api_request(url) {
      data = ""
      await $.ajax({
          url: url,
          type: "GET",
          success: function(result) {
            for(var i in result) {
                data += "<option value='" + result[i]['id'] + "'>" + result[i]['Description'] + "</option>\n"
            }
          },
          error: function(error) {
          }
        });

      return data
}

function addSelect(label, options, func, parent="#delivery-options") {
      var select = $("<select>\n" +
                            "<option disabled selected value>---</option>\n" +
                            options +
                            "</select>\n")

      $("#" + label + "-options").remove()
      var element = $("<p id='" + label + "-options'>\n<label>" + label + ":</label>\n").append(select).append("</p>")

      if (func !== null) {
          select.change(function() {
                func($(this).val())
          });
      }

      $(parent).append(element)
}

async function addAreas() {
      if(area_options === "") {
            area_options = await api_request("/api-np/area/")
      }
      addSelect("Area", area_options, addCities)
}

async function addCities(area_id) {
      if(!(area_id in city_options)) {
            city_options[area_id] = await api_request("/api-np/city/?Area=" + area_id)
      }
      addSelect("City", city_options[area_id], addWarehouses, "#Area-options")
}

async function addWarehouses(city_id) {
      if(!(city_id in warehouse_options)) {
            warehouse_options[city_id] = await api_request("/api-np/warehouse/?City=" + city_id + "&WarehouseStatus=Working")
      }
      addSelect("Warehouse", warehouse_options[city_id], null, "#City-options")
}
