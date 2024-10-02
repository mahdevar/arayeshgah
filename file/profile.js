const l = async function(container_id)
{
	let container = E(container_id);
	let data = await get('/user-data');
	if('error code' in data)
		message(T('SIGN UP: FAILURE'));
	else
	{
		//let f = document.createDocumentFragment();
		let f = new DocumentFragment();
		//let f =  document.createElement('fieldset');
		//let f = create_element('section', {class: 'boxes'});
		for(let [key, value] of Object.entries(data))
		{
			let g = create_element('div', {class: 'group'});
			let l = create_element('label', {for: key});
			l.append
			(
				create_element('i', {innerHTML: 'cut'}),
				create_element('span', {innerHTML: T('A: ' + key.toUpperCase())})
			);
			let i = create_element('input', {id: key, value: value || ''});
			g.append(l, i);
			f.append(g);
			//f.append(l, create_group(key, 'login', T('A: ' + key.toUpperCase()), value || ''));
		}
		await container.appendChild(f);
		align_labels(container.children);
	}
};

user.view = function()
{
	console.log('xxxxxxxxxx');
}

user.setup = function()
{
	l('attributes');
}