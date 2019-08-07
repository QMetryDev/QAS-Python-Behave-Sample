function loadListAllForCSV() {

 return $.getJSON(getResultRootDir() + "/meta-info.json", function(data) {
  $('#details').html('');
  var curSelceteReport = $('#reportlist li.selected');
  loadAllMethodsForCSV($(curSelceteReport).attr("dir"));
 });

}

function loadAllMethodsForCSV(dir) {
 var resultList = [];
 resultList.push({
  "suiteName": "Module",
  "storyId": "Story name",
  "name": "TestCase Name",
  "result": "Result",
  "Duration": "Duration",
  "defectId": "Defect Id",
  "author":"author",
  "fixedBy":"fixedBy",
  "status":"status",
  "groups":"groups",
  "module":"module"
 });
 chainedcsv = $.getJSON(dir + "/meta-info.json", function(data) {
  var startTimeString = msToFormatedDateStr(data.startTime, 'dd-MM-yy HH:MM')
  $.each(data.tests, function(i, item) {
   var suiteName = data.tests[i];
   loaResultForCSV(item, suiteName, resultList);
  });

  chainedcsv.done(function() {
   chainedtests.done(function() {
    chainedcls.done(function() {
     myJSON = "";
     myJSON = JSON.stringify(resultList);
     JSONToCSVConvertor(myJSON, startTimeString)
    });
   });
  });
 });

}

function loaResultForCSV(dir, suiteName, resultList) {
 tmp = curResultDir + "/" + dir;
 loadMethodsForCSV(curResultDir, dir, suiteName, resultList);
}

function loadMethodsForCSV(cresultRoot, testDir, suiteName, resultList) {
try{
 curResultDir = cresultRoot;
 var dir = cresultRoot + "/" + testDir;
 chainedtests = $.getJSON(dir + "/overview.json", function(data) {
  if(!(data.classes==null)){
  $.each(data.classes, function(i, cls) {
   chainedcls = $.getJSON(dir + "/" + cls + "/meta-info.json",
    function(minfo) {
     $.each(minfo.methods, function(j, mdata) {

      //							var testCaseName = suiteName + "^"
      //									+ mdata.metaData.name + "^" + mdata.result
      //									+ "^" + mdata.duration;
      mdata.datafile = dir + "/" + cls + "/" +
       mdata.metaData.name + ".json";
      var formattedDuration = getDuration(mdata.duration);
      var testcaseName = mdata.metaData.name;
      var storyId=mdata.metaData.Story_ID;
      var defectId=mdata.metaData.IssueId;
      var author=mdata.metaData.author;
      var fixedBy=mdata.metaData.fixedBy;
      var status=mdata.metaData.status;
      var groups=mdata.metaData.groups;
      var module=mdata.metaData.module;

      if(defectId==null){
    	  defectId="na";
      }
      if(fixedBy==null){
    	  fixedBy="na";
      }
      if(groups==null){
    	  groups="not defined";
      }
    	  
      if(module==null){
    	  module="na";
      }
      console.log(testcaseName);
      if(((typeof (mdata.args) != 'undefined') && (mdata.args).length>0)){
  		//This is data driven test.
    	  testcaseName = testcaseName;
  		
	  	} else {
	  		if(mdata.index > 1){
	//  			name = "Retry_"+name;
	  			var string1 = testcaseName.substring(0,testcaseName.lastIndexOf("_"));
	  			var string2 = testcaseName.substring(testcaseName.lastIndexOf("_"),testcaseName.length);
	  			testcaseName = string1 +"_Rerun"+string2;
	  		}else {
	  			testcaseName = testcaseName;
	  		}
	  	}
      
      
      /*if (mdata.result == "fail") {
       getCheckpointsForCSV(mdata.datafile, suiteName,

        mdata.metaData.name, mdata.result,
        formattedDuration, resultList);
      } else {*/
//      console.log(mdata);
       resultList.push({
        "suiteName": suiteName,
        "storyId": storyId,
        "name": testcaseName,
        "result": mdata.result,
        "Duration": formattedDuration,
        "defectId": defectId,
        "author":author,
        "fixedBy":fixedBy,
        "status":status,
        "groups":groups,
        "module":module
       });

//      }

     });
    });
  });
  }
 });
}
catch(e){ console.log(e);}
}

function getCheckpointsForCSV(file, suiteName, testCaseName, result, Duration,
 resultList) {
 $
  .ajax({
   dataType: "json",
   url: file,
   async: false
  })
  .done(
   function(data) {

    $
     .each(
      data.checkPoints,
      function(i, checkPoints) {
       var checkpoint = data.checkPoints[i].type
        .toLowerCase();

       if (checkpoint == 'teststepfail') {
        var teststepname = data.checkPoints[i].message;
        var subcheckpointsdata = data.checkPoints[i].subCheckPoints;
        // console.log(subcheckpointsdata[0].message);
        var errormessage = subcheckpointsdata[0].message;

        resultList.push({
        	  "suiteName": suiteName,
              "storyId": storyId,
              "name": testcaseName,
              "result": mdata.result,
              "Duration": formattedDuration,
              "defectId": defectId,
              "author":author,
              "fixedBy":fixedBy,
              "status":status,
              "groups":groups,
              "module":module
        });

       }

      });

    // };
   });

}

function JSONToCSVConvertor(JSONData, ReportTitle) {
 //If JSONData is not an object then JSON.parse will parse the JSON string in an Object


 var arrData = typeof JSONData != 'Object' ? JSON.parse(JSONData) : JSONData;

 var CSV = '';
 //Set Report title in first row or line

 CSV += ReportTitle + '\r\n\n';

 //1st loop is to extract each row
 for (var i = 0; i < arrData.length; i++) {
  var row = "";

  //2nd loop will extract each column and convert it in string comma-seprated
  for (var index in arrData[i]) {
   row += '"' + arrData[i][index] + '",';
  }

  row.slice(0, row.length - 1);

  //add a line break after each row
  CSV += row + '\r\n';
 }

 if (CSV == '') {
  alert("Invalid data");
  return;
 }

 //Generate a file name
 var fileName = "SmarshResult_";
 //this will remove the blank-spaces from the title and replace it with an underscore
 fileName += ReportTitle.replace(/ /g, "_");

 //Initialize file format you want csv or xls
 var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

 // Now the little tricky part.
 // you can use either>> window.open(uri);
 // but this will not work in some browsers
 // or you will not get the correct file extension    

 //this trick will generate a temp <a /> tag
 var link = document.createElement("a");
 link.href = uri;

 //set the visibility hidden so it will not effect on your web-layout
 link.style = "visibility:hidden";
 link.download = fileName + ".csv";

 //this part will append the anchor tag and remove it after automatic click
 document.body.appendChild(link);
 link.click();
 document.body.removeChild(link);
}
