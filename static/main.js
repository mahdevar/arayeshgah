//element.setAttributeNS(null, key, value.toString());

//"use strict";
if(!String.prototype.format) 
	String.prototype.format = function(...values)
	{
		return this.replace
		(
			/{(\d+)}/g,
			(match, number) => values[number] !== undefined ? values[number] : match
		);
	};
if(!HTMLElement.prototype.toggle)
	HTMLElement.prototype.toggle = function(attribute)
	{
		if(this.hasAttribute(attribute))
			this.removeAttribute(attribute);
		else
			this.setAttribute(attribute, '');
	};
const request_timeout = 2 * 1000;
const E = id => document.getElementById(id);
const T = id => document.translation[id] || id;

function set_cookie(name, value)
{
	document.cookie = name + '=' + value;
}

function form_payload(fields)
{
	let data = {};
	let value;
	for(let field of fields)
		if(typeof field === 'string')
		{
			if((value = E(field).value))
				data[field] = value;
		}
		else
			for(let [key, value] of Object.entries(field))
				if(value)
					data[key] = value;
	return JSON.stringify(data);
}

async function request(URL, method, data = [])
{
	const controller = new AbortController();
	const abortion_timer = setTimeout(() => controller.abort(), request_timeout);
	let result;

	let parameters =
	{
		method: method,
		headers:
		{
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'CSRF': document.head.children.CSRF.content
		},
		options:{timeout: request_timeout},
		signal: controller.signal
	};
	if(method == 'POST')
		parameters['body'] = form_payload(data);

	try
	{
		result = await fetch(URL, parameters);
	}
	catch(e)
	{
		console.log(e.name);
		console.log(e);
		result = {status: 408};
	}
	clearTimeout(abortion_timer);
	if(result.ok)
	{
		let json = await result.json();
		if(method == 'POST')
		{
			document.head.children.CSRF.content = json.CSRF || '';
			delete json.CSRF;
		}
		return json;
	}
	else
		return {'error code': result.status};
}
const post = (URL, data=[]) => request(URL, 'POST', data);
const get = (URL) => request(URL, 'GET');

function create_element(tag, ...attributes)
{
	let element = document.createElement(tag);
	let html = null;
	for(let attribute of attributes)
		if(typeof attribute === 'string')
			element.setAttribute(attribute, '');
		else
			for(let [key, value] of Object.entries(attribute))
			{
				if(key === 'innerHTML')
					html = value;
				else
					if(value.call)
						element.addEventListener(key, value);
					else
						element.setAttribute(key, value);
			}
	if(html)
		element.innerHTML = html;
	return element;
}

function message(text, category = 'danger')
{
	let c = create_element('div', {class: 'group', click: () => c.remove()});
	c.append
	(
		create_element('label', {class: 'fill', innerHTML: '<span>{0}</span>'.format(text), variant: category}),
		create_element('button', {innerHTML: '<i>close</i>', variant: category})
	);
	setTimeout(() => c.remove(), 10000);
	E('collapsed-content').after(c);
}

function check_required_fields(form)
{
	if(form)
		for(let element of form.elements)
			if(element.required && !element.value)
			{
				message(T('REQUIRES').format(element.placeholder));
				element.focus();
				return false;
			}
	return true;
}


function create_group(id, icon, placeholder, value)
{
	let c = create_element('div', {class: 'group'});
	c.append
	(
		create_element('label', {for: id, innerHTML: '<i>{0}</i>{1}'.format(icon, placeholder)}),
		//create_element('input', {id: id, placeholder: placeholder, value: value})
		create_element('input', {id: id, value: value})
	);
	return c;
}

// HTML elements can call functions of this namespace
var user =
{
	sign_out_timer: null,
	location: {accurate: null, inaccurate: null},
	sign_out: async function (reason = 'REQUESTED')
	{
		let data = await post('/sign-out');
		if('error code' in data)
			message(T('SIGN OUT: FAILURE'));
		else
		{
			message(T('SIGN OUT: ' + reason), 'success');
			clearTimeout(user.sign_out_timer);
			//document.documentElement.toggle('signed');
			document.documentElement.classList.toggle('signed');
		}
	},
	sign_in: async function()
	{
		let data = await post('/sign-in', ['user_name', 'password']);
		if('error code' in data)
			message(T('SIGN IN: FAILURE'));
		else
		{
			message(T('SIGN IN: SUCCESS').format(data.name || data.user_name), 'success');
			let menus = E('menus');
			let sign = function()
			{
				//document.documentElement.toggle('signed');
				document.documentElement.classList.toggle('signed');
				menus.removeEventListener('transitionend', sign);
			};
			menus.addEventListener('transitionend', sign);
			menus.click();
			user.sign_out_timer = setTimeout(user.sign_out, 5 * 60 * 1000, 'INACTIVITY');
		}
	},
	sign_up: async function(role)
	{
		let l = user.location.accurate || user.location.inaccurate;
		let data = await post('/sign-up', ['user_name', 'password', {role: parseInt(role), location: l ? l.x.toFixed(5) + ', ' + l.y.toFixed(5) : null, accuracy: l ? l.accuracy: null}]);
		if('error code' in data)
				message(T('SIGN UP: FAILURE'));
		else
		{
			message(T('SIGN UP: SUCCESS'), 'success');
			await user.sign_in();
		}
	},
	set_language: async function(language)
	{
		set_cookie('LANGUAGE', language);
		location.reload();
	},
	navigate: async function(URL)
	{
		window.location.href = URL;
		return false;
	}
};

if(document.documentElement.classList.contains('signed'))
	user.sign_out_timer = setTimeout(user.sign_out, 5 * 60 * 1000, 'INACTIVITY');

function geolocation_to_point(latitude, longitude)
{
	latitude *= Math.PI / 180;
	longitude *= Math.PI / 180;
	return {x: 6367 * Math.cos(latitude) * Math.cos(longitude), y: 6367 * Math.cos(latitude) * Math.sin(longitude)};
}

(
	async function()
	{
		//geoip-js.com is an alternative website
		try
		{
			let result = await fetch('https://geolocation-db.com/json/');
			if(result.ok)
			{
				let data = await result.json();
				user.location.inaccurate = {...geolocation_to_point(data.latitude, data.longitude), accuracy: null};
			}
		}
		catch
		{
			return false;
		}
	}
)();

const align_labels = function(rows)
{
	let max = 0;
	for(let row of rows)
		if(row.firstChild.clientWidth > max)
			max = row.firstChild.clientWidth;
	for(let row of rows)
		row.firstChild.style.width='{0}px'.format(max);
}

/*
function sync_get_json(file_name)
{
	let request = new XMLHttpRequest();
	request.open('GET', '/file/{0}.json'.format(file_name), false);
	request.send();
	if(request.status === 200 && request.readyState === 4)
		return JSON.parse(request.responseText);
	else
		return null;
}
document.translation = sync_get_json(document.language);
*/

/*
function is_visible(e)
{
	let rect = e.getBoundingClientRect();
	return rect.bottom >= 0 && rect.top - Math.max(document.documentElement.clientHeight, window.innerHeight) < 0;
}
function element_width(node)
{
	return node.offsetWidth + (node.style.marginLeft || 0);
}
const css_style = (element, property) => window.getComputedStyle(element, null).getPropertyValue(property);
const get_element_font = (element) => '{0} {1} {2}'.format(css_style(element, 'font-weight') || 'normal', css_style(element, 'font-size') || '18px', css_style(element, 'font-family') || 'Times New Roman');
*/

