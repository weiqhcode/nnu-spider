function onSubmint(dataStr, userAccount, userPassword){

		try{
			var useDogCode = getDogCode();
			document.getElementById("useDogCode").value=useDogCode;
		}catch(e){}

	var strUrl="/Logon.do?method=logon&flag=sess";

	var scode=dataStr.split("#")[0];
	var sxh=dataStr.split("#")[1];
	// var code=document.getElementById("userAccount").value+"%%%"+document.getElementById("userPassword").value;

	var code = userAccount+"%%%"+userPassword
	var encoded="";
	for(var i=0;i<code.length;i++){
		if(i<20){
			encoded=encoded+code.substring(i,i+1)+scode.substring(0,parseInt(sxh.substring(i,i+1)));
			scode = scode.substring(parseInt(sxh.substring(i,i+1)),scode.length);
		}else{
			encoded=encoded+code.substring(i,code.length);
			i=code.length;
		}
	}

	return encoded;

}
function selectServer(uName){
	var enableServers = true;//是否启用多服务器 true/false
	var serversArray = new Array();//服务器列表


		serversArray[0] = "http://192.168.111.5:81/jsxsd/";

		serversArray[1] = "http://192.168.111.4:80/jsxsd/";


var loginUrl = "xk/LoginToXk";
if(enableServers == true){
	if(!isNaN(uName)){//必须为数字
		var modVal = eval(uName % serversArray.length);
		loginUrl = serversArray[modVal] + loginUrl;
	}else{
		loginUrl = serversArray[0] + loginUrl;
	}
}else{
	loginUrl = ""+ loginUrl;
}
return loginUrl;
}