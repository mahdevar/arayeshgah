//"use strict";
window.addEventListener
(
	'scroll',
	function()
	{
		let classes = E('main_header').classList;
		let scrolled = window.scrollY > 0;
		let shadowed = classes.contains('shadow');
		if(scrolled !== shadowed)
			classes.toggle('shadow');
	}
);
for(let button of document.getElementsByTagName('button'))
{
	let value;
	// Toggling
	if((value = button.getAttribute('toggle')))
	{
		let classes = E(value).classList;
		button.type = 'button';
		button.setAttribute('icon', classes.contains('hide') ? 'expand_more' : 'expand_less');
		button.addEventListener
		(
			'click',
			function()
			{
				classes.toggle('hide');
				button.setAttribute('icon', classes.contains('hide') ? 'expand_more' : 'expand_less');
			}
		);
	}
	// Redirect Clicks
	if((value = button.getAttribute('for')))
	{
		let target = E(value);
		button.type = 'button';
		button.addEventListener
		(
			'click',
			function()
			{
				if(target.type === 'file' || target.type === 'button')
					target.click();
				else
					target.focus();
			}
		);
	}
	// Collapsing
	if((value = button.getAttribute('collapse')))
	{
		let target = E(value);
		button.type = 'button';
		if(!button.getAttribute('icon'))
			button.innerHTML = '<span></span>'.repeat(4);
		button.addEventListener
		(
			'click',
			function()
			{
				button.classList.toggle('open');
				target.classList.remove('hide');
				target.style.maxHeight = button.classList.contains('open') ? target.scrollHeight + 'px' : 0;
			}
		);
		target.addEventListener
		(
			'transitionend',
			function()
			{
				if(target.clientHeight === 0)
					target.classList.add('hide');
			}
		);
		window.addEventListener
		(
			'resize',
			function()
			{
				target.style.maxHeight = button.classList.contains('open') ? target.scrollHeight + 'px' : 0;
			}
		);
		let collapse = function(e)
		{
			if(e.target !== target && !target.parentElement.contains(e.target) && button.classList.contains('open'))
				button.click();
		};
		document.addEventListener('click', collapse);
		document.addEventListener('focusin', collapse);
	}
	
	if((value = button.getAttribute('click')))
	//if((value = button.dataset.click))
	{
		let f = user[value];
		button.addEventListener
		(
			'click',
			async function(event)
			{
				event.preventDefault();
				if(check_required_fields(button.form))
				{
					button.disabled = true;
					if((value = button.getAttribute('parameter')))
						await f(value);
					else
						await f();
					button.disabled = false;
				}
			}
		);
	}

	if((value = button.getAttribute('variant')))
		if(value === 'primary')
			button.type = 'submit';
	if(!button.getAttribute('type'))
		button.type = 'button';
}

if(user.setup)
	user.setup();
