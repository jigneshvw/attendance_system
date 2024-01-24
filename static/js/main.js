var currentStep = 0;
var totalSteps = 8;
var chkDataObj = {};
var uData = [];
var uIp = "";
var uBrowser = "";
var uAgent = "";
var uOs = "";
var imgBasePath = "";
var imgLogBasePath = "";
var basePyPath = "";
var empListArr = [];
var empDataArr = [];
var empFiveDataArr = [];
var addEmpName = "";
var addEmpImage = "";
var isDebug = false;

let v;
let imageCanvas;
let imageCtx;


$(document).on('ready', function () {
  $("#loader").show();

  imgBasePath = "static/assets/img/";
  imgUserPath = "static/assets/img/users/";
  imgLogBasePath = "assets/img/userslog/";
  basePyPath = "http://127.0.0.1:5000";

  console.log("vid " + $("#pyfeedImg").attr('src'));

  $(".empOperations").hide();

  setTimeout(function () {
    //$("#set_0").fadeIn("slow");
    $("#loader").hide();
    getIp();
    activateSideBar();
  }, 5000);

  /*
  http://127.0.0.1:5000/get_employee/tuser1
  http://127.0.0.1:5000/get_5_last_entries
  http://127.0.0.1:5000/add_employee?name=tuser8&img
  http://127.0.0.1:5000/get_employee_list
  http://127.0.0.1:5000/delete_employee/tuser1

  http://localhost/faceDetection/test_v1/index.html
   http://localhost/faceDetection/test_v2/index.html
  localhost (127.0.0.1)

  Error
  UnboundLocalError: local variable 'connection' referenced before assignment

  */

});

$(window).resize(function () {
  //checkWinWidth();  
});

function getIp() {
  $.getJSON("https://api.ipify.org?format=json", function (data) {
    uData.ip = data.ip;
  });
  uData.browser = platform.name + " " + platform.version;
  uData.os = platform.os.family + " " + platform.os.version;
}

function activateSideBar() {
  $(".sidenav li").click(function () {
    $(".sidenav li").removeClass("active");
    $(".empOperations").fadeOut("fast");
    $(this).addClass("active");
    activateOperations($(this).attr("id"));
  });
  $("#getemp").click();
}

function deleteEmp(_val) {
  console.log("deleteEmp " + _val);
  $("#loader").show();
  if (_val != "") {
    $.ajax({
      url: basePyPath + '/delete_employee/' + _val,
      data: {
        //name: _val
      },
      dataType: 'JSON',
      type: 'GET',
      success: function (respData) {
        console.log(respData);
        $("#loader").hide();
        if (respData == "success")
          $("#delEmpStatus").html("Employee <b>" + _val + "</b> succesfully removed").fadeIn("slow");
        else
          $("#delEmpStatus").html("Error while deleting employee, please try later").fadeIn("slow").delay(5000).fadeOut("slow");
      }
    });
  }
  else {
    $("#delEmpStatus").html("Please enter name of an employee to delete").fadeIn("slow").delay(5000).fadeOut("slow");
    $("#set_0").find(".form-actions-text-input").addClass("inputError");
    $("#loader").hide();
  }
}

function addEmp() {
  addEmpName = $("#set_4").find(".form-actions-text-input").val().trim();
  //startVideo();  
  $("#loader").show();
  if (addEmpName != "") {
    $.ajax({
      url: basePyPath + '/add_employee/' + addEmpName,
      dataType: 'JSON',
      type: 'GET',
      success: function (respData) {
        console.log(respData);
        $("#loader").hide();
        if (respData == "success") {
          /* <script src="{{url_for('static', filename='js/jquery-2.2.0.min.js')}}" type="text/javascript"></script> */
          var assetPath = imgUserPath + addEmpName + ".jpg?d=" + Date.now();
          $("#imgUser").attr("src", assetPath).fadeIn("slow");
          $("#imgUser").attr("alt", addEmpName);
          $("#addEmpStatus").html("New Employee, <b>" + addEmpName + "</b> added successfully").fadeIn("slow");
        }
        else {
          $("#addEmpStatus").html("Error adding new employee, please try again later").fadeIn("slow").delay(5000).fadeOut("slow");
          $("#loader").hide();
        }
      }
    });
  }
  else {
    $("#addEmpStatus").html("Please enter name of an employee to add.").fadeIn("slow").delay(5000).fadeOut("slow");
    $("#set_4").find(".form-actions-text-input").addClass("inputError");
    $("#loader").hide();
  }
}

