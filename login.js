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
