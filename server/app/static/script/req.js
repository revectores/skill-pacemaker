function req(api_url){
	function url_formatter(params){
		if (typeof(params) === "undefined"){
			return api_url;
		}

		if (["string", "number"].includes(typeof(params))){
			return api_url + '/' + params;
		}

		if (typeof(params) === "object"){
			params_string = '';
			for (let key in params){
				params_string = key + "=" + params[key] + '&'
			}
			return api_url + '?' + params_string;
		}
	}

	function requester(params){
		let request = new XMLHttpRequest();
		request.open('GET', url_formatter(params), false);
		request.send();
		return request.responseText;
	}

	return requester;
}