function getEmp(_val) {
  console.log("getEmp " + _val);
  $("#empDataHolder").html('');
  $("#getEmpStatus").fadeOut();
  $("#loader").show();
  if (_val != "") {
    $.ajax({
      url: basePyPath + '/get_employee/' + _val,
      data: {
        //name: _val
      },
      dataType: 'JSON',
      type: 'GET',
      success: function (respData) {
        console.log(respData.result);
        if (respData.error) {
          $("#getEmpStatus").html(respData.error).fadeIn("slow").delay(5000).fadeOut("slow");
          $("#loader").hide();
        }
        else {
          empDataArr = [];
          //empDataArr.inTimeImgPath = imgLogBasePath + respData[0].inTimeImg.toLowerCase() + ".jpg";
          //empDataArr.outTimeImgPath = imgLogBasePath + respData[0].outTimeImg.toLowerCase() + ".jpg";
          empDataArr.inTimeImgPath = respData[0].inTimeImg.toLowerCase() + "?d=" + Date.now();
          empDataArr.outTimeImgPath = respData[0].outTimeImg.toLowerCase() + "?d=" + Date.now();

          empDataArr.empName = respData[0].empName;
          empDataArr.dispImgPath = imgUserPath + respData[0].empName.toLowerCase() + ".jpg?d=" + Date.now();
          empDataArr.inTime = respData[0].inTime;
          empDataArr.outTime = respData[0].outTime;
          empDataArr.date = respData[0].date;

          var source = document.getElementById("entry-template-empData").innerHTML;
          var template = Handlebars.compile(source);
          var context = empDataArr;
          var html = template(context);
          $("#empDataHolder").html('');
          $("#empDataHolder").append(html);
          $("#loader").hide();
        }
      },
      error: function (err) {
        console.log("getemp Error  " + err);
        $("#getEmpStatus").html("Error while getting employee details. Please try later ").fadeIn("slow").delay(5000).fadeOut("slow");
        $("#loader").hide();
      }
    });
  }
  else {
    $("#getEmpStatus").html("Please enter name of an employee to get details").fadeIn("slow").delay(5000).fadeOut("slow");
    $("#set_3").find(".form-actions-text-input").addClass("inputError");
    $("#loader").hide();
  }
}

function getLastFiveEmp() {
  console.log("getLastFiveEmp ");
  $("#loader").show();
  $.ajax({
    url: basePyPath + '/get_5_last_entries',
    data: {
      //name: _val
    },
    dataType: 'JSON',
    type: 'GET',
    success: function (respData) {
      console.log(respData);
      empFiveDataArr = [];
      $.each(respData, function (index, value) {
        console.log(index, value);
        var name = value.empName;
        var dispImgPath = imgUserPath + value.empName.toLowerCase() + ".jpg?d=" + Date.now();
        var date = value.date;
        var inTime = value.inTime;
        var outTime = value.outTime;
        //var inTimeImgPath = imgLogBasePath + value.inTimeImg.toLowerCase() + ".jpg";
        //var outTimeImgPath = imgLogBasePath + value.outTimeImg.toLowerCase() + ".jpg";
        var inTimeImgPath = value.inTimeImg.toLowerCase() + "?d=" + Date.now();
        var outTimeImgPath = value.outTimeImg.toLowerCase() + "?d=" + Date.now();

        empFiveDataArr.push({ "id": index, "empName": name, "date": date, "dispImgPath": dispImgPath, "inTime": inTime, "outTime": outTime, "inTimeImgPath": inTimeImgPath, "outTimeImgPath": outTimeImgPath });
      });

      var source = document.getElementById("entry-template-empFiveList").innerHTML;
      var template = Handlebars.compile(source);
      var context = empFiveDataArr;
      var html = template(context);
      $("#empFiveListHolder").html('');
      $("#empFiveListHolder").append(html);
      $("#loader").hide();
    },
    error: function (err) {
      console.log("getemp Error  " + err);
      $("#empFiveEmpStatus").html("Error while getting employee details. Please try later ").fadeIn("slow").delay(5000).fadeOut("slow");
    }
  });
}

function getEmpList() {
  console.log("getEmpList ");
  $("#loader").show();
  $.ajax({
    url: basePyPath + '/get_employee_list',
    data: {},
    dataType: 'JSON',
    type: 'GET',
    success: function (respData) {
      empListArr = [];
      $.each(respData, function (index, value) {
        console.log(index, value);
        var dispImgPath = imgUserPath + value.toLowerCase() + ".jpg?d=" + Date.now();
        empListArr.push({ "id": index, "empName": value, "dispImgPath": dispImgPath });
      });
      var source = document.getElementById("entry-template-empList").innerHTML;
      var template = Handlebars.compile(source);
      var context = empListArr;
      var html = template(context);
      $("#empListHolder").html('');
      $("#empListHolder").append(html);
      $("#loader").hide();
    }
  });
}


function activateOperations(oprname) {
  console.log("action " + oprname);

  switch (oprname) {
    case "delemp":      
      $("#set_0").fadeIn("slow");
      $("#set_0").find(".startDel").unbind('click').click(function () {
        $(".empDelBlock").find(".form-actions-text-input").val('');
        $("#delEmpStatus").html('').fadeOut();
        $(".empDelBlock").fadeIn("slow");
        $("#set_0").find(".form-actions-text-input").unbind('keypress').keypress(function (e) {
          $(this).removeClass("inputError");
          if (e.which == 13) {
            deleteEmp($("#set_0").find(".form-actions-text-input").val().trim());
          }
        });
        $("#set_0").find(".submit").unbind('click').click(function () {
          deleteEmp($("#set_0").find(".form-actions-text-input").val().trim());
        });
      });
      break;
    case "getemp":
      $("#set_3").fadeIn("slow");
      $("#set_3").find(".form-actions-text-input").unbind('keypress').keypress(function (e) {
        $(this).removeClass("inputError");
        if (e.which == 13) {
          getEmp($("#set_3").find(".form-actions-text-input").val().trim());
        }
      });
      $("#set_3").find(".submit").unbind('click').click(function () {
        getEmp($("#set_3").find(".form-actions-text-input").val().trim());
      });
      break;
    case "listemp":
      $("#set_1").fadeIn("slow");
      $("#set_1").find(".submit").unbind('click').click(function () {
        getEmpList();
      });
      break;
    case "lastfiveemp":
      $("#set_2").fadeIn("slow");
      $("#set_2").find(".submit").unbind('click').click(function () {
        getLastFiveEmp();
      });
      break;
    case "addemp":
      $("#set_4").fadeIn("slow");
      $("#set_4").find(".startAdd").unbind('click').click(function () {
        $(".empAddBlock").find(".form-actions-text-input").removeClass("inputError");
        $(".empAddBlock").find(".form-actions-text-input").val('');
        $("#addEmpStatus").html('').fadeOut();
        $("#imgUser").attr('src', '').fadeOut();
        $(".empAddBlock").fadeIn("slow");
        $("#set_4").find(".submit").unbind('click').click(function () {
          addEmp();
        });
        $("#set_4").find(".form-actions-text-input").unbind('keypress').keypress(function (e) {
          $(this).removeClass("inputError");
          if (e.which == 13) {
            addEmp();
          }
        });
      });
      break;
  }
}


/*function startVideo() {
  v = document.getElementById("imgVideo");
  imageCanvas = document.createElement('canvas');
  imageCanvas = document.getElementById("imgCanvas");
  imageCtx = imageCanvas.getContext("2d");

  //Get camera video
  navigator.mediaDevices.getUserMedia({ video: { width: 550, height: 600 }, audio: false })
    .then(stream => {
      v.srcObject = stream;
    })
    .catch(err => {
      console.log('navigator.getUserMedia error: ', err);
    });

  //Take a picture on click
  $('.imgCapture').click(function () {
    console.log('click');
    sendImagefromCanvas();
  });
}

/* function sendImagefromCanvas() {

  //Make sure the canvas is set to the current video size
  imageCanvas.width = v.videoWidth;
  imageCanvas.height = v.videoHeight;

  imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);

  //Convert the canvas to blob and post the file
  imageCanvas.toBlob(postFile, 'image/jpeg');
}

//Add file blob to a form and post
function postFile(imgBlob) {
  let formdata = new FormData();
  formdata.append("imgblob", imgBlob);
  let xhr = new XMLHttpRequest();
  //xhr.open('POST', 'http://localhost:5000/image/trupti', true);
  xhr.open('POST', 'http://127.0.0.1:5000/add_employee/' + addEmpName, true);
  xhr.onload = function () {
    if (this.status === 200) {
      console.log(this.response);
      if (this.response == "success")
        $("#addEmpStatus").html("New Employee, <b>"+addEmpName+"</b> added successfully").fadeIn("slow");
    }
    else {
      console.error(xhr);
      $("#addEmpStatus").html("Error adding new employee, please try again later").fadeIn("slow");
    }
  };
  xhr.send(formdata);
} */

/* function uploadNewEmpData(file) {
  console.log("addnewEmp ");
  $("#loader").show();
  $.ajax({
    url: basePyPath + '/add_employee/' + addEmpName,
    data: {
      image: file
    },
    dataType: 'JSON',
    type: 'POST',
    contentType: false,
    processData: false,
    success: function (respData) {
      alert("resp " + respData);
      $("#loader").hide();
    }
  });
} */